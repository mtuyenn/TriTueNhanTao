# AI Visualizer - Đồ án cá nhân Trí tuệ nhân tạo

Dự án xây dựng một ứng dụng trực quan hóa các thuật toán Trí tuệ nhân tạo bằng **Python + Pygame**. Sử dụng nhiều thuật toán tìm kiếm trong lĩnh vực Trí tuệ nhân tạo, bao gồm các nhóm:

- Tìm kiếm không có thông tin
- Tìm kiếm có thông tin
- Tìm kiếm cục bộ
- Tìm kiếm môi trường phức tạp
- Tìm kiếm ràng buộc CSP
- Tìm kiếm đối kháng

Trong đó, mỗi nhóm sử dụng một bài toán cụ thể để minh họa:

- **Robot hút bụi**: tìm đường đi để dọn sạch các ô rác trên lưới.
- **Tô màu bản đồ TP.HCM**: minh họa các thuật toán ràng buộc CSP.
- **Cờ caro 3x3**: minh họa tìm kiếm đối kháng bằng Minimax, Alpha-Beta và Expectimax.
- **So sánh thuật toán**: đo thời gian chạy, bộ nhớ, số node đã xét và độ dài đường đi.

---

## 1. Mục tiêu

- Cài đặt và trực quan hóa các nhóm thuật toán tìm kiếm trong AI.
- Cho phép người dùng chọn thuật toán, chạy từng bước hoặc chạy tự động.
- So sánh hiệu năng giữa các thuật toán bằng biểu đồ.
- Ghi lại kết quả thực nghiệm vào file `DuAnCaNhan/project/comparison_results.csv`.

---

## 2. Công nghệ sử dụng

| Thành phần | Công nghệ |
|---|---|
| Ngôn ngữ | Python |
| Giao diện | Pygame |
| Dữ liệu so sánh | CSV |
| Bài toán tìm kiếm | Robot hút bụi trên lưới |
| Bài toán CSP | Tô màu bản đồ TP.HCM |
| Bài toán đối kháng | Cờ caro 3x3 |

---

## 3. Cài đặt và chạy chương trình

### 3.1. Cài thư viện

```bash
pip install pygame
```

### 3.2. Chạy ứng dụng

```bash
cd DuAnCaNhan
python project/Main.py
```

Khi chạy chương trình, người dùng có thể:

- Chọn thuật toán trong danh sách.
- Nhấn **Tự động** để xem mô phỏng liên tục.
- Nhấn **Bước tiếp** để quan sát từng bước.
- Nhấn **Ngẫu nhiên** để tạo trạng thái robot hút bụi mới.
- Chọn **So sánh thuật toán** để xem biểu đồ so sánh hiệu năng giữa các thuật toán trong từng nhóm.

---

## 4. Cấu trúc thư mục

```text
DuAnCaNhan/project/
├── Main.py
├── ui.py
├── map_coloring_view.py
├── comparison_results.csv
├── assets/
│   ├── gif/
│   ├── images/
│   ├── clean_floor.png
│   ├── dirty_floor.png
│   ├── robot_vacuum.png
│   └── hcm_city_map.png
└── algorithm/
    ├── uninformed_search/
    │   ├── bfs1.py
    │   ├── bfs2.py
    │   ├── dfs1.py
    │   ├── dfs2.py
    │   ├── ids1.py
    │   ├── ids2.py
    │   └── ucs.py
    ├── informed_search/
    │   ├── greedy_search.py
    │   ├── a_star.py
    │   └── ida_star.py
    ├── hill_climbing/
    │   ├── simple_hill_climbing.py
    │   ├── steepest_ascent_hill_climbing.py
    │   ├── stochastic_hill_climbing.py
    │   ├── random_restart_hill_climbing.py
    │   ├── simulated_annealing.py
    │   └── local_beam_search.py
    ├── sreach_in_complex_environments/
    │   ├── unobservable_search.py
    │   ├── partial_observation_search.py
    │   └── and_or_graph_search.py
    ├── CSP/
    │   ├── backtracking.py
    │   ├── forward_checking.py
    │   ├── ac3.py
    │   └── min_conflicts.py
    └── adversarial_search/
        ├── minimax.py
        ├── alpha_beta.py
        └── expectimax.py
```

---

## 5. Các nhóm thuật toán

### 5.1. Tìm kiếm không có thông tin

**Các thuật toán:**

- BFS 1
- BFS 2 (Optimized)
- DFS 1
- DFS 2 (Optimized)
- IDS 1
- IDS 2 (Optimized)
- UCS

**Thành phần bài toán robot hút bụi:**

