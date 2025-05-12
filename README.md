# Sudoku Solver

## 1. Mục tiêu
- Xây dựng một ứng dụng giải trò chơi Sudoku sử dụng nhiều thuật toán tìm kiếm thuộc nhiều nhóm khác nhau (gồm Uninformed Search, Informed Search, Local Search, Complex Environment Search, Constraint Satisfaction Problem, Reinforcement Learning)
- So sánh hiệu suất của các thuật toán khi áp dụng vào bài toán Sudoku
- Thiết kế giao diện thân thiện và trực quan với người dùng để có thể tương tác với ứng dụng một cách hiệu quả

## 2. Nội dung

### 2.1. Các thuật toán Tìm kiếm không có thông tin (Uninformed Search Algorithm)

#### Thành phần chính của bài toán tìm kiếm:
- **Trạng thái (State)**: Ma trận 9x9 (được lưu bằng ma trận 2 chiều numpy) đại diện cho bảng Sudoku
- **Hành động (Action)**: Điền một số từ 1-9 vào ô trống
- **Hàm chuyển trạng thái**: Cập nhật bảng Sudoku sau khi điền giá trị vào ô trống
- **Trạng thái đích**: Bảng Sudoku được điền đầy đủ và hợp lệ
- **Chi phí**: Số bước đi để đạt được trạng thái đích

#### Các thuật toán đã triển khai:
1. **Depth-First Search (DFS)**
   - Giải pháp: Sử dụng stack để lưu các trạng thái, hoạt động theo nguyên tắc LIFO (Last In First Out). Thuật toán chạy đến khi tìm được lời giải, TIMEOUT hoặc stack hết phần tử
   - Độ phức tạp: O(b^d) với b là số nhánh và d là độ sâu
     
   ![Recording2025-05-12115909-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/395131f4-8f0c-409a-bb18-87cd6fccc568)

