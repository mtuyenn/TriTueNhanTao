from .minimax import available_moves, terminal_score


def alpha_beta_value(board, current_mark, ai_mark, alpha, beta, max_mark="X", win_length=3, stats=None):
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
        for c, r in available_moves(board):
            board[r][c] = current_mark
            child_score = alpha_beta_value(board, next_mark, ai_mark, alpha, beta, max_mark, win_length, stats)
            board[r][c] = ""

            if child_score > best_score:
                best_score = child_score
            if best_score > alpha:
                alpha = best_score
            if alpha >= beta:
                break
        return best_score

    best_score = 100000
    for c, r in available_moves(board):
        board[r][c] = current_mark
        child_score = alpha_beta_value(board, next_mark, ai_mark, alpha, beta, max_mark, win_length, stats)
        board[r][c] = ""

        if child_score < best_score:
            best_score = child_score
        if best_score < beta:
            beta = best_score
        if alpha >= beta:
            break
    return best_score


def alpha_beta_decision(board, ai_mark, max_mark="X", win_length=3):
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
        score = alpha_beta_value(board, next_mark, ai_mark, -100000, 100000, max_mark, win_length, stats)
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