- **Không gian trạng thái**: vị trí của robot và tập các ô còn rác.
- **Trạng thái ban đầu**: vị trí xuất phát của robot và các ô rác.
- **Trạng thái đích**: tất cả ô rác đã được dọn sạch.
- **Hành động**: di chuyển lên, xuống, trái, phải nếu hợp lệ.
- **Chi phí**: mỗi bước di chuyển có chi phí bằng 1.
- **Lời giải**: đường đi của robot từ trạng thái ban đầu đến khi dọn sạch.

#### GIF minh họa

| Thuật toán | GIF |
|---|---|
| BFS 1 | <img src="DuAnCaNhan/project/assets/gif/1/bfs1.gif" width="760" alt="BFS 1"> |
| BFS 2 (Optimized) | <img src="DuAnCaNhan/project/assets/gif/1/bfs2.gif" width="760" alt="BFS 2"> |
| DFS 1 | <img src="DuAnCaNhan/project/assets/gif/1/dfs1.gif" width="760" alt="DFS 1"> |
| DFS 2 (Optimized) | <img src="DuAnCaNhan/project/assets/gif/1/dfs2.gif" width="760" alt="DFS 2"> |
| IDS 1 | <img src="DuAnCaNhan/project/assets/gif/1/ids1.gif" width="760" alt="IDS 1"> |
| IDS 2 (Optimized) | <img src="DuAnCaNhan/project/assets/gif/1/ids2.gif" width="760" alt="IDS 2"> |
| UCS | <img src="DuAnCaNhan/project/assets/gif/1/ucs.gif" width="760" alt="UCS"> |

#### So sánh thuật toán

| Thời gian | Số node đã xét |
|---|---|
| <img src="DuAnCaNhan/project/assets/images/1/1_time.png" width="500" alt="Uninformed time"> | <img src="DuAnCaNhan/project/assets/images/1/1_node.png" width="500" alt="Uninformed nodes"> |

| Bộ nhớ | Độ dài đường đi |
|---|---|
| <img src="DuAnCaNhan/project/assets/images/1/1_mem.png" width="500" alt="Uninformed memory"> | <img src="DuAnCaNhan/project/assets/images/1/1_length.png" width="500" alt="Uninformed path length"> |

**Nhận xét:**

- **BFS** thường tìm được đường đi ngắn nhưng tốn bộ nhớ vì phải lưu nhiều trạng thái ở cùng độ sâu.
- **DFS** dùng ít bộ nhớ hơn nhưng có thể đi sâu vào nhánh không tối ưu.
- **IDS** cân bằng giữa BFS và DFS bằng cách tăng dần giới hạn độ sâu.
- **UCS** phù hợp khi cần tối ưu theo chi phí đường đi.

---

### 5.2. Tìm kiếm có thông tin

Nhóm này sử dụng heuristic để ưu tiên trạng thái có triển vọng tốt hơn. Trong bài toán robot hút bụi, heuristic dựa trên khoảng cách Manhattan đến ô rác gần nhất và số ô rác còn lại.

- **Hàm g(n)**: Chi phí thực tế từ trạng thái bắt đầu đến trạng thái hiện tại. (Số bước di chuyển).
- **Hàm h(n)**: Ước lượng chi phí từ trạng thái hiện tại đến trạng thái kết thúc (heuristic). (Khoảng cách Manhattan đến ô rác gần nhất + Số ô rác còn lại)
- **Hàm f(n) = g(n) + h(n)**: Ước lượng tổng chi phí từ trạng thái bắt đầu đến trạng thái kết thúc.

**Các thuật toán:**

- Greedy Search (chỉ dùng h(n))
- A* (dùng f(n))
- IDA* (dùng f(n) theo giới hạn độ sâu)

#### GIF minh họa

| Thuật toán | GIF |
|---|---|
| Greedy Search | <img src="DuAnCaNhan/project/assets/gif/2/greedy.gif" width="760" alt="Greedy Search"> |
| A* | <img src="DuAnCaNhan/project/assets/gif/2/a_star.gif" width="760" alt="A star"> |
| IDA* | <img src="DuAnCaNhan/project/assets/gif/2/ida_star.gif" width="760" alt="IDA star"> |

#### So sánh thuật toán

| Thời gian | Số node đã xét |
|---|---|
| <img src="DuAnCaNhan/project/assets/images/2/2_time.png" width="500" alt="Informed time"> | <img src="DuAnCaNhan/project/assets/images/2/2_node.png" width="500" alt="Informed nodes"> |