2. **Breadth-First Search (BFS)**
   - Giải pháp: Dùng queue để lưu các trạng thái, hoạt động theo nguyên tắc FIFO (First In First Out). Thuật toán chạy đến khi tìm được lời giải, TIMEOUT hoặc stack hết phần tử
   - Độ phức tạp: O(b^d)

   ![BFS](https://github.com/user-attachments/assets/cd3d84dd-8eb6-469c-b418-2f2cd6e9cd20)

3. **Uniform Cost Search (UCS)**
   - Giải pháp: Dùng hàng đợi priority queue để lấy ra phần tử có chi phí thấp nhất. Tuy nhiên, trong bài toán Sudoku vì các chi phí cho các bước (điền vào 1 ô trống) là 1 nên thuật toán này cho ra kết quả giống với BFS
   - Độ phức tạp: O(b^(1 + floor(C/ε))) với b là số bậc, C là chi phí tổng và ε là chi phí nhỏ nhất cho 1 hành động

   ![UCS](https://github.com/user-attachments/assets/95028c47-025a-4a55-ba2f-f998b9a77c35)

4. **Iterative Deepening Search (IDS)**
   - Giải pháp: Kết hợp DFS và BFS, đặt ra 1 độ sâu ban đầu và dùng DFS để xét các trạng thái thỏa độ sâu ấy rồi tăng dần độ sâu.
   - Độ phức tạp: O(b^d)

   ![IDS](https://github.com/user-attachments/assets/7f2f9a8d-eae2-46bc-92f9-9935e012ae4a)

#### Nhận xét:
- DFS thường nhanh hơn trong các trường hợp có nhiều giải pháp
- BFS đảm bảo tìm được giải pháp tối ưu nhưng tốn nhiều bộ nhớ
- IDS cân bằng giữa hiệu suất và bộ nhớ
- UCS không hiệu quả bằng các thuật toán khác trong bài toán Sudoku

### 2.2. Các thuật toán Tìm kiếm có thông tin (Informed Search Algorithm)

#### Thành phần chính:
- **Hàm heuristic**: Được tính dựa trên số ô còn trống trong bảng game.
- **Hàm đánh giá**: f(n) = g(n) + h(n) với g(n) là chi phí từ trạng thái ban đầu đến n, h(n) là giá trị heuristic, g(n) là chi phí của các bước di chuyển (trong bài toán này, mỗi bước di chuyển tương ứng với 1)

#### Các thuật toán đã triển khai:
1. **A* Search**
   - Giải pháp: Dùng hàng chờ ưu tiên (Priprity Queue) để chọn trạng thái kế tiếp với f(x) bé nhất
   - Độ phức tạp: O(b^d)

   ![A-star](https://github.com/user-attachments/assets/05a3b441-353e-4950-9c05-9a15acbff823)

2. **Greed Search (Best-First Search)**
   - Giải pháp: Dùng hàng chờ ưu tiên (Priprity Queue) để chọn trạng thái kế tiếp với h(x) bé nhất
   - Độ phức tạp: O(b^d)

   ![GreedySearch](https://github.com/user-attachments/assets/1e96d9ac-15f5-4930-ba8b-15a9f8aef5dd)

3. **IDA* Search**
   - Giải pháp: Kết hợp A* và Iterative Deepening, tương tự như A*, thuật toán này dùng hàng đợi ưu tiên để chọn trạng thái kế tiếp để xét với f(x) bé nhất.
   - Độ phức tạp: O(b^d)

   ![IDA-Star](https://github.com/user-attachments/assets/d867d9ca-5072-4b30-8945-812e88e7c6b6)
   
#### Nhận xét:
- A* thường hiệu quả nhất trong nhóm này nhờ cân bằng giữa chi phí đã đi và ước lượng còn lại
- Greed Search có thể nhanh hơn nhưng không đảm bảo tìm được giải pháp tối ưu
- IDA* cân bằng giữa hiệu suất và bộ nhớ, phù hợp với bài toán có không gian trạng thái lớn

### 2.3. Các thuật toán Tìm kiếm cục bộ (Local Search Algorithm)

#### Các thuật toán đã triển khai:
1. **Simple Hill Climbing**
   - Giải pháp: Chọn trạng thái đầu tiên có chi phí tốt hơn trạng thái hiện tại thay vì bỏ vào hàng đợi và xét hết
   - Độ phức tạp: O(n) với n là số ô trống

   ![Simplehill](https://github.com/user-attachments/assets/09ccb9cc-02e3-4bb3-bbb2-12ef331fe205)

2. **Steepest-Ascent Hill Climbing**
   - Giải pháp: Xem xét tất cả các trạng thái kế tiếp sau khi áp dụng hành động và chọn ra trạng thái có chi phí tốt nhất
   - Độ phức tạp: O(n)

   ![Steepest hill](https://github.com/user-attachments/assets/5de3c8ab-7557-4c47-a34d-cffdcc1ce852)

3. **Stochastic Hill Climbing**
   - Giải pháp: Chọn ngẫu nhiên trạng thái tiếp theo có chi phí tốt hơn trạng thái hiện tại.
   - Độ phức tạp: O(n)

   ![stochastichill](https://github.com/user-attachments/assets/29dc8d2a-6647-49e7-b355-36a796919799)

4. **Simulated Annealing**
   - Giải pháp: Xét ngẫu nhiên 1 trong các trạng thái tiếp theo sau khi áp dụng các bước di chuyển, nếu chi phí tốt hơn thì chọn luôn. Ngược lại, nếu trạng thái kế tiếp có chi phí lớn hơn nhưng vẫn đảm bảo công thức xác suất dựa trên nhiệt độ thì vẫn có thể chọn để làm trạng thái tiếp theo. Nhiệt độ sẽ giảm dần dựa vào chỉ số làm nguội.
   - Độ phức tạp: O(n)

   ![simulatedannealing](https://github.com/user-attachments/assets/90eebe43-24e7-420b-a249-38f240e12cfb)

5. **Local Beam Search**
   - Giải pháp: Từ các trạng thái được sinh ra bằng cách áp dụng các hành động, duy trì k trạng thái có chi phí thấp nhất để tiếp tục xét.
   - Độ phức tạp: O(k*n) với k là số trạng thái được duy trì

   ![localbeam](https://github.com/user-attachments/assets/c8bc18ee-c893-4a73-8953-0dae130acb8c)

6. **Genetic Algorithm**
   - Giải pháp: Sử dụng quần thể các trạng thái, áp dụng chọn lọc các cả thể gần với trạng đích nhất, lai ghép và đột biến
   - Độ phức tạp: O(p*n*g) với p là kích thước quần thể, g là số thế hệ

   ![GA](https://github.com/user-attachments/assets/de168436-21ad-43d0-ad46-37bc35affbd6)

#### Nhận xét:
- Hill Climbing dễ bị mắc kẹt ở cực tiểu địa phương
- Simulated Annealing có khả năng thoát khỏi cực tiểu địa phương tốt hơn
- Local Beam Search và Genetic Algorithm phù hợp cho không gian tìm kiếm lớn

### 2.4. Các thuật toán Tìm kiếm trong môi trường phức tạp (Complex Environment Search)

#### Các thuật toán đã triển khai:
1. **AND-OR Graph Search**
   - Giải pháp: Áp dụng đệ quy xen kẽ giữa And-Search(dùng để giải toàn bộ bài toán) và Or-Search(dùng để tìm hành động khả thi).
   - Độ phức tạp: O(b^d)

   ![AndOr](https://github.com/user-attachments/assets/5a48adb4-b2e4-4e0e-b626-a027525e7334)

2. **Partial Observation Search**
   - Giải pháp: Lặp lại hành động chọn trạng thái có niềm tin tốt nhất và tạo môi trường quan sát cho tất cả tất cả các states được suy ra từ state trước bằng cách áp dụng các cách di chuyển, tính tính khả thi cho các trạng thái đó rồi lại chọn state tốt nhất để tiếp tục 
   - Độ phức tạp: O(|S|^2 * |O|) với S là không gian trạng thái, O là không gian quan sát

   ![Partialobservation](https://github.com/user-attachments/assets/68527d97-dada-4168-b642-0f4406c8cfec)

#### Nhận xét:
- AND-OR Graph Search phù hợp với các bài toán có nhiều trạng thái không xác định
- Partial Observation Search hiệu quả khi không thể quan sát đầy đủ trạng thái của bảng Sudoku

### 2.5. Các thuật toán Thỏa mãn ràng buộc (Constraint Satisfaction Problem)

#### Các thuật toán đã triển khai:
1. **AC-3**
   - Giải pháp: Tạo ra tập tất cả các cung (từng cặp vị trí) theo hàng, cột và các khối(3x3). Đặt vào 1 hàng đợi và tiến hành lại các giá trị vi phạm ràng buộc về bài toán trong miền giá trị của cung đó. Các ràng buộc gồm: Các ô trên cùng hàng, cùng cột và cùng khối không được trùng giá trị.
   - Độ phức tạp: O(n²d³) với n là số biến, d là kích thước miền

   ![AC3](https://github.com/user-attachments/assets/fdf56a7b-f71c-4639-a902-a3e018ebfbc4)

2. **Forward Checking**
   - Giải pháp: Chọn ngẫu nhiên 1 giá trị rồi điền vào ô trống, sau đó kiểm tra ràng buộc. Nếu thỏa thì dùng đệ quy để tiếp tục giải, không thì ô đó bằng 1 giá trị khác rồi thực hiện lại tương tự.
   - Độ phức tạp: O(d²n)

   ![Forwardchecking](https://github.com/user-attachments/assets/734f785a-fc74-41c9-8b2f-ae73f13ef9e1)

3. **Backtracking**
   - Giải pháp: Gán giá trị ngẫu nhiên cho 1 ô trống và tiến hành giải (dùng đệ quy), nếu không tìm thấy đường đi hợp lệ thì quay lui.
   - Độ phức tạp: O(d^n)

   ![backtracking](https://github.com/user-attachments/assets/cc2cd355-2ead-477b-8513-160b4906388c)

#### Nhận xét:
- AC-3 hiệu quả trong việc loại bỏ các giá trị không thỏa mãn từ sớm
- Forward Checking cân bằng giữa tốc độ và khả năng phát hiện xung đột
- Backtracking là nền tảng cho các thuật toán CSP khác

### 2.6. Các thuật toán Học tăng cường (Reinforcement Learning)

#### Các thuật toán đã triển khai:
1. **Q-Learning**
   - Giải pháp: Tìm các cách đặt giá trị vào 1 ô trống sau đó chọn hành động. Hành động được chọn theo nguyên tắc: Thỉnh thoảng sẽ chọn 1 hành động ngẫu nhiên, còn lại sẽ chọn hành động có q_value lớn nhất. Sau khi thực hiện hành động sẽ nhận được “phần thưởng” dựa vào số ô đã điền được và số ô điền sai các ràng buộc của trò chơi. Cập nhật lại trạng thái của q_value và tiếp tục.
   - Độ phức tạp: O(n * m) với n là số trạng thái, m là số hành động

   ![Q-learning](https://github.com/user-attachments/assets/f252a065-bb1d-404e-a28d-a27e9ecc5f0c)

#### Nhận xét:
- Q-Learning có khả năng học từ trải nghiệm và cải thiện hiệu suất theo thời gian
- Phù hợp cho các bài toán có không gian trạng thái lớn và phức tạp
- Cần thời gian huấn luyện dài để đạt hiệu quả cao

### 2.7. Bảng so sánh hiệu suất các thuật toán

![Screenshot 2025-05-12 133946](https://github.com/user-attachments/assets/4c839d56-0be3-4a88-9310-e8acae5c8046)

## 3. Kết luận

### Kết quả đạt được:
1. Đã triển khai thành công 19 thuật toán tìm kiếm khác nhau
2. Xây dựng được giao diện khá thân thiện với người dùng
3. Có khả năng so sánh hiệu suất giữa các thuật toán
4. Hỗ trợ 3 mức độ khó khác nhau của Sudoku
5. Có khả năng xuất kết quả và báo cáo phân tích ra file excel

### Hướng phát triển:
1. Tối ưu hóa các thuật toán hiện có
2. Thêm các thuật toán mới
3. Cải thiện giao diện người dùng
4. Mở rộng sang các biến thể của Sudoku 
