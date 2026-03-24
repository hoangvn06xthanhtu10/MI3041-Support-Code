import sympy as sp
import math

# ==========================================
# HÀM PHỤ TRỢ: TÌM M, m VÀ TỰ ĐỘNG CHỌN x0
# ==========================================
def phan_tich_ham(f_expr, x_sym, a, b, num_points=1000):
    """Tính đạo hàm, tìm M, m và chọn x0 theo điều kiện Fourier"""
    df_expr = sp.diff(f_expr, x_sym)
    d2f_expr = sp.diff(df_expr, x_sym)
    
    f_num = sp.lambdify(x_sym, f_expr, 'math')
    df_num = sp.lambdify(x_sym, df_expr, 'math')
    d2f_num = sp.lambdify(x_sym, d2f_expr, 'math')
    
    # Tìm M (max |f''(x)|) và m (min |f'(x)|)
    start, end = min(a, b), max(a, b)
    step = (end - start) / num_points
    
    try:
        df_vals = [abs(df_num(start + i * step)) for i in range(num_points + 1)]
        d2f_vals = [abs(d2f_num(start + i * step)) for i in range(num_points + 1)]
        M = max(d2f_vals)
        m = min(df_vals)
    except Exception as e:
        print(f"Lỗi khi quét tìm M, m: {e}")
        return None
        
    # Tự động chọn x0 theo điều kiện Fourier
    fa, d2fa = f_num(a), d2f_num(a)
    fb, d2fb = f_num(b), d2f_num(b)

    if fa * d2fa > 0:
        x0 = a
        ly_do = f"f({a}) * f''({a}) > 0"
    elif fb * d2fb > 0:
        x0 = b
        ly_do = f"f({b}) * f''({b}) > 0"
    else:
        x0 = a
        ly_do = f"Không có mút nào thỏa mãn Fourier, mặc định chọn a = {a}"
        
    return df_expr, d2f_expr, f_num, df_num, M, m, x0, ly_do

# ==========================================
# CHẾ ĐỘ 1: CHẠY THEO SỐ VÒNG LẶP CỐ ĐỊNH
# ==========================================
def newton_by_steps(f_expr, x_sym, a, b, max_iter):
    data = phan_tich_ham(f_expr, x_sym, a, b)
    if not data: return None
    df_expr, d2f_expr, f_num, df_num, M, m, x0, ly_do = data

    if m == 0:
        print("Lỗi: m = 0 (đạo hàm bậc 1 triệt tiêu). Không thể tính toán sai số.")
        return None

    print("\n" + "="*115)
    print(" CHẾ ĐỘ 1: PHƯƠNG PHÁP TIẾP TUYẾN (DỪNG THEO SỐ VÒNG LẶP)")
    print(f" f'(x)  = {df_expr}")
    print(f" f''(x) = {d2f_expr}")
    print(f" Chọn x0 = {x0} (Vì {ly_do})")
    print(f" Thông số: M = {M:.5f}, m = {m:.5f}")
    print("="*115)
    
    print(f"| {'Lần lặp':<8} | {'x_n':<16} | {'f(x_n)':<16} | {'f\'(x_n)':<16} | {'|x_n - x_n-1|':<16} | {'Sai số Δn':<16} |")
    print("-" * 115)
    
    xn = x0
    x_prev = None
    
    for i in range(max_iter + 1):
        fxn = f_num(xn)
        dfxn = df_num(xn)

        if x_prev is not None:
            kc_epsilon = abs(xn - x_prev)
            delta_n = (M / (2 * m)) * (kc_epsilon**2)
            kc_str = f"{kc_epsilon:.9f}"
            sai_so_str = f"{delta_n:.9e}"
        else:
            kc_str = "---"
            sai_so_str = "---"

        print(f"| {i:<8} | {xn:<16.9f} | {fxn:<16.9f} | {dfxn:<16.9f} | {kc_str:<16} | {sai_so_str:<16} |")

        if dfxn == 0:
            print("Lỗi: f'(x) = 0, tiếp tuyến nằm ngang, thuật toán thất bại.")
            return None
        if fxn == 0:
            print("-" * 115)
            print("-> Đã tìm được nghiệm chính xác tuyệt đối!")
            return xn
            
        x_prev = xn
        xn = xn - fxn / dfxn

    print("-" * 115)
    print(f"=> Nghiệm gần đúng sau {max_iter} lần lặp: x ≈ {x_prev:.9f}")
    return x_prev