| Bộ nhớ | Độ dài đường đi |
|---|---|
| <img src="DuAnCaNhan/project/assets/images/2/2_mem.png" width="500" alt="Informed memory"> | <img src="DuAnCaNhan/project/assets/images/2/2_length.png" width="500" alt="Informed path length"> |

**Nhận xét:**

- **Greedy Search** chạy nhanh vì chỉ ưu tiên heuristic, nhưng không luôn đảm bảo đường đi tối ưu.
- **A*** kết hợp chi phí đã đi và heuristic nên thường cho lời giải tốt hơn.
- **IDA*** tiết kiệm bộ nhớ hơn A* nhờ tìm kiếm theo ngưỡng chi phí.

---

### 5.3. Tìm kiếm cục bộ

Nhóm này cải thiện trạng thái hiện tại theo heuristic thay vì mở rộng toàn bộ cây tìm kiếm. Cách tiếp cận này phù hợp để quan sát quá trình chọn trạng thái lân cận tốt hơn.

**Các thuật toán:**

- Simple Hill Climbing
- Steepest-Ascent Hill Climbing
- Stochastic Hill Climbing
- Random-Restart Hill Climbing
- Simulated Annealing
- Local Beam Search

#### GIF minh họa

| Thuật toán | GIF |
|---|---|
| Simple Hill Climbing | <img src="DuAnCaNhan/project/assets/gif/3/simple.gif" width="760" alt="Simple Hill Climbing"> |
| Steepest-Ascent Hill Climbing | <img src="DuAnCaNhan/project/assets/gif/3/steepes.gif" width="760" alt="Steepest Hill Climbing"> |
| Stochastic Hill Climbing | <img src="DuAnCaNhan/project/assets/gif/3/stochastic.gif" width="760" alt="Stochastic Hill Climbing"> |
| Random-Restart Hill Climbing | <img src="DuAnCaNhan/project/assets/gif/3/random_restart.gif" width="760" alt="Random Restart Hill Climbing"> |
| Simulated Annealing | <img src="DuAnCaNhan/project/assets/gif/3/simulated.gif" width="760" alt="Simulated Annealing"> |
| Local Beam Search | <img src="DuAnCaNhan/project/assets/gif/3/local_beam.gif" width="760" alt="Local Beam Search"> |

#### So sánh thuật toán

| Thời gian | Số node đã xét |
|---|---|
| <img src="DuAnCaNhan/project/assets/images/3/3_time.png" width="500" alt="Local search time"> | <img src="DuAnCaNhan/project/assets/images/3/3_node.png" width="500" alt="Local search nodes"> |

| Bộ nhớ | Độ dài đường đi |
|---|---|
| <img src="DuAnCaNhan/project/assets/images/3/3_mem.png" width="500" alt="Local search memory"> | <img src="DuAnCaNhan/project/assets/images/3/3_length.png" width="500" alt="Local search path length"> |

**Nhận xét:**

- **Hill Climbing** dễ quan sát và chạy nhanh, nhưng có thể kẹt ở cực trị cục bộ.
- **Random-Restart** giảm nguy cơ kẹt bằng cách thử nhiều điểm xuất phát.
- **Simulated Annealing** có thể chấp nhận bước đi xấu trong một số thời điểm để thoát cực trị cục bộ.
- **Local Beam Search** theo dõi nhiều trạng thái cùng lúc nên có khả năng tìm lời giải tốt hơn so với chỉ giữ một trạng thái.

---

### 5.4. Tìm kiếm trong môi trường phức tạp

Nhóm này mô phỏng trường hợp agent không biết đầy đủ trạng thái môi trường. Chương trình sử dụng nhiều trường hợp giả định để biểu diễn belief state.

- **Không gian niềm tin:** Là tập hợp các trạng thái có thể xảy ra.
- **Trạng thái ban đầu:** Là tập hợp các trạng thái vật lý mà tác nhân cho là có thể xảy ra ban đầu. Thông thường là toàn bộ không gian trạng thái( trong project chỉ mô phỏng 3 state)
- **Trạng thái kết thúc:** tất cả ô rác đã được dọn sạch.
- **Hành động:** di chuyển lên, xuống, trái, phải nếu hợp lệ.
- **Quan sát:** robot chỉ biết trạng thái ô nó đang đứng
- **Mô hình:** Vì không biết chính xác mình đang ở trạng thái nào, tác nhân phải xét tập hợp tất cả các trạng thái có thể đạt được sau khi thực hiện hành động

**Các thuật toán:**

- Unobservable Search
- Partial-Observation Search
- AND-OR Graph Search

#### GIF minh họa

