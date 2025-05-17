# Sudoku Solver

## 1. Mục tiêu
- Xây dựng một ứng dụng giải trò chơi Sudoku sử dụng nhiều thuật toán tìm kiếm thuộc nhiều nhóm khác nhau (gồm Uninformed Search, Informed Search, Local Search, Complex Environment Search, Constraint Satisfaction Problem, Reinforcement Learning)
- So sánh hiệu suất của các thuật toán khi áp dụng vào bài toán Sudoku
- Thiết kế giao diện thân thiện và trực quan với người dùng để có thể tương tác với ứng dụng một cách hiệu quả

## 2. Nội dung

### 2.1. Các thuật toán Tìm kiếm không có thông tin (Uninformed Search Algorithm)

#### Thành phần chính của bài toán tìm kiếm:
- **Trạng thái (State)**: Ma trận 9x9 (được lưu bằng ma trận 2 chiều numpy) đại diện cho bảng Sudoku, với các ô trống được đánh dấu bằng số 0
- **Trạng thái đầu vào**: Bảng Sudoku ban đầu chứa một số ô đã được điền sẵn (phụ thuộc vào độ khó)
- **Trạng thái đích**: Bảng Sudoku đã được điền đầy đủ số từ 1-9, thỏa mãn các ràng buộc: không trùng số trên cùng hàng, cùng cột và cùng ô vuông 3x3
- **Hành động (Action)**: Điền một số từ 1-9 vào ô trống được chọn
- **Hàm chuyển trạng thái**: Cập nhật bảng Sudoku sau khi điền giá trị vào ô trống
- **Chi phí**: Mỗi bước đặt số vào một ô trống có chi phí bằng 1

#### Các thuật toán đã triển khai:
1. **Depth-First Search (DFS)**
   - **Trạng thái đầu vào**: Bảng Sudoku ban đầu chứa các ô đã được điền sẵn
   - **Trạng thái đích**: Bảng Sudoku hoàn chỉnh không vi phạm ràng buộc
   - **Quá trình**: 
     - Sử dụng stack để lưu các trạng thái theo nguyên tắc LIFO (Last In First Out)
     - Tìm ô trống đầu tiên và thử lần lượt các giá trị 1-9
     - Với mỗi giá trị hợp lệ, tạo trạng thái mới và đẩy vào stack
     - Lấy ra trạng thái từ đỉnh stack và tiếp tục quá trình cho đến khi tìm được lời giải hoặc hết stack
     - Nếu không tìm được lời giải từ trạng thái hiện tại, thuật toán quay lui và thử giá trị khác
   - **Độ phức tạp**: O(b^d) với b là số nhánh (tối đa 9 giá trị mỗi ô) và d là độ sâu (số ô trống cần điền)
     
   ![Recording2025-05-12115909-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/395131f4-8f0c-409a-bb18-87cd6fccc568)

