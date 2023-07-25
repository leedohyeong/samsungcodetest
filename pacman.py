
m,t = 6,10
pac_x,pac_y = 2,2
with open('./input.txt', "r") as file:
    monsters =  [list(map(int,line.split())) for line in file]

pac_x, pac_y = pac_x - 1, pac_y - 1
dxs,dys = [-1,-1,0,1,1,1,0,-1],[0,-1,-1,-1,0,1,1,1]
pac_dxs,pac_dys = [-1,0,1,0],[0,-1,0,1]

arr = [[0 for _ in range(4)] for _ in range(4)]
dead_area = [[0 for _ in range(4)] for _ in range(4)]

monster_alive = [[[0 for _ in range(8)]for _ in range(4)] for _ in range(4)]
egg = [[[0 for _ in range(8)]for _ in range(4)] for _ in range(4)]

values =0
dead = []
def in_range(x, y):
    return 0 <= x and x < 4 and 0 <= y and y < 4

def pr(arr):
    for r in arr:
        for e in r:
            print(e, end = ' ')
        print()

def pr_2(arr):
    for r in arr:
        for e in r:
            print(sum(e), end = ' ')
        print()
def init():
    for i in range(m):
        monsters[i][0] -= 1
        monsters[i][1] -= 1
        monsters[i][2] -= 1

    arr[pac_x][pac_y] = 3
    for i in range(m):
        monster_alive[monsters[i][0]][monsters[i][1]][monsters[i][2]] += 1
init()


def clone():
    global egg

    for i in range(4):
        for j in range(4):
            for k in range(8):
                if monster_alive[i][j][k] != 0:
                    temp = monster_alive[i][j][k]
                    egg[i][j][k] = temp

def move():
    global monster_alive
    monster_temp = [[[0 for _ in range(8)] for _ in range(4)] for _ in range(4)]

    for i in range(4):
        for j in range(4):
            for k in range(8):
                for l in range(9):
                    if monster_alive[i][j][k] !=0:
                        temp = monster_alive[i][j][k]
                        new_loc = (k + l) % 8
                        new_x, new_y = i + dxs[new_loc], j + dys[new_loc]
                        if l ==8:
                            monster_temp[i][j][k] += temp
                        if in_range(new_x,new_y) and arr[new_x][new_y] !=3 and dead_area[new_x][new_y] >=0 :
                            monster_temp[new_x][new_y][new_loc] += temp
                            break

    pr(monster_temp)
    monster_alive = monster_temp

def pac_move():
    global pac_x,pac_y
    global dead
    new_x, new_y = pac_x, pac_y
    mid_x,mid_y = -1,-1
    one_x,one_y = -1,-1
    value = 0
    dead = []
    flag = True

    for a,b in zip(pac_dxs,pac_dys):
        if in_range(pac_x+a,pac_y+b):
            for c,d in zip(pac_dxs,pac_dys):
                if in_range(pac_x+a+c,pac_y+b+d):
                    for e,f in zip(pac_dxs,pac_dys):
                        if in_range(pac_x + a + c + e,pac_y + b + d + f):
                            temp = 0
                            for i in set([(pac_x + a, pac_y + b),(pac_x + a + c, pac_y + b + d),(pac_x + a + c + e, pac_y + b + d + f)]):
                                temp += sum(monster_alive[i[0]][i[1]])
                            if value < temp or flag :
                                value = temp
                                new_x, new_y = pac_x + a + c + e, pac_y + b + d + f
                                mid_x, mid_y = pac_x + a + c, pac_y + b + d
                                one_x, one_y = pac_x + a, pac_y + b
                                print((new_x, new_y),(mid_x,mid_y),(one_x,one_y))
                                flag = False

    arr[pac_x][pac_y] = 0
    pac_x, pac_y = new_x, new_y
    arr[pac_x][pac_y] = 3

    dead.append([new_x, new_y])
    dead.append([mid_x, mid_y])
    dead.append([one_x, one_y])


def monster_dead():
    global  monster_alive
    global dead_area
    for i,j in dead:
        if sum(monster_alive[i][j]) !=0:
            dead_area[i][j] = -3
            monster_alive[i][j] = [0,0,0,0,0,0,0,0]

def monster_reborn():
    global  monster_alive
    global egg

    for i in range(4):
        for j in range(4):
            for k in range(8):
                if egg[i][j][k] != 0:
                    monster_alive[i][j][k] += egg[i][j][k]
def heal():
    global dead_area
    for i in range(4):
        for j in range(4):
            if dead_area[i][j] < 0:
                dead_area[i][j] +=1

# heal()
for time in range(t):
    heal()
    clone()
    move()
    pac_move()
    monster_dead()
    monster_reborn()

cnt = 0
for i in range(4):
    for j in range(4):
        for k in range(8):
            cnt += monster_alive[i][j][k]
print(cnt)