| Thuật toán | GIF |
|---|---|
| Unobservable Search | <img src="DuAnCaNhan/project/assets/gif/4/unobservable.gif" width="760" alt="Unobservable Search"> |
| Partial-Observation Search | <img src="DuAnCaNhan/project/assets/gif/4/partial.gif" width="760" alt="Partial Observation Search"> |
| AND-OR Graph Search | <img src="DuAnCaNhan/project/assets/gif/4/and_or.gif" width="760" alt="AND-OR Graph Search"> |

#### So sánh thuật toán

| Thời gian | Số node đã xét |
|---|---|
| <img src="DuAnCaNhan/project/assets/images/4/4_time.png" width="500" alt="Complex environment time"> | <img src="DuAnCaNhan/project/assets/images/4/4_node.png" width="500" alt="Complex environment nodes"> |

| Bộ nhớ | Độ dài đường đi |
|---|---|
| <img src="DuAnCaNhan/project/assets/images/4/4_mem.png" width="500" alt="Complex environment memory"> | <img src="DuAnCaNhan/project/assets/images/4/4_length.png" width="500" alt="Complex environment path length"> |


**Nhận xét:**

- **Unobservable Search** phù hợp khi agent không có quan sát trực tiếp nên phải xét nhiều trạng thái khả dĩ.
- **Partial-Observation Search** hiệu quả hơn khi agent biết trước một phần môi trường.
- **AND-OR Graph Search** phù hợp với bài toán có nhánh kết quả hoặc điều kiện khác nhau sau mỗi hành động.

---

### 5.5. Bài toán ràng buộc CSP

Nhóm CSP được minh họa bằng bài toán **tô màu bản đồ TP.HCM**. Mục tiêu là gán màu cho các vùng sao cho hai vùng kề nhau không trùng màu.

**Các thuật toán:**

- Backtracking
- Forward Checking
- AC-3
- Min-Conflicts

**Thành phần bài toán:**

- **Biến**: các vùng trên bản đồ TP.HCM.
- **Miền giá trị**: tập màu có thể gán.
- **Ràng buộc**: hai vùng liền kề không được cùng màu.
- **Lời giải**: một phép gán màu hợp lệ cho toàn bộ bản đồ.

#### GIF minh họa

| Thuật toán | GIF |
|---|---|
| Backtracking | <img src="DuAnCaNhan/project/assets/gif/5/backtracking.gif" width="760" alt="Backtracking"> |
| Forward Checking | <img src="DuAnCaNhan/project/assets/gif/5/forward.gif" width="760" alt="Forward Checking"> |
| AC-3 | <img src="DuAnCaNhan/project/assets/gif/5/ac3.gif" width="760" alt="AC-3"> |
| Min-Conflicts | <img src="DuAnCaNhan/project/assets/gif/5/min.gif" width="760" alt="Min Conflicts"> |

#### So sánh thuật toán

| Thời gian | Số node đã xét |
|---|---|
| <img src="DuAnCaNhan/project/assets/images/5/5_time.png" width="500" alt="CSP time"> | <img src="DuAnCaNhan/project/assets/images/5/5_node.png" width="500" alt="CSP nodes"> |

| Bộ nhớ | Số vùng đã tô |
|---|---|
| <img src="DuAnCaNhan/project/assets/images/5/5_mem.png" width="500" alt="CSP memory"> | <img src="DuAnCaNhan/project/assets/images/5/5_length.png" width="500" alt="CSP assignments"> |

**Nhận xét:**

- **Backtracking** đơn giản, dễ triển khai nhưng có thể phải quay lui nhiều.
- **Forward Checking** cắt giảm sớm các lựa chọn không hợp lệ.
- **AC-3** dùng lan truyền ràng buộc để làm gọn miền giá trị.
- **Min-Conflicts** phù hợp khi cần sửa dần một cấu hình gần đúng.

---

### 5.6. Tìm kiếm đối kháng

Nhóm này được minh họa bằng trò chơi **cờ caro 3x3**. Người chơi có thể chọn X hoặc O, sau đó AI chọn nước đi bằng thuật toán đối kháng.

**Các thuật toán:**

- Minimax
- Alpha-Beta Pruning
- Expectimax

#### GIF minh họa

| Thuật toán | GIF |
|---|---|
| Minimax | <img src="DuAnCaNhan/project/assets/gif/6/minimax.gif" width="760" alt="Minimax"> |
| Alpha-Beta | <img src="DuAnCaNhan/project/assets/gif/6/alpha_beta.gif" width="760" alt="Alpha-Beta"> |
| Expectimax | <img src="DuAnCaNhan/project/assets/gif/6/expectimax.gif" width="760" alt="Expectimax"> |

#### So sánh thuật toán

