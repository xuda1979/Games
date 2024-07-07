import pygame
import sys
import logging

# 初始化Pygame
pygame.init()

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# 屏幕尺寸
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
GRID_SIZE = 80
BOARD_OFFSET = 40

# 颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 创建屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('中国象棋')

# 加载并缩小图像
def load_and_scale_image(path, scale):
    image = pygame.image.load(path)
    scaled_image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
    return scaled_image

scale_factor = 0.2
images = {
    '红车': load_and_scale_image('images/red_car.png', scale_factor),
    '红马': load_and_scale_image('images/red_horse.png', scale_factor),
    '红相': load_and_scale_image('images/red_elephant.png', scale_factor),
    '红仕': load_and_scale_image('images/red_guard.png', scale_factor),
    '红帅': load_and_scale_image('images/red_general.png', scale_factor),
    '红兵': load_and_scale_image('images/red_soldier.png', scale_factor),
    '红炮': load_and_scale_image('images/red_cannon.png', scale_factor),
    '黑车': load_and_scale_image('images/black_car.png', scale_factor),
    '黑马': load_and_scale_image('images/black_horse.png', scale_factor),
    '黑相': load_and_scale_image('images/black_elephant.png', scale_factor),
    '黑仕': load_and_scale_image('images/black_guard.png', scale_factor),
    '黑将': load_and_scale_image('images/black_general.png', scale_factor),
    '黑卒': load_and_scale_image('images/black_soldier.png', scale_factor),
    '黑炮': load_and_scale_image('images/black_cannon.png', scale_factor)
}

