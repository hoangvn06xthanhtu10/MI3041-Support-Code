import sympy as sp
import math

# ==========================================
# HÀM PHỤ TRỢ: TÌM M VÀ m CỦA ĐẠO HÀM
# ==========================================
def tim_M_m(f_expr, a, b, num_points=1000):
    """Tìm giá trị lớn nhất (M) và nhỏ nhất (m) của |f'(x)| trên đoạn [a, b]"""
    x = sp.Symbol('x')
    df = sp.diff(f_expr, x)
    df_num = sp.lambdify(x, df, 'math')
    
    start, end = min(a, b), max(a, b)
    step = (end - start) / num_points
    
    try:
        df_vals = [abs(df_num(start + i * step)) for i in range(num_points + 1)]
        return max(df_vals), min(df_vals)
    except Exception as e:
        print(f"Lỗi khi tính đạo hàm: {e}")
        return None, None

# ==========================================
# CHẾ ĐỘ 1: CHẠY THEO SỐ BƯỚC LẶP CỐ ĐỊNH
# ==========================================
def day_cung_by_steps(f_expr, f_num, a, b, max_iter):
    print("\n" + "="*85)
    print(" CHẾ ĐỘ 1: PHƯƠNG PHÁP DÂY CUNG THEO SỐ VÒNG LẶP")
    print(f" Hàm số f(x) = {f_expr}")
    print(f" Điểm chạy bắt đầu a  = {a}")
    print(f" Đầu mút cố định b    = {b}")
    print("="*85)
    
    print(f"| {'Lần lặp':<10} | {'x_n':<16} | {'f(x_n)':<16} | {'|x_n - x_{n-1}|':<22} |")
    print("-" * 85)

    xn = a
    last_epsilon = 0.0
    fb = f_num(b)
    fxn = f_num(xn)

    print(f"| {0:<10} | {xn:<16.9f} | {fxn:<16.9f} | {'---':<22} |")

    for i in range(1, max_iter + 1):
        if abs(fxn - fb) == 0:
            print(f"Lỗi: f(x_n) = f(b) = {fb}, mẫu số bằng 0. Dừng thuật toán.")
            return None

        # Công thức: x_{n+1} = x_n - f(x_n)*(x_n - b)/(f(x_n) - f(b))
        x_next = xn - fxn * (xn - b) / (fxn - fb)
        fx_next = f_num(x_next)

        sai_so = abs(x_next - xn)
        last_epsilon = sai_so
        
        print(f"| {i:<10} | {x_next:<16.9f} | {fx_next:<16.9f} | {sai_so:<22.9f} |")

        xn = x_next
        fxn = fx_next
        
        if fxn == 0:
            print("-" * 85)
            print(f"-> Đã tìm được nghiệm chính xác tuyệt đối tại lần lặp {i}.")
            break

    print("-" * 85)
    print(f"=> Nghiệm gần đúng sau {max_iter} lần lặp: x ≈ {xn:.9f}")
    
    # Đánh giá sai số cuối cùng
    M, m = tim_M_m(f_expr, a, b)
    if M is not None and m is not None:
        if m == 0:
            print("[!] Không thể đánh giá sai số Delta_n vì m = 0.")
        else:
            delta_n = ((M - m) / m) * last_epsilon
            print(f"=> Đánh giá sai số giới hạn: Delta_n <= {delta_n:.9e}")
            
    return xn

# ==========================================
# CHẾ ĐỘ 2: CHẠY THEO ĐỘ CHÍNH XÁC EPSILON
# ==========================================
def day_cung_by_epsilon(f_expr, f_num, a, b, tol):
    print("\n" + "="*95)
    print(f" CHẾ ĐỘ 2: PHƯƠNG PHÁP DÂY CUNG THEO SAI SỐ TOL = {tol}")
    print("="*95)
    
    # Tính M, m trước để dùng cho công thức dừng
    M, m = tim_M_m(f_expr, a, b)
    if M is None or m is None or m == 0:
        print("Lỗi: Không thể chạy chế độ Epsilon vì m = 0 (đạo hàm triệt tiêu trên khoảng phân ly).")
        return None
        
    he_so_sai_so = (M - m) / m
    print(f"Thông số đạo hàm: M = {M:.5f}, m = {m:.5f} => Hệ số (M-m)/m = {he_so_sai_so:.5f}")
    
    print(f"| {'Lần lặp':<8} | {'x_n':<16} | {'f(x_n)':<16} | {'|x_n - x_{n-1}|':<16} | {'Sai số Delta_n':<16} |")
    print("-" * 95)

    xn = a
    fb = f_num(b)
    fxn = f_num(xn)
    
    print(f"| {0:<8} | {xn:<16.9f} | {fxn:<16.9f} | {'---':<16} | {'---':<16} |")

    n = 1
    while True:
        if abs(fxn - fb) == 0:
            print("Lỗi mẫu số bằng 0. Dừng thuật toán.")
            return None

        x_next = xn - fxn * (xn - b) / (fxn - fb)
        fx_next = f_num(x_next)

        sai_so_tuong_doi = abs(x_next - xn)
        delta_n = he_so_sai_so * sai_so_tuong_doi # Công thức sai số giới hạn
        
        print(f"| {n:<8} | {x_next:<16.9f} | {fx_next:<16.9f} | {sai_so_tuong_doi:<16.9f} | {delta_n:<16.9e} |")

        xn = x_next
        fxn = fx_next
        
        # Kiểm tra điều kiện dừng dựa trên Delta_n
        if delta_n <= tol or fxn == 0:
            break
            
        n += 1

    print("-" * 95)
    print(f"=> Nghiệm gần đúng đạt yêu cầu: x ≈ {xn:.9f} (sau {n} bước lặp)")
    return xn

# ==========================================
# MENU TƯƠNG TÁC CHÍNH
# ==========================================
def main():
    print("============= CHƯƠNG TRÌNH TÌM NGHIỆM BẰNG PHƯƠNG PHÁP DÂY CUNG =============")
    x = sp.Symbol('x')
    
    # 1. Nhập hàm số
    func_str = input("Nhập hàm số f(x) = ")
    try:
        f_expr = sp.sympify(func_str)
        f_num = sp.lambdify(x, f_expr, 'math')
        # Test nhẹ hàm số
        f_num(1)
        print(f"[+] Đã ghi nhận hàm số: f(x) = {f_expr}")
    except Exception as e:
        print(f"Lỗi: Hàm số nhập vào không hợp lệ ({e}).")
        return

    # 2. Nhập đầu mút
    try:
        a = float(input("Nhập đầu mút a (điểm di chuyển): "))
        b = float(input("Nhập đầu mút b (điểm cố định): "))
    except ValueError:
        print("Lỗi: Vui lòng nhập số hợp lệ.")
        return

    # 3. Chọn chế độ
    print("\nChọn chế độ chạy:")
    print("1. Chạy theo số vòng lặp cố định (n)")
    print("2. Chạy theo sai số giới hạn (epsilon)")
    
    choice = input("Nhập lựa chọn (1 hoặc 2): ")
    
    if choice == '1':
        try:
            n_steps = int(input("Nhập số lần lặp: "))
            day_cung_by_steps(f_expr, f_num, a, b, n_steps)
        except ValueError:
            print("Vui lòng nhập số nguyên hợp lệ.")
            
    elif choice == '2':
        try:
            tol = float(input("Nhập sai số giới hạn epsilon (VD: 1e-4): "))
            day_cung_by_epsilon(f_expr, f_num, a, b, tol)
        except ValueError:
            print("Vui lòng nhập một số hợp lệ cho epsilon.")
            
    else:
        print("Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    main()