| Thời gian | Số node đã xét |
|---|---|
| <img src="DuAnCaNhan/project/assets/images/6/6_time.png" width="500" alt="Adversarial time"> | <img src="DuAnCaNhan/project/assets/images/6/6_node.png" width="500" alt="Adversarial nodes"> |

| Bộ nhớ | Số ô còn lại |
|---|---|
| <img src="DuAnCaNhan/project/assets/images/6/6_mem.png" width="500" alt="Adversarial memory"> | <img src="DuAnCaNhan/project/assets/images/6/6_length.png" width="500" alt="Adversarial path length"> |

**Nhận xét:**

- **Minimax** xét toàn bộ cây trò chơi để chọn nước đi tốt nhất.
- **Alpha-Beta** cho cùng logic với Minimax nhưng cắt tỉa các nhánh không cần xét, nhờ đó giảm số node duyệt.
- **Expectimax** phù hợp khi đối thủ hoặc môi trường có yếu tố xác suất, nhưng thường phải xét nhiều khả năng hơn.

---

## 6. Giao diện chương trình

Ứng dụng gồm các vùng chính:

- **Thanh chọn thuật toán** ở phía trên.
- **Vùng mô phỏng** ở giữa, thay đổi theo từng nhóm bài toán.
- **Bảng trạng thái** hiển thị bước chạy, tiến độ và thông tin phụ.
- **Khung log** ghi lại các bước xử lý của thuật toán.
- **Màn hình so sánh** hiển thị bảng kết quả và biểu đồ.

Một số asset chính:

| Robot | Ô sạch | Ô rác | Bản đồ TP.HCM |
|---|---|---|---|
| <img src="DuAnCaNhan/project/assets/robot_vacuum.png" width="140" alt="Robot vacuum"> | <img src="DuAnCaNhan/project/assets/clean_floor.png" width="140" alt="Clean floor"> | <img src="DuAnCaNhan/project/assets/dirty_floor.png" width="140" alt="Dirty floor"> | <img src="DuAnCaNhan/project/assets/hcm_city_map.png" width="220" alt="HCM city map"> |

---

## 7. Kết luận

Dự án đã triển khai và trực quan hóa nhiều nhóm thuật toán AI trên các bài toán khác nhau:

- Tìm kiếm đường đi cho robot hút bụi.
- Tìm kiếm có heuristic.
- Tìm kiếm cục bộ.
- Tìm kiếm trong môi trường thiếu quan sát.
- Bài toán ràng buộc CSP trên bản đồ TP.HCM.
- Tìm kiếm đối kháng trong cờ caro.

Thông qua giao diện Pygame, có thể quan sát cách thuật toán mở rộng trạng thái, chọn bước đi, quay lui, cắt tỉa hoặc ra quyết định. Phần so sánh thuật toán giúp đánh giá rõ hơn sự khác biệt giữa các phương pháp về thời gian, bộ nhớ, số node và chất lượng lời giải.

Học được từ dự án: Hiểu sâu hơn về cách áp dụng các thuật toán AI vào bài toán thực tế, kỹ năng lập trình Python.

Khó khăn: Một số thuật toán rất trừu tượng, khó hiểu nên có thể mô phỏng không đúng ý tưởng

---

## 8. Hướng phát triển

- Cho phép lưu và tải lại kịch bản mô phỏng.
- Mở rộng cờ caro lên kích thước lớn hơn.
- Bổ sung thêm thuật toán học tăng cường cho robot hút bụi.

---

## 9. Tài liệu tham khảo

1. Russell, S., & Norvig, P. (2016). Artificial Intelligence: A Modern Approach (3rd ed.). Pearson.
2. Scaler Topics. (n.d.). Artificial Intelligence Tutorial. Retrieved from https://www.scaler.com/topics/artificial-intelligence-tutorial
3. Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow (3rd edition) - Aurélien Géron.
4. Python Programming and Numerical Methods, A Guide for Engineers and Scientists by Qingkai Kong, Timmy Siauw, Alexandre M. Bayen, https://www.taylorfrancis.com/books/mono/10.1201/9780203302297
5. Deep Reinforcement Learning Hands-On by Maxim Lapan, https://www.oreilly.com/library/view/deep-reinforcement-learning-hands-on/9781617296864/
6. Russell, S., & Norvig, P. (2020). Artificial Intelligence: A Modern Approach (3rd ed.). Pearson.

---

## Tác giả

#### Tác giả

**Ninh Nguyễn Minh Tuyên**

MSSV: `24110372`

**Môn học** `Trí tuệ nhân tạo`

**Giáo viên hướng dẫn** `Phan Thị Huyền Trang`
