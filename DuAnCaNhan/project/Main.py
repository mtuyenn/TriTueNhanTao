# pyrefly: ignore [missing-import]
import pygame
import os
import algorithm
import random
from ui import ComboBox, InputBox, WHITE, BLACK, GRAY, BLUE, GREEN, RED, YELLOW, DARK_GRAY

# Khởi tạo Pygame
pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vacuum Cleaner Visualization (TSP Pathfinding)")
font = pygame.font.SysFont('segoeui', 18)
log_font = pygame.font.SysFont('segoeui', 16)

# Kích thước Grid
COLS, ROWS = 7, 7
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
                         ["BFS 1", "BFS 2 (Optimal)", "DFS 1", "DFS 2 (Optimal)", "IDS 1", "IDS 2 (Optimal)", "UCS", "Greedy", "A*", "IDA*", "Simple Hill Climbing", "Steepest Ascent", "Stochastic HC", "Random Restart HC", "Simulated Annealing", "Local Beam Search"], font)

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
    final_path = []
    path_index = 0
    
    logs = [f"Khởi tạo: Bắt đầu {start_state}, {len(initial_dirties)} đích"]
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
                final_path, path_index = [], 0
                current_dirties = list(initial_dirties)
                logs = ["Đã đổi thuật toán, chờ chạy..."]
                log_offset = 0

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Click Run
                if btn_run.collidepoint(event.pos):
                    is_running_auto = not is_running_auto
                    if is_running_auto and phase == PHASE_IDLE and current_dirties:
                        current_dirties = list(initial_dirties)
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
                        
                        logs.clear()
                        log_offset = 0
                        final_path = []
                        for state_data in algo_generator:
                            if state_data.get('done'):
                                final_path = state_data.get('path', [])
                                break
                        
                        if final_path:
                            phase = PHASE_EXECUTE
                            path_index = 0
                            logs.append(f"Đã tìm thấy đường đi ({len(final_path) - 1} bước)!")
                        else:
                            is_running_auto = False
                            logs.append("Không tìm thấy đường đi!")

                # Click Next
                if btn_next.collidepoint(event.pos) and not is_running_auto:
                    if phase == PHASE_IDLE and current_dirties:
                        current_dirties = list(initial_dirties)
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
                        
                        logs.clear()
                        log_offset = 0
                        final_path = []
                        for state_data in algo_generator:
                            if state_data.get('done'):
                                final_path = state_data.get('path', [])
                                break
                        
                        if final_path:
                            phase = PHASE_EXECUTE
                            path_index = 0
                            logs.append(f"Đã tìm thấy đường đi ({len(final_path) - 1} bước)!")
                        else:
                            logs.append("Không tìm thấy đường đi!")
                            
                    elif phase == PHASE_EXECUTE:
                        if final_path and path_index < len(final_path) - 1:
                            path_index += 1
                            pos = final_path[path_index]
                            logs.append(f"Bước {path_index}: Robot di chuyển đến {pos}")
                            log_offset = 0
                            if pos in current_dirties:
                                current_dirties.remove(pos)
                                logs.append(f"ĐÃ DỌN SẠCH rác tại {pos}!")
                            
                            if path_index == len(final_path) - 1:
                                if len(current_dirties) == 0:
                                    logs.append("SÀN NHÀ ĐÃ SẠCH HOÀN TOÀN!")
                                else:
                                    logs.append("DỪNG LẠI (KẸT TẠI CỰC TRỊ ĐỊA PHƯƠNG)!")
                                is_running_auto = False

                # Click Randomize
                if btn_random.collidepoint(event.pos):
                    if input_cols.text.isdigit(): current_cols = max(3, int(input_cols.text))
                    if input_rows.text.isdigit(): current_rows = max(3, int(input_rows.text))

                    is_running_auto = False
                    phase = PHASE_IDLE
                    final_path, path_index = [], 0
                    start_state, initial_dirties = get_random_states(current_cols, current_rows)
                    current_dirties = list(initial_dirties)
                    logs = [f"Đã Random! Sàn {current_cols}x{current_rows}. Bắt đầu {start_state}, {len(initial_dirties)} đích"]
                    log_offset = 0
            
            if event.type == pygame.MOUSEWHEEL:
                mouse_pos = pygame.mouse.get_pos()
                # Check if mouse is within log area
                if 20 <= mouse_pos[0] <= 980 and 500 <= mouse_pos[1] <= 680:
                    log_offset += event.y
                    max_offset = max(0, len(logs) - 8) # 8 is max_visible_logs
                    if log_offset > max_offset: log_offset = max_offset
                    if log_offset < 0: log_offset = 0

        # Logic chạy tự động 
        if is_running_auto:
            if phase == PHASE_EXECUTE:
                pygame.time.delay(300) # Di chuyển chậm (300ms)
                if final_path and path_index < len(final_path) - 1:
                    path_index += 1
                    pos = final_path[path_index]
                    logs.append(f"Bước {path_index}: Robot di chuyển đến {pos}")
                    log_offset = 0
                    if pos in current_dirties:
                        current_dirties.remove(pos)
                        logs.append(f"ĐÃ DỌN SẠCH rác tại {pos}!")
                    
                    if path_index == len(final_path) - 1:
                        if len(current_dirties) == 0:
                            logs.append("SÀN NHÀ ĐÃ SẠCH HOÀN TOÀN!")
                        else:
                            logs.append("DỪNG LẠI (KẸT TẠI CỰC TRỊ ĐỊA PHƯƠNG)!")
                        is_running_auto = False
                else:
                    is_running_auto = False

        # --- VẼ GIAO DIỆN ---

        # 1. Vẽ Grid Sàn nhà 
        draw_text(screen, "Máy Hút Bụi", GRID_OFFSET_X, GRID_OFFSET_Y - 25, font)
        
        # Determine what to draw based on phase
        vacuum_pos = None
        draw_dirties = []
        if phase == PHASE_IDLE:
            vacuum_pos = start_state
            draw_dirties = current_dirties
        elif phase == PHASE_EXECUTE:
            vacuum_pos = final_path[path_index] if final_path else start_state
            draw_dirties = current_dirties

        for r in range(current_rows):
            for c in range(current_cols):
                rect = pygame.Rect(GRID_OFFSET_X + c * CELL_SIZE, GRID_OFFSET_Y + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                cell_pos = (c, r)

                if USE_IMAGES:
                    if cell_pos in draw_dirties:
                        screen.blit(img_dirty_floor, rect)
                    else:
                        screen.blit(img_clean_floor, rect)
                else:
                    # Sàn nhà sạch màu xanh, sàn nhà bẩn màu đỏ
                    color = GREEN
                    if cell_pos in draw_dirties:
                        color = RED

                    pygame.draw.rect(screen, color, rect)
                    
                pygame.draw.rect(screen, BLACK, rect, 1)

                # Vẽ path marker cho đường đi robot đã đi qua (chỉ ở Phase Execute)
                if phase == PHASE_EXECUTE and final_path and cell_pos in final_path[:path_index+1]:
                    path_rect = pygame.Rect(rect.x + 15, rect.y + 15, 20, 20)
                    pygame.draw.rect(screen, YELLOW, path_rect)

                # Vẽ robot hút bụi
                if cell_pos == vacuum_pos:
                    if USE_IMAGES:
                        screen.blit(img_robot, (rect.x + 5, rect.y + 5))
                    else:
                        pygame.draw.circle(screen, BLUE, rect.center, 15)

        # 2. Vẽ danh sách đường đi (ở giữa)
        PATH_X = 400
        PATH_Y = 80
        draw_text(screen, "LỊCH TRÌNH DI CHUYỂN", PATH_X, PATH_Y - 25, font)

        if phase == PHASE_EXECUTE and final_path:
            start_idx = max(0, path_index - 10)
            display_steps = final_path[start_idx:start_idx + 14]
            
            for i, p in enumerate(display_steps):
                real_i = start_idx + i
                p_rect = pygame.Rect(PATH_X, PATH_Y + i * 30, 200, 25)
                bg_color = YELLOW if real_i == path_index else BLUE
                text_color = BLACK if real_i == path_index else WHITE
                
                pygame.draw.rect(screen, bg_color, p_rect)
                pygame.draw.rect(screen, BLACK, p_rect, 1)
                
                action = "Đi"
                if p in initial_dirties and final_path.index(p) == real_i:
                    action = "Dọn"
                draw_text(screen, f"Bước {real_i}: {p} ({action})", PATH_X + 10, PATH_Y + i * 30 + 3, font, text_color)

        if phase == PHASE_EXECUTE and final_path and path_index == len(final_path) - 1:
            if len(current_dirties) == 0:
                bg_rect = pygame.Rect(630, 80, 300, 40)
                pygame.draw.rect(screen, GREEN, bg_rect)
                pygame.draw.rect(screen, BLACK, bg_rect, 2)
                draw_text(screen, "SÀN NHÀ ĐÃ SẠCH HOÀN TOÀN!", 640, 90, font, BLACK)
            else:
                bg_rect = pygame.Rect(630, 80, 300, 40)
                pygame.draw.rect(screen, RED, bg_rect)
                pygame.draw.rect(screen, BLACK, bg_rect, 2)
                draw_text(screen, "KẸT TẠI CỰC TRỊ ĐỊA PHƯƠNG!", 640, 90, font, WHITE)

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
        draw_text(screen, "Ngẫu Nhiên", btn_random.x + 15, btn_random.y + 5, font)

        input_cols.draw(screen)
        input_rows.draw(screen)


        # Vẽ Combobox sau cùng để nó popup lên trên các element khác
        combo_box.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()