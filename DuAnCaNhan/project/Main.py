# pyrefly: ignore [missing-import]
import os
import random

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
pygame.display.set_caption("Trực quan hóa thuật toán AI")

font = pygame.font.SysFont("segoeui", 18)
small_font = pygame.font.SysFont("segoeui", 15)
log_font = pygame.font.SysFont("consolas", 15)
title_font = pygame.font.SysFont("segoeui", 28, bold=True)
section_font = pygame.font.SysFont("segoeui", 20, bold=True)
metric_font = pygame.font.SysFont("segoeui", 24, bold=True)

COLS, ROWS = 3, 3
CELL_SIZE = 50
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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


ALGORITHM_OPTIONS = [
    "BFS 1",
    "BFS 2 (Tối ưu)",
    "DFS 1",
    "DFS 2 (Tối ưu)",
    "IDS 1",
    "IDS 2 (Tối ưu)",
    "UCS",
    "Tìm kiếm tham lam",
    "A*",
    "IDA*",
    "Leo đồi đơn giản",
    "Leo đồi dốc nhất",
    "Leo đồi ngẫu nhiên",
    "Leo đồi khởi động lại",
    "Tôi luyện mô phỏng",
    "Tìm kiếm chùm cục bộ",
    "Tìm kiếm không quan sát",
    "Tìm kiếm quan sát một phần",
    "Tìm kiếm đồ thị AND-OR",
    "Quay lui tô màu",
    "Kiểm tra tiến tô màu",
    "AC-3 tô màu",
    "Xung đột tối thiểu tô màu",
]

MAP_ALGORITHMS = {
    "Quay lui tô màu",
    "Kiểm tra tiến tô màu",
    "AC-3 tô màu",
    "Xung đột tối thiểu tô màu",
}


def draw_text(surface, text, x, y, text_font, color=BLACK, max_width=None):
    label = fit_text(text_font, str(text), max_width) if max_width else str(text)
    surface.blit(text_font.render(label, True, color), (x, y))


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
    if "tham lam" in selection:
        return algorithm.Greedy_Search(start_state, initial_dirties, cols, rows)
    if "IDA*" in selection:
        return algorithm.IDA_start(start_state, initial_dirties, cols, rows)
    if "A*" in selection:
        return algorithm.A_star(start_state, initial_dirties, cols, rows)
    if "đơn giản" in selection:
        return algorithm.Simple_Hill_Climbing(start_state, initial_dirties, cols, rows)
    if "dốc nhất" in selection:
        return algorithm.steepest_ascent_hill_climbing(start_state, initial_dirties, cols, rows)
    if "ngẫu nhiên" in selection and "khởi động" not in selection:
        return algorithm.stochastic_hill_climbing(start_state, initial_dirties, cols, rows)
    if "khởi động lại" in selection:
        return algorithm.random_restart_hill_climbing(start_state, initial_dirties, cols, rows)
    if "Tôi luyện" in selection:
        return algorithm.simulated_annealing(start_state, initial_dirties, cols, rows)
    if "chùm" in selection:
        return algorithm.local_beam_search(start_state, initial_dirties, cols, rows)
    if "không quan sát" in selection:
        return algorithm.unobservable_search(simulation_cases, cols, rows)
    if "quan sát một phần" in selection:
        return algorithm.partialobservation_search(simulation_cases, cols, rows)
    return algorithm.and_or_graph_search_generator(start_state, initial_dirties, cols, rows)


