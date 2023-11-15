# img_model.py
import numpy as np
import cv2
import os
from tensorflow import keras
import sys

class model_all:

    def __init__(self, model_path = "model/model_sep.h5"):
        self.width = 800
        self.height = 600
        model_path = os.path.abspath(model_path) 
        
        # 모델을 불러옴
        self.model = keras.models.load_model(model_path)
        self.label = ['1 : 0', '2 : 1', '3 : 2', '4 : 3', '5 : 4', 
                      'down : 5', 'left : 6', 'right : 7', 'up : 8']

    def img_filming(self):
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            while True: # 코드에서 프레임을 읽는 동안 무한 루프를 유지하므로 웹캠에서 지속적으로 프레임을 읽어들여 처리 가능
                ret, frame = cap.read() # ret은 프레임을 성공적으로 읽으면 True, 아니면 False를 반환
                # frame은 함수로 부터 읽어들인 현재 프레임 의미
                if ret:
                    flipped_frame = cv2.flip(frame, -1) # 화면에 보이는 모습을 180도 반전
                    cv2.imshow('camera', flipped_frame)
                    key = cv2.waitKey(1) # waitKey(delay) 함수의 키보드 입력을 대기하는 함수 delay는 입력을 기다리는 시간(밀리초 단위)를 의미

                    if key == 27: # esc버튼
                        cap.release()
                        cv2.destroyAllWindows() # 이거를 쓰는데 웹에서 꺼지는지 모르겠다.
                        break

                    elif key == 32: # 스페이스바를 누르는 경우
                        output_folder = 'move_img/raw_data/'
                        os.makedirs(output_folder, exist_ok=True)
                        cv2.imwrite(os.path.join(output_folder, 'photo.jpg'), flipped_frame) # 현재 프레임인 flipped_frame을 photo.jpg로 저장
                        processing_img = self.img_processing()
                        # 전처리된 이미지 저장
                        cv2.imwrite('move_img/processing_data/photo.jpg', processing_img)
                        binarization_img_block,binarization_img_num = self.img_binarization(processing_img)

                        predictions_block = self.model.predict(np.expand_dims(binarization_img_block, axis=0))
                        predicted_class_block = np.argmax(predictions_block)
                        predicted_class_label_block = self.label[predicted_class_block].split(' : ')[0]

                        predictions_num = self.model.predict(np.expand_dims(binarization_img_num, axis=0))
                        predicted_class_num = np.argmax(predictions_num)
                        predicted_class_label_num = self.label[predicted_class_num].split(' : ')[0]

                        block_name = predicted_class_label_block +' ' + predicted_class_label_num

                        print("Predicted Class:", block_name)

                        max_probability_block = np.max(predictions_block)
                        max_probability_num = np.max(predictions_num)

                        if max_probability_block < 0.9 or max_probability_num < 0.9:
                            block_list = ['left 1','left 2','left 3','left 4','left 5',
                                          'right 1','right 2','right 3','right 4','right 5',
                                          'down 1','down 2','down','down','down',
                                          'up 1','up 2','up 3','up 4','up 5']

                            if block_name in block_list:
                                event_image = cv2.imread(f'event_img/{block_name}.jpg')
                                cv2.imshow('camera', event_image)

                                while True:
                                    key_overlay = cv2.waitKey(1)
                                    if key_overlay == ord('y'):
                                        break
                                    elif key_overlay == ord('n'):
                                        break
                                cv2.imshow('camera', flipped_frame)  # 카메라 화면으로 복귀


                            else:
                                event_image = cv2.imread(f'event_img/noblock.jpg')
                                cv2.imshow('camera', event_image)
                                key_overlay = cv2.waitKey(0)

                                if key_overlay == ord('y'): # ??아무거나 눌러도 적용되네?
                                    cv2.imshow('camera', flipped_frame)  # 카메라 화면으로 복귀

                        else:
                            # 모든 조건에 해당하지 않을 경우 처리
                            block_name = "high_probability_block" if max_probability_block >= max_probability_num else "high_probability_num"
                            # 더 높은 확률을 가진 것에 따라 block_name 설정
                else:
                    print('no frame')
                    break
        else:
            print('no camera!')


        return block_name

    
    # 이미지 전처리 함수(model_sep.h5 전용)
    def img_processing(self):
        
        img_ori = cv2.imread('move_img/raw_data/photo.jpg')

        gray = cv2.cvtColor(img_ori, cv2.COLOR_BGR2GRAY) # 컬러를 흑백으로 전환해서 저장
        blurred = cv2.GaussianBlur(gray, (5,5), 0) # 가우시안 블러 처리후 변수에 저장. 더 정확한 윤곽을 뽑아내기 위해서
        
        _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) # 이진화는 특정 임계점을 기준으로 픽셀 값을 0또는 255로 변환
        
        contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) # 이진화된 이미지에서 윤곽선을 따기
        contours = sorted(contours, key=lambda x: cv2.arcLength(x, True), reverse=True) 
        largest_contour = contours[1] # 배경지도 외각선으로 인식하기에 두번째로 큰 외각선을 설정한다.
        
        # 꼭지점 좌표 찾기
        epsilon = 0.04 * cv2.arcLength(largest_contour, True)
        approx = cv2.approxPolyDP(largest_contour, epsilon, True)
        edge_point = []
        for point in approx:
            x, y = point[0]
            edge_point.append((x,y))

        left_top_screen = (float('inf'), float('inf'))
        right_top_screen = (float('-inf'), float('inf'))
        left_bottom_screen = (float('inf'), float('-inf'))
        right_bottom_screen = (float('-inf'), float('-inf'))

        for x, y in edge_point:
            if x + y < left_top_screen[0] + left_top_screen[1]:
                left_top_screen = (x, y)
            if x - y > right_top_screen[0] - right_top_screen[1]:
                right_top_screen = (x, y)
            if x - y < left_bottom_screen[0] - left_bottom_screen[1]:
                left_bottom_screen = (x, y)
            if x + y > right_bottom_screen[0] + right_bottom_screen[1]:
                right_bottom_screen = (x, y)
        
        src_points = np.float32([left_top_screen, right_top_screen, left_bottom_screen, right_bottom_screen])
        width, height = 800, 600  # 목표 이미지 크기
        dst_points = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        # 원근 변환 행렬 계산
        perspective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)
        # 이미지 평면화
        warped_image = cv2.warpPerspective(binary, perspective_matrix, (width, height))
        

        return warped_image
    

    def img_binarization(self, warped_image):
        RGB_img = cv2.cvtColor(warped_image, cv2.COLOR_BGR2RGB) # 그레이 색상의 이미지(warped_image)를 RGB로 변환
        R_img, G_img, B_img = cv2.split(RGB_img)

        N = 30
        for h in range(RGB_img.shape[0]):
            for w in range(RGB_img.shape[1]):
                if(np.int32(R_img[h,w])>N):
                    R_img[h,w] = G_img[h,w] = B_img[h,w] = 255
                else:
                    R_img[h,w] = G_img[h,w] = B_img[h,w] = 0

        RGB_img[:,:,0] = R_img
        RGB_img[:,:,1] = G_img
        RGB_img[:,:,2] = B_img

        # 방향과 숫자 분리
        trim_image_block = self.im_trim(RGB_img) #trim_image 변수에 결과물을 넣는다

        trim_image_num = self.im_trim_num(RGB_img) #trim_image 변수에 결과물을 넣는다


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
    
    def im_trim (self,img): 
        x = 154; y = 170; 
        w = 340; h = 250; 
        img_trim = img[y:y+h, x:x+w] 
        
        return img_trim 

    def im_trim_num (self,img): 
        x = 500; y = 170; 
        w = 175; h = 250; 
        img_trim = img[y:y+h, x:x+w]

        return img_trim
