<h3 align="center"> HJKY-big4 프로젝트 K-OSMO </h3>
<h4 align="center"> 파이썬을 이용한 코딩 교구 제작 </h4>
<br><br>

<br>

> 천재교육 빅데이터 개발자 양성과정 4기 <br>
> 개발기간: 2023.10.30 ~ 2023.11.17 (3주)

<br>
<div align="center">
  <p> 팀원 소개 </p>
  <table border="1">
    <tr>
      <td>현동호: <a href="https://github.com/donghohyun" >개인 깃허브</a>
        </td>
      <td>전혁선: </td>
    </tr>
    <tr>
      <td>강형근: </td>
      <td>유선준: </td>
    </tr>
  </table> 
</div>

<div>
  <h3> 프로젝트 소개 </h3>
  <p> 유아기 아이들에게 퍼즐과 같은 교구를 활용하여 블록코딩을 접하게 함으로써 흥미를 유발시키고 프로그래밍에 있어 거부감을 삭감하고 창의성과 논리적 사고를 기를 수 있도록 한다. </p>
</div>

<br><br><br><br>

---
# 블록코딩 교구 제작
이미지 인식률을 높이고 영유아로 하여금 퍼즐과 같이 블록들을 체결하도록 함으로써 프로그래밍의 흥미유발과 함께 창의성, 논리적 사고방식을 기르고자 하였다.
<p align="center">
  <img src="https://github.com/HJKY-big4/K-osmo/assets/139213175/f306cb8e-1ea5-46f8-9ac9-3f2113f3a2f5">
</p>

- 퍼즐과 같은 체결방식을 통해 이미지 인식 시 회전을 고려하지 않아도 되도록 하였다.
- 블록을 넣는 가이드를 제공해줌으로써 아이들에게 재미요소를 추가해주며, 이미지 인식 시 이미지에서 블록의 평면화가 용이해짐
- 대비가 강한 색감을 이용하여 이미지 인식률을 높이고자 하였다.

----
# 이미지 전처리
<p align="center">
  <img src="img_data/image/전처리 전체.png" weight = "500">
</p>
  
 - 원본이미지를 gray 스케일로 변경한다.## PI1
 - 이미지에 블러효과를 주어 잡티를 제거한다. ## PI2
 - 이진화를 진행한다. ## PI3
 - 이미지에서 교구의 꼭짓점을 찾는다. ## PI4
 - 구한 꼭짓점을 기준으로 이미지를 평면화 시켜준다. ## PI5
 - 평면화 한 이미지를 PI1~PI3 과정을 다시거쳐 이진화 시켜준다. ## PI3.1 
 - 이미지에서 방향과 숫자 부분을 따로 크롭하여 모델에 들어갈 수 있는 사이즈로 변경해준다. ## PI6, PI7

---
<br><br><br><br>
<h3 align="center"> 웹 구현 파트 </h3>
<br>

<div align="center">
  <h3> 시작 가이드 </h3>
  <br>
  * python 3.9 이상 <br>
  * pycharm 2022.2 community version 이상 <br>
  * windows 10 이상 <br>

  <p> 준비사항! </p>
  <br>
  <p> 실행시 model_sep.h5 파일의 용량 문제로 아래의 링크🔽에서 다운 받은 후 사용하셔야 합니다! </p>
  <div>
    <a href="https://drive.google.com/file/d/1TLBhdzT16R-N0e9M8J_2Npd6r9jqZqGj/view?usp=drive_link"> 모델 download in 구글 드라이브 </a>
  </div>
  <br>
  
  <h4> installation </h4> 
  <h5> 터미널에서 실행 🔽 </h5>
  <code>git clone https://github.com/HJKY-big4/K-osmo.git</code>
</div>

<div>

  <br>

  <h4 align="center"> ❗️ 프로그램 실행을 위한 준비!  </h4>
  <h4 align="center"> 1. 리포지토리의 code -> download.zip을 눌러 파일을 다운 받는다! </h4>
  <h4 align="center"> 2. "웹 최종 구현" 폴더 안에 있는 "model" 폴더에 링크에서 다운받은 "model_sep.h5"파일을 옮긴다. </h4>
  <br>

  <div align="center"> 
    <h3> 컴퓨터에 연결할 웹캠 </h3>
    <img src="웹 구현 최종/이미지파일/camera.jpg" width="30%" heigt="30%" alt="필요한_카메라">
  </div>

  
</div>

<div align="center">
  <h2> Stacks </h2>
  <div>
    <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=Python&logoColor=white"/>
    

  </div>
</div>

<div align="center">
  <h2> 화면구성 </h2>
  <table border="1">
    <tr>
      <td>
        <strong>첫 번째 칸</strong><br>
        이 칸은 첫 번째 설명란입니다.
      </td>
      <td>
        <strong>두 번째 칸</strong><br>
        이 칸은 두 번째 설명란입니다.
      </td>
    </tr>
    <tr>
      <td>
        <strong>세 번째 칸</strong><br>
        이 칸은 세 번째 설명란입니다.
      </td>
      <td>
        <strong>네 번째 칸</strong><br>
        이 칸은 네 번째 설명란입니다.
      </td>
    </tr>
  </table>
</div>


<h3 align="center"> 첫 시행화면 </h3>

<div>
  <h3> Prezi로 최종 발표 </h3>
  <a href="https://prezi.com/view/qUNAH6YLxnHAxNKfAUKP/">발표내용 확인하기(Prezi)</a>

  <br>
  <a style="color: inherit; text-decoration: none;" href="https://youtu.be/IRs1-0oI75o"> 시연영상 확인하기(YouTube) </a>
</div>