def draw_grid_case(surface, case, x, y, cols, rows, phase, title, initial_dirties):
    grid_w = cols * CELL_SIZE
    grid_h = rows * CELL_SIZE
    card = pygame.Rect(x, y, grid_w + 28, grid_h + 58)
    draw_card(surface, card)
    draw_text(surface, title, card.x + 14, card.y + 12, font, BLACK, card.w - 28)

    vacuum_pos = case["start_state"] if phase == 0 else case["path"][case["path_index"]] if case["path"] else case["start_state"]
    origin_x = card.x + 14
    origin_y = card.y + 42

    for r in range(rows):
        for c in range(cols):
            rect = pygame.Rect(origin_x + c * CELL_SIZE, origin_y + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            cell_pos = (c, r)

            if USE_IMAGES:
                surface.blit(img_dirty_floor if cell_pos in case["current_dirties"] else img_clean_floor, rect)
            else:
                pygame.draw.rect(surface, RED if cell_pos in case["current_dirties"] else GREEN, rect)
            pygame.draw.rect(surface, (148, 163, 184), rect, 1)

            if phase == 1 and case["path"] and cell_pos in case["path"][: case["path_index"] + 1]:
                pygame.draw.circle(surface, YELLOW, rect.center, 9)
                pygame.draw.circle(surface, (133, 77, 14), rect.center, 9, 1)

            if cell_pos in initial_dirties:
                pygame.draw.circle(surface, RED, (rect.right - 9, rect.y + 9), 5)

            if cell_pos == vacuum_pos:
                if USE_IMAGES:
                    surface.blit(img_robot, (rect.x + 5, rect.y + 5))
                else:
                    pygame.draw.circle(surface, BLUE, rect.center, 16)


def draw_timeline(surface, rect, case, initial_dirties, phase):
    draw_text(surface, "Bước di chuyển", rect.x, rect.y, section_font, BLACK, rect.w)
    pygame.draw.line(surface, BORDER, (rect.x, rect.y + 58), (rect.right, rect.y + 58), 1)

    p_idx = case["path_index"]
    start_idx = max(0, p_idx - 7)
    display_steps = case["path"][start_idx : start_idx + 11]

    for i, point in enumerate(display_steps):
        real_i = start_idx + i
        y = rect.y + 74 + i * 30
        is_current = real_i == p_idx
        pygame.draw.circle(surface, YELLOW if is_current else BLUE, (rect.x + 10, y + 12), 8)
        if i < len(display_steps) - 1:
            pygame.draw.line(surface, BORDER, (rect.x + 10, y + 21), (rect.x + 10, y + 31), 2)
        action = "Dọn rác" if point in initial_dirties and case["path"].index(point) == real_i else "Di chuyển"
        draw_text(surface, f"Bước {real_i}: {point} - {action}", rect.x + 28, y + 2, font, BLACK if is_current else MUTED, rect.w - 28)


def draw_logs(surface, rect, logs, log_offset):
    pygame.draw.rect(surface, DARK_GRAY, rect, border_radius=8)
    pygame.draw.rect(surface, (51, 65, 85), rect, 1, border_radius=8)
    draw_text(surface, "Nhật ký hoạt động", rect.x + 18, rect.y + 14, section_font, WHITE)

    max_visible_logs = 7
    start_idx = max(0, len(logs) - max_visible_logs - log_offset)
    for i, message in enumerate(logs[start_idx : start_idx + max_visible_logs]):
        lower = str(message).lower()
        color = (134, 239, 172)
        if "không" in lower or "từ chối" in lower:
            color = (252, 165, 165)
        elif "quay" in lower:
            color = (251, 191, 36)
        draw_text(surface, f"> {message}", rect.x + 18, rect.y + 48 + i * 19, log_font, color, rect.w - 36)


def main():
    clock = pygame.time.Clock()
    current_cols = COLS
    current_rows = ROWS
    start_state, initial_dirties = get_random_states(current_cols, current_rows)

    combo_box = ComboBox(24, 54, 330, 36, ALGORITHM_OPTIONS, font)
    btn_run = pygame.Rect(374, 54, 118, 36)
    btn_next = pygame.Rect(504, 54, 118, 36)
    btn_random = pygame.Rect(634, 54, 150, 36)
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
    logs = [f"Sẵn sàng: bắt đầu {start_state}, số ô rác {len(initial_dirties)}"]
    log_offset = 0

    map_generator = None
    map_assignments = {}
    map_current_region = None
    map_current_color = None
    map_order = list(algorithm.HCM_REGIONS)
    map_done = False
    map_last_action = "Sẵn sàng"

    def reset_cases():
        simulation_cases.clear()
        partial_bs_positions.clear()
        selection = combo_box.get_selected()
        is_unobservable = "không quan sát" in selection
        is_partial = "quan sát một phần" in selection

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
            clean_positions = [(c, r) for c in range(current_cols) for r in range(current_rows) if (c, r) not in initial_dirties]
            selected_positions = random.sample(clean_positions, min(2, len(clean_positions)))
            all_positions = [(c, r) for c in range(current_cols) for r in range(current_rows)]
            for pos in selected_positions:
                partial_bs_positions.append(pos)
                possible_dirties = [p for p in all_positions if p not in selected_positions]
                guess_dirties = list(random.sample(possible_dirties, random.randint(1, len(possible_dirties)))) if possible_dirties else []
                simulation_cases.append({"start_state": pos, "initial_dirties": tuple(guess_dirties), "current_dirties": list(guess_dirties), "path": [], "path_index": 0, "done": False})
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
        if selection == "Quay lui tô màu":
            map_generator = algorithm.backtracking_map_coloring(map_order)
        elif selection == "Kiểm tra tiến tô màu":
            map_generator = algorithm.forward_checking_map_coloring(map_order)
        elif selection == "AC-3 tô màu":
            map_generator = algorithm.ac3_map_coloring(map_order)
        elif selection == "Xung đột tối thiểu tô màu":
            map_generator = algorithm.min_conflicts_map_coloring(map_order)
        map_assignments = {}
        map_current_region = None
        map_current_color = None
        map_done = False
        map_last_action = "Sẵn sàng"

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
            if ("không quan sát" in selection or "quan sát một phần" in selection) and unobservable_paths:
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
        all_done = True
        for case in simulation_cases:
            if case["path"] and case["path_index"] < len(case["path"]) - 1:
                all_done = False
                case["path_index"] += 1
                pos = case["path"][case["path_index"]]
                if pos in case["current_dirties"]:
                    case["current_dirties"].remove(pos)
                if case["path_index"] == len(case["path"]) - 1:
                    case["done"] = True
        if not all_done:
            case0 = simulation_cases[0]
            pos = case0["path"][case0["path_index"]]
            mode = "Tự động" if auto else "Bước"
            logs.append(f"{mode} {case0['path_index']}: robot di chuyển đến {pos}")
        else:
            logs.append("Hoàn tất: sàn đã sạch hoặc lộ trình đã kết thúc.")
            is_running_auto = False
        log_offset = 0

    reset_cases()
    running = True
    while running:
        screen.fill(WHITE)
        selection = combo_box.get_selected()
        map_mode = is_map_coloring_mode(selection)
        uncertain_mode = "không quan sát" in selection or "quan sát một phần" in selection

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            previous_selection = combo_box.get_selected()
            combo_used = combo_box.handle_event(event)
            selection_changed = combo_box.get_selected() != previous_selection
            if not combo_used:
                input_cols.handle_event(event)
                input_rows.handle_event(event)

            if selection_changed:
                is_running_auto = False
                phase = PHASE_IDLE
                final_path = []
                unobservable_paths = []
                reset_cases()
                logs = [f"Đã chọn {combo_box.get_selected()}. Nhấn Tự động hoặc Bước tiếp."]
                if is_map_coloring_mode(combo_box.get_selected()):
                    reset_map_coloring()
                    logs = [f"Đã chọn {combo_box.get_selected()}. Theo dõi các vùng được tô màu từng bước."]
                log_offset = 0

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not combo_box.active:
                if btn_run.collidepoint(event.pos):
                    is_running_auto = not is_running_auto
                    if map_mode and is_running_auto and (phase == PHASE_IDLE or map_done):
                        reset_map_coloring(preserve_order=True)
                        phase = PHASE_EXECUTE
                        logs.clear()
                    elif is_running_auto and phase == PHASE_IDLE and initial_dirties:
                        run_selected_algorithm()

                if btn_next.collidepoint(event.pos) and not is_running_auto:
                    if map_mode:
                        if phase == PHASE_IDLE or map_done:
                            reset_map_coloring(preserve_order=True)
                            phase = PHASE_EXECUTE
                            logs.clear()
                        advance_map_coloring()
                    elif phase == PHASE_IDLE and initial_dirties:
                        run_selected_algorithm()
                    elif phase == PHASE_EXECUTE:
                        step_simulation(auto=False)

                if btn_random.collidepoint(event.pos):
                    is_running_auto = False
                    phase = PHASE_IDLE
                    final_path = []
                    unobservable_paths = []
                    if map_mode:
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
                    log_offset = 0

            if event.type == pygame.MOUSEWHEEL and not combo_box.active:
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
        draw_text(screen, "Trực quan hóa thuật toán AI", 24, 16, title_font, BLACK)
        draw_button(screen, btn_run, "Dừng" if is_running_auto else "Tự động", RED if is_running_auto else GREEN, WHITE)
        draw_button(screen, btn_next, "Bước tiếp", BLUE, WHITE)
        draw_button(screen, btn_random, "Đảo thứ tự" if map_mode else "Ngẫu nhiên", YELLOW, BLACK)
        if not map_mode:
            input_cols.draw(screen)
            input_rows.draw(screen)

        if map_mode:
            map_rect = pygame.Rect(24, 124, 700, 424)
            side_rect = pygame.Rect(748, 124, 408, 424)
            draw_card(screen, map_rect, "Tô màu bản đồ TP.HCM", selection)
            if HCM_MAP_RENDERER is not None:
                screen.blit(HCM_MAP_RENDERER.render(map_assignments), (map_rect.x + 54, map_rect.y + 60))
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
        else:
            sim_rect = pygame.Rect(24, 124, 700, 424)
            side_rect = pygame.Rect(748, 124, 408, 424)
            draw_text(screen, "Mô phỏng máy hút bụi", sim_rect.x, sim_rect.y, section_font, BLACK)
            draw_text(screen, selection, sim_rect.x, sim_rect.y + 28, small_font, MUTED, sim_rect.w)

            if uncertain_mode:
                grid_w = current_cols * CELL_SIZE + 28
                grid_h = current_rows * CELL_SIZE + 58
                x, y = sim_rect.x, sim_rect.y + 64
                for idx, case in enumerate(simulation_cases[:9]):
                    if x + grid_w > sim_rect.right - 10:
                        x = sim_rect.x
                        y += grid_h + 12
                    if y + grid_h <= sim_rect.bottom - 10:
                        draw_grid_case(screen, case, x, y, current_cols, current_rows, phase, f"Trường hợp {idx + 1}", case["initial_dirties"])
                    x += grid_w + 12
            elif simulation_cases:
                draw_grid_case(screen, simulation_cases[0], sim_rect.x, sim_rect.y + 78, current_cols, current_rows, phase, "Máy hút bụi", initial_dirties)

            case0 = simulation_cases[0] if simulation_cases else None
            cleaned = len(initial_dirties) - len(case0["current_dirties"]) if case0 else 0
            draw_card(screen, side_rect, "Trạng thái chạy")
            draw_metric(screen, side_rect.x + 18, side_rect.y + 76, "Bước", str(case0["path_index"] if case0 else 0), BLUE)
            draw_metric(screen, side_rect.x + 160, side_rect.y + 76, "Đã dọn", f"{cleaned}/{len(initial_dirties)}", GREEN)
            if case0 and case0.get("path"):
                draw_progress(screen, side_rect.x + 18, side_rect.y + 166, side_rect.w - 36, 12, case0["path_index"] + 1, len(case0["path"]))
                draw_text(screen, f"Độ dài đường đi: {len(case0['path'])}", side_rect.x + 18, side_rect.y + 188, font, MUTED)
            draw_timeline(screen, pygame.Rect(side_rect.x + 18, side_rect.y + 220, side_rect.w - 36, 204), case0 or {}, initial_dirties, phase)

        draw_logs(screen, pygame.Rect(24, 570, 1132, 170), logs, log_offset)
        combo_box.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
