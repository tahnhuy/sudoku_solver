# Sudoku Solver

## 1. Mục tiêu
- Xây dựng một ứng dụng giải Sudoku sử dụng nhiều thuật toán tìm kiếm khác nhau
- So sánh hiệu suất của các thuật toán khi áp dụng vào bài toán Sudoku
- Tạo giao diện trực quan để người dùng có thể tương tác và theo dõi quá trình giải

## 2. Nội dung

### 2.1. Các thuật toán Tìm kiếm không có thông tin

#### Thành phần chính của bài toán tìm kiếm:
- **Trạng thái (State)**: Ma trận 9x9 đại diện cho bảng Sudoku
- **Hành động (Action)**: Điền một số từ 1-9 vào ô trống
- **Hàm chuyển trạng thái**: Cập nhật bảng Sudoku sau khi điền số
- **Trạng thái đích**: Bảng Sudoku được điền đầy đủ và hợp lệ
- **Chi phí**: Số bước đi để đạt được trạng thái đích

#### Các thuật toán đã triển khai:
1. **Depth-First Search (DFS)**
   - Giải pháp: Sử dụng đệ quy để thử các giá trị có thể cho từng ô trống
   - Độ phức tạp: O(b^d) với b là số nhánh và d là độ sâu
   - [GIF minh họa]

2. **Breadth-First Search (BFS)**
   - Giải pháp: Duyệt theo từng mức độ sâu, thử tất cả các khả năng ở mỗi mức
   - Độ phức tạp: O(b^d)
   - [GIF minh họa]

3. **Uniform Cost Search (UCS)**
   - Giải pháp: Tương tự BFS nhưng ưu tiên các đường đi có chi phí thấp
   - Độ phức tạp: O(b^(1 + floor(C/ε)))
   - [GIF minh họa]

4. **Iterative Deepening Search (IDS)**
   - Giải pháp: Kết hợp DFS và BFS, tăng dần độ sâu tìm kiếm
   - Độ phức tạp: O(b^d)
   - [GIF minh họa]

#### So sánh hiệu suất:
[Biểu đồ so sánh thời gian và số bước của các thuật toán]

#### Nhận xét:
- DFS thường nhanh hơn trong các trường hợp có nhiều giải pháp
- BFS đảm bảo tìm được giải pháp tối ưu nhưng tốn nhiều bộ nhớ
- IDS cân bằng giữa hiệu suất và bộ nhớ
- UCS không hiệu quả bằng các thuật toán khác trong bài toán Sudoku

### 2.2. Các thuật toán Tìm kiếm có thông tin

#### Thành phần chính:
- **Hàm heuristic**: Đếm số ô trống còn lại hoặc số xung đột trên bảng
- **Hàm đánh giá**: f(n) = g(n) + h(n) với g(n) là chi phí từ trạng thái ban đầu đến n, h(n) là giá trị heuristic

#### Các thuật toán đã triển khai:
1. **A* Search**
   - Giải pháp: Sử dụng hàm heuristic để hướng dẫn tìm kiếm
   - Độ phức tạp: O(b^d)
   - [GIF minh họa]

2. **Best-First Search**
   - Giải pháp: Chỉ dựa vào hàm heuristic để chọn trạng thái tiếp theo
   - Độ phức tạp: O(b^d)
   - [GIF minh họa]

3. **IDA* Search**
   - Giải pháp: Kết hợp A* với tìm kiếm theo độ sâu tăng dần
   - Độ phức tạp: O(b^d)
   - [GIF minh họa]

#### So sánh hiệu suất:
[Biểu đồ so sánh thời gian và số bước của các thuật toán]

#### Nhận xét:
- A* thường hiệu quả nhất trong nhóm này
- Best-First Search có thể bị mắc kẹt ở cực tiểu địa phương
- IDA* cân bằng giữa hiệu suất và bộ nhớ

### 2.3. Các thuật toán Tìm kiếm cục bộ

#### Các thuật toán đã triển khai:
1. **Simple Hill Climbing**
2. **Steepest-Ascent Hill Climbing**
3. **Stochastic Hill Climbing**
4. **Simulated Annealing**
5. **Local Beam Search**
6. **Genetic Algorithm**

[Chi tiết và so sánh hiệu suất cho từng thuật toán]

### 2.4. Các thuật toán Tìm kiếm trong môi trường phức tạp

#### Các thuật toán đã triển khai:
1. **AND-OR Graph Search**
2. **Partial Observation Search**

[Chi tiết và so sánh hiệu suất cho từng thuật toán]

### 2.5. Các thuật toán Thỏa mãn ràng buộc

#### Các thuật toán đã triển khai:
1. **AC-3**
2. **Forward Checking**
3. **Backtracking**

[Chi tiết và so sánh hiệu suất cho từng thuật toán]

### 2.6. Các thuật toán Học tăng cường

#### Các thuật toán đã triển khai:
1. **Q-Learning**

[Chi tiết và so sánh hiệu suất]

## 3. Kết luận

### Kết quả đạt được:
1. Đã triển khai thành công 20+ thuật toán tìm kiếm khác nhau
2. Xây dựng được giao diện trực quan cho người dùng
3. Có khả năng so sánh hiệu suất giữa các thuật toán
4. Hỗ trợ nhiều mức độ khó khác nhau của Sudoku
5. Có khả năng xuất kết quả và báo cáo phân tích

### Hướng phát triển:
1. Tối ưu hóa các thuật toán hiện có
2. Thêm các thuật toán mới
3. Cải thiện giao diện người dùng
4. Thêm tính năng lưu/tải game
5. Mở rộng sang các biến thể của Sudoku 