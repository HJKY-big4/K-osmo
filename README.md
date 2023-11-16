# coding_AiProjcet
파이썬을 이용한 코딩 교구 제작

----
# 이미지 전처리
<p align="center">
  <img src="img_data/pending_img/전처리 전체.png" weight = "500">
</p>
이미지에 대한 자세한 설명
 - 원본이미지를 gray 스케일로 변경한다.## PI1

 - 이미지에 블러효과를 주어 잡티를 제거한다. ## PI2

 - 이진화를 진행한다. ## PI3

 - 이미지에서 교구의 꼭짓점을 찾는다. ## PI4

 - 구한 꼭짓점을 기준으로 이미지를 평면화 시켜준다. ## PI5

 - 이미지에서 방향과 숫자 부분을 따로 크롭하여 모델에 들어갈 수 있는 사이즈로 변경해준다. ## PI6, PI7


<br><br><br><br>
<h3 align="center"> 웹 구현 파트 </h3>
<br>
<div>
  <p align="center"> 주의사항! </p>
  <br>
  <p align="center"> 실행시 model_sep.h5 파일의 용량 문제로 아래의 링크에서 다운 받은 후 사용하셔야 합니다! </p>
  <br>
  <div align="center">
    <a href="https://drive.google.com/file/d/1TLBhdzT16R-N0e9M8J_2Npd6r9jqZqGj/view?usp=drive_link">모델다운 in 구글 드라이브</a>
  </div>
  <br>

  <h4 align="center"> ❗️ 프로그램 실행을 위한 준비!  </h4>
  <h4 align="center"> 1. 리포지토리의 code -> download.zip을 눌러 파일을 다운 받는다! </h4>
  
  <h4 align="center"> 2. "웹 최종 구현" 폴더 안에 있는 "model" 폴더에 링크에서 다운받은 "model_sep.h5"파일을 옮긴다. </h4>
  <br>
</div>

