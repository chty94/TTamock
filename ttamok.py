from bangtal import *
import queue
import time

'''
- 돌 놓을때 소리 추가
'''

#   5개가 이어지면 게임 승리 (알고리즘)
def complete(matrix, i): # i는 흑돌인지 백돌인지 확인 (i = 1 or 10)
    # 경기 결과가 변화가 없으면 0리턴 흑돌이 이기면 1리턴 백돌이 이기면 10리턴

    # 가로로 5개
    for start in range(0, 343, 19):
        for index in range(0, 15):
            if sum(matrix[start+index:start+index+5]) == 5*i:
                return i
    # 세로로 5개
    for index in range(0, 285):
        if sum(matrix[index:index+77:19]) == 5*i:
            return i

    # 대각선 5개(왼위오아)
    for index in range(0, 281):
        if sum(matrix[index:index+81:20]) == 5*i:
            return i

    # 대각선 5개(왼아오위)
    for start in range(4, 271, 19):
        for index in range(0, 15):
            if sum(matrix[start+index:start+index+73:18]) == 5*i:
                return i
    
    return 0 # 끝이 나지 않았음을 나타내는 리턴값

#   따목 규칙 추가 (알고리즘)
def delete(matrix, i, j, index): # i : 최근 돌 / j : 따일 돌 / index: 둔 위치
    # 삭제할 인덱스 번호 리턴
    startLine = index // 19
    INDEX = []
    if startLine >= 3 and (index-20) // 19 == startLine-1 and (index-40) // 19 == startLine-2 and (index-60) // 19 == startLine-3:
        if matrix[index-20] == j and matrix[index-40] == j and matrix[index-60] == i:
            INDEX.append((index-20, index-40))
    if startLine >= 3 and (index-19) // 19 == startLine-1 and (index-38) // 19 == startLine-2 and (index-57) // 19 == startLine-3:
        if matrix[index-19] == j and matrix[index-38] == j and matrix[index-57] == i:
            INDEX.append((index-19, index-38))
    if startLine >= 3 and (index-18) // 19 == startLine-1 and (index-36) // 19 == startLine-2 and (index-54) // 19 == startLine-3:
        if matrix[index-18] == j and matrix[index-36] == j and matrix[index-54] == i:
            INDEX.append((index-18, index-36))
    if (index-3) // 19 == startLine:
        if matrix[index-1] == j and matrix[index-2] == j and matrix[index-3] == i:
            INDEX.append((index-1, index-2))
    if (index+3) // 19 == startLine:
        if matrix[index+1] == j and matrix[index+2] == j and matrix[index+3] == i:
            INDEX.append((index+1, index+2))
    if startLine <= 15 and (index+18) // 19 == startLine+1 and (index+36) // 19 == startLine+2 and (index+54) // 19 == startLine+3:
        if matrix[index+18] == j and matrix[index+36] == j and matrix[index+54] == i:
            INDEX.append((index+18, index+36))
    if startLine <= 15 and (index+19) // 19 == startLine+1 and (index+38) // 19 == startLine+2 and (index+57) // 19 == startLine+3:
        if matrix[index+19] == j and matrix[index+38] == j and matrix[index+57] == i:
            INDEX.append((index+19, index+38))
    if startLine <= 15 and (index+20) // 19 == startLine+1 and (index+40) // 19 == startLine+2 and (index+60) // 19 == startLine+3:
        if matrix[index+20] == j and matrix[index+40] == j and matrix[index+60] == i:
            INDEX.append((index+20, index+40))
    if len(INDEX) != 0:
        return INDEX
    else:
        return 0 # 따일 필요가 업는 경우 0 리턴        

#   인덱스를 찾는 함수
def find_index(x, y):
    temp = x//32 + 19*((611-y)//32)
    if temp < 0:
        return temp+19
    else:
        return temp

#   인덱스를 통해 좌표값을 찾는 함수
def find_xy(index):
    Q = index // 19
    R = index % 19
    return (348 + R*32, 68 + (18-Q)*32)

white_before = [[0]]               # 전에 백돌을 땄는지를 확인
black_before = [[0]]               # 전에 흑돌을 땄는지를 확인
count = 0                       # 몇 수인지 + 누구 차례인지 확인
tt = 0                          # 게임이 끝났는지 확인
seq = queue.LifoQueue()         # 뒤로 돌아갈떄 필요한 변수
timer = Timer(0.)               # 몇 수 인지 표시
removeDwhite = 0                # 따낸 백돌
removeDblack = 0                # 따낸 흑돌

setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)

scene = Scene('따목', 'images/big5.jpg')
board = Object("images/Blank_Go_board-612.png")
board.locate(scene, 346, 66)
board.show()

black = [Object('images/black-go-stone32.png') for _ in range(180)] # 흑돌
white = [Object('images/white-go-stone32.png') for _ in range(180)] # 백돌

restartButton = Object('images/restart.png')
restartButton.locate(scene, 12, 550)
restartButton.setScale(0.20)
restartButton.show()

undoButton = Object('images/undo.png')
undoButton.locate(scene, 110, 565)
undoButton.setScale(0.16)
undoButton.show()

endButton = Object('images/end.png')
endButton.locate(scene, 198, 560)
endButton.setScale(0.18)
endButton.show()

DeadBlackStone = Object('images/DeadBlack.png')
DeadBlackStone.locate(scene, 6, 425)
DeadBlackStone.setScale(0.8)
DeadBlackStone.show()

DeadWhiteStone = Object('images/DeadWhite.png')
DeadWhiteStone.locate(scene, 6, 300)
DeadWhiteStone.setScale(0.8)
DeadWhiteStone.show()

BlackTurn = Object('images/Blackturn.png')
BlackTurn.locate(scene, 980, 450)
BlackTurn.setScale(0.8)
BlackTurn.show()

WhiteTurn = Object('images/Whiteturn.png')
WhiteTurn.locate(scene, 980, 450)
WhiteTurn.setScale(0.8)
BlackTurn.show()


#   보드판 배열
matrix = [0 for _ in range(361)] # 따목판 상태(흑,백) 표시(1, 10)
matrix_index = [-1 for _ in range(361)] # 따목판 상태(오브젝트 인덱스) 표시

#   숫자 배열
black_numbers = []
white_numbers = []

black_numbers.append([Object('images/0.png'), Object('images/0.png')]) # 0
black_numbers.append([Object('images/0.png'), Object('images/2.png')]) # 1
black_numbers.append([Object('images/0.png'), Object('images/4.png')]) # 2
black_numbers.append([Object('images/0.png'), Object('images/6.png')]) # 3
black_numbers.append([Object('images/0.png'), Object('images/8.png')]) # 4
black_numbers.append([Object('images/1.png'), Object('images/0.png')]) # 5
black_numbers.append([Object('images/1.png'), Object('images/2.png')]) # 6
black_numbers.append([Object('images/1.png'), Object('images/4.png')]) # 7
black_numbers.append([Object('images/1.png'), Object('images/6.png')]) # 8

white_numbers.append([Object('images/0.png'), Object('images/0.png')]) # 0
white_numbers.append([Object('images/0.png'), Object('images/2.png')]) # 1
white_numbers.append([Object('images/0.png'), Object('images/4.png')]) # 2
white_numbers.append([Object('images/0.png'), Object('images/6.png')]) # 3
white_numbers.append([Object('images/0.png'), Object('images/8.png')]) # 4
white_numbers.append([Object('images/1.png'), Object('images/0.png')]) # 5
white_numbers.append([Object('images/1.png'), Object('images/2.png')]) # 6
white_numbers.append([Object('images/1.png'), Object('images/4.png')]) # 7
white_numbers.append([Object('images/1.png'), Object('images/6.png')]) # 8

for number in black_numbers:
    for i in range(2):
        number[0].locate(scene, 175, 425)
        number[1].locate(scene, 255, 425)
        number[0].setScale(0.1)
        number[1].setScale(0.1)

for number in white_numbers:
    for i in range(2):
        number[0].locate(scene, 175, 300)
        number[1].locate(scene, 255, 300)
        number[0].setScale(0.1)
        number[1].setScale(0.1)

black_numbers[0][0].show()
black_numbers[0][1].show()
white_numbers[0][0].show()
white_numbers[0][1].show()


def endButton_onMouseAction(x, y, action):
    endGame()
endButton.onMouseAction = endButton_onMouseAction

