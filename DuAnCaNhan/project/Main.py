# pyrefly: ignore [missing-import]
import csv
import os
import random
import time
import tracemalloc

# pyrefly: ignore [missing-import]
import pygame

import algorithm
from map_coloring_view import HCMMapRenderer
from ui import (
    BLACK,
    BLUE,
    BORDER,
    DARK_GRAY,
    GRAY,
    GREEN,
    MUTED,
    PANEL,
    RED,
    WHITE,
    YELLOW,
    ComboBox,
    InputBox,
    fit_text,
)


pygame.init()
WIDTH, HEIGHT = 1180, 760
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Visual")

font = pygame.font.SysFont("segoeui", 18)
small_font = pygame.font.SysFont("segoeui", 15)
log_font = pygame.font.SysFont("consolas", 15)
title_font = pygame.font.SysFont("segoeui", 28, bold=True)
section_font = pygame.font.SysFont("segoeui", 20, bold=True)
metric_font = pygame.font.SysFont("segoeui", 24, bold=True)

COLS, ROWS = 3, 3
CELL_SIZE = 50
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMPARISON_FILE = os.path.join(BASE_DIR, "comparison_results.csv")
CARO_SIZE = 3
CARO_WIN_LENGTH = 3
CARO_CELL_SIZE = 104

try:
    img_clean_floor = pygame.image.load(os.path.join(BASE_DIR, "assets", "clean_floor.png")).convert()
    img_clean_floor = pygame.transform.scale(img_clean_floor, (CELL_SIZE, CELL_SIZE))
    img_dirty_floor = pygame.image.load(os.path.join(BASE_DIR, "assets", "dirty_floor.png")).convert()
    img_dirty_floor = pygame.transform.scale(img_dirty_floor, (CELL_SIZE, CELL_SIZE))
    img_robot = pygame.image.load(os.path.join(BASE_DIR, "assets", "robot_vacuum.png")).convert()
    img_robot.set_colorkey((255, 255, 255))
    img_robot = pygame.transform.scale(img_robot, (CELL_SIZE - 10, CELL_SIZE - 10))
    USE_IMAGES = True
except Exception as exc:
    print(f"Không thể tải ảnh: {exc}")
    USE_IMAGES = False

try:
    HCM_MAP_RENDERER = HCMMapRenderer(os.path.join(BASE_DIR, "assets", "hcm_city_map.png"))
except Exception as exc:
    print(f"Không thể tải bản đồ TP.HCM: {exc}")
    HCM_MAP_RENDERER = None

try:
    img_x = pygame.image.load(os.path.join(BASE_DIR, "assets", "x.png")).convert_alpha()
    img_o = pygame.image.load(os.path.join(BASE_DIR, "assets", "o.png")).convert_alpha()
    img_x = pygame.transform.smoothscale(img_x, (CARO_CELL_SIZE - 18, CARO_CELL_SIZE - 18))
    img_o = pygame.transform.smoothscale(img_o, (CARO_CELL_SIZE - 18, CARO_CELL_SIZE - 18))
    USE_CARO_IMAGES = True
except Exception as exc:
    print(f"KhĂ´ng thá»ƒ táº£i áº£nh X/O: {exc}")
    USE_CARO_IMAGES = False


ALGORITHM_OPTIONS = [
    "BFS 1",
    "BFS 2 (Optimized)",
    "DFS 1",
    "DFS 2 (Optimized)",
    "IDS 1",
    "IDS 2 (Optimized)",
    "UCS",
    "Greedy Search",
    "A*",
    "IDA*",
    "Simple Hill Climbing",
    "Steepest-Ascent Hill Climbing",
    "Stochastic Hill Climbing",
    "Random-Restart Hill Climbing",
    "Simulated Annealing",
    "Local Beam Search",
    "Unobservable Search",
    "Partial-Observation Search",
    "AND-OR Graph Search",
    "Backtracking",
    "Forward Checking",
    "AC-3",
    "Min-Conflicts",
    "Minimax",
    "Alpha-Beta",
    "Expectimax",
    "So sánh thuật toán",
]

COMPARISON_MODE = "So sánh thuật toán"

COMPARISON_GROUPS = [
    ("Không thông tin", ["BFS 1", "BFS 2 (Optimized)", "DFS 1", "DFS 2 (Optimized)", "IDS 1", "IDS 2 (Optimized)", "UCS"]),
    ("Có thông tin", ["Greedy Search", "A*", "IDA*"]),
    ("Leo đồi", ["Simple Hill Climbing", "Steepest-Ascent Hill Climbing", "Stochastic Hill Climbing", "Random-Restart Hill Climbing", "Simulated Annealing", "Local Beam Search"]),
    ("Môi trường phức tạp", ["Unobservable Search", "Partial-Observation Search", "AND-OR Graph Search"]),
    ("CSP", ["Backtracking", "Forward Checking", "AC-3", "Min-Conflicts"]),
    ("Đối kháng", ["Minimax", "Alpha-Beta", "Expectimax"]),
]

COMPARISON_METRICS = [
    ("Thời gian chạy", "time_ms", "ms", BLUE),
    ("Bộ nhớ sử dụng", "memory_kb", "KB", YELLOW),
    ("Số node đã xét", "visited", "node", GREEN),
    ("Độ dài đường đi", "path_len", "bước", RED),
]

COMPARISON_HEADERS = [
    "group",
    "algorithm",
    "time_ms",
    "visited",
    "memory_kb",
    "path_len",
    "success",
    "state",
    "cols",
    "rows",
    "start",
    "dirties",
    "detail",
]

MAP_ALGORITHMS = {
    "Backtracking",
    "Forward Checking",
    "AC-3",
    "Min-Conflicts",
}

ADVERSARIAL_ALGORITHMS = {
    "Minimax",
    "Alpha-Beta",
    "Expectimax",
}


def is_csp_comparison_group(group_name):
    return group_name == "CSP"


def is_adversarial_comparison_group(group_name):
    return group_name == "Đối kháng"


def draw_text(surface, text, x, y, text_font, color=BLACK, max_width=None):
    label = fit_text(text_font, str(text), max_width) if max_width else str(text)
    surface.blit(text_font.render(label, True, color), (x, y))


def draw_centered_text(surface, text, center_x, y, text_font, color=BLACK, max_width=None):
    label = fit_text(text_font, str(text), max_width) if max_width else str(text)
    text_surface = text_font.render(label, True, color)
    surface.blit(text_surface, text_surface.get_rect(midtop=(center_x, y)))


def draw_card(surface, rect, title=None, subtitle=None):
    pygame.draw.rect(surface, PANEL, rect, border_radius=8)
    pygame.draw.rect(surface, BORDER, rect, 1, border_radius=8)
    if title:
        draw_text(surface, title, rect.x + 18, rect.y + 14, section_font, BLACK, rect.w - 36)
    if subtitle:
        draw_text(surface, subtitle, rect.x + 18, rect.y + 40, small_font, MUTED, rect.w - 36)


def draw_button(surface, rect, label, bg, fg=BLACK):
    pygame.draw.rect(surface, bg, rect, border_radius=8)
    pygame.draw.rect(surface, (148, 163, 184), rect, 1, border_radius=8)
    label_surf = font.render(label, True, fg)
    surface.blit(label_surf, label_surf.get_rect(center=rect.center))


def draw_metric(surface, x, y, label, value, color):
    pygame.draw.rect(surface, (248, 250, 252), (x, y, 128, 70), border_radius=8)
    draw_text(surface, label, x + 12, y + 10, small_font, MUTED, 104)
    draw_text(surface, value, x + 12, y + 32, metric_font, color, 104)