# 棋盘布局
board = [
    ['黑车', '黑马', '黑相', '黑仕', '黑将', '黑仕', '黑相', '黑马', '黑车'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', '黑炮', ' ', ' ', ' ', ' ', ' ', '黑炮', ' '],
    ['黑卒', ' ', '黑卒', ' ', '黑卒', ' ', '黑卒', ' ', '黑卒'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['红兵', ' ', '红兵', ' ', '红兵', ' ', '红兵', ' ', '红兵'],
    [' ', '红炮', ' ', ' ', ' ', ' ', ' ', '红炮', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['红车', '红马', '红相', '红仕', '红帅', '红仕', '红相', '红马', '红车']
]

# 初始化变量
selected_piece = None
selected_pos = None
is_dragging = False
turn = '红'  # '红' 或 '黑'


# def draw_board():
#     screen.fill(WHITE)
#     # 画棋盘线
#     for i in range(10):
#         pygame.draw.line(screen, BLACK, (BOARD_OFFSET, BOARD_OFFSET + i * GRID_SIZE), (BOARD_OFFSET + 8 * GRID_SIZE, BOARD_OFFSET + i * GRID_SIZE), 2)
#     for j in range(9):
#         pygame.draw.line(screen, BLACK, (BOARD_OFFSET + j * GRID_SIZE, BOARD_OFFSET), (BOARD_OFFSET + j * GRID_SIZE, BOARD_OFFSET + 9 * GRID_SIZE), 2)
#     # 画九宫格斜线
#     pygame.draw.line(screen, BLACK, (BOARD_OFFSET + 3 * GRID_SIZE, BOARD_OFFSET), (BOARD_OFFSET + 5 * GRID_SIZE, BOARD_OFFSET + 2 * GRID_SIZE), 2)
#     pygame.draw.line(screen, BLACK, (BOARD_OFFSET + 5 * GRID_SIZE, BOARD_OFFSET), (BOARD_OFFSET + 3 * GRID_SIZE, BOARD_OFFSET + 2 * GRID_SIZE), 2)
#     pygame.draw.line(screen, BLACK, (BOARD_OFFSET + 3 * GRID_SIZE, BOARD_OFFSET + 7 * GRID_SIZE), (BOARD_OFFSET + 5 * GRID_SIZE, BOARD_OFFSET + 9 * GRID_SIZE), 2)
#     pygame.draw.line(screen, BLACK, (BOARD_OFFSET + 5 * GRID_SIZE, BOARD_OFFSET + 7 * GRID_SIZE), (BOARD_OFFSET + 3 * GRID_SIZE, BOARD_OFFSET + 9 * GRID_SIZE), 2)
#     # 画楚河汉界
#     font = pygame.font.SysFont('SimHei', 48)
#     text = font.render('楚河', True, BLACK)
#     screen.blit(text, (BOARD_OFFSET + 1.5 * GRID_SIZE, BOARD_OFFSET + 4 * GRID_SIZE))
#     text = font.render('汉界', True, BLACK)
#     screen.blit(text, (BOARD_OFFSET + 5.5 * GRID_SIZE, BOARD_OFFSET + 4 * GRID_SIZE))
#     # 画棋子
#     for y in range(10):
#         for x in range(9):
#             piece = board[y][x]
#             if piece != ' ':
#                 piece_image = images[piece]
#                 piece_rect = piece_image.get_rect(center=(BOARD_OFFSET + x * GRID_SIZE, BOARD_OFFSET + y * GRID_SIZE))
#                 screen.blit(piece_image, piece_rect.topleft)
#     # 画正在拖动的棋子
#     if is_dragging and selected_piece:
#         piece_image = images[selected_piece]
#         piece_rect = piece_image.get_rect(center=pygame.mouse.get_pos())
#         screen.blit(piece_image, piece_rect.topleft)

def draw_board():
    screen.fill(WHITE)
    # 画棋盘线
    for i in range(10):
        pygame.draw.line(screen, BLACK, (BOARD_OFFSET, BOARD_OFFSET + i * GRID_SIZE), (BOARD_OFFSET + 8 * GRID_SIZE, BOARD_OFFSET + i * GRID_SIZE), 2)
    for j in range(9):
        if j == 0 or j == 8:  # 边缘的纵向线
            pygame.draw.line(screen, BLACK, (BOARD_OFFSET + j * GRID_SIZE, BOARD_OFFSET), (BOARD_OFFSET + j * GRID_SIZE, BOARD_OFFSET + 9 * GRID_SIZE), 2)
        else:
            pygame.draw.line(screen, BLACK, (BOARD_OFFSET + j * GRID_SIZE, BOARD_OFFSET), (BOARD_OFFSET + j * GRID_SIZE, BOARD_OFFSET + 4 * GRID_SIZE), 2)
            pygame.draw.line(screen, BLACK, (BOARD_OFFSET + j * GRID_SIZE, BOARD_OFFSET + 5 * GRID_SIZE), (BOARD_OFFSET + j * GRID_SIZE, BOARD_OFFSET + 9 * GRID_SIZE), 2)
      
    # 画九宫格斜线
    pygame.draw.line(screen, BLACK, (BOARD_OFFSET + 3 * GRID_SIZE, BOARD_OFFSET), (BOARD_OFFSET + 5 * GRID_SIZE, BOARD_OFFSET + 2 * GRID_SIZE), 2)
    pygame.draw.line(screen, BLACK, (BOARD_OFFSET + 5 * GRID_SIZE, BOARD_OFFSET), (BOARD_OFFSET + 3 * GRID_SIZE, BOARD_OFFSET + 2 * GRID_SIZE), 2)
    pygame.draw.line(screen, BLACK, (BOARD_OFFSET + 3 * GRID_SIZE, BOARD_OFFSET + 7 * GRID_SIZE), (BOARD_OFFSET + 5 * GRID_SIZE, BOARD_OFFSET + 9 * GRID_SIZE), 2)
    pygame.draw.line(screen, BLACK, (BOARD_OFFSET + 5 * GRID_SIZE, BOARD_OFFSET + 7 * GRID_SIZE), (BOARD_OFFSET + 3 * GRID_SIZE, BOARD_OFFSET + 9 * GRID_SIZE), 2)
    # 画楚河汉界
    font = pygame.font.SysFont('SimHei', 48)
    text = font.render('楚河', True, BLACK)
    screen.blit(text, (BOARD_OFFSET + 1.5 * GRID_SIZE, BOARD_OFFSET + 4.5 * GRID_SIZE - 24))  # 调整位置使其在两线之间
    text = font.render('汉界', True, BLACK)
    screen.blit(text, (BOARD_OFFSET + 5.5 * GRID_SIZE, BOARD_OFFSET + 4.5 * GRID_SIZE - 24))  # 调整位置使其在两线之间
    # 画棋子
    for y in range(10):
        for x in range(9):
            piece = board[y][x]
            if piece != ' ':
                piece_image = images[piece]
                piece_rect = piece_image.get_rect(center=(BOARD_OFFSET + x * GRID_SIZE, BOARD_OFFSET + y * GRID_SIZE))
                screen.blit(piece_image, piece_rect.topleft)
    # 画正在拖动的棋子
    if is_dragging and selected_piece:
        piece_image = images[selected_piece]
        piece_rect = piece_image.get_rect(center=pygame.mouse.get_pos())
        screen.blit(piece_image, piece_rect.topleft)





def get_pos_from_mouse(pos):
    mouse_x, mouse_y = pos
    min_distance = float('inf')
    closest_pos = None

    for row in range(10):
        for col in range(9):
            center_x = BOARD_OFFSET + col * GRID_SIZE
            center_y = BOARD_OFFSET + row * GRID_SIZE
            distance = ((mouse_x - center_x) ** 2 + (mouse_y - center_y) ** 2) ** 0.5

            if distance < min_distance:
                min_distance = distance
                closest_pos = (row, col)
    
    logging.info(f"鼠标点击位置: {pos}, 转换后的最近棋盘坐标: {closest_pos}")
    return closest_pos



def is_first_move_soldier(start_pos):
    x, y = start_pos
    piece = board[x][y]
    if piece == '红兵':
        return x == 6
    elif piece == '黑卒':
        return x == 3
    return False

# def is_valid_move_soldier(start_pos, end_pos, board, is_first_move):
#     start_x, start_y = start_pos
#     end_x, end_y = end_pos

#     piece = board[start_x][start_y]
#     direction = 1 if piece == '红兵' else -1  # Assuming 红兵 moves down and 黑卒 moves up

#     # Standard move forward
#     if end_x == start_x + direction and end_y == start_y:
#         return True


#     # Capture move
#     if (not is_first_move) and end_x == start_x and abs(end_y - start_y) == 1:
#         return True

#     return False

def is_valid_move_soldier(start_pos, end_pos, board, is_first_move):
    start_x, start_y = start_pos
    end_x, end_y = end_pos

    piece = board[start_x][start_y]
    direction = -1 if piece == '红兵' else 1  # 红兵向下，黑卒向上

    # 普通前进
    if end_x == start_x + direction and end_y == start_y:
        return True

    # 过河后的左右移动
    if (direction == 1 and start_x >= 5) or (direction == -1 and start_x <= 4):
        if end_x == start_x and abs(end_y - start_y) == 1:
            return True
    print("兵移动失败")
    return False


def is_valid_move_cannon(start_pos, end_pos):
    start_x, start_y = start_pos
    end_x, end_y = end_pos

    # Ensure the move is within bounds
    if not (0 <= end_x < len(board) and 0 <= end_y < len(board[0])):
        return False

    # Check if the move is in the same row or the same column
    if start_x != end_x and start_y != end_y:
        return False
    
    # Check if there are pieces between the start and end positions
    pieces_between = 0
    if start_x == end_x:  # Moving horizontally
        for col in range(min(start_y, end_y) + 1, max(start_y, end_y)):
            if board[start_x][col] != ' ':
                pieces_between += 1
    else:  # Moving vertically
        for row in range(min(start_x, end_x) + 1, max(start_x, end_x)):
            if board[row][start_y] != ' ':
                pieces_between += 1

    # Moving without capturing
    if pieces_between == 0 and board[end_x][end_y] == ' ':
        return True

    # Capturing move
    if pieces_between == 1 and board[end_x][end_y] != ' ':
        return True

    return False

def is_valid_move_horse(start_pos, end_pos):
    start_x, start_y = start_pos
    end_x, end_y = end_pos

    dx = abs(start_x - end_x)
    dy = abs(start_y - end_y)
    if (dx == 2 and dy == 1) or (dx == 1 and dy == 2):
        if dx == 2:
            if board[(start_x + end_x) // 2][start_y] == ' ':
                return True
        elif dy == 2:
            if board[start_x][(start_y + end_y) // 2] == ' ':
                return True
    return False

def is_valid_move_general(start_pos, end_pos):
    start_x, start_y = start_pos
    end_x, end_y = end_pos

    # 将帅只能在九宫内移动
    if not (0 <= end_x < 3 or 7 <= end_x < 10):
        return False
    if not (3 <= end_y < 6):
        return False

    dx = abs(start_x - end_x)
    dy = abs(start_y - end_y)
    return (dx == 1 and dy == 0) or (dx == 0 and dy == 1)

def is_valid_move_guard(start_pos, end_pos):
    start_x, start_y = start_pos
    end_x, end_y = end_pos

    # 仕只能在九宫内移动，并且只能斜着走
    if not ((0 <= end_x < 3 or 7 <= end_x < 10) and 3 <= end_y < 6):
        return False

    dx = abs(start_x - end_x)
    dy = abs(start_y - end_y)
    return dx == 1 and dy == 1

def is_valid_move_elephant(start_pos, end_pos):
    start_x, start_y = start_pos
    end_x, end_y = end_pos

    # 相只能走田字格，并且不能过河
    if start_x < 5 and end_x >= 5:
        return False
    if start_x >= 5 and end_x < 5:
        return False

    dx = abs(start_x - end_x)
    dy = abs(start_y - end_y)
    if dx == 2 and dy == 2:
        # 确保田字中心没有棋子
        if board[(start_x + end_x) // 2][(start_y + end_y) // 2] == ' ':
            return True
    return False

def is_valid_move_chariot(start_pos, end_pos):
    start_x, start_y = start_pos
    end_x, end_y = end_pos

    # 检查移动是否在同一行或同一列
    if start_x != end_x and start_y != end_y:
        return False
    
    if start_x == end_x and start_y == end_y:
        return False

    # 检查移动路径上是否有其他棋子
    if start_x == end_x:  # 水平移动
        for col in range(min(start_y, end_y) + 1, max(start_y, end_y)):
            if board[start_x][col] != ' ':
                return False
    else:  # 垂直移动
        for row in range(min(start_x, end_x) + 1, max(start_x, end_x)):
            if board[row][start_y] != ' ':
                return False

    return True

def is_valid_move(start_pos, end_pos):
    start_piece = board[start_pos[0]][start_pos[1]]
    end_piece = board[end_pos[0]][end_pos[1]]

    if (turn == '红' and '红' not in start_piece) or (turn == '黑' and '黑' not in start_piece):
        return False

    if start_piece == '红帅' or start_piece == '黑将':
        return is_valid_move_general(start_pos, end_pos)
    elif start_piece == '红仕' or start_piece == '黑仕':
        return is_valid_move_guard(start_pos, end_pos)
    elif start_piece == '红相' or start_piece == '黑相':
        return is_valid_move_elephant(start_pos, end_pos)
    elif start_piece == '红马' or start_piece == '黑马':
        return is_valid_move_horse(start_pos, end_pos)
    elif start_piece == '红车' or start_piece == '黑车':
        return is_valid_move_chariot(start_pos, end_pos)
    elif start_piece == '红炮' or start_piece == '黑炮':
        return is_valid_move_cannon(start_pos, end_pos)
    elif start_piece == '红兵' or start_piece == '黑卒':
        is_first_move = is_first_move_soldier(start_pos)
        return is_valid_move_soldier(start_pos, end_pos, board, is_first_move)

    return False  # 默认不允许移动

def move_piece(selected_pos, board_pos, board):
    """
    移动棋子从选定位置到目标位置。

    :param selected_pos: 元组 (x, y) 表示棋子的起始位置。
    :param board_pos: 元组 (x, y) 表示棋子的目标位置。
    :param board: 代表棋盘的二维列表。
    :return: 更新后的棋盘。
    """
    start_x, start_y = selected_pos
    end_x, end_y = board_pos

    # 确保移动在边界内
    if not (0 <= start_x < len(board) and 0 <= start_y < len(board[0]) and 0 <= end_x < len(board) and 0 <= end_y < len(board[0])):
        print("移动超出边界。")
        return board

    # 获取选定位置的棋子
    piece = board[start_x][start_y]

    # 确保选定位置有棋子
    if piece == ' ':
        print("选定位置没有棋子。")
        return board

    # 将棋子移动到新位置
    board[end_x][end_y] = piece
    # 清空旧位置
    board[start_x][start_y] = ' '

    # 记录移动日志
    logging.info(f"移动棋子 {piece} 从 {selected_pos} 到 {board_pos}")

    return board

def switch_turn():
    global turn
    turn = '黑' if turn == '红' else '红'
    logging.info(f"{turn}方走棋")

def check_win():
    red_general = False
    black_general = False
    for row in board:
        for piece in row:
            if piece == '红帅':
                red_general = True
            elif piece == '黑将':
                black_general = True
    if not red_general:
        return '黑'
    if not black_general:
        return '红'
    return None

# # Main game loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             if event.button == 1:  # 左键按下
#                 pos = pygame.mouse.get_pos()
#                 board_pos = get_pos_from_mouse(pos)
#                 if board_pos:
#                     row, col = board_pos
#                     if board[row][col] != ' ':
#                         selected_piece = board[row][col]
#                         selected_pos = board_pos
#                         is_dragging = True
#                         logging.info(f"选中棋子 {selected_piece} 在位置 {selected_pos}")
#         elif event.type == pygame.MOUSEBUTTONUP:
#             if event.button == 1 and is_dragging:  # 左键松开
#                 pos = pygame.mouse.get_pos()
#                 board_pos = get_pos_from_mouse(pos)
#                 if board_pos and selected_piece:
#                     logging.info(f"试图将棋子 {selected_piece} 从 {selected_pos} 移动到 {board_pos}")
#                     if is_valid_move(selected_pos, board_pos):
#                         board = move_piece(selected_pos, board_pos, board)
#                         logging.info(f"放下棋子 {selected_piece} 在位置 {board_pos}")
#                         if check_win() is not None:
#                             print(f'{check_win()}方胜利!')
#                             running = False
#                         else:
#                             switch_turn()
#                 selected_piece = None
#                 selected_pos = None
#                 is_dragging = False
#         elif event.type == pygame.MOUSEMOTION:
#             if is_dragging:
#                 draw_board()
#                 piece_image = images[selected_piece]
#                 piece_rect = piece_image.get_rect(center=pygame.mouse.get_pos())
#                 screen.blit(piece_image, piece_rect.topleft)
#                 pygame.display.flip()

#     draw_board()
#     pygame.display.flip()

# pygame.quit()
# sys.exit()
 
 # Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键按下
                pos = pygame.mouse.get_pos()
                board_pos = get_pos_from_mouse(pos)
                if board_pos:
                    row, col = board_pos
                    if board[row][col] != ' ':
                        selected_piece = board[row][col]
                        selected_pos = board_pos
                        is_dragging = True
                        logging.info(f"选中棋子 {selected_piece} 在位置 {selected_pos}")
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and is_dragging:  # 左键松开
                pos = pygame.mouse.get_pos()
                board_pos = get_pos_from_mouse(pos)
                if board_pos and selected_piece:
                    logging.info(f"试图将棋子 {selected_piece} 从 {selected_pos} 移动到 {board_pos}")
                    if is_valid_move(selected_pos, board_pos):
                        board = move_piece(selected_pos, board_pos, board)
                        logging.info(f"放下棋子 {selected_piece} 在位置 {board_pos}")
                        if check_win() is not None:
                            print(f'{check_win()}方胜利!')
                            running = False
                        else:
                            switch_turn()
                selected_piece = None
                selected_pos = None
                is_dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if is_dragging:
                draw_board()
                piece_image = images[selected_piece]
                piece_rect = piece_image.get_rect(center=pygame.mouse.get_pos())
                screen.blit(piece_image, piece_rect.topleft)
                pygame.display.flip()

    draw_board()
    pygame.display.flip()

pygame.quit()
sys.exit()
