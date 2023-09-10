n,m,k = 5,4,1


with open('./input.txt', "r") as file:
    arr =  [list(map(int,line.split())) for line in file]

grid = arr[:n]
new_grid = [[[0 for _ in range(n*n)] for _ in range(n)] for _ in range(n)]
# x,y,d,s 좌표 방향 초기 능력치
# 위치는 겹치지 않으며 초기 위치에는 총이 없음
# 0은 빈칸 0보다 큰 건 총의 공격력

player = arr[n:]
players = [[0,0,0,0,0] for _ in range(m)]
player_ground = [[-1 for _ in range(n)] for _ in range(n)]
point = [0 for _ in range(m)]
# 시계방향
dxs,dys = [-1,0,1,0],[0,1,0,-1]

def in_range(x, y):
    return 0 <= x and x < n and 0 <= y and y < n

def pr(arr):
    for r in arr:
        for e in r:
            print(e, end = ' ')
        print()

def init():
    for idx,_ in enumerate(player):
        player[idx][0] -= 1
        player[idx][1] -= 1

    for x in range(n):
        for y in range(n):
            new_grid[x][y][0] = grid[x][y]

    for idx,play in zip(range(m),player):
        x,y,d,s = play
        players[idx] = [x,y,d,s,0]
init()

def player_move():
    #play_ground 초기화
    player_ground = [[-1 for _ in range(n)] for _ in range(n)]

    for idx,play in zip(range(m),players):
        x,y,_,_,_ = play
        player_ground[x][y] = idx

    for idx,play in zip(range(m),players):
        x,y,d,s,get_gun = play
        new_x, new_y = dxs[d]+x, dys[d]+y
        if in_range(new_x,new_y):
            players[idx][0] = new_x
            players[idx][1] = new_y
        else:
            new_x, new_y = dxs[(d+2)%4]+x, dys[(d+2)%4]+y
            players[idx][0] = new_x
            players[idx][1] = new_y

        # 플레이어가 없으면서 총이 있는 경우
        if new_grid[new_x][new_y][0] != 0 and player_ground[new_x][new_y] == -1:
            if get_gun < max(new_grid[new_x][new_y]):
                new_grid[new_x][new_y].append(get_gun)
                players[idx][-1] = max(new_grid[new_x][new_y])
                gun_idx = new_grid[new_x][new_y].index( max(new_grid[new_x][new_y]))
                new_grid[new_x][new_y].pop(gun_idx)
            player_ground[new_x][new_y] = idx
            player_ground[x][y] = -1

        # 플레이어가 있는 경우
        if player_ground[new_x][new_y] >= 0:
            first = player_ground[new_x][new_y]
            x_1,y_1,d_1,s_1,get_gun_1 = players[first]
            # 먼저 들어온 사람이 이긴 경우
            if (get_gun_1+s_1-s-get_gun) > 0 or ( (get_gun_1+s_1-s-get_gun) == 0 and s_1 > s):
                point[first] += (get_gun_1+s_1-s-get_gun)
                for i in range(4):
                    new_x, new_y = dxs[(d + i) % 4] + new_x, dys[(d + i) % 4] + new_y
                    if in_range(new_x,new_y) and player_ground[new_x][new_y] == -1:
                        player_ground[new_x][new_y] = idx
                        player_ground[x][y] = -1

            # 현재 플레이어가 이긴 경우
            if (get_gun_1 + s_1 - s - get_gun) < 0 or ( (get_gun_1+s_1-s-get_gun) == 0 and s_1 < s):
                point[idx] += abs(get_gun_1 + s_1 - s - get_gun)
                for i in range(4):
                    new_x, new_y = dxs[(d + i) % 4] + new_x, dys[(d + i) % 4] + new_y
                    if in_range(new_x,new_y) and player_ground[new_x][new_y] == -1:
                        player_ground[new_x][new_y] = idx
                        player_ground[x][y] = -1

        # print(idx,point)
        # 플레이어가 없으면서 총이 없는 경우

player_move()
print(point)