2. **Breadth-First Search (BFS)**
   - **Trạng thái đầu vào**: Bảng Sudoku ban đầu chứa các ô đã được điền sẵn
   - **Trạng thái đích**: Bảng Sudoku hoàn chỉnh không vi phạm ràng buộc
   - **Quá trình**:
     - Sử dụng queue (deque) để lưu các trạng thái theo nguyên tắc FIFO (First In First Out)
     - Tìm ô trống đầu tiên và thử lần lượt các giá trị 1-9
     - Với mỗi giá trị hợp lệ, tạo trạng thái mới và đẩy vào cuối queue
     - Lấy ra trạng thái từ đầu queue và tiếp tục quá trình
     - Thuật toán đảm bảo tìm được lời giải tối ưu (sử dụng ít bước nhất) nếu tồn tại
   - **Độ phức tạp**: O(b^d)

   ![BFS](https://github.com/user-attachments/assets/cd3d84dd-8eb6-469c-b418-2f2cd6e9cd20)

3. **Uniform Cost Search (UCS)**
   - **Trạng thái đầu vào**: Bảng Sudoku ban đầu chứa các ô đã được điền sẵn
   - **Trạng thái đích**: Bảng Sudoku hoàn chỉnh không vi phạm ràng buộc
   - **Quá trình**:
     - Sử dụng hàng đợi ưu tiên (priority queue) để lấy ra trạng thái có chi phí tích lũy thấp nhất
     - Trong bài toán Sudoku, chi phí mỗi bước đều bằng 1, nên kết quả tương đương với BFS
     - Các trạng thái được sắp xếp theo chi phí tích lũy từ trạng thái ban đầu
     - Thuật toán chạy đến khi tìm được lời giải, TIMEOUT hoặc hàng đợi hết phần tử
   - **Độ phức tạp**: O(b^(1 + floor(C/ε))) với b là số bậc, C là chi phí tổng và ε là chi phí nhỏ nhất cho 1 hành động

   ![UCS](https://github.com/user-attachments/assets/95028c47-025a-4a55-ba2f-f998b9a77c35)

4. **Iterative Deepening Search (IDS)**
   - **Trạng thái đầu vào**: Bảng Sudoku ban đầu chứa các ô đã được điền sẵn
   - **Trạng thái đích**: Bảng Sudoku hoàn chỉnh không vi phạm ràng buộc
   - **Quá trình**:
     - Kết hợp DFS và BFS, bắt đầu với độ sâu giới hạn là 1
     - Thực hiện DFS với giới hạn độ sâu hiện tại
     - Nếu không tìm được lời giải, tăng độ sâu giới hạn lên 1 và thực hiện lại
     - Lặp lại quá trình cho đến khi tìm được lời giải hoặc đạt giới hạn độ sâu tối đa
     - Thuật toán kết hợp ưu điểm của cả DFS (tiết kiệm bộ nhớ) và BFS (tìm được lời giải tối ưu)
   - **Độ phức tạp**: O(b^d)

   ![IDS](https://github.com/user-attachments/assets/7f2f9a8d-eae2-46bc-92f9-9935e012ae4a)

#### Nhận xét:
- DFS thường nhanh hơn trong các trường hợp có nhiều giải pháp và khi cần tìm một lời giải bất kỳ
- BFS đảm bảo tìm được giải pháp tối ưu nhưng tốn nhiều bộ nhớ, khó áp dụng cho bảng Sudoku khó
- IDS cân bằng giữa hiệu suất và bộ nhớ, thích hợp cho bài toán có không gian trạng thái lớn
- UCS không hiệu quả bằng các thuật toán khác trong bài toán Sudoku vì mọi bước có chi phí bằng nhau

### 2.2. Các thuật toán Tìm kiếm có thông tin (Informed Search Algorithm)

#### Thành phần chính:
- **Hàm heuristic**: Được tính dựa trên số ô còn trống trong bảng Sudoku (h(n) = số ô trống)
- **Hàm đánh giá**: f(n) = g(n) + h(n) 
  - g(n): chi phí từ trạng thái ban đầu đến trạng thái n (số bước đã thực hiện)
  - h(n): ước lượng chi phí từ trạng thái n đến trạng thái đích

#### Các thuật toán đã triển khai:
1. **A* Search**
   - **Trạng thái đầu vào**: Bảng Sudoku ban đầu chứa các ô đã được điền sẵn
   - **Trạng thái đích**: Bảng Sudoku hoàn chỉnh không vi phạm ràng buộc
   - **Quá trình**: 
     - Sử dụng hàng đợi ưu tiên (Priority Queue) để quản lý các trạng thái
     - Trạng thái có giá trị f(n) = g(n) + h(n) nhỏ nhất được chọn trước
     - g(n) là số bước đã thực hiện, tăng 1 mỗi khi điền một ô trống
     - h(n) là số ô còn trống trên bảng Sudoku
     - Trạng thái được lấy ra khỏi hàng đợi, sinh ra các trạng thái kế tiếp bằng cách thử các giá trị hợp lệ
     - Thuật toán chạy cho đến khi tìm được lời giải, hết thời gian hoặc hàng đợi trống
   - **Độ phức tạp**: O(b^d)

   ![A-star](https://github.com/user-attachments/assets/05a3b441-353e-4950-9c05-9a15acbff823)

2. **Greed Search (Best-First Search)**
   - **Trạng thái đầu vào**: Bảng Sudoku ban đầu chứa các ô đã được điền sẵn
   - **Trạng thái đích**: Bảng Sudoku hoàn chỉnh không vi phạm ràng buộc
   - **Quá trình**:
     - Tương tự A*, nhưng chỉ xét hàm heuristic h(n) mà không quan tâm đến chi phí đã đi g(n)
     - Sử dụng hàng đợi ưu tiên, chọn trạng thái có h(n) nhỏ nhất (ít ô trống nhất)
     - Thử điền các giá trị hợp lệ vào ô trống và cập nhật hàng đợi
     - Thuật toán tập trung vào việc giảm nhanh số ô trống mà không đảm bảo tối ưu về số bước
   - **Độ phức tạp**: O(b^d)

   ![GreedySearch](https://github.com/user-attachments/assets/1e96d9ac-15f5-4930-ba8b-15a9f8aef5dd)

3. **IDA* Search**
   - **Trạng thái đầu vào**: Bảng Sudoku ban đầu chứa các ô đã được điền sẵn
   - **Trạng thái đích**: Bảng Sudoku hoàn chỉnh không vi phạm ràng buộc
   - **Quá trình**:
     - Kết hợp A* với Iterative Deepening để tiết kiệm bộ nhớ
     - Bắt đầu với ngưỡng giới hạn f(n) = h(n) ban đầu
     - Thực hiện tìm kiếm DFS với điều kiện f(n) ≤ ngưỡng hiện tại
     - Nếu không tìm được lời giải, cập nhật ngưỡng bằng giá trị f(n) nhỏ nhất vượt quá ngưỡng cũ
     - Lặp lại quá trình cho đến khi tìm được lời giải hoặc ngưỡng vượt quá giới hạn
     - Thuật toán kết hợp ưu điểm của A* (đánh giá hướng đi tốt) và DFS (tiết kiệm bộ nhớ)
   - **Độ phức tạp**: O(b^d)

   ![IDA-Star](https://github.com/user-attachments/assets/d867d9ca-5072-4b30-8945-812e88e7c6b6)
   
#### Nhận xét:
- A* thường hiệu quả nhất trong nhóm này nhờ cân bằng giữa chi phí đã đi và ước lượng còn lại
- Greedy Search có thể nhanh hơn nhưng không đảm bảo tìm được giải pháp tối ưu, dễ rơi vào tình huống không tìm được lời giải
- IDA* cân bằng giữa hiệu suất và bộ nhớ, phù hợp với bài toán có không gian trạng thái lớn như Sudoku khó

### 2.3. Các thuật toán Tìm kiếm cục bộ (Local Search Algorithm)

#### Thành phần chính:
- **Trạng thái**: Ma trận 9x9 đại diện cho bảng Sudoku
- **Hàm đánh giá**: Đánh giá chất lượng của trạng thái dựa trên số ô đã điền và số xung đột (số vi phạm ràng buộc)
- **Hàng xóm (Neighbors)**: Các trạng thái có thể đạt được bằng cách thay đổi giá trị của một ô trống

#### Các thuật toán đã triển khai:
1. **Simple Hill Climbing**
   - **Trạng thái đầu vào**: Bảng Sudoku ban đầu với các ô đã được điền sẵn
   - **Trạng thái đích**: Bảng Sudoku hoàn chỉnh không vi phạm ràng buộc
   - **Quá trình**:
     - Bắt đầu từ trạng thái hiện tại, tìm ô trống đầu tiên
     - Thử lần lượt các giá trị từ 1-9 cho ô đó
     - Khi tìm thấy giá trị đầu tiên cải thiện trạng thái (giảm số ô trống, không tạo thêm xung đột), chọn trạng thái đó làm trạng thái hiện tại
     - Lặp lại quá trình cho đến khi không thể cải thiện thêm hoặc tìm được lời giải
     - Thuật toán dễ bị mắc kẹt ở cực đại địa phương (local maximum)
   - **Độ phức tạp**: O(n) với n là số ô trống

   ![Simplehill](https://github.com/user-attachments/assets/09ccb9cc-02e3-4bb3-bbb2-12ef331fe205)

2. **Steepest-Ascent Hill Climbing**
   - **Trạng thái đầu vào**: Bảng Sudoku ban đầu với các ô đã được điền sẵn
   - **Trạng thái đích**: Bảng Sudoku hoàn chỉnh không vi phạm ràng buộc
   - **Quá trình**:
     - Bắt đầu từ trạng thái hiện tại, tìm tất cả các ô trống
     - Với mỗi ô trống, thử tất cả các giá trị hợp lệ từ 1-9
     - Đánh giá tất cả các trạng thái con có thể và chọn trạng thái tốt nhất (giảm nhiều nhất số ô trống và xung đột)
     - Nếu không tìm được trạng thái tốt hơn, thuật toán kết thúc
     - Nếu có, chuyển sang trạng thái tốt nhất và lặp lại quá trình
   - **Độ phức tạp**: O(n)

   ![Steepest hill](https://github.com/user-attachments/assets/5de3c8ab-7557-4c47-a34d-cffdcc1ce852)

3. **Stochastic Hill Climbing**
   - **Trạng thái đầu vào**: Bảng Sudoku ban đầu với các ô đã được điền sẵn
   - **Trạng thái đích**: Bảng Sudoku hoàn chỉnh không vi phạm ràng buộc
   - **Quá trình**:
     - Tương tự Simple Hill Climbing, nhưng thay vì chọn giá trị đầu tiên cải thiện trạng thái, thuật toán chọn ngẫu nhiên một trong các giá trị cải thiện
     - Tìm tất cả các giá trị hợp lệ cho ô trống đầu tiên
     - Đánh giá các trạng thái sau khi điền giá trị
     - Chọn ngẫu nhiên một trạng thái trong số các trạng thái tốt hơn trạng thái hiện tại
     - Yếu tố ngẫu nhiên giúp thuật toán có khả năng thoát khỏi cực đại địa phương
   - **Độ phức tạp**: O(n)

   ![stochastichill](https://github.com/user-attachments/assets/29dc8d2a-6647-49e7-b355-36a796919799)

4. **Simulated Annealing**
   - **Trạng thái đầu vào**: Bảng Sudoku ban đầu với các ô đã được điền sẵn
   - **Trạng thái đích**: Bảng Sudoku hoàn chỉnh không vi phạm ràng buộc
   - **Quá trình**:
     - Bắt đầu với nhiệt độ T cao và trạng thái hiện tại
     - Tìm ngẫu nhiên một ô trống và thử điền một giá trị ngẫu nhiên hợp lệ
     - Tính toán sự thay đổi chi phí ΔE giữa trạng thái mới và trạng thái hiện tại
     - Nếu ΔE < 0 (trạng thái mới tốt hơn), luôn chấp nhận trạng thái mới
     - Nếu ΔE > 0 (trạng thái mới kém hơn), vẫn có thể chấp nhận với xác suất e^(-ΔE/T)
     - Giảm dần nhiệt độ T theo lịch làm nguội (cooling schedule)
     - Lặp lại quá trình cho đến khi T gần 0 hoặc tìm được lời giải
     - Khả năng chấp nhận trạng thái tệ hơn giúp thoát khỏi cực đại địa phương hiệu quả
   - **Độ phức tạp**: O(n)

   ![simulatedannealing](https://github.com/user-attachments/assets/90eebe43-24e7-420b-a249-38f240e12cfb)

5. **Local Beam Search**
   - **Trạng thái đầu vào**: Bảng Sudoku ban đầu với các ô đã được điền sẵn
   - **Trạng thái đích**: Bảng Sudoku hoàn chỉnh không vi phạm ràng buộc
   - **Quá trình**:
     - Thay vì chỉ duy trì một trạng thái hiện tại, thuật toán duy trì k trạng thái tốt nhất
     - Bắt đầu từ trạng thái ban đầu, sinh ra các trạng thái con bằng cách thử các giá trị cho các ô trống
     - Đánh giá tất cả các trạng thái con và chọn k trạng thái tốt nhất
     - Lặp lại quá trình với k trạng thái được chọn
     - Thuật toán kết hợp các ưu điểm của Hill Climbing và Breadth-First Search
   - **Độ phức tạp**: O(k*n) với k là số trạng thái được duy trì

   ![localbeam](https://github.com/user-attachments/assets/c8bc18ee-c893-4a73-8953-0dae130acb8c)

6. **Genetic Algorithm**
   - **Trạng thái đầu vào**: Bảng Sudoku ban đầu với các ô đã được điền sẵn
   - **Trạng thái đích**: Bảng Sudoku hoàn chỉnh không vi phạm ràng buộc
   - **Quá trình**:
     - Tạo quần thể ban đầu gồm nhiều cá thể (mỗi cá thể là một bảng Sudoku với các ô trống được điền ngẫu nhiên)
     - Đánh giá độ thích nghi (fitness) của mỗi cá thể dựa trên số xung đột
     - Chọn lọc các cá thể có độ thích nghi cao để làm cha mẹ
     - Lai ghép (crossover): Tạo cá thể con bằng cách kết hợp gen từ hai cá thể cha mẹ
     - Đột biến (mutation): Thay đổi ngẫu nhiên giá trị của một số ô trong cá thể con
     - Tạo thế hệ mới từ cá thể con và cá thể tốt từ thế hệ trước
     - Lặp lại quá trình cho đến khi tìm được lời giải hoặc đạt số thế hệ tối đa
   - **Độ phức tạp**: O(p*n*g) với p là kích thước quần thể, n là số ô trống, g là số thế hệ

   ![GA](https://github.com/user-attachments/assets/de168436-21ad-43d0-ad46-37bc35affbd6)

#### Nhận xét:
- Simple Hill Climbing đơn giản nhưng dễ bị mắc kẹt ở cực đại địa phương
- Steepest-Ascent Hill Climbing đòi hỏi nhiều tính toán hơn nhưng có thể tìm được lời giải tốt hơn
- Stochastic Hill Climbing giới thiệu yếu tố ngẫu nhiên để tránh cực đại địa phương
- Simulated Annealing có khả năng thoát khỏi cực đại địa phương tốt nhất trong các thuật toán Hill Climbing
- Local Beam Search và Genetic Algorithm phù hợp cho không gian tìm kiếm lớn và phức tạp

### 2.4. Các thuật toán Tìm kiếm trong môi trường phức tạp (Complex Environment Search)

#### Thành phần chính:
- **Trạng thái**: Ma trận 9x9 đại diện cho bảng Sudoku
- **Môi trường không xác định**: Một số thông tin về trạng thái có thể bị thiếu hoặc không chắc chắn
- **Quan sát (Observation)**: Thông tin nhận được từ môi trường, có thể không đầy đủ

#### Các thuật toán đã triển khai:
1. **AND-OR Graph Search**
   - **Trạng thái đầu vào**: Bảng Sudoku ban đầu chứa các ô đã được điền sẵn
   - **Trạng thái đích**: Bảng Sudoku hoàn chỉnh không vi phạm ràng buộc
   - **Quá trình**:
     - Áp dụng đệ quy xen kẽ giữa OR-Search và AND-Search
     - OR-Search: Tìm một hành động khả thi (điền giá trị) cho một ô trống
     - AND-Search: Tìm lời giải cho tất cả các ô trống còn lại sau khi đã áp dụng hành động
     - Xây dựng cây tìm kiếm AND-OR thay vì cây tìm kiếm thông thường
     - OR-nodes: Các trạng thái cần chọn một hành động để tiến tới trạng thái tiếp theo
     - AND-nodes: Tập hợp các trạng thái cần được giải tất cả
     - Thuật toán xử lý hiệu quả với các trạng thái không xác định (cần xử lý nhiều khả năng)
   - **Độ phức tạp**: O(b^d)

   ![AndOr](https://github.com/user-attachments/assets/5a48adb4-b2e4-4e0e-b626-a027525e7334)

2. **Partial Observation Search**
   - **Trạng thái đầu vào**: Bảng Sudoku ban đầu, nhưng một số ô (hoặc thông tin về ràng buộc) có thể không được quan sát đầy đủ
   - **Trạng thái đích**: Bảng Sudoku hoàn chỉnh không vi phạm ràng buộc
   - **Quá trình**:
     - Duy trì một tập hợp các niềm tin (belief states) về trạng thái thực sự của bảng Sudoku
     - Mỗi niềm tin là một phân phối xác suất trên các trạng thái có thể
     - Thực hiện hành động (điền giá trị) dựa trên niềm tin hiện tại
     - Sau mỗi hành động, nhận quan sát mới từ môi trường
     - Cập nhật niềm tin dựa trên hành động và quan sát theo công thức Bayes
     - Chọn hành động tiếp theo dựa trên niềm tin đã cập nhật
     - Thuật toán phù hợp cho các tình huống có thông tin không chắc chắn hoặc thiếu
   - **Độ phức tạp**: O(|S|^2 * |O|) với S là không gian trạng thái, O là không gian quan sát

   ![Partialobservation](https://github.com/user-attachments/assets/68527d97-dada-4168-b642-0f4406c8cfec)

#### Nhận xét:
- AND-OR Graph Search hiệu quả cho các bài toán có cấu trúc phân tách được thành các phần con độc lập
- Partial Observation Search phù hợp với các tình huống thông tin không đầy đủ, nhưng có yêu cầu tính toán cao
- Các thuật toán này phức tạp hơn nhưng mạnh mẽ trong các tình huống thực tế khi thông tin không hoàn hảo

### 2.5. Các thuật toán Thỏa mãn ràng buộc (Constraint Satisfaction Problem)

#### Thành phần chính:
- **Biến (Variables)**: 81 ô của bảng Sudoku (vị trí hàng, cột)
- **Miền giá trị (Domain)**: Tập các giá trị {1, 2, 3, 4, 5, 6, 7, 8, 9} cho mỗi ô trống
- **Ràng buộc (Constraints)**: 
  - Mỗi hàng chỉ chứa mỗi số một lần duy nhất
  - Mỗi cột chỉ chứa mỗi số một lần duy nhất
  - Mỗi ô vuông 3x3 chỉ chứa mỗi số một lần duy nhất

#### Các thuật toán đã triển khai:
1. **AC-3**
   - **Trạng thái đầu vào**: Bảng Sudoku ban đầu với các ô đã được điền sẵn
   - **Trạng thái đích**: Bảng Sudoku với miền giá trị của các biến đã được thu hẹp, hoặc đã được giải hoàn toàn
   - **Quá trình**:
     - Khởi tạo miền giá trị cho các ô trống ({1-9}) và các ô đã điền (giá trị duy nhất)
     - Tạo hàng đợi chứa tất cả các cặp ràng buộc (arcs) giữa các ô theo hàng, cột và khối 3x3
     - Lấy lần lượt từng cặp (Xi, Xj) từ hàng đợi và thực hiện "loại bỏ tính không nhất quán cung" (arc consistency)
     - Nếu miền giá trị của Xi thay đổi, thêm tất cả các cặp (Xk, Xi) vào hàng đợi
     - Quá trình tiếp tục cho đến khi hàng đợi trống (đạt tính nhất quán cung)
     - Khi miền của một biến chỉ còn một giá trị, gán giá trị đó cho biến
     - Thuật toán có thể giải trực tiếp các bảng Sudoku đơn giản, hoặc giảm đáng kể không gian tìm kiếm
   - **Độ phức tạp**: O(n²d³) với n là số biến (81 ô), d là kích thước miền (tối đa 9)

   ![AC3](https://github.com/user-attachments/assets/fdf56a7b-f71c-4639-a902-a3e018ebfbc4)

2. **Forward Checking**
   - **Trạng thái đầu vào**: Bảng Sudoku ban đầu với các ô đã được điền sẵn
   - **Trạng thái đích**: Bảng Sudoku hoàn chỉnh không vi phạm ràng buộc
   - **Quá trình**:
     - Khi một biến (ô) được gán giá trị, kiểm tra tác động đến miền của các biến liên quan (cùng hàng, cột, khối 3x3)
     - Loại bỏ giá trị vừa được gán khỏi miền của các biến liên quan
     - Nếu miền của bất kỳ biến nào trở thành rỗng, hành động gán giá trị thất bại
     - Forward Checking thường kết hợp với Backtracking để tìm lời giải
     - Thuật toán phát hiện sớm các xung đột, cắt bỏ các nhánh tìm kiếm vô ích
   - **Độ phức tạp**: O(d²n)

   ![Forwardchecking](https://github.com/user-attachments/assets/734f785a-fc74-41c9-8b2f-ae73f13ef9e1)

3. **Backtracking**
   - **Trạng thái đầu vào**: Bảng Sudoku ban đầu với các ô đã được điền sẵn
   - **Trạng thái đích**: Bảng Sudoku hoàn chỉnh không vi phạm ràng buộc
   - **Quá trình**:
     - Chọn một biến chưa được gán giá trị (một ô trống)
     - Thử lần lượt các giá trị từ miền của biến đó
     - Với mỗi giá trị, kiểm tra các ràng buộc với các biến đã được gán giá trị trước đó
     - Nếu vi phạm ràng buộc, thử giá trị tiếp theo
     - Nếu tất cả các ràng buộc đều thỏa mãn, tiếp tục đệ quy với biến tiếp theo
     - Nếu tất cả các giá trị đều thất bại, quay lui (backtrack) đến biến trước đó và thử giá trị khác
     - Thuật toán kết thúc khi tất cả các biến đã được gán giá trị hoặc đã thử tất cả các khả năng
     - Trong mã nguồn, thuật toán kết hợp với Forward Checking để tăng hiệu quả
   - **Độ phức tạp**: O(d^n)

   ![backtracking](https://github.com/user-attachments/assets/cc2cd355-2ead-477b-8513-160b4906388c)

#### Nhận xét:
- AC-3 hiệu quả trong việc thu hẹp miền giá trị của các biến, giảm không gian tìm kiếm
- Forward Checking cân bằng giữa tốc độ và khả năng phát hiện xung đột sớm
- Backtracking là nền tảng cho nhiều thuật toán CSP khác, nhưng có thể chậm đối với bài toán lớn
- Kết hợp các thuật toán (như Backtracking + Forward Checking) thường mang lại hiệu quả tốt nhất

### 2.6. Các thuật toán Học tăng cường (Reinforcement Learning)

#### Thành phần chính:
- **Trạng thái (State)**: Ma trận 9x9 đại diện cho bảng Sudoku
- **Hành động (Action)**: Điền một số từ 1-9 vào một ô trống
- **Phần thưởng (Reward)**: Được tính dựa trên số ô đã điền và số vi phạm ràng buộc
- **Chính sách (Policy)**: Quy tắc chọn hành động dựa trên giá trị Q hiện tại

#### Các thuật toán đã triển khai:
1. **Q-Learning**
   - **Trạng thái đầu vào**: Bảng Sudoku ban đầu với các ô đã được điền sẵn
   - **Trạng thái đích**: Bảng Sudoku hoàn chỉnh không vi phạm ràng buộc
   - **Quá trình**:
     - Khởi tạo bảng Q-values với các giá trị bằng 0
     - Tìm ô trống và xác định các hành động hợp lệ (giá trị 1-9 có thể điền)
     - Chọn hành động dựa trên chiến lược epsilon-greedy:
       - Với xác suất epsilon, chọn hành động ngẫu nhiên (khám phá)
       - Với xác suất 1-epsilon, chọn hành động có Q-value cao nhất (khai thác)
     - Thực hiện hành động và quan sát phần thưởng:
       - Phần thưởng dương nếu giảm số ô trống và không tạo thêm xung đột
       - Phần thưởng âm nếu tạo thêm xung đột
     - Cập nhật giá trị Q theo công thức: Q(s,a) ← (1-α)Q(s,a) + α(r + γ max Q(s',a'))
       - α: tốc độ học (learning rate)
       - γ: hệ số chiết khấu (discount factor)
       - r: phần thưởng tức thời
       - max Q(s',a'): giá trị Q tối đa của trạng thái tiếp theo
     - Lặp lại quá trình cho đến khi đạt trạng thái đích hoặc đủ số bước
     - Thuật toán có khả năng cải thiện hiệu suất qua thời gian
   - **Độ phức tạp**: O(n * m) với n là số trạng thái, m là số hành động

   ![Q-learning](https://github.com/user-attachments/assets/f252a065-bb1d-404e-a28d-a27e9ecc5f0c)

#### Nhận xét:
- Q-Learning có khả năng học từ trải nghiệm và cải thiện hiệu suất theo thời gian
- Thuật toán cần thời gian huấn luyện dài để đạt hiệu quả cao, đặc biệt với không gian trạng thái lớn như Sudoku
- Phù hợp cho các bài toán lặp lại nhiều lần, nơi kinh nghiệm có thể được tích lũy
- Kết hợp với các kỹ thuật như function approximation có thể giúp xử lý không gian trạng thái lớn hiệu quả hơn

### 2.7. Bảng so sánh hiệu suất các thuật toán

![Screenshot 2025-05-12 133946](https://github.com/user-attachments/assets/4c839d56-0be3-4a88-9310-e8acae5c8046)

## 3. Kết luận

### Kết quả đạt được:
1. Đã triển khai thành công 19 thuật toán tìm kiếm khác nhau, thuộc 6 nhóm thuật toán phổ biến trong AI
2. Mỗi thuật toán đều được đánh giá dựa trên 3 yếu tố chính:
   - Số bước thực hiện để tìm ra lời giải
   - Thời gian thực thi
   - Độ phức tạp lý thuyết
3. Xây dựng được giao diện thân thiện với người dùng, có thể:
   - Tùy chỉnh độ khó của bảng Sudoku
   - Chọn thuật toán giải
   - Xem quá trình giải từng bước
   - So sánh hiệu suất giữa các thuật toán
4. Hỗ trợ 3 mức độ khó khác nhau của Sudoku (Easy, Medium, Hard)
5. Có khả năng xuất kết quả và báo cáo phân tích ra file Excel để nghiên cứu sâu hơn

### Nhận xét về hiệu suất các thuật toán:
1. **Các thuật toán tìm kiếm không có thông tin**:
   - DFS thường nhanh nhất khi cần tìm một lời giải bất kỳ
   - BFS và IDS đảm bảo tìm được lời giải tối ưu nhưng tiêu tốn nhiều bộ nhớ

2. **Các thuật toán tìm kiếm có thông tin**:
   - A* thường cân bằng tốt giữa thời gian và chất lượng lời giải
   - Greedy Search nhanh nhưng không đảm bảo tối ưu
   - IDA* phù hợp nhất với bài toán Sudoku mức độ khó

3. **Các thuật toán tìm kiếm cục bộ**:
   - Simulated Annealing và Genetic Algorithm hiệu quả nhất trong nhóm này
   - Hill Climbing dễ bị mắc kẹt ở cực đại địa phương
   - Local Beam Search cân bằng tốt giữa khám phá và khai thác

4. **Các thuật toán thỏa mãn ràng buộc**:
   - Backtracking kết hợp với Forward Checking cho hiệu suất tốt nhất
   - AC-3 hiệu quả để tiền xử lý và thu hẹp không gian tìm kiếm

5. **Thuật toán học tăng cường**:
   - Q-Learning cải thiện hiệu suất qua thời gian, nhưng cần nhiều vòng lặp huấn luyện

### Hướng phát triển:
1. Tối ưu hóa các thuật toán hiện có:
   - Cải thiện heuristic cho các thuật toán Informed Search
   - Kết hợp các thuật toán như AC-3 + Backtracking để tăng hiệu suất
   - Tối ưu hóa cấu trúc dữ liệu để giảm thời gian thực thi

2. Thêm các thuật toán mới:
   - Min-Conflicts cho nhóm CSP
   - Monte Carlo Tree Search
   - Deep Reinforcement Learning với Neural Network

3. Cải thiện giao diện người dùng:
   - Thêm chức năng tùy chỉnh thuật toán (tham số, heuristic)
   - Trực quan hóa quá trình giải chi tiết hơn
   - Hỗ trợ lưu và tải bảng Sudoku tùy chỉnh

4. Mở rộng sang các biến thể của Sudoku:
   - Sudoku 16x16
   - Killer Sudoku
   - Irregularly-shaped Sudoku 
