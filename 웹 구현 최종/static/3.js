// 3.js

let mazeData; // 전역 변수로 선언
let mazeElement = document.getElementById('maze-container'); // 전역 변수로 정의
let currentRow = 1;
let currentCol = 1;

function drawMaze(mazeData) {
    mazeElement.innerHTML = ''; // 이전 미로를 지우고 새로운 미로를 그림

    mazeData.forEach((row, rowIndex) => {
        const rowElement = document.createElement('div');
        rowElement.classList.add('maze-row');
        row.forEach((cell, colIndex) => {
            const cellElement = document.createElement('div');
            cellElement.classList.add('maze-cell');
            if (cell === 1) {
                cellElement.classList.add('wall');
            } else if (cell === 6) {
                cellElement.classList.add('start');
            } else if (cell === 9) {
                cellElement.classList.add('end');
            } else if (cell === 5) {
                cellElement.classList.add('obstacle');
            }
            rowElement.appendChild(cellElement);
        });
        mazeElement.appendChild(rowElement);
    });
}

function getAndDrawMaze() {
    // 추가된 부분: 사용자가 입력한 미로 크기 가져오기
    let mazeSize = document.getElementById("mazeSize").value;

    fetch(`/get_maze?size=${mazeSize}`)
        .then(response => response.json())
        .then(data => {
            mazeData = data; // 전역 변수에 미로 데이터 저장
            currentRow = 1; // 플레이어의 초기 행 위치 설정
            currentCol = 1; // 플레이어의 초기 열 위치 설정
            drawMaze(mazeData); // 미로 그리기
            document.addEventListener('keydown', movePlayer); // 플레이어 이동 이벤트 리스너 등록
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