# ==========================================
# CHẾ ĐỘ 2: CHẠY THEO ĐỘ CHÍNH XÁC EPSILON
# ==========================================
def newton_by_epsilon(f_expr, x_sym, a, b, tol):
    data = phan_tich_ham(f_expr, x_sym, a, b)
    if not data: return None
    df_expr, d2f_expr, f_num, df_num, M, m, x0, ly_do = data

    if m == 0:
        print("Lỗi: m = 0. Không thể sử dụng tiêu chuẩn sai số Δn.")
        return None

    he_so_sai_so = M / (2 * m)

    print("\n" + "="*115)
    print(f" CHẾ ĐỘ 2: PHƯƠNG PHÁP TIẾP TUYẾN (DỪNG THEO SAI SỐ TOL = {tol})")
    print(f" Chọn x0 = {x0} (Vì {ly_do})")
    print(f" Hệ số sai số M/(2m) = {he_so_sai_so:.5f}")
    print("="*115)
    
    print(f"| {'Lần lặp':<8} | {'x_n':<16} | {'f(x_n)':<16} | {'f\'(x_n)':<16} | {'|x_n - x_n-1|':<16} | {'Sai số Δn':<16} |")
    print("-" * 115)
    
    xn = x0
    x_prev = None
    i = 0
    
    while True:
        fxn = f_num(xn)
        dfxn = df_num(xn)

        if x_prev is not None:
            kc_epsilon = abs(xn - x_prev)
            delta_n = he_so_sai_so * (kc_epsilon**2)
            kc_str = f"{kc_epsilon:.9f}"
            sai_so_str = f"{delta_n:.9e}"
        else:
            delta_n = float('inf') # Đảm bảo vòng lặp chạy tiếp ở bước 0
            kc_str = "---"
            sai_so_str = "---"

        print(f"| {i:<8} | {xn:<16.9f} | {fxn:<16.9f} | {dfxn:<16.9f} | {kc_str:<16} | {sai_so_str:<16} |")

        # Điều kiện dừng
        if (x_prev is not None and delta_n <= tol) or fxn == 0:
            break

        if dfxn == 0:
            print("Lỗi: f'(x) = 0, tiếp tuyến nằm ngang, thuật toán thất bại.")
            return None
            
        x_prev = xn
        xn = xn - fxn / dfxn
        i += 1

    print("-" * 115)
    print(f"=> Đạt độ chính xác yêu cầu tại bước {i}. Nghiệm x ≈ {xn:.9f}")
    return xn

# ==========================================
# MENU TƯƠNG TÁC
# ==========================================
def main():
    print("============= CHƯƠNG TRÌNH TÌM NGHIỆM: PHƯƠNG PHÁP TIẾP TUYẾN (NEWTON) =============")
    x = sp.Symbol('x')
    
    func_str = input("Nhập hàm số f(x) = ")
    try:
        f_expr = sp.sympify(func_str)
        # Test cú pháp
        sp.lambdify(x, f_expr, 'math')(1)
        print(f"[+] Đã ghi nhận hàm số: f(x) = {f_expr}")
    except Exception as e:
        print(f"Lỗi cú pháp hàm số: {e}")
        return

    try:
        a = float(input("Nhập đầu mút a của khoảng phân ly: "))
        b = float(input("Nhập đầu mút b của khoảng phân ly: "))
    except ValueError:
        print("Lỗi: Vui lòng nhập số hợp lệ.")
        return

    print("\nChọn chế độ chạy:")
    print("1. Chạy theo số vòng lặp cố định (n)")
    print("2. Chạy theo sai số giới hạn (epsilon)")
    
    choice = input("Nhập lựa chọn (1 hoặc 2): ")
    
    if choice == '1':
        try:
            n_steps = int(input("Nhập số vòng lặp (VD: 3, 5): "))
            newton_by_steps(f_expr, x, a, b, n_steps)
        except ValueError:
            print("Vui lòng nhập số nguyên hợp lệ.")
            
    elif choice == '2':
        try:
            tol = float(input("Nhập sai số giới hạn epsilon (VD: 1e-4): "))
            newton_by_epsilon(f_expr, x, a, b, tol)
        except ValueError:
            print("Vui lòng nhập một số hợp lệ cho epsilon.")
            
    else:
        print("Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    main()