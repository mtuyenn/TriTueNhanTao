# pyrefly: ignore [missing-import]
import pygame
import os
import algorithm
import random
from ui import ComboBox, InputBox, WHITE, BLACK, GRAY, BLUE, GREEN, RED, YELLOW, DARK_GRAY
from map_coloring_view import HCMMapRenderer

# Khởi tạo Pygame
pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vacuum Cleaner Visualization (TSP Pathfinding)")
font = pygame.font.SysFont('segoeui', 18)
log_font = pygame.font.SysFont('segoeui', 16)
title_font = pygame.font.SysFont('segoeui', 22, bold=True)

# Kích thước Grid
COLS, ROWS = 3, 3
CELL_SIZE = 50
GRID_OFFSET_X, GRID_OFFSET_Y = 20, 80

# Load images
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
except Exception as e:
    print(f"Không thể load ảnh: {e}")
    USE_IMAGES = False

try:
    HCM_MAP_RENDERER = HCMMapRenderer(
        os.path.join(BASE_DIR, "assets", "hcm_city_map.png")
    )
except Exception as e:
    print(f"Không thể load bản đồ TP.HCM: {e}")
    HCM_MAP_RENDERER = None


def draw_text(surface, text, x, y, f_sys, color=BLACK):
    img = f_sys.render(text, True, color)
    surface.blit(img, (x, y))

def get_random_states(cols, rows):
    all_positions = [(c, r) for c in range(cols) for r in range(rows)]
    start = random.choice(all_positions)
    all_positions.remove(start)
    
    num_dirties = random.randint(1, min(6, len(all_positions))) # Random từ 1 đến 6 ô bẩn
    dirties = tuple(random.sample(all_positions, num_dirties))
    return start, dirties

