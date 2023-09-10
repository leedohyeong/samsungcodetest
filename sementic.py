n = int(input())
arr = list(list(map(int,input().split())) for _ in range(n))

visited =  list(list([0 for _ in range(n)]) for _ in range(n))
group_area =  list(list([0 for _ in range(n)]) for _ in range(n))
#
values = 0
group_nums = []
area = []

cnt = 0
dxs,dys = [-1,0,1,0],[0,1,0,-1]


def in_range(x,y):
    return 0 <= x and x < n and 0 <= y and y< n

def can_go(x,y,key,group_num):
    global group_nums

    if not in_range(x,y):
        return False
    if visited[x][y] == 1:
        return False
        # 만나는 번호가 다를 때 그룹 nums에 현재 그룹 다음좌표 그룹 값 넣기
    if arr[x][y] != key:
        group_nums.append((group_num,group_area[x][y]))
        return False
    return True

def dfs(x,y,key,group_num):
    global cnt

    for dx,dy in zip(dxs,dys):
        new_x,new_y = x+dx,y+dy
        if can_go(new_x,new_y,key,group_num):
            visited[new_x][new_y] = 1
            group_area[new_x][new_y] = group_num
            cnt +=1
            dfs(new_x,new_y,key,group_num)

# 그룹배열만들기와 그룹의 영역넓이 구하기
def grouping():
    global cnt #
    global area
    global visited
    visited = list(list([0 for _ in range(n)]) for _ in range(n))

    area = []
    group_num = 1
    for x in range(n):
        for y in range(n):
            if visited[x][y] == 0:
                cnt = 1
                visited[x][y] = 1
                key = arr[x][y]
                group_area[x][y] = group_num

                dfs(x,y,key,group_num)
                area.append([key,cnt])
                group_num += 1

# 그룹 배열과 현재배열을 비교하며 만나는 면마다 그룹 번호 적어주기
def counting():
    global group_nums
    global visited
    visited = list(list([0 for _ in range(n)]) for _ in range(n))
    group_nums = []
    group_num = 1
    for x in range(n):
        for y in range(n):
            if visited[x][y] == 0:
                visited[x][y] = 1
                key = arr[x][y]
                group_area[x][y] = group_num
                dfs(x,y,key,group_num)
                group_num += 1

# 계산
def cal():
    global area
    global group_nums
    global values
    for g in set(group_nums):
        a_index = g[0]-1
        b_index = g[1]-1
        values+= (area[a_index][1]+area[b_index][1])*area[a_index][0]*area[b_index][0]*group_nums.count(g)

# rotate
def rotate():
    temp  = list(list([0 for _ in range(n)]) for _ in range(n))
    x = n//2
    for i in range(n):
        temp[x][i] = arr[i][x]
    for i in range(n):
        temp[n-i-1][x] = arr[x][i]
    # 1
    for i in range(x):
        for j in range(x):
            temp[j][x-i-1] = arr[i][j]

    for i in range(x+1,n):
        for j in range(x):
            temp[j+x+1][x-(i+1)+x+1] = arr[i][j]

    for i in range(x):
        for j in range(x+1,n):
            temp[j-(x+1)][x-(i+1)+x+1] = arr[i][j]

    for i in range(x+1,n):
        for j in range(x+1,n):
            temp[j][x-(i+1)+2*(x+1)] = arr[i][j]


    for i in range(n):
        for j in range(n):
            arr[i][j] = temp[i][j]

for _ in range(4):
    grouping()
    counting()
    cal()
    rotate()
print(values)