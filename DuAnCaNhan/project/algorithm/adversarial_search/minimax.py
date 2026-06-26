def create_board(size=3):
    board = []
    for _ in range(size):
        row = []
        for _ in range(size):
            row.append("")
        board.append(row)
    return board


def available_moves(board):
    moves = []
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == "":
                moves.append((c, r))
    return moves


def winner(board, win_length=3):
    size = len(board)
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    for r in range(size):
        for c in range(size):
            mark = board[r][c]
            if mark == "":
                continue

            for dc, dr in directions:
                end_c = c + (win_length - 1) * dc
                end_r = r + (win_length - 1) * dr
                if end_c < 0 or end_c >= size or end_r < 0 or end_r >= size:
                    continue

                count = 0
                for i in range(win_length):
                    check_r = r + i * dr
                    check_c = c + i * dc
                    if board[check_r][check_c] == mark:
                        count += 1

                if count == win_length:
                    return mark

    if len(available_moves(board)) == 0:
        return "draw"
    return None


def terminal_score(board, max_mark="X", win_length=3):
    result = winner(board, win_length)
    if result == "draw":
        return 0
    if result == max_mark:
        return 100
    if result is not None:
        return -100
    return None


def minimax_value(board, current_mark, ai_mark, max_mark="X", win_length=3, stats=None):
    if stats is not None:
        stats["nodes"] += 1

    score = terminal_score(board, max_mark, win_length)
    if score is not None:
        return score

    if current_mark == "X":
        next_mark = "O"
    else:
        next_mark = "X"

    if current_mark == max_mark:
        best_score = -100000
    else:
        best_score = 100000

    moves = available_moves(board)
    for c, r in moves:
        board[r][c] = current_mark
        child_score = minimax_value(board, next_mark, ai_mark, max_mark, win_length, stats)
        board[r][c] = ""

        if current_mark == max_mark:
            if child_score > best_score:
                best_score = child_score
        else:
            if child_score < best_score:
                best_score = child_score

    return best_score


def minimax_decision(board, ai_mark, max_mark="X", win_length=3):
    stats = {"nodes": 0}

    if ai_mark == "X":
        next_mark = "O"
    else:
        next_mark = "X"

    ai_is_max = ai_mark == max_mark
    if ai_is_max:
        best_score = -100000
    else:
        best_score = 100000

    best_move = None
    moves = available_moves(board)
    for c, r in moves:
        board[r][c] = ai_mark
        score = minimax_value(board, next_mark, ai_mark, max_mark, win_length, stats)
        board[r][c] = ""

        if best_move is None:
            best_move = (c, r)
            best_score = score
        elif ai_is_max and score > best_score:
            best_move = (c, r)
            best_score = score
        elif (not ai_is_max) and score < best_score:
            best_move = (c, r)
            best_score = score

    return best_move, int(best_score), stats["nodes"]
