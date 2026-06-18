"""
AND-OR GRAPH SEARCH cho mô phỏng máy hút bụi.

Ý tưởng:
- OR node: robot đang ở một trạng thái, phải chọn 1 hành động.
- AND node: một hành động có thể sinh ra nhiều kết quả, kế hoạch phải xử lý được TẤT CẢ kết quả đó.

State dùng trong bài toán:
    state = (robot_pos, dirties)
    robot_pos = (c, r)
    dirties   = tuple các ô bẩn, ví dụ ((0, 1), (2, 2))

"""

FAILURE = "failure"


def and_or_graph_search(problem):
    """Trả về conditional plan hoặc FAILURE."""
    return or_search(problem.initial_state, problem, set())


def or_search(state, problem, path):
    """
    OR-SEARCH(state):
    Tại một trạng thái, robot chỉ cần chọn được 1 hành động tốt.
    """
    if problem.goal_test(state):
        return []

    if state in path:
        return FAILURE

    new_path = set(path)
    new_path.add(state)

    for action in problem.actions(state):
        result_states = problem.results(state, action)
        plan = and_search(result_states, problem, new_path)

        if plan != FAILURE:
            return [action, plan]

    return FAILURE


def and_search(states, problem, path):
    plans = {}

    for s in states:
        plan_s = or_search(s, problem, path)

        if plan_s == FAILURE:
            return FAILURE

        plans[s] = plan_s

    return plans