def main():
    clock = pygame.time.Clock()

    current_cols = COLS
    current_rows = ROWS
    start_state, initial_dirties = get_random_states(current_cols, current_rows)
    current_dirties = list(initial_dirties)

    combo_box = ComboBox(20, 20, 190, 30,
                         ["BFS 1", "BFS 2 (Optimal)", "DFS 1", "DFS 2 (Optimal)", "IDS 1", "IDS 2 (Optimal)", "UCS", "Greedy", "A*", "IDA*", "Simple Hill Climbing", "Steepest Ascent", "Stochastic HC", "Random Restart HC", "Simulated Annealing", "Local Beam Search", "UnObservable Search", "PartialObservation Search", "AND-OR Graph Search", "Backtracking tô màu", "Forward Checking tô màu"], font)

    btn_run = pygame.Rect(220, 20, 100, 30)
    btn_next = pygame.Rect(330, 20, 100, 30)
    btn_random = pygame.Rect(440, 20, 130, 30)

    input_cols = InputBox(600, 20, 50, 30, str(current_cols), font, label="Cột:")
    input_rows = InputBox(670, 20, 50, 30, str(current_rows), font, label="Hàng:")

    is_running_auto = False
    
    # State machine
    PHASE_IDLE = 0
    PHASE_EXECUTE = 1
    phase = PHASE_IDLE
    
    # Execute variables
    simulation_cases = []
    partial_bs_positions = []
    
    def reset_cases():
        simulation_cases.clear()
        partial_bs_positions.clear()
        sel = combo_box.get_selected()
        is_unobservable = "UnObservable" in sel
        is_partial = "PartialObservation" in sel
        
        if is_unobservable:
            all_positions = [(c, r) for c in range(current_cols) for r in range(current_rows)]
            for c in range(current_cols):
                for r in range(current_rows):
                    pos = (c, r)
                    num_guess = random.randint(1, len(all_positions) - 1)
                    possible_dirties = [p for p in all_positions if p != pos]
                    guess_dirties = list(random.sample(possible_dirties, num_guess))
                    
                    simulation_cases.append({
                        "start_state": pos,
                        "initial_dirties": tuple(guess_dirties),
                        "current_dirties": list(guess_dirties),
                        "path": [],
                        "path_index": 0,
                        "done": False
                    })
        elif is_partial:
            clean_positions = [(c, r) for c in range(current_cols) for r in range(current_rows) if (c, r) not in initial_dirties]
            if len(clean_positions) >= 2:
                selected_positions = random.sample(clean_positions, 2)
            else:
                selected_positions = clean_positions
            
            all_positions = [(c, r) for c in range(current_cols) for r in range(current_rows)]
            for pos in selected_positions:
                partial_bs_positions.append(pos)
                
                possible_dirties = [p for p in all_positions if p not in selected_positions]
                if possible_dirties:
                    num_guess = random.randint(1, len(possible_dirties))
                    guess_dirties = list(random.sample(possible_dirties, num_guess))
                else:
                    guess_dirties = []
                    
                simulation_cases.append({
                    "start_state": pos,
                    "initial_dirties": tuple(guess_dirties),
                    "current_dirties": list(guess_dirties),
                    "path": [],
                    "path_index": 0,
                    "done": False
                })
        else:
            simulation_cases.append({
                "start_state": start_state,
                "initial_dirties": tuple(initial_dirties),
                "current_dirties": list(initial_dirties),
                "path": [],
                "path_index": 0,
                "done": False
            })

    def prepare_cases_for_execution():
        """Start a run without changing the scenario shown to the user."""
        for case in simulation_cases:
            case["current_dirties"] = list(case["initial_dirties"])
            case["path"] = []
            case["path_index"] = 0
            case["done"] = False
            
    reset_cases()
    final_path = []
    unobservable_paths = []
    map_generator = None
    map_assignments = {}
    map_current_region = None
    map_current_color = None
    map_order = list(algorithm.HCM_REGIONS)
    map_done = False

    def is_map_coloring_mode():
        sel = combo_box.get_selected()
        return sel == "Backtracking tô màu" or sel == "Forward Checking tô màu"

    def reset_map_coloring(shuffle_order=False, preserve_order=False):
        nonlocal map_generator, map_assignments, map_current_region
        nonlocal map_current_color, map_order, map_done
        if not preserve_order:
            map_order = list(algorithm.HCM_REGIONS)
        if shuffle_order:
            random.shuffle(map_order)
            
        if combo_box.get_selected() == "Backtracking tô màu":
            map_generator = algorithm.backtracking_map_coloring(map_order)
        elif combo_box.get_selected() == "Forward Checking tô màu":
            map_generator = algorithm.forward_checking_map_coloring(map_order)
            
        map_assignments = {}
        map_current_region = None
        map_current_color = None
        map_done = False

    def advance_map_coloring():
        nonlocal map_assignments, map_current_region
        nonlocal map_current_color, map_done, is_running_auto
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
        logs.append(step["log"])
        if map_done:
            is_running_auto = False
    
    logs = [f"Khởi tạo: Bắt đầu {start_state}, {len(initial_dirties)} đích"]
    if "PartialObservation" in combo_box.get_selected():
        logs.append(f"Biết trước vị trí của partialobservation: {partial_bs_positions}")
    log_offset = 0

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            input_cols.handle_event(event)
            input_rows.handle_event(event)

            if combo_box.handle_event(event):
                # Reset 
                is_running_auto = False
                phase = PHASE_IDLE
                final_path = []
                unobservable_paths = []
                reset_cases()
                logs = ["Đã đổi thuật toán, chờ chạy..."]
                if is_map_coloring_mode():
                    reset_map_coloring()
                    mode_name = combo_box.get_selected()
                    logs = [f"Đã chọn {mode_name}. Nhấn Auto/Stop hoặc Next Step."]
                if "PartialObservation" in combo_box.get_selected():
                    logs.append(f"Biết trước vị trí của partialobservation: {partial_bs_positions}")
                log_offset = 0

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Click Run
                if btn_run.collidepoint(event.pos):
                    is_running_auto = not is_running_auto
                    if is_map_coloring_mode() and is_running_auto and (phase == PHASE_IDLE or map_done):
                        reset_map_coloring(preserve_order=True)
                        phase = PHASE_EXECUTE
                        logs.clear()
                        log_offset = 0
                    elif is_running_auto and phase == PHASE_IDLE and initial_dirties:
                        prepare_cases_for_execution()
                        sel = combo_box.get_selected()
                        if "BFS 1" in sel: algo_generator = algorithm.bfs1(start_state, initial_dirties, current_cols, current_rows)
                        elif "BFS 2" in sel: algo_generator = algorithm.bfs2(start_state, initial_dirties, current_cols, current_rows)
                        elif "DFS 1" in sel: algo_generator = algorithm.dfs1(start_state, initial_dirties, current_cols, current_rows)
                        elif "DFS 2" in sel: algo_generator = algorithm.dfs2(start_state, initial_dirties, current_cols, current_rows)
                        elif "IDS 1" in sel: algo_generator = algorithm.ids_normal(start_state, initial_dirties, current_cols, current_rows)
                        elif "IDS 2" in sel: algo_generator = algorithm.ids2_optimize(start_state, initial_dirties, current_cols, current_rows)
                        elif "UCS" in sel: algo_generator = algorithm.ucs(start_state, initial_dirties, current_cols, current_rows)
                        elif "Greedy" in sel: algo_generator = algorithm.Greedy_Search(start_state, initial_dirties, current_cols, current_rows)
                        elif "A*" in sel: algo_generator = algorithm.A_star(start_state, initial_dirties, current_cols, current_rows)
                        elif "IDA*" in sel: algo_generator = algorithm.IDA_start(start_state, initial_dirties, current_cols, current_rows)
                        elif "Simple Hill Climbing" in sel: algo_generator = algorithm.Simple_Hill_Climbing(start_state, initial_dirties, current_cols, current_rows)
                        elif "Steepest Ascent" in sel: algo_generator = algorithm.steepest_ascent_hill_climbing(start_state, initial_dirties, current_cols, current_rows)
                        elif "Stochastic HC" in sel: algo_generator = algorithm.stochastic_hill_climbing(start_state, initial_dirties, current_cols, current_rows)
                        elif "Random Restart HC" in sel: algo_generator = algorithm.random_restart_hill_climbing(start_state, initial_dirties, current_cols, current_rows)
                        elif "Simulated Annealing" in sel: algo_generator = algorithm.simulated_annealing(start_state, initial_dirties, current_cols, current_rows)
                        elif "Local Beam Search" in sel: algo_generator = algorithm.local_beam_search(start_state, initial_dirties, current_cols, current_rows)
                        elif "UnObservable Search" in sel: algo_generator = algorithm.unobservable_search(simulation_cases, current_cols, current_rows)
                        elif "PartialObservation Search" in sel: algo_generator = algorithm.partialobservation_search(simulation_cases, current_cols, current_rows)
                        elif "AND-OR Graph Search" in sel: algo_generator = algorithm.and_or_graph_search_generator(start_state, initial_dirties, current_cols, current_rows)
                        
                        logs.clear()
                        log_offset = 0
                        final_path = []
                        unobservable_paths = []
                        for state_data in algo_generator:
                            if state_data.get("done"):
                                final_path = state_data.get("path", [])
                                unobservable_paths = state_data.get("all_paths", [])
                                break
                        
                        if final_path or unobservable_paths:
                            phase = PHASE_EXECUTE
                            if ("UnObservable" in sel or "PartialObservation" in sel) and unobservable_paths:
                                path_map = {st: p for st, p in unobservable_paths}
                                for case in simulation_cases:
                                    if case["start_state"] in path_map:
                                        case["path"] = path_map[case["start_state"]]
                            else:
                                for case in simulation_cases:
                                    case["path"] = final_path
                            logs.append("Đã tìm thấy đường đi!")
                            if "PartialObservation" in sel:
                                logs.append(f"Biết trước vị trí của partialobservation: {partial_bs_positions}")
                        else:
                            is_running_auto = False
                            logs.append("Không tìm thấy đường đi!")

                # Click Next
                if btn_next.collidepoint(event.pos) and not is_running_auto and is_map_coloring_mode():
                    if phase == PHASE_IDLE or map_done:
                        reset_map_coloring(preserve_order=True)
                        phase = PHASE_EXECUTE
                        logs.clear()
                    advance_map_coloring()
                    log_offset = 0

                if btn_next.collidepoint(event.pos) and not is_running_auto and not is_map_coloring_mode():
                    if phase == PHASE_IDLE and initial_dirties:
                        prepare_cases_for_execution()
                        sel = combo_box.get_selected()
                        if "BFS 1" in sel: algo_generator = algorithm.bfs1(start_state, initial_dirties, current_cols, current_rows)
                        elif "BFS 2" in sel: algo_generator = algorithm.bfs2(start_state, initial_dirties, current_cols, current_rows)
                        elif "DFS 1" in sel: algo_generator = algorithm.dfs1(start_state, initial_dirties, current_cols, current_rows)
                        elif "DFS 2" in sel: algo_generator = algorithm.dfs2(start_state, initial_dirties, current_cols, current_rows)
                        elif "IDS 1" in sel: algo_generator = algorithm.ids_normal(start_state, initial_dirties, current_cols, current_rows)
                        elif "IDS 2" in sel: algo_generator = algorithm.ids2_optimize(start_state, initial_dirties, current_cols, current_rows)
                        elif "UCS" in sel: algo_generator = algorithm.ucs(start_state, initial_dirties, current_cols, current_rows)
                        elif "Greedy" in sel: algo_generator = algorithm.Greedy_Search(start_state, initial_dirties, current_cols, current_rows)
                        elif "A*" in sel: algo_generator = algorithm.A_star(start_state, initial_dirties, current_cols, current_rows)
                        elif "IDA*" in sel: algo_generator = algorithm.IDA_start(start_state, initial_dirties, current_cols, current_rows)
                        elif "Simple Hill Climbing" in sel: algo_generator = algorithm.Simple_Hill_Climbing(start_state, initial_dirties, current_cols, current_rows)
                        elif "Steepest Ascent" in sel: algo_generator = algorithm.steepest_ascent_hill_climbing(start_state, initial_dirties, current_cols, current_rows)
                        elif "Stochastic HC" in sel: algo_generator = algorithm.stochastic_hill_climbing(start_state, initial_dirties, current_cols, current_rows)
                        elif "Random Restart HC" in sel: algo_generator = algorithm.random_restart_hill_climbing(start_state, initial_dirties, current_cols, current_rows)
                        elif "Simulated Annealing" in sel: algo_generator = algorithm.simulated_annealing(start_state, initial_dirties, current_cols, current_rows)
                        elif "Local Beam Search" in sel: algo_generator = algorithm.local_beam_search(start_state, initial_dirties, current_cols, current_rows)
                        elif "UnObservable Search" in sel: algo_generator = algorithm.unobservable_search(simulation_cases, current_cols, current_rows)
                        elif "PartialObservation Search" in sel: algo_generator = algorithm.partialobservation_search(simulation_cases, current_cols, current_rows)
                        elif "AND-OR Graph Search" in sel: algo_generator = algorithm.and_or_graph_search_generator(start_state, initial_dirties, current_cols, current_rows)
                        
                        logs.clear()
                        log_offset = 0
                        final_path = []
                        unobservable_paths = []
                        for state_data in algo_generator:
                            if state_data.get("done"):
                                final_path = state_data.get("path", [])
                                unobservable_paths = state_data.get("all_paths", [])
                                break
                        
                        if final_path or unobservable_paths:
                            phase = PHASE_EXECUTE
                            if ("UnObservable" in sel or "PartialObservation" in sel) and unobservable_paths:
                                path_map = {st: p for st, p in unobservable_paths}
                                for case in simulation_cases:
                                    if case["start_state"] in path_map:
                                        case["path"] = path_map[case["start_state"]]
                            else:
                                for case in simulation_cases:
                                    case["path"] = final_path
                            logs.append("Đã tìm thấy đường đi!")
                            if "PartialObservation" in sel:
                                logs.append(f"Biết trước vị trí của partialobservation: {partial_bs_positions}")
                        else:
                            logs.append("Không tìm thấy đường đi!")
                            
                    elif phase == PHASE_EXECUTE:
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
                            logs.append(f"Bước {case0['path_index']}: Robot tiến vào ô {pos}")
                            log_offset = 0
                        else:
                            logs.append("SÀN NHÀ ĐÃ SẠCH! (hoặc kết thúc đường đi)")
                            is_running_auto = False

                # Click Randomize
                if btn_random.collidepoint(event.pos) and is_map_coloring_mode():
                    is_running_auto = False
                    phase = PHASE_IDLE
                    reset_map_coloring(shuffle_order=True)
                    logs = ["Đã đổi ngẫu nhiên thứ tự tô các quận/huyện."]
                    log_offset = 0

                if btn_random.collidepoint(event.pos) and not is_map_coloring_mode():
                    if input_cols.text.isdigit(): current_cols = max(3, int(input_cols.text))
                    if input_rows.text.isdigit(): current_rows = max(3, int(input_rows.text))

                    is_running_auto = False
                    phase = PHASE_IDLE
                    final_path = []
                    unobservable_paths = []
                    start_state, initial_dirties = get_random_states(current_cols, current_rows)
                    reset_cases()
                    logs = [f"Đã Random! Sàn {current_cols}x{current_rows}. Bắt đầu {start_state}, {len(initial_dirties)} đích"]
                    if "PartialObservation" in combo_box.get_selected():
                        logs.append(f"Biết trước vị trí của partialobservation: {partial_bs_positions}")
                    log_offset = 0
            
            if event.type == pygame.MOUSEWHEEL:
                mouse_pos = pygame.mouse.get_pos()
                if 20 <= mouse_pos[0] <= 980 and 500 <= mouse_pos[1] <= 680:
                    log_offset += event.y
                    max_offset = max(0, len(logs) - 8)
                    if log_offset > max_offset: log_offset = max_offset
                    if log_offset < 0: log_offset = 0

        # Logic chạy tự động 
        if is_running_auto:
            if is_map_coloring_mode() and phase == PHASE_EXECUTE:
                pygame.time.delay(250)
                advance_map_coloring()
                log_offset = 0
            elif phase == PHASE_EXECUTE:
                pygame.time.delay(300)
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
                    logs.append(f"Bước {case0['path_index']}: Tự động di chuyển đến ô {pos}")
                    log_offset = 0
                else:
                    logs.append("SÀN NHÀ ĐÃ SẠCH! (hoặc kết thúc đường đi)")
                    is_running_auto = False

        # --- VẼ GIAO DIỆN ---
        is_backtracking = is_map_coloring_mode()
        is_unobservable = "UnObservable" in combo_box.get_selected() or "PartialObservation" in combo_box.get_selected()

        if is_backtracking:
            title_text = "TÔ MÀU BẢN ĐỒ TP.HCM BẰNG " + combo_box.get_selected().replace(" tô màu", "").upper()
            draw_text(screen, title_text, 20, 50, title_font, BLUE)
            if HCM_MAP_RENDERER is not None:
                screen.blit(HCM_MAP_RENDERER.render(map_assignments), (20, 75))
            else:
                draw_text(screen, "Không thể tải assets/hcm_city_map.png", 20, 100, font, RED)

            panel_x = 390
            draw_text(screen, f"Đã tô: {len(map_assignments)}/{len(algorithm.HCM_REGIONS)}", panel_x, 85, font)
            if map_current_region:
                draw_text(screen, f"Đang xét: {map_current_region}", panel_x, 115, font)
            if map_current_color is not None:
                color_name, color_rgb = algorithm.MAP_COLORS[map_current_color]
                pygame.draw.rect(screen, color_rgb, (panel_x, 148, 24, 24))
                pygame.draw.rect(screen, BLACK, (panel_x, 148, 24, 24), 1)
                draw_text(screen, color_name, panel_x + 34, 149, font)

            draw_text(screen, "Bảng màu", panel_x, 195, font)
            for color_index, (color_name, color_rgb) in enumerate(algorithm.MAP_COLORS):
                y = 225 + color_index * 34
                pygame.draw.rect(screen, color_rgb, (panel_x, y, 24, 24))
                pygame.draw.rect(screen, BLACK, (panel_x, y, 24, 24), 1)
                draw_text(screen, color_name, panel_x + 34, y + 1, font)

            if map_done:
                draw_text(screen, "HOÀN TẤT", panel_x, 385, font, GREEN)
        
        grid_w = current_cols * CELL_SIZE
        grid_h = current_rows * CELL_SIZE
        margin_x = 20
        margin_y = 40
        start_x = 20
        start_y = 80
        
        current_x = start_x
        current_y = start_y
        
        cases_to_draw = [] if is_backtracking else simulation_cases
        for idx, case in enumerate(cases_to_draw):
            if current_x + grid_w > 980 and current_x != start_x:
                current_x = start_x
                current_y += grid_h + margin_y
                
            if is_unobservable:
                draw_text(screen, f"Trường hợp {idx+1}", current_x, current_y - 25, font)
            else:
                draw_text(screen, "Máy Hút Bụi", current_x, current_y - 25, font)
                
            if phase == PHASE_IDLE:
                vacuum_pos = case["start_state"]
            else:
                vacuum_pos = case["path"][case["path_index"]] if case["path"] else case["start_state"]

            for r in range(current_rows):
                for c in range(current_cols):
                    rect = pygame.Rect(current_x + c * CELL_SIZE, current_y + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    cell_pos = (c, r)

                    if USE_IMAGES:
                        if cell_pos in case["current_dirties"]:
                            screen.blit(img_dirty_floor, rect)
                        else:
                            screen.blit(img_clean_floor, rect)
                    else:
                        color = GREEN
                        if cell_pos in case["current_dirties"]:
                            color = RED
                        pygame.draw.rect(screen, color, rect)
                        
                    pygame.draw.rect(screen, BLACK, rect, 1)

                    if phase == PHASE_EXECUTE and case["path"] and cell_pos in case["path"][:case["path_index"]+1]:
                        path_rect = pygame.Rect(rect.x + 15, rect.y + 15, 20, 20)
                        pygame.draw.rect(screen, YELLOW, path_rect)

                    if cell_pos == vacuum_pos:
                        if USE_IMAGES:
                            screen.blit(img_robot, (rect.x + 5, rect.y + 5))
                        else:
                            pygame.draw.circle(screen, BLUE, rect.center, 15)
            
            current_x += grid_w + margin_x

        if not is_backtracking and not is_unobservable and simulation_cases:
            PATH_X = start_x + grid_w + 50
            PATH_Y = 80
            draw_text(screen, "LỊCH TRÌNH DI CHUYỂN", PATH_X, PATH_Y - 25, font)

            case0 = simulation_cases[0]
            if phase == PHASE_EXECUTE and case0["path"]:
                p_idx = case0["path_index"]
                start_idx = max(0, p_idx - 10)
                display_steps = case0["path"][start_idx:start_idx + 14]
                
                for i, p in enumerate(display_steps):
                    real_i = start_idx + i
                    p_rect = pygame.Rect(PATH_X, PATH_Y + i * 30, 200, 25)
                    bg_color = YELLOW if real_i == p_idx else BLUE
                    text_color = BLACK if real_i == p_idx else WHITE
                    
                    pygame.draw.rect(screen, bg_color, p_rect)
                    pygame.draw.rect(screen, BLACK, p_rect, 1)
                    
                    action = "Đi"
                    if p in initial_dirties and case0["path"].index(p) == real_i:
                        action = "Dọn"
                    draw_text(screen, f"Bước {real_i}: {p} ({action})", PATH_X + 10, PATH_Y + i * 30 + 3, font, text_color)

            if phase == PHASE_EXECUTE and case0["path"] and case0["path_index"] == len(case0["path"]) - 1:
                if len(case0["current_dirties"]) == 0:
                    bg_rect = pygame.Rect(PATH_X, 80 + 15 * 30, 200, 40)
                    pygame.draw.rect(screen, GREEN, bg_rect)
                    pygame.draw.rect(screen, BLACK, bg_rect, 2)
                    draw_text(screen, "SÀN NHÀ ĐÃ SẠCH HOÀN TOÀN!", PATH_X + 10, 80 + 15 * 30 + 10, font, BLACK)
                else:
                    bg_rect = pygame.Rect(PATH_X, 80 + 15 * 30, 200, 40)
                    pygame.draw.rect(screen, RED, bg_rect)
                    pygame.draw.rect(screen, BLACK, bg_rect, 2)
                    draw_text(screen, "KẸT TẠI CỰC TRỊ ĐỊA PHƯƠNG!", PATH_X + 10, 80 + 15 * 30 + 10, font, WHITE)

        # 3. Vẽ Log/Catalog 
        LOG_X = 20
        LOG_Y = 500
        log_rect = pygame.Rect(LOG_X, LOG_Y, 960, 180)
        pygame.draw.rect(screen, DARK_GRAY, log_rect)
        draw_text(screen, "HOẠT ĐỘNG", LOG_X + 10, LOG_Y + 10, font, WHITE)

        max_visible_logs = 8
        start_idx = max(0, len(logs) - max_visible_logs - log_offset)
        end_idx = start_idx + max_visible_logs
        display_logs = logs[start_idx:end_idx]
        
        for i, log_msg in enumerate(display_logs):
            draw_text(screen, f"> {log_msg}", LOG_X + 10, LOG_Y + 35 + i * 18, log_font, GREEN)

        # Vẽ Button
        pygame.draw.rect(screen, GREEN if not is_running_auto else RED, btn_run)
        pygame.draw.rect(screen, BLACK, btn_run, 2)
        draw_text(screen, "Auto/Stop", btn_run.x + 10, btn_run.y + 5, font)

        pygame.draw.rect(screen, GRAY, btn_next)
        pygame.draw.rect(screen, BLACK, btn_next, 2)
        draw_text(screen, "Next Step", btn_next.x + 15, btn_next.y + 5, font)

        pygame.draw.rect(screen, YELLOW, btn_random)
        pygame.draw.rect(screen, BLACK, btn_random, 2)
        random_label = "Đổi thứ tự" if is_backtracking else "Ngẫu Nhiên"
        draw_text(screen, random_label, btn_random.x + 15, btn_random.y + 5, font)

        if not is_backtracking:
            input_cols.draw(screen)
            input_rows.draw(screen)


        # Vẽ Combobox sau cùng để nó popup lên trên các element khác
        combo_box.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
