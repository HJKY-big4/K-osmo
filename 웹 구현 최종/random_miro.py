from collections import deque
import random

def generate_maze(n):
    def obstacle_func(miro, n):
        obstacles = (n-2)*(n-2)
        tmp = []
        for _ in range(obstacles):
            x, y = random.randint(1, n), random.randint(1, n)
            tmp.append([x, y])
        for x, y in tmp:
            miro[x][y] = 5

        miro[1][1] = 0
        miro[n][n] = 0

    def check(x, y, miro, n):
        dx = [-1, 1, 0, 0]
        dy = [0, 0, -1, 1]
        q = deque()
        q.append([x, y])

        visited = [[0 for _ in range(n + 2)] for _ in range(n + 2)]
        visited[x][y] = 1

        while q:
            x, y = q.popleft()
            if x == n and y == n:
                return True
            for i in range(4):
                nx = x + dx[i]
                ny = y + dy[i]
                if 1 <= nx <= n and 1 <= ny <= n and visited[nx][ny] == 0 and miro[nx][ny] != 5:
                    visited[nx][ny] = 1
                    q.append([nx, ny])
        return False

    def generate_miro(n):
        maze = False
        while 1:
            miro = [[1 for _ in range(n + 2)] for _ in range(n + 2)]
            
            for i in range(1, n + 1):
                for j in range(1, n + 1):
                    miro[i][j] = 0

            obstacle_func(miro, n)
            maze = check(1, 1, miro, n)

            # 시작지점과 도착지점이 잘 연결되어 있다면 반복문 종료
            if maze == True:
                break
                
        miro[1][1] = 6
        miro[n][n] = 9
        

        return miro

        

    return generate_miro(n)