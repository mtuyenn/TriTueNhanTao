import random

# 1 = có bụi
# 0 = sạch
room = [
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1]
]

rows = len(room)
cols = len(room[0])

# Model của agent
model = [[None for _ in range(cols)] for _ in range(rows)]

# Các ô đã đi qua
visited = set()

# Vị trí ban đầu
x = 0
y = 0


# In trạng thái phòng
def display_room():
    for row in room:
        print(row)
    print()


# Cập nhật model
def update_model(x, y):
    model[x][y] = room[x][y]
    visited.add((x, y))


# Kiểm tra ô hiện tại có bụi không
def is_dirty(x, y):
    return room[x][y] == 1


# Hút bụi
def suck(x, y):
    print(f"Action: SUCK at ({x}, {y})")
    room[x][y] = 0


# Các hướng có thể đi
def possible_moves(x, y):
    moves = []

    if x > 0:
        moves.append(("UP", x - 1, y))

    if x < rows - 1:
        moves.append(("DOWN", x + 1, y))

    if y > 0:
        moves.append(("LEFT", x, y - 1))

    if y < cols - 1:
        moves.append(("RIGHT", x, y + 1))
    
    actions = []

    for action, nx, ny in moves:
        if (nx, ny) not in visited:
            actions.append((action, nx, ny))

    return actions if actions else None
        


# Chọn hành động
def choose_action(x, y):
    actions = possible_moves(x, y)
    if actions == None:
        return None

    return random.choice(actions)

# Chương trình chính
print("Phòng Ban Đầu:")
display_room()

for step in range(20):

    print(f"Step {step + 1}")

    update_model(x, y)

    # Nếu có bụi thì hút
    if is_dirty(x, y):
        suck(x, y)

    else:
        move = choose_action(x, y)

        if move is None:
            print("Không còn hành động nào khả thi!")
            break

        action, nx, ny = move

        print(f"Action: {action}")

        x = nx
        y = ny

    display_room()

    # Kiểm tra phòng sạch hoàn toàn
    clean = True

    for row in room:
        for cell in row:
            if cell == 1:
                clean = False

    if clean:
        print("Phòng đã được dọn sạch hoàn toàn!")
        break