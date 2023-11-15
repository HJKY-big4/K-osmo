# app.py
from flask import Flask, jsonify, render_template, Response, request
import cv2, os, base64
import random_miro
import numpy as np
from tensorflow import keras

app = Flask(__name__)

# ------------------------- 웹캠 관련 부분 ----------------------------
UPLOAD_FOLDER = 'move_img/raw_data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

camera = cv2.VideoCapture(0)

video_feed_url = "/video_feed"
black_image_url = "/static/black_img.jpeg"

def im_trim(img):
    x = 154;
    y = 170;
    w = 340;
    h = 250;
    img_trim = img[y:y + h, x:x + w]
    return img_trim

def im_trim_num(img):
    x = 500;
    y = 170;
    w = 175;
    h = 250;
    img_trim = img[y:y + h, x:x + w]
    return img_trim

# 이미지 이진화 함수
def img_binarization(warped_image):
    RGB_img = cv2.cvtColor(warped_image, cv2.COLOR_BGR2RGB)  # 그레이 색상의 이미지(warped_image)를 RGB로 변환
    R_img, G_img, B_img = cv2.split(RGB_img)

    N = 30
    for h in range(RGB_img.shape[0]):
        for w in range(RGB_img.shape[1]):
            if (np.int32(R_img[h, w]) > N):
                R_img[h, w] = G_img[h, w] = B_img[h, w] = 255
            else:
                R_img[h, w] = G_img[h, w] = B_img[h, w] = 0

    RGB_img[:, :, 0] = R_img
    RGB_img[:, :, 1] = G_img
    RGB_img[:, :, 2] = B_img

    # 방향과 숫자 분리
    trim_image_block = im_trim(RGB_img)  # trim_image 변수에 결과물을 넣는다

    trim_image_num = im_trim_num(RGB_img)  # trim_image 변수에 결과물을 넣는다

    img_ori_block = cv2.resize(trim_image_block, (480, 480))
    img_ori_num = cv2.resize(trim_image_num, (480, 480))

    gray_block = cv2.cvtColor(img_ori_block, cv2.COLOR_BGR2GRAY)
    gray_num = cv2.cvtColor(img_ori_num, cv2.COLOR_BGR2GRAY)

    img_blurred_block = cv2.GaussianBlur(gray_block, ksize=(5, 5), sigmaX=0)
    img_blur_thresh_block = cv2.adaptiveThreshold(
        img_blurred_block,
        maxValue=1,  # 변경된 부분: maxValue를 1로 설정
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY_INV,
        blockSize=19,
        C=9
    )

    img_blurred_num = cv2.GaussianBlur(gray_num, ksize=(5, 5), sigmaX=0)
    img_blur_thresh_num = cv2.adaptiveThreshold(
        img_blurred_num,
        maxValue=1,  # 변경된 부분: maxValue를 1로 설정
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY_INV,
        blockSize=19,
        C=9
    )

    # 이미지 데이터를 0과 1로 표현
    image_data_block = img_blur_thresh_block
    image_data_num = img_blur_thresh_num

    return image_data_block, image_data_num

# 이미지 전처리 함수(model_sep.h5 전용)
def img_processing(image_path):

    img_ori = cv2.imread('move_img/raw_data/photo.jpg')

    gray = cv2.cvtColor(img_ori, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    _, binary = cv2.threshold(blurred, 0, 255,
                              cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.arcLength(x, True), reverse=True)
    largest_contour = contours[1]

    epsilon = 0.04 * cv2.arcLength(largest_contour, True)
    approx = cv2.approxPolyDP(largest_contour, epsilon, True)
    edge_point = [(x, y) for point in approx for x, y in point]

    left_top_screen = min(edge_point, key=lambda x: x[0] + x[1])
    right_top_screen = max(edge_point, key=lambda x: x[0] - x[1])
    left_bottom_screen = min(edge_point, key=lambda x: x[0] - x[1])
    right_bottom_screen = max(edge_point, key=lambda x: x[0] + x[1])

    src_points = np.float32([left_top_screen, right_top_screen, left_bottom_screen, right_bottom_screen])
    width, height = 800, 600 # 너비와 높이를 여기서 조절
    dst_points = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    perspective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    warped_image = cv2.warpPerspective(binary, perspective_matrix, (width, height))

    # 전처리된 이미지 특정 폴더에 특정 이름으로 저장
    processed_image_path = os.path.join('move_img', 'processing_data', 'photo.jpg')
    cv2.imwrite(processed_image_path, warped_image)

    # 이미지 이진화 함수 호출
    image_data_block, image_data_num = img_binarization(warped_image)

    return image_data_block, image_data_num

# 웹캠에서 프레임을 스트리밍하는 함수
def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/capture', methods=['POST'])
def capture():
    try:
        image_data = request.form['image_data']
        image_data = image_data.replace('data:image/jpeg;base64,', '')
        decoded_image = base64.b64decode(image_data)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'photo.jpg')
        with open(image_path, 'wb') as f:
            f.write(decoded_image)

        binarization_img_block, binarization_img_num = img_processing(image_path)



        # 모델 불러오기
        model = keras.models.load_model(model_path)



        # 모델 예측
        predictions_block = model.predict(np.expand_dims(binarization_img_block, axis=0))
        predicted_class_block = np.argmax(predictions_block)
        predicted_class_label_block = label[predicted_class_block].split(' : ')[0]

        predictions_num = model.predict(np.expand_dims(binarization_img_num, axis=0))
        predicted_class_num = np.argmax(predictions_num)
        predicted_class_label_num = label[predicted_class_num].split(' : ')[0]

        block_name = predicted_class_label_block + ' ' + predicted_class_label_num

        # block_name을 HTML에 전달하고 렌더링된 HTML 반환
        return jsonify({'block_name': block_name})
    except Exception as e:
        print(str(e))
        return '이미지 전처리 및 저장 중 오류가 발생했습니다.'


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# ----------- 미로 생성 부분 --------------------

# 미로 생성 미로의 크기를 매개변수로 넣어줘야 한다.
def generate_maze(maze_size):
    n = maze_size
    maze_data = random_miro.generate_maze(n) # 행렬의 크기는 12
    return maze_data

# 엔드포인트 정의
@app.route('/get_maze', methods=['GET'])
def get_maze():
    maze_size = int(request.args.get('size', 12))
    
    maze_data = generate_maze(maze_size)
    return jsonify(maze_data)

# ------------ 모델 관련 부분 -----------------------------

# 모델을 저장한 폴더 경로
model_folder = 'model'
model_filename = 'model_sep.h5'
model_path = f'{model_folder}/{model_filename}'

label = ['1 : 0', '2 : 1', '3 : 2', '4 : 3', '5 : 4',
         'down : 5', 'left : 6', 'right : 7', 'up : 8']



# ------------------------------------------------------

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

@app.route('/')
def index():
    return render_template('index.html', video_feed_url=video_feed_url, black_image_url=black_image_url)

if __name__ == '__main__':
    app.run(debug=True)
