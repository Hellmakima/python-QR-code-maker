# version 2-6
'''
# choose version
# make grid
# put alignments
input data encoding (alphanumeric/bytes) prefer bytes.
	# byte 8 bits per char and has all ascii
	AlphaNumeric is 6(5.8) bits per char (only 48 different chars) and stored compacted to fit 2 chars per 11 bits, so more chars but smaller character set
# input data
decide correction level (static/dynamic) or just fill random
	probaby will not need this part so do bare minimum(Low level)
	or try a work-around and fill with padding
# fill data
scramble 8 ways and choose best scrambling or just scramble 1 way
return code
scan and hope.for the best :)

refer
https://m.youtube.com/watch?v=w5ebcowAJD8
https://www.qrcode.com/en/about/version.html
cutt.ly/QRC1 or https://leiradel.github.io/2020/08/02/QR-Codes-on-the-ZX81.html

later:
	microqr
	all versions
'''


import pygame

QR_SIZE = 25
CELL_SIZE = 600//QR_SIZE
WIDTH = QR_SIZE * CELL_SIZE
HEIGHT = QR_SIZE * CELL_SIZE
BACKGROUND_COLOR = (255, 255, 255)  # White

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('QR Code')

qr_matrix = [[0]*QR_SIZE for y in range(QR_SIZE)]
colors = [(0,100,200), (0,200,100), 'black', 'white', 'red']
# x and y are flipped in some places. do not trust
# only binary encoding implemented

def read():
    global qr_matrix
    with open('/home/hell/Documents/python/QR/a.txt','r') as f:
        a = f.read().split(',')
        qr_matrix = [[0 if i=='0' else 1 for i in ii] for ii in a][:-1]
def update():
    with open('/home/hell/Documents/python/QR/b.txt','w') as f:
        for i in qr_matrix:
            f.write(''.join([str(ii) for ii in i]))
            f.write(',')


def init_graph():
    global qr_matrix
    def insert_block(x,y):
        # outer box
        for i in range(7):
            qr_matrix[x+0][i+y] = 2
            qr_matrix[x+i][0+y] = 2
            qr_matrix[x+6][i+y] = 2
            qr_matrix[x+i][6+y] = 2

        # inner box
        for i in range(2,5):
            for j in range(2,5):
                qr_matrix[x+i][y+j] = 2
        
        # white filling
        for i in range(5):
            qr_matrix[x+1+i][y+1] = 3
            qr_matrix[x+1][y+1+i] = 3
            qr_matrix[x+5][y+i+1] = 3
            qr_matrix[x+i+1][y+5] = 3
    
    insert_block(0,0)
    insert_block(0, QR_SIZE-7)
    insert_block(QR_SIZE-7, 0)

    # white saperation
    for i in range(8):
        qr_matrix[7][i] = 3
        qr_matrix[i][7] = 3
        qr_matrix[i][QR_SIZE-8] = 3
        qr_matrix[QR_SIZE-8][i] = 3
        qr_matrix[7][QR_SIZE-i-1] = 3
        qr_matrix[QR_SIZE-i-1][7] = 3

    # small box
    qr_matrix[QR_SIZE-7][QR_SIZE-7] = 2
    for i in range(5):
        qr_matrix[QR_SIZE-9+i][QR_SIZE-9] = 2
        qr_matrix[QR_SIZE-9][QR_SIZE-9+i] = 2
        qr_matrix[QR_SIZE-5][QR_SIZE-9+i] = 2
        qr_matrix[QR_SIZE-9+i][QR_SIZE-5] = 2
    for i in range(3):
        qr_matrix[QR_SIZE-8+i][QR_SIZE-8] = 3
        qr_matrix[QR_SIZE-8][QR_SIZE-8+i] = 3
        qr_matrix[QR_SIZE-6][QR_SIZE-8+i] = 3
        qr_matrix[QR_SIZE-8+i][QR_SIZE-6] = 3

    # zebra crossing
    for i in range(8,QR_SIZE-7):
        if i%2 == 0:
            qr_matrix[6][i] = 2
            qr_matrix[i][6] = 2
        else:
            qr_matrix[6][i] = 3
            qr_matrix[i][6] = 3
    
    # referance dots
    for i in range(9):
        if i < 8:
            qr_matrix[8][QR_SIZE-i-1] = 4
            qr_matrix[QR_SIZE-i-1][8] = 4
        if i == 6:
            continue
        qr_matrix[8][i] = 4
        qr_matrix[i][8] = 4
    qr_matrix[QR_SIZE-8][8] = 2
init_graph()

def draw_qr_code():
    screen.fill('black')
    for y in range(QR_SIZE):
        for x in range(QR_SIZE):
            color = colors[qr_matrix[y][x]]
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()
draw_qr_code()

data = 'hellmakima'
data = [f'{ord(i):08b}' for i in data] 
# print(bin(ord('@'))[2:].rjust(8,'0'))
data = ''.join(data)
data_length = len(data)//8
data = bin(data_length)[2:].rjust(8,'0') + data
formats = {
    'Numeric':'0001',
    'Alphanumeric':'0010',
    'Binary':'0100',
    'Kanji':'1000'}
data = formats['Binary'] + data

# TODO add paddind/error correction

def fill(data):
    up = True
    data_index = 0
    x,y = QR_SIZE-2, QR_SIZE-1
    while len(data) > data_index:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                pygame.quit()
        draw_qr_code()
        if qr_matrix[y][x+1] == 0:
            qr_matrix[y][x+1] = int(data[data_index])
            data_index += 1
        draw_qr_code()
        if qr_matrix[y][x] == 0:
            qr_matrix[y][x] = int(data[data_index])
            data_index += 1
        draw_qr_code()
        if up:
            y -= 1
            if y < 0:
                up = False
                y = 0
                x -= 2
                if x < 0:
                    for i in range(QR_SIZE):
                        qr_matrix[0][i] = int(data[data_index])
                        data_index += 1
                        draw_qr_code()
                    break
        else:
            y += 1
            if y == QR_SIZE:
                up = True
                y = QR_SIZE -1
                x -= 2
                if x < 0:
                    for i in range(QR_SIZE-1,-1,-1):
                        qr_matrix[0][i] = int(data[data_index])
                        data_index += 1
                        draw_qr_code()
                    break
fill(data)

def draw_final():
    screen.fill('black')
    for y in range(QR_SIZE):
        for x in range(QR_SIZE):
            color = 'white' if qr_matrix[y][x] in [0, 3] else 'black'
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()
draw_final()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            grid_x = x // CELL_SIZE
            grid_y = y // CELL_SIZE
            
            # Check if the clicked position is within bounds
            if 0 <= grid_x < QR_SIZE and 0 <= grid_y < QR_SIZE:
                # Toggle the cell state
                if qr_matrix[grid_y][grid_x] == 1 or qr_matrix[grid_y][grid_x] == 0:
                    qr_matrix[grid_y][grid_x] = 1 if qr_matrix[grid_y][grid_x] == 0 else 0
                draw_qr_code()
                # update()

pygame.quit()