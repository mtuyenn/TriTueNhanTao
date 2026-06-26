from .minimax import available_moves, terminal_score


def expectimax_value(board, current_mark, ai_mark, max_mark="X", win_length=3, stats=None):
    if stats is not None:
        stats["nodes"] += 1

    score = terminal_score(board, max_mark, win_length)
    if score is not None:
        return score

    if current_mark == "X":
        next_mark = "O"
    else:
        next_mark = "X"

    values = []
    for c, r in available_moves(board):
        board[r][c] = current_mark
        child_score = expectimax_value(board, next_mark, ai_mark, max_mark, win_length, stats)
        board[r][c] = ""
        values.append(child_score)

    if current_mark == ai_mark:
        if ai_mark == max_mark:
            best_score = values[0]
            for value in values:
                if value > best_score:
                    best_score = value
            return best_score

        best_score = values[0]
        for value in values:
            if value < best_score:
                best_score = value
        return best_score

    total = 0
    for value in values:
        total += value
    return total / len(values)


def expectimax_decision(board, ai_mark, max_mark="X", win_length=3):
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
    for c, r in available_moves(board):
        board[r][c] = ai_mark
        score = expectimax_value(board, next_mark, ai_mark, max_mark, win_length, stats)
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

    return best_move, round(best_score, 2), stats["nodes"]