def restartButton_onMouseAction(x, y, action):
    global count
    global seq
    global timer
    global black
    global white
    global matrix
    global matrix_index
    global tt
    global removeDblack
    global removeDwhite
    global black_before
    global white_before


    # 기존 오브젝트들 숨기기
    if count%2 == 0: # ex.4 6 8
        for i in range(int(count/2)):
            black[i].hide()
            white[i].hide() 
    else: # ex 3 5 7
        for i in range(int((count+1)/2)):
            black[i].hide()
            white[i].hide()

    # 변수 초기화
    black_before = [0]
    white_before = [0]
    count = 0 
    seq = queue.LifoQueue()
    tt = 0
    
    black_numbers[removeDblack//2][0].hide()
    black_numbers[removeDblack//2][1].hide()
    white_numbers[removeDwhite//2][0].hide()
    white_numbers[removeDwhite//2][1].hide()
    removeDblack = 0
    removeDwhite = 0
    black_numbers[0][0].show()
    black_numbers[0][1].show()
    white_numbers[0][0].show()
    white_numbers[0][1].show()

    restartButton.show()
    endButton.show()
    BlackTurn.show()
    WhiteTurn.hide()

    # 보드판 배열 초기화
    matrix = [0 for _ in range(361)] # 따목판 상태(흑,백) 표시
    matrix_index = [-1 for _ in range(361)] # 따목판 상태(오브젝트 인덱스) 표시
    
    # 몇번째 수인지 알려주는 타이머 초기화
    timer = Timer(0.)
    showTimer(timer) 
restartButton.onMouseAction = restartButton_onMouseAction

def undoButton_onMouseAction(x, y, action):
    global seq
    global count
    global removeDblack
    global removeDwhite
    global black_before
    global white_before
    global matrix
    global matrix_index

    token = 0
    if count == 0:
        return
    
    # 따낸 경우에만 추가하는 경우
    b = black_before[-1]
    w = white_before[-1]

    if count%2 == 0 and len(b) >= 2:
        token = 1
        b = black_before.pop()
        for i in range(2, len(b)):
            black[b[i][0]].locate(scene, find_xy(b[1][i-2][0])[0], find_xy(b[1][i-2][0])[1])
            black[b[i][1]].locate(scene, find_xy(b[1][i-2][1])[0], find_xy(b[1][i-2][1])[1])
            black[b[i][0]].show()
            black[b[i][1]].show()
            matrix[b[1][i-2][0]] = 1
            matrix[b[1][i-2][1]] = 1

            matrix_index[b[1][i-2][0]] = b[i][0]
            matrix_index[b[1][i-2][1]] = b[i][1]
            
            black_numbers[removeDblack//2][0].hide()
            black_numbers[removeDblack//2][1].hide()
            removeDblack -= 2
            black_numbers[removeDblack//2][0].show()
            black_numbers[removeDblack//2][1].show()
                 
    elif count%2 == 1 and len(w) >= 2:               # 백이 둘 차례에서 뒤로가기
        token = 1
        w = white_before.pop()
        for i in range(2, len(w)):
            white[w[i][0]].locate(scene, find_xy(w[1][i-2][0])[0], find_xy(w[1][i-2][0])[1])
            white[w[i][1]].locate(scene, find_xy(w[1][i-2][1])[0], find_xy(w[1][i-2][1])[1])
            white[w[i][0]].show()
            white[w[i][1]].show()
            matrix[w[1][i-2][0]] = 10
            matrix[w[1][i-2][1]] = 10
            matrix_index[w[1][i-2][0]] = w[i][0]
            matrix_index[w[1][i-2][1]] = w[i][1]

            white_numbers[removeDwhite//2][0].hide()
            white_numbers[removeDwhite//2][1].hide()
            removeDwhite -= 2
            white_numbers[removeDwhite//2][0].show()
            white_numbers[removeDwhite//2][1].show()  

    # 한수 무르기 하는경우
    index = seq.get()

    blackORwhite = matrix[index] # 1 OR 10
    i = matrix_index[index]

    if blackORwhite == 1 and token == 0:
        black[i].hide()
        white_before.pop()
        BlackTurn.show()
        WhiteTurn.hide()
    elif blackORwhite == 10 and token == 0:
        white[i].hide()
        black_before.pop()
        BlackTurn.hide()
        WhiteTurn.show()      
    elif blackORwhite == 1 and token == 1:
        black[i].hide()
        BlackTurn.show()
        WhiteTurn.hide()
    elif blackORwhite == 10 and token == 1:
        white[i].hide()
        BlackTurn.hide()
        WhiteTurn.show()      

    matrix[index] = 0
    matrix_index[index] = -1
    count -= 1
    if count == 1:
        black_before = [[0]]
    elif count == 0:
        white_before = [[0]]

    timer = Timer(float(count))
    showTimer(timer)
undoButton.onMouseAction = undoButton_onMouseAction

def onMouseAction_board(x, y, action):
    global count
    global matrix
    global matrix_index
    global tt
    global removeDblack
    global removeDwhite
    global white_before
    global black_before

    index = find_index(x, y)

    # 돌 순서 기억
    seq.put(index)
    
    X, Y = find_xy(index)
    if count % 2 == 0: # 흑이 둘 차례 (1)
        BlackTurn.hide()
        WhiteTurn.show()
        matrix[index] = 1
        matrix_index[index] = count // 2
        black[count//2].locate(scene, X, Y)
        black[count//2].show()

        comp = complete(matrix, 1)
        if comp != 0 and tt == 0: # 게임 종료 # 5개의 연속된 돌로 종료
            showMessage("흑이 승리했습니다!!(재시작, 한수돌리기, 나가기)\n따목판에 돌을 막 놓을 수 있습니다")
            tt = 1


        delete_white = delete(matrix, 1, 10, index)
        if delete_white != 0 and tt == 0:
            white_numbers[removeDwhite//2][0].hide()
            white_numbers[removeDwhite//2][1].hide()
            removeDwhite += 2*(len(delete_white))
            white_numbers[removeDwhite//2][0].show()
            white_numbers[removeDwhite//2][1].show()       
            
            temp = len(delete_white)
            white_before.append([1, delete_white])    # 이번턴에 백돌을 땄다는 의미
            for i in range(temp):
                matrix[delete_white[i][0]] = 0
                matrix[delete_white[i][1]] = 0
                white[matrix_index[delete_white[i][0]]].hide()
                white[matrix_index[delete_white[i][1]]].hide()
                white_before[-1].append([matrix_index[delete_white[i][0]],matrix_index[delete_white[i][1]]])
                matrix_index[delete_white[i][0]] = -1
                matrix_index[delete_white[i][1]] = -1
        else:
            white_before.append([0])    # 이번턴에 백돌을 따지 않았다는 의미
        
        if removeDwhite == 16 and tt == 0: # 게임 종료 # 따낸 돌수로 종료
            showMessage("흑이 승리했습니다!!(재시작, 한수돌리기, 나가기)\n따목판에 돌을 막 놓을 수 있습니다")
            tt = 1

        count += 1
    else: # 백이 둘 차례 (10)
        BlackTurn.show()
        WhiteTurn.hide()

        matrix[index] = 10
        matrix_index[index] = count // 2
        white[count//2].locate(scene, X, Y)
        white[count//2].show()

        comp = complete(matrix, 10)
        if comp != 0 and tt == 0: # 게임 종료
            showMessage("백이 승리했습니다!!(재시작, 한수돌리기, 나가기)\n따목판에 돌을 막 놓을 수 있습니다")
            tt = 1

        delete_black = delete(matrix, 10, 1, index)
        if delete_black != 0 and tt == 0:
            black_numbers[removeDblack//2][0].hide()
            black_numbers[removeDblack//2][1].hide()
            removeDblack += 2*(len(delete_black))
            black_numbers[removeDblack//2][0].show()
            black_numbers[removeDblack//2][1].show()

            temp = len(delete_black)
            black_before.append([1, delete_black]) # 이번턴에 흑돌을 땄다는 의미

            for i in range(temp):
                matrix[delete_black[i][0]] = 0
                matrix[delete_black[i][1]] = 0
                black[matrix_index[delete_black[i][0]]].hide()
                black[matrix_index[delete_black[i][1]]].hide()
                black_before[-1].append([matrix_index[delete_black[i][0]],matrix_index[delete_black[i][1]]])
                matrix_index[delete_black[i][0]] = -1
                matrix_index[delete_black[i][1]] = -1

        else:
            black_before.append([0]) # 이번턴에 흑돌을 따지 않았다는 의미

        if removeDblack == 16 and tt == 0: # 게임 종료 # 따낸 돌수로 종료
            showMessage("흑이 승리했습니다!!(재시작, 한수돌리기, 나가기)\n따목판에 돌을 막 놓을 수 있습니다")
            tt = 1



        count += 1
    timer = Timer(float(count))
    showTimer(timer)
board.onMouseAction = onMouseAction_board

showTimer(timer)
startGame(scene)