def draw_progress(surface, x, y, w, h, value, total):
    pygame.draw.rect(surface, GRAY, (x, y, w, h), border_radius=h // 2)
    if total:
        fill_w = int(w * min(1, value / total))
        pygame.draw.rect(surface, BLUE, (x, y, fill_w, h), border_radius=h // 2)


def get_random_states(cols, rows):
    all_positions = [(c, r) for c in range(cols) for r in range(rows)]
    start = random.choice(all_positions)
    all_positions.remove(start)
    num_dirties = random.randint(1, min(6, len(all_positions)))
    dirties = tuple(random.sample(all_positions, num_dirties))
    return start, dirties


def is_map_coloring_mode(selection):
    return selection in MAP_ALGORITHMS


def is_adversarial_mode(selection):
    return selection in ADVERSARIAL_ALGORITHMS


def is_comparison_mode(selection):
    return selection == COMPARISON_MODE


def create_caro_board():
    return algorithm.create_caro_board(CARO_SIZE)


def create_comparison_caro_board():
    board = create_caro_board()
    board[0][0] = "X"
    board[1][1] = "O"
    board[0][2] = "X"
    return board


def caro_winner(board):
    return algorithm.caro_winner(board, CARO_WIN_LENGTH)


def search_caro_move(board, algorithm_name, ai_mark):
    if algorithm_name == "Alpha-Beta":
        return algorithm.alpha_beta_decision(board, ai_mark, "X", CARO_WIN_LENGTH)
    if algorithm_name == "Expectimax":
        return algorithm.expectimax_decision(board, ai_mark, "X", CARO_WIN_LENGTH)
    return algorithm.minimax_decision(board, ai_mark, "X", CARO_WIN_LENGTH)


def describe_known_observations(known_positions, dirties):
    dirties = set(dirties)
    return ", ".join(f"{pos}: {'có rác' if pos in dirties else 'không rác'}" for pos in known_positions)


def benchmark_algorithm(selection, start_state, dirties, cols, rows, max_steps=50000):
    if selection in MAP_ALGORITHMS:
        return benchmark_csp_algorithm(selection, max_steps)
    if selection in ADVERSARIAL_ALGORITHMS:
        return benchmark_adversarial_algorithm(selection)

    result = {
        "algorithm": selection,
        "time_ms": 0,
        "visited": 0,
        "memory_kb": 0,
        "path_len": 0,
        "success": False,
    }

    comparison_cases = build_comparison_cases(selection, start_state, dirties, cols, rows)
    generator = build_search_generator(selection, start_state, dirties, cols, rows, comparison_cases)
    max_visited = 0
    final_path = []
    success = False

    tracemalloc.start()
    start_time = time.perf_counter()
    try:
        step_count = 0
        for step in generator:
            step_count += 1
            if step_count > max_steps:
                result["error"] = "Vượt giới hạn bước đo"
                break
            explored = step.get("explored", set())
            frontier = step.get("frontier", [])
            current = step.get("current")
            visited_count = len(explored) + len(frontier)
            if current is not None:
                visited_count += 1
            if visited_count > max_visited:
                max_visited = visited_count

            if step.get("done"):
                final_path = step.get("path", [])
                success = len(final_path) > 0
                break
    except Exception as exc:
        result["error"] = str(exc)
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    end_time = time.perf_counter()
    result["time_ms"] = (end_time - start_time) * 1000
    result["visited"] = max_visited
    result["memory_kb"] = peak_mem / 1024
    result["path_len"] = max(0, len(final_path) - 1)
    result["success"] = success
    return result


def build_comparison_cases(selection, start_state, dirties, cols, rows):
    all_positions = [(c, r) for c in range(cols) for r in range(rows)]
    dirties = tuple(dirties)

    if "Unobservable Search" in selection:
        cases = []
        sample_starts = [start_state]
        for pos in all_positions:
            if pos != start_state and len(sample_starts) < 3:
                sample_starts.append(pos)
        for index, pos in enumerate(sample_starts):
            guessed = set(dirties)
            extra_candidates = [p for p in all_positions if p != pos and p not in guessed]
            if extra_candidates and index % 2 == 1:
                guessed.add(extra_candidates[0])
            cases.append({"start_state": pos, "initial_dirties": tuple(sorted(guessed)), "current_dirties": list(sorted(guessed)), "path": [], "path_index": 0, "done": False})
        return cases

    if "Partial-Observation Search" in selection:
        observed_positions = all_positions[:min(2, len(all_positions))]
        known_dirties = [pos for pos in observed_positions if pos in dirties]
        unknown_positions = [pos for pos in all_positions if pos not in observed_positions and pos != start_state]
        cases = []
        for index in range(2):
            guessed = set(known_dirties)
            for pos in unknown_positions[index::2]:
                if pos in dirties or len(guessed) < len(dirties):
                    guessed.add(pos)
            cases.append({
                "start_state": start_state,
                "initial_dirties": tuple(sorted(guessed)),
                "current_dirties": list(sorted(guessed)),
                "known_positions": tuple(observed_positions),
                "path": [],
                "path_index": 0,
                "done": False,
            })
        return cases

    return []


def benchmark_csp_algorithm(selection, max_steps=50000):
    result = {
        "algorithm": selection,
        "time_ms": 0,
        "visited": 0,
        "memory_kb": 0,
        "path_len": 0,
        "success": False,
    }
    order = list(algorithm.HCM_REGIONS)
    if selection == "Backtracking":
        generator = algorithm.backtracking_map_coloring(order)
    elif selection == "Forward Checking":
        generator = algorithm.forward_checking_map_coloring(order)
    elif selection == "AC-3":
        generator = algorithm.ac3_map_coloring(order)
    else:
        generator = algorithm.min_conflicts_map_coloring(order, seed=7)

    visited = 0
    final_assignments = {}
    tracemalloc.start()
    start_time = time.perf_counter()
    try:
        for step in generator:
            visited += 1
            if visited > max_steps:
                result["error"] = "Vượt giới hạn bước đo"
                break
            final_assignments = step.get("assignments", final_assignments)
            if step.get("done"):
                result["success"] = bool(step.get("success"))
                break
    except Exception as exc:
        result["error"] = str(exc)
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    result["time_ms"] = (time.perf_counter() - start_time) * 1000
    result["visited"] = visited
    result["memory_kb"] = peak_mem / 1024
    result["path_len"] = len(final_assignments)
    result["assignments"] = dict(final_assignments)
    result["state"] = "Bản đồ TP.HCM"
    return result


def benchmark_adversarial_algorithm(selection):
    result = {
        "algorithm": selection,
        "time_ms": 0,
        "visited": 0,
        "memory_kb": 0,
        "path_len": 0,
        "success": False,
    }
    board = create_comparison_caro_board()
    ai_mark = "O"
    result["state"] = "Cờ caro"
    result["board"] = [row[:] for row in board]

    tracemalloc.start()
    start_time = time.perf_counter()
    try:
        move, score, nodes = search_caro_move(board, selection, ai_mark)
        result["success"] = move is not None
        result["visited"] = nodes
        result["path_len"] = len([cell for row in board for cell in row if not cell])
        result["score"] = score
        result["move"] = move
        result["board"] = [row[:] for row in board]
        result["state"] = "Cờ caro"
    except Exception as exc:
        result["error"] = str(exc)
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    result["time_ms"] = (time.perf_counter() - start_time) * 1000
    result["memory_kb"] = peak_mem / 1024
    return result


def get_comparison_algorithms(group_name):
    for name, algorithm_names in COMPARISON_GROUPS:
        if name == group_name:
            return algorithm_names
    return COMPARISON_GROUPS[0][1]


def save_comparison_results(results, group_name, start_state, dirties, cols, rows):
    should_write_header = not os.path.exists(COMPARISON_FILE) or os.path.getsize(COMPARISON_FILE) == 0
    with open(COMPARISON_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if should_write_header:
            writer.writerow(COMPARISON_HEADERS)
        for item in results:
            state_name = item.get("state", "Máy hút bụi")
            detail = ""
            if is_csp_comparison_group(group_name):
                detail = f"{len(item.get('assignments', {}))}/{len(algorithm.HCM_REGIONS)} vùng đã tô"
            elif is_adversarial_comparison_group(group_name):
                detail = f"AI O chọn {item.get('move')} | điểm {item.get('score', '')}"
            else:
                detail = f"rác {tuple(dirties)}"
            writer.writerow([
                group_name,
                item.get("algorithm", ""),
                f"{item.get('time_ms', 0):.4f}",
                item.get("visited", 0),
                f"{item.get('memory_kb', 0):.4f}",
                item.get("path_len", 0),
                item.get("success", False),
                state_name,
                cols,
                rows,
                start_state,
                tuple(dirties),
                detail,
            ])


def benchmark_algorithm_groups(start_state, dirties, cols, rows, group_name=None):
    results = []
    if group_name is None:
        selected_groups = COMPARISON_GROUPS
    else:
        selected_groups = [(group_name, get_comparison_algorithms(group_name))]

    for selected_group_name, algorithm_names in selected_groups:
        for algorithm_name in algorithm_names:
            item = benchmark_algorithm(algorithm_name, start_state, dirties, cols, rows)
            item["group"] = selected_group_name
            results.append(item)
    return results


def build_search_generator(selection, start_state, initial_dirties, cols, rows, simulation_cases):
    if "BFS 1" in selection:
        return algorithm.bfs1(start_state, initial_dirties, cols, rows)
    if "BFS 2" in selection:
        return algorithm.bfs2(start_state, initial_dirties, cols, rows)
    if "DFS 1" in selection:
        return algorithm.dfs1(start_state, initial_dirties, cols, rows)
    if "DFS 2" in selection:
        return algorithm.dfs2(start_state, initial_dirties, cols, rows)
    if "IDS 1" in selection:
        return algorithm.ids_normal(start_state, initial_dirties, cols, rows)
    if "IDS 2" in selection:
        return algorithm.ids2_optimize(start_state, initial_dirties, cols, rows)
    if "UCS" in selection:
        return algorithm.ucs(start_state, initial_dirties, cols, rows)
    if "Greedy Search" in selection:
        return algorithm.Greedy_Search(start_state, initial_dirties, cols, rows)
    if "IDA*" in selection:
        return algorithm.IDA_start(start_state, initial_dirties, cols, rows)
    if "A*" in selection:
        return algorithm.A_star(start_state, initial_dirties, cols, rows)
    if "Simple Hill Climbing" in selection:
        return algorithm.Simple_Hill_Climbing(start_state, initial_dirties, cols, rows)
    if "Steepest-Ascent Hill Climbing" in selection:
        return algorithm.steepest_ascent_hill_climbing(start_state, initial_dirties, cols, rows)
    if "Stochastic Hill Climbing" in selection:
        return algorithm.stochastic_hill_climbing(start_state, initial_dirties, cols, rows)
    if "Random-Restart Hill Climbing" in selection:
        return algorithm.random_restart_hill_climbing(start_state, initial_dirties, cols, rows)
    if "Simulated Annealing" in selection:
        return algorithm.simulated_annealing(start_state, initial_dirties, cols, rows)
    if "Local Beam Search" in selection:
        return algorithm.local_beam_search(start_state, initial_dirties, cols, rows)
    if "Unobservable Search" in selection:
        return algorithm.unobservable_search(simulation_cases, cols, rows)
    if "Partial-Observation Search" in selection:
        return algorithm.partialobservation_search(simulation_cases, cols, rows)
    return algorithm.and_or_graph_search_generator(start_state, initial_dirties, cols, rows)


def draw_grid_case(surface, case, x, y, cols, rows, phase, title, initial_dirties, known_positions=None):
    grid_w = cols * CELL_SIZE
    grid_h = rows * CELL_SIZE
    card = pygame.Rect(x, y, grid_w + 28, grid_h + 58)
    draw_card(surface, card)
    draw_text(surface, title, card.x + 14, card.y + 12, font, BLACK, card.w - 28)

    vacuum_pos = case["start_state"] if phase == 0 else case["path"][case["path_index"]] if case["path"] else case["start_state"]
    origin_x = card.x + 14
    origin_y = card.y + 42
    known_positions = set(known_positions or [])

    for r in range(rows):
        for c in range(cols):
            rect = pygame.Rect(origin_x + c * CELL_SIZE, origin_y + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            cell_pos = (c, r)

            if USE_IMAGES:
                surface.blit(img_dirty_floor if cell_pos in case["current_dirties"] else img_clean_floor, rect)
            else:
                pygame.draw.rect(surface, RED if cell_pos in case["current_dirties"] else GREEN, rect)
            pygame.draw.rect(surface, (148, 163, 184), rect, 1)
            if cell_pos in known_positions:
                pygame.draw.rect(surface, BLUE, rect.inflate(-4, -4), 3, border_radius=4)

    if phase == 1 and case["path"]:
        walked_path = case["path"][: case["path_index"] + 1]
        path_points = [
            (origin_x + c * CELL_SIZE + CELL_SIZE // 2, origin_y + r * CELL_SIZE + CELL_SIZE // 2)
            for c, r in walked_path
        ]
        if len(path_points) > 1:
            pygame.draw.lines(surface, (15, 23, 42), False, path_points, 8)
            pygame.draw.lines(surface, YELLOW, False, path_points, 4)
        for point in path_points[:-1]:
            pygame.draw.circle(surface, WHITE, point, 5)
            pygame.draw.circle(surface, YELLOW, point, 4)
        pygame.draw.circle(surface, YELLOW, path_points[-1], 11)
        pygame.draw.circle(surface, (133, 77, 14), path_points[-1], 11, 2)

    robot_rect = pygame.Rect(
        origin_x + vacuum_pos[0] * CELL_SIZE,
        origin_y + vacuum_pos[1] * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE,
    )
    if USE_IMAGES:
        surface.blit(img_robot, (robot_rect.x + 5, robot_rect.y + 5))
    else:
        pygame.draw.circle(surface, BLUE, robot_rect.center, 16)


def draw_timeline(surface, rect, case, initial_dirties, phase):
    previous_clip = surface.get_clip()
    surface.set_clip(rect)
    draw_text(surface, "Bước di chuyển", rect.x, rect.y, section_font, BLACK, rect.w)
    pygame.draw.line(surface, BORDER, (rect.x, rect.y + 58), (rect.right, rect.y + 58), 1)

    p_idx = case["path_index"]
    max_visible_steps = max(1, (rect.h - 82) // 30)
    start_idx = max(0, p_idx - max_visible_steps + 1)
    display_steps = case["path"][start_idx : start_idx + max_visible_steps]

    for i, point in enumerate(display_steps):
        real_i = start_idx + i
        y = rect.y + 74 + i * 30
        is_current = real_i == p_idx
        pygame.draw.circle(surface, YELLOW if is_current else BLUE, (rect.x + 10, y + 12), 8)
        if i < len(display_steps) - 1:
            pygame.draw.line(surface, BORDER, (rect.x + 10, y + 21), (rect.x + 10, y + 31), 2)
        action = "Dọn rác" if point in initial_dirties and case["path"].index(point) == real_i else "Di chuyển"
        draw_text(surface, f"Bước {real_i}: {point} - {action}", rect.x + 28, y + 2, font, BLACK if is_current else MUTED, rect.w - 28)
    surface.set_clip(previous_clip)


def draw_case_statuses(surface, rect, cases):
    previous_clip = surface.get_clip()
    surface.set_clip(rect)
    draw_text(surface, "Trạng thái từng trường hợp", rect.x, rect.y, section_font, BLACK, rect.w)
    pygame.draw.line(surface, BORDER, (rect.x, rect.y + 38), (rect.right, rect.y + 38), 1)

    row_y = rect.y + 54
    for idx, case in enumerate(cases[:8]):
        total = len(case.get("initial_dirties", []))
        remaining = len(case.get("current_dirties", []))
        cleaned = total - remaining
        path = case.get("path", [])
        step = case.get("path_index", 0)
        if remaining == 0:
            status = "Đã sạch"
            color = GREEN
        elif path and step >= len(path) - 1:
            status = "Còn rác"
            color = RED
        else:
            status = "Đang chạy"
            color = BLUE
        draw_text(surface, f"TH {idx + 1}", rect.x, row_y, font, BLACK, 58)
        draw_text(surface, f"Bước {step}", rect.x + 64, row_y, small_font, MUTED, 70)
        draw_text(surface, f"Dọn {cleaned}/{total}", rect.x + 142, row_y, small_font, MUTED, 78)
        draw_text(surface, status, rect.x + 228, row_y, small_font, color, rect.w - 228)
        row_y += 32
        if row_y > rect.bottom - 24:
            break

    surface.set_clip(previous_clip)


def draw_comparison_table(surface, rect, results):
    draw_card(surface, rect, "So sánh nhóm thuật toán")
    draw_text(surface, "Chạy trên cùng trạng thái sàn hiện tại", rect.x + 18, rect.y + 42, small_font, MUTED, rect.w - 36)

    if not results:
        draw_text(surface, "Nhấn Tự động để bắt đầu đo thời gian, node đã thăm và bộ nhớ.", rect.x + 18, rect.y + 92, font, MUTED, rect.w - 36)
        return

    headers = ["Nhóm", "Thuật toán", "Thời gian", "Node", "Bộ nhớ", "Độ dài", "KQ"]
    widths = [132, 210, 100, 82, 92, 72, 70]
    x = rect.x + 18
    y = rect.y + 78

    col_x = x
    for index, header in enumerate(headers):
        draw_text(surface, header, col_x, y, small_font, MUTED, widths[index] - 8)
        col_x += widths[index]
    pygame.draw.line(surface, BORDER, (x, y + 26), (rect.right - 18, y + 26), 1)

    y += 38
    for item in results[:12]:
        col_x = x
        success_text = "OK" if item.get("success") else "Fail"
        values = [
            item.get("group", ""),
            item.get("algorithm", ""),
            f"{item.get('time_ms', 0):.2f} ms",
            str(item.get("visited", 0)),
            f"{item.get('memory_kb', 0):.1f} KB",
            str(item.get("path_len", 0)),
            success_text,
        ]
        for index, value in enumerate(values):
            color = GREEN if index == 6 and success_text == "OK" else RED if index == 6 else BLACK
            draw_text(surface, value, col_x, y, small_font, color, widths[index] - 8)
            col_x += widths[index]
        y += 28


def draw_vacuum_comparison_state(surface, rect, start_state, dirties, cols, rows):
    draw_text(surface, "Trạng thái so sánh", rect.x, rect.y, section_font, BLACK, rect.w)
    cell = min(42, (rect.w - 8) // cols, (rect.h - 46) // rows)
    grid_w = cols * cell
    grid_h = rows * cell
    origin_x = rect.x + (rect.w - grid_w) // 2
    origin_y = rect.y + 42
    dirties = set(dirties)

    for r in range(rows):
        for c in range(cols):
            cell_rect = pygame.Rect(origin_x + c * cell, origin_y + r * cell, cell, cell)
            if USE_IMAGES:
                tile = img_dirty_floor if (c, r) in dirties else img_clean_floor
                tile = pygame.transform.scale(tile, (cell, cell))
                surface.blit(tile, cell_rect)
            else:
                pygame.draw.rect(surface, RED if (c, r) in dirties else GREEN, cell_rect)
            pygame.draw.rect(surface, (148, 163, 184), cell_rect, 1)
            if (c, r) == start_state:
                if USE_IMAGES:
                    robot = pygame.transform.scale(img_robot, (cell - 8, cell - 8))
                    surface.blit(robot, (cell_rect.x + 4, cell_rect.y + 4))
                else:
                    pygame.draw.circle(surface, BLUE, cell_rect.center, max(8, cell // 3))


def draw_map_comparison_state(surface, rect, results):
    draw_text(surface, "Trạng thái so sánh", rect.x, rect.y, section_font, BLACK, rect.w)
    draw_text(surface, "CSP: tô màu bản đồ TP.HCM", rect.x, rect.y + 30, small_font, MUTED, rect.w)

    assignments = {}
    for item in results:
        candidate = item.get("assignments", {})
        if len(candidate) > len(assignments):
            assignments = candidate

    map_area = pygame.Rect(rect.x, rect.y + 58, rect.w, rect.h - 98)
    if HCM_MAP_RENDERER is None:
        draw_text(surface, "Không thể tải bản đồ TP.HCM", map_area.x, map_area.y + 24, font, RED, map_area.w)
    else:
        map_surface = HCM_MAP_RENDERER.render(assignments)
        source_w, source_h = map_surface.get_size()
        scale = min(map_area.w / source_w, map_area.h / source_h)
        display_size = (max(1, int(source_w * scale)), max(1, int(source_h * scale)))
        display_surface = pygame.transform.smoothscale(map_surface, display_size)
        surface.blit(display_surface, display_surface.get_rect(center=map_area.center))

    draw_text(surface, f"Vùng: {len(algorithm.HCM_REGIONS)}", rect.x, rect.bottom - 32, small_font, MUTED, 74)
    draw_text(surface, f"Đã tô: {len(assignments)}", rect.x + 82, rect.bottom - 32, small_font, GREEN if assignments else MUTED, 72)
    for index, (_, color_rgb) in enumerate(algorithm.MAP_COLORS):
        swatch_x = rect.right - 78 + index * 18
        pygame.draw.rect(surface, color_rgb, (swatch_x, rect.bottom - 34, 14, 14), border_radius=3)
        pygame.draw.rect(surface, BORDER, (swatch_x, rect.bottom - 34, 14, 14), 1, border_radius=3)


def draw_caro_comparison_state(surface, rect, results):
    draw_text(surface, "Trạng thái so sánh", rect.x, rect.y, section_font, BLACK, rect.w)
    draw_text(surface, "Đối kháng: cờ caro", rect.x, rect.y + 30, small_font, MUTED, rect.w)

    board = create_comparison_caro_board()
    move = None
    if results:
        board = [row[:] for row in results[0].get("board", board)]
        move = results[0].get("move")

    cell = min(56, (rect.w - 10) // CARO_SIZE, (rect.h - 88) // CARO_SIZE)
    board_px = cell * CARO_SIZE
    board_rect = pygame.Rect(rect.x + (rect.w - board_px) // 2, rect.y + 64, board_px, board_px)
    pygame.draw.rect(surface, (248, 250, 252), board_rect, border_radius=8)
    pygame.draw.rect(surface, BORDER, board_rect, 2, border_radius=8)

    for i in range(1, CARO_SIZE):
        x = board_rect.x + i * cell
        y = board_rect.y + i * cell
        pygame.draw.line(surface, (148, 163, 184), (x, board_rect.y), (x, board_rect.bottom), 2)
        pygame.draw.line(surface, (148, 163, 184), (board_rect.x, y), (board_rect.right, y), 2)

    if move:
        c, r = move
        highlight = pygame.Rect(board_rect.x + c * cell + 5, board_rect.y + r * cell + 5, cell - 10, cell - 10)
        pygame.draw.rect(surface, (219, 234, 254), highlight, border_radius=6)

    for r in range(CARO_SIZE):
        for c in range(CARO_SIZE):
            mark = board[r][c]
            if not mark:
                continue
            mark_rect = pygame.Rect(board_rect.x + c * cell + 7, board_rect.y + r * cell + 7, cell - 14, cell - 14)
            if USE_CARO_IMAGES:
                image = img_x if mark == "X" else img_o
                surface.blit(pygame.transform.smoothscale(image, mark_rect.size), mark_rect)
            else:
                draw_centered_text(surface, mark, mark_rect.centerx, mark_rect.y + 4, metric_font, BLUE if mark == "X" else RED, mark_rect.w)

    status = "Lượt AI: O"
    if results and move:
        status = f"Nước gợi ý: ({move[0] + 1}, {move[1] + 1})"
    draw_centered_text(surface, status, rect.centerx, rect.bottom - 28, small_font, MUTED, rect.w)


def draw_comparison_state(surface, rect, group_name, results, start_state, dirties, cols, rows):
    if is_csp_comparison_group(group_name):
        draw_map_comparison_state(surface, rect, results)
        return
    if is_adversarial_comparison_group(group_name):
        draw_caro_comparison_state(surface, rect, results)
        return
    draw_vacuum_comparison_state(surface, rect, start_state, dirties, cols, rows)


def draw_comparison_chart(surface, rect, results):
    draw_text(surface, "Biểu đồ minh họa", rect.x, rect.y, section_font, BLACK, rect.w)
    if not results:
        return

    max_time = max(item.get("time_ms", 0) for item in results) or 1
    max_node = max(item.get("visited", 0) for item in results) or 1
    max_mem = max(item.get("memory_kb", 0) for item in results) or 1
    row_y = rect.y + 38
    bar_w = max(40, rect.w - 150)

    for item in results[:6]:
        name = item.get("algorithm", "")
        draw_text(surface, name, rect.x, row_y, small_font, BLACK, 132)
        time_w = int(bar_w * item.get("time_ms", 0) / max_time)
        node_w = int(bar_w * item.get("visited", 0) / max_node)
        mem_w = int(bar_w * item.get("memory_kb", 0) / max_mem)
        pygame.draw.rect(surface, BLUE, (rect.x + 140, row_y, time_w, 5), border_radius=2)
        pygame.draw.rect(surface, GREEN, (rect.x + 140, row_y + 8, node_w, 5), border_radius=2)
        pygame.draw.rect(surface, YELLOW, (rect.x + 140, row_y + 16, mem_w, 5), border_radius=2)
        row_y += 30

    legend_y = rect.bottom - 20
    pygame.draw.rect(surface, BLUE, (rect.x, legend_y, 12, 8), border_radius=2)
    draw_text(surface, "Thời gian", rect.x + 18, legend_y - 4, small_font, MUTED, 78)
    pygame.draw.rect(surface, GREEN, (rect.x + 104, legend_y, 12, 8), border_radius=2)
    draw_text(surface, "Node", rect.x + 122, legend_y - 4, small_font, MUTED, 50)
    pygame.draw.rect(surface, YELLOW, (rect.x + 174, legend_y, 12, 8), border_radius=2)
    draw_text(surface, "Bộ nhớ", rect.x + 192, legend_y - 4, small_font, MUTED, 70)


def draw_single_bar_chart(surface, rect, results, title, key, unit, color):
    pygame.draw.rect(surface, (248, 250, 252), rect, border_radius=8)
    pygame.draw.rect(surface, BORDER, rect, 1, border_radius=8)
    draw_text(surface, title, rect.x + 14, rect.y + 10, small_font, BLACK, rect.w - 28)
    if not results:
        return

    values = [item.get(key, 0) for item in results]
    max_value = max(values) or 1
    chart_top = rect.y + 42
    chart_bottom = rect.bottom - 38
    chart_h = max(20, chart_bottom - chart_top)
    bar_count = len(results)
    gap = 16
    bar_w = max(24, min(64, (rect.w - gap * (bar_count + 1)) // bar_count))
    total_w = bar_count * bar_w + (bar_count - 1) * gap
    start_x = rect.x + (rect.w - total_w) // 2

    pygame.draw.line(surface, BORDER, (rect.x + 14, chart_bottom), (rect.right - 14, chart_bottom), 1)
    pygame.draw.line(surface, BORDER, (rect.x + 14, chart_top), (rect.right - 14, chart_top), 1)
    draw_text(surface, f"max {max_value:.1f}" if unit in ("ms", "KB") else f"max {int(max_value)}", rect.right - 112, rect.y + 10, small_font, MUTED, 96)

    for index, item in enumerate(results):
        value = item.get(key, 0)
        bar_h = max(4, int(chart_h * value / max_value))
        x = start_x + index * (bar_w + gap)
        y = chart_bottom - bar_h
        pygame.draw.rect(surface, (226, 232, 240), (x, chart_top, bar_w, chart_h), border_radius=4)
        pygame.draw.rect(surface, color, (x, y, bar_w, bar_h), border_radius=4)

        if unit == "ms":
            value_text = f"{value:.1f}"
        elif unit == "KB":
            value_text = f"{value:.0f}"
        else:
            value_text = str(int(value))
        label_y = max(chart_top + 3, y - 20)
        draw_text(surface, value_text, x - 6, label_y, small_font, BLACK, bar_w + 12)

        name = item.get("algorithm", "")
        short_name = name.replace(" (Optimized)", "")
        short_name = short_name.replace("Search", "")
        draw_text(surface, short_name, x - 12, chart_bottom + 8, small_font, MUTED, bar_w + 24)


def get_comparison_metric(metric_name):
    for metric in COMPARISON_METRICS:
        if metric[0] == metric_name:
            return metric
    return COMPARISON_METRICS[0]


def format_chart_value(value, unit):
    if unit == "ms":
        return f"{value:.2f}"
    if unit == "KB":
        return f"{value:.1f}"
    return str(int(value))


def shorten_algorithm_name(name):
    short_name = name.replace(" (Optimized)", "")
    short_name = short_name.replace("Simple ", "")
    short_name = short_name.replace("Steepest-Ascent ", "Steepest ")
    short_name = short_name.replace("Random-Restart ", "Restart ")
    short_name = short_name.replace("Stochastic ", "Stoch. ")
    short_name = short_name.replace("Simulated Annealing", "Anneal")
    short_name = short_name.replace("Local Beam Search", "Beam")
    short_name = short_name.replace("Greedy Search", "Greedy")
    short_name = short_name.replace("Unobservable Search", "Unobservable")
    short_name = short_name.replace("Partial-Observation Search", "Partial")
    short_name = short_name.replace("AND-OR Graph Search", "AND-OR")
    short_name = short_name.replace("Forward Checking", "Forward")
    short_name = short_name.replace("Min-Conflicts", "MinConf")
    short_name = short_name.replace("Alpha-Beta", "AlphaBeta")
    return short_name


def draw_main_comparison_chart(surface, rect, results, metric_name):
    metric_label, key, unit, color = get_comparison_metric(metric_name)
    pygame.draw.rect(surface, (248, 250, 252), rect, border_radius=8)
    pygame.draw.rect(surface, BORDER, rect, 1, border_radius=8)
    draw_text(surface, f"{metric_label} ({unit})", rect.x + 18, rect.y + 14, section_font, BLACK, rect.w - 36)

    if not results:
        draw_text(surface, "Nhấn So sánh để đo dữ liệu rồi vẽ biểu đồ.", rect.x + 18, rect.y + 72, font, MUTED, rect.w - 36)
        return

    values = [float(item.get(key, 0) or 0) for item in results]
    max_value = max(values) or 1
    axis_max = max_value * 1.15 if max_value > 0 else 1

    chart_left = rect.x + 78
    chart_right = rect.right - 34
    chart_top = rect.y + 72
    chart_bottom = rect.bottom - 76
    chart_w = max(100, chart_right - chart_left)
    chart_h = max(100, chart_bottom - chart_top)

    pygame.draw.line(surface, (148, 163, 184), (chart_left, chart_top), (chart_left, chart_bottom), 2)
    pygame.draw.line(surface, (148, 163, 184), (chart_left, chart_bottom), (chart_right, chart_bottom), 2)

    for tick in range(5):
        ratio = tick / 4
        y = chart_bottom - int(chart_h * ratio)
        value = axis_max * ratio
        pygame.draw.line(surface, (226, 232, 240), (chart_left, y), (chart_right, y), 1)
        draw_text(surface, format_chart_value(value, unit), rect.x + 16, y - 9, small_font, MUTED, chart_left - rect.x - 24)

    bar_count = len(results)
    slot_w = chart_w / max(1, bar_count)
    bar_w = max(26, min(72, int(slot_w * 0.58)))

    for index, item in enumerate(results):
        value = float(item.get(key, 0) or 0)
        bar_h = int(chart_h * value / axis_max) if axis_max else 0
        bar_h = max(4 if value > 0 else 0, bar_h)
        center_x = chart_left + int(slot_w * index + slot_w / 2)
        x = center_x - bar_w // 2
        y = chart_bottom - bar_h

        pygame.draw.rect(surface, (241, 245, 249), (x, chart_top, bar_w, chart_h), border_radius=6)
        if bar_h:
            pygame.draw.rect(surface, color, (x, y, bar_w, bar_h), border_radius=6)

        value_text = f"{format_chart_value(value, unit)} {unit}"
        draw_centered_text(surface, value_text, center_x, max(chart_top + 4, y - 24), small_font, BLACK, max(72, int(slot_w) - 8))

        name = shorten_algorithm_name(item.get("algorithm", ""))
        label_w = max(54, int(slot_w) - 6)
        draw_centered_text(surface, name, center_x, chart_bottom + 14, small_font, MUTED, label_w)

    draw_centered_text(surface, "Thuật toán", chart_left + chart_w // 2, rect.bottom - 34, small_font, MUTED, 120)
    draw_text(surface, f"Trục Y: {metric_label}", chart_left, rect.y + 44, small_font, MUTED, chart_w)
    draw_text(surface, f"max dữ liệu {format_chart_value(max_value, unit)} {unit}", rect.right - 190, rect.y + 44, small_font, MUTED, 172)


def draw_comparison_screen(surface, rect, results, group_name, metric_name, start_state, dirties, cols, rows):
    draw_card(surface, rect, "So sánh nhóm thuật toán")
    draw_text(surface, f"Nhóm: {group_name} | Dữ liệu lưu tại comparison_results.csv", rect.x + 18, rect.y + 42, small_font, MUTED, rect.w - 36)

    state_rect = pygame.Rect(rect.x + 24, rect.y + 86, 230, 250)
    chart_rect = pygame.Rect(rect.x + 286, rect.y + 86, rect.w - 322, rect.h - 128)
    draw_comparison_state(surface, state_rect, group_name, results, start_state, dirties, cols, rows)
    draw_text(surface, "Tiêu chí biểu đồ", rect.x + 24, rect.y + 374, small_font, MUTED, 230)
    draw_main_comparison_chart(surface, chart_rect, results, metric_name)


def draw_caro_board(surface, rect, board, last_move=None):
    draw_card(surface, rect, "Mô phỏng cờ caro")
    board_px = CARO_SIZE * CARO_CELL_SIZE
    board_rect = pygame.Rect(0, 0, board_px, board_px)
    board_rect.center = (rect.centerx, rect.y + 246)

    pygame.draw.rect(surface, (248, 250, 252), board_rect, border_radius=8)
    pygame.draw.rect(surface, BORDER, board_rect, 2, border_radius=8)
    for i in range(1, CARO_SIZE):
        x = board_rect.x + i * CARO_CELL_SIZE
        y = board_rect.y + i * CARO_CELL_SIZE
        pygame.draw.line(surface, (148, 163, 184), (x, board_rect.y), (x, board_rect.bottom), 2)
        pygame.draw.line(surface, (148, 163, 184), (board_rect.x, y), (board_rect.right, y), 2)

    if last_move:
        c, r = last_move
        highlight = pygame.Rect(board_rect.x + c * CARO_CELL_SIZE + 6, board_rect.y + r * CARO_CELL_SIZE + 6, CARO_CELL_SIZE - 12, CARO_CELL_SIZE - 12)
        pygame.draw.rect(surface, (219, 234, 254), highlight, border_radius=8)

    for r in range(CARO_SIZE):
        for c in range(CARO_SIZE):
            mark = board[r][c]
            if not mark:
                continue
            cell = pygame.Rect(board_rect.x + c * CARO_CELL_SIZE, board_rect.y + r * CARO_CELL_SIZE, CARO_CELL_SIZE, CARO_CELL_SIZE)
            if USE_CARO_IMAGES:
                image = img_x if mark == "X" else img_o
                surface.blit(image, image.get_rect(center=cell.center))
            else:
                color = BLUE if mark == "X" else RED
                draw_text(surface, mark, cell.x + 22, cell.y + 12, title_font, color)

    return board_rect


def draw_caro_side_panel(surface, rect, selection, user_mark, ai_mark, current_turn, winner, ai_score, ai_nodes):
    draw_card(surface, rect, "Trạng thái caro")
    draw_metric(surface, rect.x + 18, rect.y + 76, "Người", user_mark, BLUE if user_mark == "X" else RED)
    draw_metric(surface, rect.x + 160, rect.y + 76, "AI", ai_mark, BLUE if ai_mark == "X" else RED)
    draw_text(surface, "Thuật toán", rect.x + 18, rect.y + 172, small_font, MUTED)
    draw_text(surface, selection, rect.x + 18, rect.y + 194, section_font, BLACK, rect.w - 36)
    draw_text(surface, "Lượt hiện tại", rect.x + 18, rect.y + 244, small_font, MUTED)
    status = f"{current_turn} đang đánh"
    if winner == "draw":
        status = "Hòa cờ"
    elif winner:
        status = f"{winner} chiến thắng"
    draw_text(surface, status, rect.x + 18, rect.y + 266, section_font, GREEN if winner else BLACK, rect.w - 36)
    draw_text(surface, "Đánh giá AI", rect.x + 18, rect.y + 318, small_font, MUTED)
    draw_text(surface, f"Điểm: {ai_score} | Nút duyệt: {ai_nodes}", rect.x + 18, rect.y + 340, font, BLACK, rect.w - 36)
    draw_text(surface, "Chọn X/O bằng 2 nút trên, bấm vào ô trống để đi.", rect.x + 18, rect.y + 386, small_font, MUTED, rect.w - 36)


def draw_logs(surface, rect, logs, log_offset):
    pygame.draw.rect(surface, DARK_GRAY, rect, border_radius=8)
    pygame.draw.rect(surface, (51, 65, 85), rect, 1, border_radius=8)
    previous_clip = surface.get_clip()
    surface.set_clip(rect)
    draw_text(surface, "Nhật ký hoạt động", rect.x + 18, rect.y + 14, section_font, WHITE)

    max_visible_logs = max(1, (rect.h - 56 - log_font.get_height()) // 19 + 1)
    start_idx = max(0, len(logs) - max_visible_logs - log_offset)
    for i, message in enumerate(logs[start_idx : start_idx + max_visible_logs]):
        lower = str(message).lower()
        color = (134, 239, 172)
        if "không" in lower or "từ chối" in lower:
            color = (252, 165, 165)
        elif "quay" in lower:
            color = (251, 191, 36)
        draw_text(surface, f"> {message}", rect.x + 18, rect.y + 48 + i * 19, log_font, color, rect.w - 36)
    surface.set_clip(previous_clip)


def main():
    clock = pygame.time.Clock()
    current_cols = COLS
    current_rows = ROWS
    start_state, initial_dirties = get_random_states(current_cols, current_rows)

    combo_box = ComboBox(24, 54, 330, 36, ALGORITHM_OPTIONS, font)
    comparison_group_box = ComboBox(504, 54, 250, 36, [group[0] for group in COMPARISON_GROUPS], font)
    comparison_metric_box = ComboBox(48, 530, 230, 36, [metric[0] for metric in COMPARISON_METRICS], font)
    btn_run = pygame.Rect(374, 54, 118, 36)
    btn_next = pygame.Rect(504, 54, 118, 36)
    btn_random = pygame.Rect(634, 54, 150, 36)
    btn_compare_random = pygame.Rect(774, 54, 150, 36)
    btn_caro_x = pygame.Rect(504, 54, 58, 36)
    btn_caro_o = pygame.Rect(574, 54, 58, 36)
    input_cols = InputBox(828, 54, 58, 36, str(current_cols), font, label="Cột")
    input_rows = InputBox(900, 54, 58, 36, str(current_rows), font, label="Hàng")

    is_running_auto = False
    PHASE_IDLE = 0
    PHASE_EXECUTE = 1
    phase = PHASE_IDLE
    simulation_cases = []
    partial_bs_positions = []
    final_path = []
    unobservable_paths = []
    comparison_results = []
    logs = [f"Sẵn sàng: bắt đầu {start_state}, số ô rác {len(initial_dirties)}"]
    log_offset = 0

    map_generator = None
    map_assignments = {}
    map_current_region = None
    map_current_color = None
    map_order = list(algorithm.HCM_REGIONS)
    map_done = False
    caro_board = create_caro_board()
    caro_user_mark = "X"
    caro_ai_mark = "O"
    caro_current_turn = "X"
    caro_winner_state = None
    caro_last_move = None
    caro_ai_score = 0
    caro_ai_nodes = 0
    caro_board_rect = pygame.Rect(0, 0, 0, 0)
    map_last_action = "Sẵn sàng"

    def reset_cases():
        simulation_cases.clear()
        partial_bs_positions.clear()
        selection = combo_box.get_selected()
        is_unobservable = "Unobservable Search" in selection
        is_partial = "Partial-Observation Search" in selection

        if is_unobservable:
            all_positions = [(c, r) for c in range(current_cols) for r in range(current_rows)]
            for c in range(current_cols):
                for r in range(current_rows):
                    pos = (c, r)
                    possible_dirties = [p for p in all_positions if p != pos]
                    guess_dirties = list(random.sample(possible_dirties, random.randint(1, len(possible_dirties))))
                    simulation_cases.append({"start_state": pos, "initial_dirties": tuple(guess_dirties), "current_dirties": list(guess_dirties), "path": [], "path_index": 0, "done": False})
            return

        if is_partial:
            all_positions = [(c, r) for c in range(current_cols) for r in range(current_rows)]
            observed_positions = random.sample(all_positions, min(2, len(all_positions)))
            partial_bs_positions.extend(observed_positions)
            known_dirties = [pos for pos in observed_positions if pos in initial_dirties]
            unknown_positions = [pos for pos in all_positions if pos not in observed_positions and pos != start_state]
            for _ in range(2):
                max_guess = min(4, len(unknown_positions))
                guess_count = random.randint(0, max_guess) if max_guess else 0
                guessed_unknown_dirties = random.sample(unknown_positions, guess_count) if guess_count else []
                guess_dirties = sorted(set(known_dirties + guessed_unknown_dirties))
                simulation_cases.append({"start_state": start_state, "initial_dirties": tuple(guess_dirties), "current_dirties": list(guess_dirties), "known_positions": tuple(observed_positions), "path": [], "path_index": 0, "done": False})
            return

        simulation_cases.append({"start_state": start_state, "initial_dirties": tuple(initial_dirties), "current_dirties": list(initial_dirties), "path": [], "path_index": 0, "done": False})

    def prepare_cases_for_execution():
        for case in simulation_cases:
            case["current_dirties"] = list(case["initial_dirties"])
            case["path"] = []
            case["path_index"] = 0
            case["done"] = False

    def reset_map_coloring(shuffle_order=False, preserve_order=False):
        nonlocal map_generator, map_assignments, map_current_region, map_current_color, map_order, map_done, map_last_action
        if not preserve_order:
            map_order = list(algorithm.HCM_REGIONS)
        if shuffle_order:
            random.shuffle(map_order)
        selection = combo_box.get_selected()
        if selection == "Backtracking":
            map_generator = algorithm.backtracking_map_coloring(map_order)
        elif selection == "Forward Checking":
            map_generator = algorithm.forward_checking_map_coloring(map_order)
        elif selection == "AC-3":
            map_generator = algorithm.ac3_map_coloring(map_order)
        elif selection == "Min-Conflicts":
            map_generator = algorithm.min_conflicts_map_coloring(map_order)
        map_assignments = {}
        map_current_region = None
        map_current_color = None
        map_done = False
        map_last_action = "Sẵn sàng"

    def reset_caro(user_mark=None):
        nonlocal caro_board, caro_user_mark, caro_ai_mark, caro_current_turn, caro_winner_state
        nonlocal caro_last_move, caro_ai_score, caro_ai_nodes, logs, log_offset, is_running_auto, phase
        if user_mark:
            caro_user_mark = user_mark
        caro_ai_mark = "O" if caro_user_mark == "X" else "X"
        caro_board = create_caro_board()
        caro_current_turn = "X"
        caro_winner_state = None
        caro_last_move = None
        caro_ai_score = 0
        caro_ai_nodes = 0
        is_running_auto = False
        phase = PHASE_IDLE
        logs = [f"Nguoi choi danh {caro_user_mark}, AI danh {caro_ai_mark}."]
        log_offset = 0
        if caro_ai_mark == "X":
            make_caro_ai_move()

    def make_caro_ai_move():
        nonlocal caro_current_turn, caro_winner_state, caro_last_move, caro_ai_score, caro_ai_nodes, logs
        if caro_winner_state or caro_current_turn != caro_ai_mark:
            return
        is_opening_move = caro_ai_mark == "X" and all(not cell for row in caro_board for cell in row)
        if is_opening_move:
            move = (random.randrange(CARO_SIZE), random.randrange(CARO_SIZE))
            score = 0
            nodes = 0
        else:
            move, score, nodes = search_caro_move(caro_board, combo_box.get_selected(), caro_ai_mark)
        caro_ai_score = score
        caro_ai_nodes = nodes
        if move:
            c, r = move
            caro_board[r][c] = caro_ai_mark
            caro_last_move = move
            logs.append(f"AI ({caro_ai_mark}) danh o ({c + 1}, {r + 1}) | diem {score} | nut {nodes}")
        caro_winner_state = caro_winner(caro_board)
        if caro_winner_state:
            logs.append("Hoa co." if caro_winner_state == "draw" else f"{caro_winner_state} chien thang.")
            return
        caro_current_turn = caro_user_mark

    def handle_caro_click(pos):
        nonlocal caro_current_turn, caro_winner_state, caro_last_move, logs, log_offset
        if caro_winner_state or caro_current_turn != caro_user_mark or not caro_board_rect.collidepoint(pos):
            return
        c = (pos[0] - caro_board_rect.x) // CARO_CELL_SIZE
        r = (pos[1] - caro_board_rect.y) // CARO_CELL_SIZE
        if not (0 <= c < CARO_SIZE and 0 <= r < CARO_SIZE) or caro_board[r][c]:
            return
        caro_board[r][c] = caro_user_mark
        caro_last_move = (c, r)
        logs.append(f"Nguoi choi ({caro_user_mark}) danh o ({c + 1}, {r + 1}).")
        caro_winner_state = caro_winner(caro_board)
        if caro_winner_state:
            logs.append("Hoa co." if caro_winner_state == "draw" else f"{caro_winner_state} chien thang.")
        else:
            caro_current_turn = caro_ai_mark
            make_caro_ai_move()
        log_offset = 0

    def advance_map_coloring():
        nonlocal map_assignments, map_current_region, map_current_color, map_done, is_running_auto, map_last_action
        if map_generator is None or map_done:
            return
        try:
            step = next(map_generator)
        except StopIteration:
            map_done = True
            is_running_auto = False
            return
        map_assignments = step["assignments"]
        map_current_region = step["region"]
        map_current_color = step["color"]
        map_done = step["done"]
        map_last_action = {"start": "Bắt đầu", "assign": "Gán màu", "reject": "Từ chối", "backtrack": "Quay lui", "done": "Hoàn tất"}.get(step.get("action"), "Bước")
        logs.append(step["log"])
        if map_done:
            is_running_auto = False

    def run_selected_algorithm():
        nonlocal phase, final_path, unobservable_paths, is_running_auto, log_offset
        prepare_cases_for_execution()
        generator = build_search_generator(combo_box.get_selected(), start_state, initial_dirties, current_cols, current_rows, simulation_cases)
        logs.clear()
        log_offset = 0
        final_path = []
        unobservable_paths = []
        for state_data in generator:
            if state_data.get("done"):
                final_path = state_data.get("path", [])
                unobservable_paths = state_data.get("all_paths", [])
                break

        if final_path or unobservable_paths:
            phase = PHASE_EXECUTE
            selection = combo_box.get_selected()
            if "Partial-Observation Search" in selection and unobservable_paths:
                for entry in unobservable_paths:
                    case_index = entry.get("case_index")
                    if case_index is not None and case_index < len(simulation_cases):
                        simulation_cases[case_index]["path"] = entry.get("path", [])
            elif "Unobservable Search" in selection and unobservable_paths:
                path_map = {st: p for st, p in unobservable_paths}
                for case in simulation_cases:
                    if case["start_state"] in path_map:
                        case["path"] = path_map[case["start_state"]]
            else:
                for case in simulation_cases:
                    case["path"] = final_path
            logs.append(f"Đã tìm thấy đường đi. Độ dài: {len(final_path) if final_path else 'nhiều trường hợp'}")
        else:
            is_running_auto = False
            logs.append("Không tìm thấy đường đi.")

    def step_simulation(auto=False):
        nonlocal is_running_auto, log_offset
        moved_cases = []
        for case in simulation_cases:
            if case["path"] and case["path_index"] < len(case["path"]) - 1:
                case["path_index"] += 1
                pos = case["path"][case["path_index"]]
                moved_cases.append((case, pos))
                if pos in case["current_dirties"]:
                    case["current_dirties"].remove(pos)
                if case["path_index"] == len(case["path"]) - 1:
                    case["done"] = True
        if moved_cases:
            case0 = simulation_cases[0]
            pos = case0["path"][case0["path_index"]]
            mode = "Tự động" if auto else "Bước"
            if "Partial-Observation Search" in combo_box.get_selected():
                logs.append(f"{mode} {case0['path_index']}: cập nhật {len(moved_cases)} trạng thái trong BS.")
            else:
                logs.append(f"{mode} {case0['path_index']}: robot di chuyển đến {pos}")
        else:
            all_clean = all(not case["current_dirties"] for case in simulation_cases)
            if all_clean:
                logs.append("Hoàn tất: tất cả trạng thái trong BS đã sạch.")
            else:
                logs.append("Chưa hoàn tất: có trạng thái trong BS vẫn còn rác nhưng lộ trình đã kết thúc.")
            is_running_auto = False
        log_offset = 0

    reset_cases()
    running = True
    while running:
        screen.fill(WHITE)
        selection = combo_box.get_selected()
        map_mode = is_map_coloring_mode(selection)
        adversarial_mode = is_adversarial_mode(selection)
        comparison_mode = is_comparison_mode(selection)
        uncertain_mode = "Unobservable Search" in selection or "Partial-Observation Search" in selection

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            previous_selection = combo_box.get_selected()
            combo_used = combo_box.handle_event(event)
            selection_changed = combo_box.get_selected() != previous_selection
            group_used = False
            previous_group = comparison_group_box.get_selected()
            if comparison_mode and not combo_used:
                group_used = comparison_group_box.handle_event(event)
                if comparison_group_box.get_selected() != previous_group:
                    comparison_results = []
                    logs = [f"Đã chọn nhóm so sánh: {comparison_group_box.get_selected()}"]
                    log_offset = 0
            metric_used = False
            previous_metric = comparison_metric_box.get_selected()
            if comparison_mode and not combo_used and not group_used:
                metric_used = comparison_metric_box.handle_event(event)
                if comparison_metric_box.get_selected() != previous_metric:
                    logs = [f"Đã chọn tiêu chí biểu đồ: {comparison_metric_box.get_selected()}"]
                    log_offset = 0
            if not combo_used and not group_used and not metric_used and not adversarial_mode and not comparison_mode:
                input_cols.handle_event(event)
                input_rows.handle_event(event)

            if selection_changed:
                is_running_auto = False
                phase = PHASE_IDLE
                final_path = []
                unobservable_paths = []
                comparison_results = []
                reset_cases()
                logs = [f"Đã chọn {combo_box.get_selected()}. Nhấn Tự động hoặc Bước tiếp."]
                if "Partial-Observation Search" in combo_box.get_selected() and partial_bs_positions:
                    logs.append(f"Agent biết trước: {describe_known_observations(partial_bs_positions, initial_dirties)}")
                if is_map_coloring_mode(combo_box.get_selected()):
                    reset_map_coloring()
                    logs = [f"Đã chọn {combo_box.get_selected()}. Theo dõi các vùng được tô màu từng bước."]
                if is_adversarial_mode(combo_box.get_selected()):
                    reset_caro()
                log_offset = 0

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not combo_box.active and not comparison_group_box.active and not comparison_metric_box.active:
                if adversarial_mode:
                    if btn_run.collidepoint(event.pos):
                        reset_caro()
                    elif btn_caro_x.collidepoint(event.pos):
                        reset_caro("X")
                    elif btn_caro_o.collidepoint(event.pos):
                        reset_caro("O")
                    else:
                        handle_caro_click(event.pos)
                    continue

                if btn_run.collidepoint(event.pos):
                    if comparison_mode:
                        selected_group = comparison_group_box.get_selected()
                        comparison_results = benchmark_algorithm_groups(start_state, initial_dirties, current_cols, current_rows, selected_group)
                        save_comparison_results(comparison_results, selected_group, start_state, initial_dirties, current_cols, current_rows)
                        logs = [f"Đã so sánh {len(comparison_results)} thuật toán nhóm {selected_group}.", f"Đã lưu thêm dữ liệu vào {COMPARISON_FILE}"]
                        log_offset = 0
                    else:
                        is_running_auto = not is_running_auto
                    if map_mode and is_running_auto and (phase == PHASE_IDLE or map_done):
                        reset_map_coloring(preserve_order=True)
                        phase = PHASE_EXECUTE
                        logs.clear()
                    elif (not comparison_mode) and is_running_auto and phase == PHASE_IDLE and initial_dirties:
                        run_selected_algorithm()

                if btn_next.collidepoint(event.pos) and not is_running_auto:
                    if map_mode:
                        if phase == PHASE_IDLE or map_done:
                            reset_map_coloring(preserve_order=True)
                            phase = PHASE_EXECUTE
                            logs.clear()
                        advance_map_coloring()
                    elif (not comparison_mode) and phase == PHASE_IDLE and initial_dirties:
                        run_selected_algorithm()
                    elif phase == PHASE_EXECUTE:
                        step_simulation(auto=False)

                random_clicked = btn_compare_random.collidepoint(event.pos) if comparison_mode else btn_random.collidepoint(event.pos)
                if random_clicked:
                    is_running_auto = False
                    phase = PHASE_IDLE
                    final_path = []
                    unobservable_paths = []
                    comparison_results = []
                    if comparison_mode and is_csp_comparison_group(comparison_group_box.get_selected()):
                        logs = ["Nhóm CSP dùng trạng thái so sánh cố định: bản đồ TP.HCM."]
                    elif comparison_mode and is_adversarial_comparison_group(comparison_group_box.get_selected()):
                        logs = ["Nhóm đối kháng dùng trạng thái so sánh cố định: bàn cờ caro."]
                    elif map_mode:
                        reset_map_coloring(shuffle_order=True)
                        logs = ["Đã đảo thứ tự tô màu các vùng."]
                    else:
                        if input_cols.text.isdigit():
                            current_cols = max(3, int(input_cols.text))
                        if input_rows.text.isdigit():
                            current_rows = max(3, int(input_rows.text))
                        start_state, initial_dirties = get_random_states(current_cols, current_rows)
                        reset_cases()
                        logs = [f"Đã tạo sàn {current_cols}x{current_rows}. Bắt đầu {start_state}, số ô rác {len(initial_dirties)}"]
                        if "Partial-Observation Search" in selection and partial_bs_positions:
                            logs.append(f"Agent biết trước: {describe_known_observations(partial_bs_positions, initial_dirties)}")
                    log_offset = 0

            if event.type == pygame.MOUSEWHEEL and not combo_box.active and not comparison_mode:
                mouse_pos = pygame.mouse.get_pos()
                if 24 <= mouse_pos[0] <= 1156 and 570 <= mouse_pos[1] <= 740:
                    log_offset += event.y
                    log_offset = max(0, min(log_offset, max(0, len(logs) - 7)))

        if is_running_auto:
            if map_mode and phase == PHASE_EXECUTE:
                pygame.time.delay(230)
                advance_map_coloring()
            elif phase == PHASE_EXECUTE:
                pygame.time.delay(260)
                step_simulation(auto=True)

        pygame.draw.rect(screen, (241, 245, 249), (0, 0, WIDTH, 108))
        pygame.draw.line(screen, BORDER, (0, 108), (WIDTH, 108), 1)
        draw_text(screen, "AI Visualizer", 24, 16, title_font, BLACK)
        if adversarial_mode:
            draw_button(screen, btn_run, "Reset", YELLOW, BLACK)
            draw_button(screen, btn_caro_x, "X", BLUE if caro_user_mark == "X" else GRAY, WHITE if caro_user_mark == "X" else BLACK)
            draw_button(screen, btn_caro_o, "O", RED if caro_user_mark == "O" else GRAY, WHITE if caro_user_mark == "O" else BLACK)
        elif comparison_mode:
            draw_button(screen, btn_run, "So sánh", GREEN, WHITE)
            comparison_group_box.draw(screen)
            compare_random_label = "Cố định" if (
                is_csp_comparison_group(comparison_group_box.get_selected())
                or is_adversarial_comparison_group(comparison_group_box.get_selected())
            ) else "Ngẫu nhiên"
            draw_button(screen, btn_compare_random, compare_random_label, YELLOW, BLACK)
        else:
            draw_button(screen, btn_run, "Dừng" if is_running_auto else "Tự động", RED if is_running_auto else GREEN, WHITE)
            draw_button(screen, btn_next, "Bước tiếp", BLUE, WHITE)
            draw_button(screen, btn_random, "Đảo thứ tự" if map_mode else "Ngẫu nhiên", YELLOW, BLACK)
        if not map_mode and not adversarial_mode and not comparison_mode:
            input_cols.draw(screen)
            input_rows.draw(screen)

        if comparison_mode:
            table_rect = pygame.Rect(24, 124, 1132, 616)
            draw_comparison_screen(screen, table_rect, comparison_results, comparison_group_box.get_selected(), comparison_metric_box.get_selected(), start_state, initial_dirties, current_cols, current_rows)
        elif map_mode:
            map_rect = pygame.Rect(24, 124, 700, 424)
            side_rect = pygame.Rect(748, 124, 408, 424)
            draw_card(screen, map_rect, "Tô màu bản đồ TP.HCM", selection)
            if HCM_MAP_RENDERER is not None:
                map_surface = HCM_MAP_RENDERER.render(map_assignments)
                map_content_rect = pygame.Rect(map_rect.x + 18, map_rect.y + 76, map_rect.w - 36, map_rect.h - 94)
                screen.blit(map_surface, map_surface.get_rect(center=map_content_rect.center))
            else:
                draw_text(screen, "Không thể tải assets/hcm_city_map.png", map_rect.x + 18, map_rect.y + 72, font, RED)
            draw_metric(screen, side_rect.x + 18, side_rect.y + 76, "Đã tô", f"{len(map_assignments)}/{len(algorithm.HCM_REGIONS)}", BLUE)
            draw_metric(screen, side_rect.x + 160, side_rect.y + 76, "Hành động", map_last_action, GREEN if map_done else YELLOW)
            draw_progress(screen, side_rect.x + 18, side_rect.y + 166, side_rect.w - 36, 12, len(map_assignments), len(algorithm.HCM_REGIONS))
            draw_text(screen, "Vùng đang xét", side_rect.x + 18, side_rect.y + 198, small_font, MUTED)
            draw_text(screen, map_current_region or "Đang chờ", side_rect.x + 18, side_rect.y + 220, section_font, BLACK, side_rect.w - 36)
            draw_text(screen, "Bảng màu", side_rect.x + 18, side_rect.y + 318, section_font, BLACK)
            for color_index, (color_name, color_rgb) in enumerate(algorithm.MAP_COLORS):
                x = side_rect.x + 18 + color_index * 92
                y = side_rect.y + 356
                pygame.draw.rect(screen, color_rgb, (x, y, 32, 32), border_radius=6)
                pygame.draw.rect(screen, BORDER, (x, y, 32, 32), 1, border_radius=6)
                draw_text(screen, color_name, x, y + 38, small_font, MUTED, 82)
        elif adversarial_mode:
            caro_rect = pygame.Rect(24, 124, 700, 424)
            side_rect = pygame.Rect(748, 124, 408, 424)
            caro_board_rect = draw_caro_board(screen, caro_rect, caro_board, caro_last_move)
            draw_caro_side_panel(screen, side_rect, selection, caro_user_mark, caro_ai_mark, caro_current_turn, caro_winner_state, caro_ai_score, caro_ai_nodes)
        else:
            sim_rect = pygame.Rect(24, 124, 700, 424)
            side_rect = pygame.Rect(748, 124, 408, 424)
            draw_text(screen, "Mô phỏng máy hút bụi", sim_rect.x, sim_rect.y, section_font, BLACK)
            draw_text(screen, selection, sim_rect.x, sim_rect.y + 28, small_font, MUTED, sim_rect.w)

            visible_cases = []

            if uncertain_mode:
                grid_w = current_cols * CELL_SIZE + 28
                grid_h = current_rows * CELL_SIZE + 58
                x, y = sim_rect.x, sim_rect.y + 64
                for idx, case in enumerate(simulation_cases[:9]):
                    if x + grid_w > sim_rect.right - 10:
                        x = sim_rect.x
                        y += grid_h + 12
                    if y + grid_h <= sim_rect.bottom - 10:
                        known_positions = partial_bs_positions if "Partial-Observation Search" in selection else None
                        draw_grid_case(screen, case, x, y, current_cols, current_rows, phase, f"Trường hợp {idx + 1}", case["initial_dirties"], known_positions)
                        visible_cases.append(case)
                    x += grid_w + 12
            elif simulation_cases:
                draw_grid_case(screen, simulation_cases[0], sim_rect.x, sim_rect.y + 78, current_cols, current_rows, phase, "Máy hút bụi", initial_dirties)
                visible_cases.append(simulation_cases[0])

            case0 = simulation_cases[0] if simulation_cases else None
            case_initial_dirties = case0["initial_dirties"] if case0 else initial_dirties
            cleaned = len(case_initial_dirties) - len(case0["current_dirties"]) if case0 else 0
            draw_card(screen, side_rect, "Trạng thái chạy")
            draw_metric(screen, side_rect.x + 18, side_rect.y + 76, "Bước", str(case0["path_index"] if case0 else 0), BLUE)
            if uncertain_mode:
                visible_cases = visible_cases or simulation_cases[:1]
                clean_cases = sum(1 for case in visible_cases if not case.get("current_dirties"))
                draw_metric(screen, side_rect.x + 160, side_rect.y + 76, "Đã sạch", f"{clean_cases}/{len(visible_cases)}", GREEN)
            else:
                draw_metric(screen, side_rect.x + 160, side_rect.y + 76, "Đã dọn", f"{cleaned}/{len(case_initial_dirties)}", GREEN)
            if case0 and case0.get("path"):
                draw_progress(screen, side_rect.x + 18, side_rect.y + 166, side_rect.w - 36, 12, case0["path_index"] + 1, len(case0["path"]))
                draw_text(screen, f"Độ dài đường đi: {len(case0['path'])}", side_rect.x + 18, side_rect.y + 188, font, MUTED)
            if uncertain_mode:
                draw_case_statuses(screen, pygame.Rect(side_rect.x + 18, side_rect.y + 220, side_rect.w - 36, 204), visible_cases)
            else:
                draw_timeline(screen, pygame.Rect(side_rect.x + 18, side_rect.y + 220, side_rect.w - 36, 204), case0 or {}, initial_dirties, phase)

        if not comparison_mode:
            draw_logs(screen, pygame.Rect(24, 570, 1132, 170), logs, log_offset)
        combo_box.draw(screen)
        if comparison_mode:
            comparison_group_box.draw(screen)
            comparison_metric_box.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
