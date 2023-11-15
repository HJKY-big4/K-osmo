import cv2
import numpy as np



class DataLoad:

    # 한글로 된 경로를 읽어올 수 있다.
    def hangulRead ( filePath ) :
        stream = open( filePath.encode("utf-8") , "rb")
        bytes = bytearray(stream.read())
        numpyArray = np.asarray(bytes, dtype=np.uint8)

        return cv2.imdecode(numpyArray , cv2.IMREAD_UNCHANGED)

,