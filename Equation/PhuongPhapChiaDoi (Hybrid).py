import math
import sympy as sp

# ---------------------------------------------------------
# HÀM XỬ LÝ BIỂU THỨC BẰNG SYMPY
# ---------------------------------------------------------
def create_function(expr_str):
    """
    Dùng SymPy để phân tích chuỗi người dùng nhập và 
    chuyển thành hàm tính toán (callable).
    """
    x = sp.symbols('x') # Định nghĩa biến x
    # Chuyển chuỗi thành biểu thức toán học SymPy
    expr = sp.sympify(expr_str) 
    
    # lambdify giúp chuyển biểu thức SymPy thành hàm Python thông thường 
    # sử dụng thư viện 'math' để tính toán cực nhanh trong vòng lặp
    f_callable = sp.lambdify(x, expr, 'math') 
    
    return f_callable, expr

# ---------------------------------------------------------
# CHẾ ĐỘ 1: CHẠY THEO SỐ BƯỚC LẶP N
# ---------------------------------------------------------
def bisection_by_steps(f, a, b, n_steps):
    print(f"\n=== KẾT QUẢ: CHẠY THEO {n_steps} BƯỚC LẶP ===")
    
    if f(a) * f(b) >= 0:
        print("Lỗi: Hàm số không đổi dấu trên khoảng [a, b]. Vui lòng chọn khoảng khác.")
        return None

    print(f"{'Lần lặp':<10} | {'a':<12} | {'b':<12} | {'x_n (Nghiệm)':<15} | {'Sai số':<15}")
    print("-" * 75)

    x_n = (a + b) / 2.0
    for i in range(n_steps):
        x_n = (a + b) / 2.0
        error = (b - a) / 2.0
        
        print(f"{i:<10} | {a:<12.6f} | {b:<12.6f} | {x_n:<15.6f} | {error:<15.6f}")

        if f(x_n) == 0:
            print("\nĐã tìm thấy nghiệm chính xác!")
            break
        
        if f(a) * f(x_n) < 0:
            b = x_n
        else:
            a = x_n

    print("-" * 75)
    print(f"Nghiệm gần đúng sau {n_steps} bước: x ≈ {x_n:.6f}")
    return x_n

# ---------------------------------------------------------
# CHẾ ĐỘ 2: CHẠY THEO ĐỘ CHÍNH XÁC EPSILON
# ---------------------------------------------------------
def bisection_by_epsilon(f, a, b, tol):
    print(f"\n=== KẾT QUẢ: CHẠY THEO SAI SỐ TOL = {tol} ===")
    
    if f(a) * f(b) >= 0:
        print("Lỗi: Hàm số không đổi dấu trên khoảng [a, b]. Vui lòng chọn khoảng khác.")
        return None

    n_priori = math.ceil(math.log2((b - a) / tol))
    print(f"Số bước lặp dự kiến để đạt sai số {tol}: {n_priori} lần")
    
    print(f"{'Lần lặp':<10} | {'a':<12} | {'b':<12} | {'x_n (Nghiệm)':<15} | {'Sai số hiện tại':<15}")
    print("-" * 80)

    n = 0
    while (b - a) / 2.0 > tol:
        x_n = (a + b) / 2.0
        error = (b - a) / 2.0
        
        print(f"{n:<10} | {a:<12.6f} | {b:<12.6f} | {x_n:<15.6f} | {error:<15.6f}")
        
        if f(x_n) == 0:
            print("\nĐã tìm thấy nghiệm chính xác!")
            break
            
        if f(a) * f(x_n) < 0:
            b = x_n
        else:
            a = x_n
        n += 1

    x_final = (a + b) / 2.0
    print("-" * 80)
    print(f"Nghiệm tìm được: x ≈ {x_final:.6f} sau {n} bước lặp.")
    return x_final

# ---------------------------------------------------------
# MENU TƯƠNG TÁC
# ---------------------------------------------------------
def main():
    print("============= CHƯƠNG TRÌNH TÌM NGHIỆM BẰNG PHƯƠNG PHÁP CHIA ĐÔI =============")
    print("Hướng dẫn nhập hàm (Hỗ trợ bởi SymPy):")
    print("- Dùng 'x' làm biến số.")
    print("- Hỗ trợ cú pháp tự nhiên: exp(x), E**x, sin(x), log(x)...")
    print("-----------------------------------------------------------------------------")
    
    # 1. Nhập hàm số
    expr_str = input("Nhập hàm f(x) = ")
    try:
        f, expr = create_function(expr_str)
        print(f"\n[+] Đã ghi nhận hàm số: f(x) = {expr}")
        # Test thử hàm
        f(1) 
    except Exception as e:
        print(f"Lỗi khi đọc hàm bằng SymPy: {e}. Vui lòng kiểm tra lại cú pháp!")
        return

    # 2. Nhập khoảng phân ly
    try:
        a = float(input("Nhập đầu mút a: "))
        b = float(input("Nhập đầu mút b: "))
    except ValueError:
        print("Vui lòng nhập một số hợp lệ cho a và b.")
        return

    # Kiểm tra điều kiện ngay từ đầu
    if f(a) * f(b) >= 0:
        print("\n[CẢNH BÁO] Hàm số không đổi dấu trên khoảng này (f(a) * f(b) >= 0). Không thể áp dụng phương pháp chia đôi.")
        return

    # 3. Chọn chế độ
    print("\nChọn chế độ chạy:")
    print("1. Chạy theo số vòng lặp cố định (n)")
    print("2. Chạy theo độ chính xác (epsilon)")
    
    choice = input("Nhập lựa chọn của bạn (1 hoặc 2): ")
    
    if choice == '1':
        try:
            n_steps = int(input("Nhập số vòng lặp n: "))
            bisection_by_steps(f, a, b, n_steps)
        except ValueError:
            print("Vui lòng nhập một số nguyên hợp lệ.")
            
    elif choice == '2':
        try:
            tol = float(input("Nhập sai số epsilon (VD: 0.0001 hoặc 1e-4): "))
            bisection_by_epsilon(f, a, b, tol)
        except ValueError:
            print("Vui lòng nhập một số hợp lệ cho epsilon.")
            
    else:
        print("Lựa chọn không hợp lệ. Vui lòng chạy lại chương trình.")

if __name__ == "__main__":
    main()