class ErraticVacuumProblem:
    def __init__(
        self,
        start_pos,
        dirties,
        cols,
        rows,
        nondeterministic_suck=True,
        slippery_move=True,
    ):
        self.initial_state = (tuple(start_pos), tuple(sorted(dirties)))
        self.cols = cols
        self.rows = rows
        self.nondeterministic_suck = nondeterministic_suck
        self.slippery_move = slippery_move
        
    # kiểm tra đã hết bụi chưa 
    def goal_test(self, state):
        _, dirties = state
        return len(dirties) == 0
    
    # kiểm tra có nằm trong biên không
    def in_bounds(self, pos):
        c, r = pos
        return 0 <= c < self.cols and 0 <= r < self.rows
    # thực hiện di chuyển
    def move(self, pos, action):
        c, r = pos

        if action == "Up":
            new_pos = (c, r - 1)
        elif action == "Down":
            new_pos = (c, r + 1)
        elif action == "Left":
            new_pos = (c - 1, r)
        elif action == "Right":
            new_pos = (c + 1, r)
        else:
            new_pos = pos

        if self.in_bounds(new_pos):
            return new_pos

        return pos

    def legal_moves(self, pos):
        moves = []
        for action in ["Up", "Down", "Left", "Right"]:
            new_pos = self.move(pos, action)
            if new_pos != pos:
                moves.append(action)
        return moves

    def manhattan(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def actions(self, state):
        pos, dirties = state

        if pos in dirties:
            return ["Suck"]

        moves = self.legal_moves(pos)

        if not dirties:
            return moves

        # Sắp xếp hướng đi theo khoảng cách tới ô bẩn gần nhất sau khi di chuyển.
        # Điều này không biến AND-OR thành thuật toán tối ưu, nhưng giúp mô phỏng hợp lý hơn.
        def move_score(action):
            new_pos = self.move(pos, action)
            nearest_dirty_distance = min(self.manhattan(new_pos, d) for d in dirties)
            fixed_order = {"Up": 0, "Left": 1, "Right": 2, "Down": 3}
            return nearest_dirty_distance, fixed_order[action]

        return sorted(moves, key=move_score)

    def results(self, state, action):
        """
        Trả về danh sách các trạng thái có thể xảy ra sau khi thực hiện action.
        """
        pos, dirties = state
        dirties = tuple(sorted(dirties))
        outcomes = []

        if action == "Suck":
            if pos not in dirties:
                outcomes.append((pos, dirties))
            else:
                # Kết quả chắc chắn: ô hiện tại sạch.
                cleaned_current = tuple(d for d in dirties if d != pos)
                outcomes.append((pos, cleaned_current))

                # Kết quả không chắc chắn có lợi: hút mạnh làm sạch thêm 1 ô bẩn kề bên.
                if self.nondeterministic_suck:
                    adjacent_dirties = []
                    for d in cleaned_current:
                        if self.manhattan(pos, d) == 1:
                            adjacent_dirties.append(d)

                    for extra_dirty in adjacent_dirties:
                        cleaned_extra = tuple(d for d in cleaned_current if d != extra_dirty)
                        outcomes.append((pos, cleaned_extra))

        else:
            intended_pos = self.move(pos, action)
            outcomes.append((intended_pos, dirties))

            # Tùy chọn: môi trường trượt khi di chuyển.
            # Lưu ý: nếu bật trượt quá mạnh, có thể không tồn tại kế hoạch chắc chắn 100%.
            if self.slippery_move:
                if action in ["Up", "Down"]:
                    slip_actions = ["Left", "Right"]
                else:
                    slip_actions = ["Up", "Down"]

                for slip_action in slip_actions:
                    slip_pos = self.move(pos, slip_action)
                    if slip_pos != pos:
                        outcomes.append((slip_pos, dirties))

        return self.unique_states(outcomes)

    def unique_states(self, states):
        """Xóa trạng thái trùng nhưng giữ nguyên thứ tự."""
        result = []
        seen = set()

        for pos, dirties in states:
            s = (tuple(pos), tuple(sorted(dirties)))
            if s not in seen:
                result.append(s)
                seen.add(s)

        return result

def choose_sample_state(branches):
    return next(iter(branches.keys()))


def extract_sample_path(state, plan):

    if plan == []:
        return [state[0]]

    if plan == FAILURE or not plan:
        return [state[0]]

    action, branches = plan

    if not branches:
        return [state[0]]

    next_state = choose_sample_state(branches)
    return [state[0]] + extract_sample_path(next_state, branches[next_state])


def extract_sample_actions(plan):
    """Lấy danh sách hành động mẫu: Suck, Up, Down, Left, Right."""
    actions = []

    while plan and plan != FAILURE:
        action, branches = plan
        actions.append(action)

        if not branches:
            break

        next_state = choose_sample_state(branches)
        plan = branches[next_state]

    return actions


def pretty_plan(plan, indent=0):

    space = "  " * indent

    if plan == []:
        return space + "GOAL"

    if plan == FAILURE:
        return space + "FAILURE"

    action, branches = plan
    lines = [space + f"Do: {action}"]

    for state, subplan in branches.items():
        pos, dirties = state
        lines.append(space + f"  If pos={pos}, dirties={list(dirties)}:")
        lines.append(pretty_plan(subplan, indent + 2))

    return "\n".join(lines)


def and_or_graph_search_generator(start_pos, dirties, cols, rows):
    
    problem = ErraticVacuumProblem(
        start_pos=start_pos,
        dirties=dirties,
        cols=cols,
        rows=rows,
        nondeterministic_suck=True,
        slippery_move=False,
    )

    def or_search_gen(state, problem, path):
        yield {
            "current": state[0],
            "frontier": [],
            "explored": {p[0] for p in path},
            "log": f"[OR] Xét vị trí {state[0]}, còn {len(state[1])} ô bẩn."
        }

        if problem.goal_test(state):
            yield {
                "current": state[0],
                "log": f"[OR] Đạt mục tiêu: sàn đã sạch tại {state[0]}."
            }
            return []

        if state in path:
            yield {
                "current": state[0],
                "log": f"[OR] Gặp vòng lặp tại {state[0]} với cùng tập rác -> bỏ nhánh."
            }
            return FAILURE

        new_path = set(path)
        new_path.add(state)

        for action in problem.actions(state):
            yield {
                "current": state[0],
                "log": f"[OR] Thử hành động {action} từ {state[0]}."
            }

            result_states = problem.results(state, action)
            plan = yield from and_search_gen(result_states, problem, new_path)

            if plan != FAILURE:
                yield {
                    "current": state[0],
                    "log": f"[OR] Chọn hành động {action} tại {state[0]}."
                }
                return [action, plan]

        yield {
            "current": state[0],
            "log": f"[OR] Không có hành động nào thành công tại {state[0]}."
        }
        return FAILURE

    def and_search_gen(states, problem, path):
        yield {
            "log": f"[AND] Hành động sinh ra {len(states)} kết quả. Cần giải được tất cả."
        }

        plans = {}

        for s in states:
            yield {
                "current": s[0],
                "log": f"[AND] Kiểm tra kết quả pos={s[0]}, còn {len(s[1])} ô bẩn."
            }

            plan_s = yield from or_search_gen(s, problem, path)

            if plan_s == FAILURE:
                yield {
                    "current": s[0],
                    "log": f"[AND] Có 1 kết quả thất bại tại {s[0]} -> hành động này không an toàn."
                }
                return FAILURE

            plans[s] = plan_s

        return plans

    yield {
        "current": start_pos,
        "frontier": [],
        "explored": set(),
        "log": "Bắt đầu AND-OR GRAPH SEARCH cho máy hút bụi."
    }

    final_plan = yield from or_search_gen(problem.initial_state, problem, set())

    if final_plan == FAILURE:
        yield {
            "done": True,
            "path": [],
            "actions": [],
            "plan": FAILURE,
            "log": "Không tìm thấy kế hoạch chắc chắn để làm sạch toàn bộ sàn."
        }
    else:
        sample_path = extract_sample_path(problem.initial_state, final_plan)
        sample_actions = extract_sample_actions(final_plan)

        yield {
            "done": True,
            "path": sample_path,
            "actions": sample_actions,
            "plan": final_plan,
            "log": f"Tìm thấy kế hoạch AND-OR. Đường mẫu có {len(sample_actions)} hành động."
        }
