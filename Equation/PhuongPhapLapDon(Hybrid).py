import sympy as sp

def tim_q_lap_don(g, dg, x, a, b, num_points=1000):
    """Hàm quét trên khoảng [a, b] để tìm hệ số co q = max |g'(x)|"""
    dg_num = sp.lambdify(x, dg, 'math')
    start, end = min(a, b), max(a, b)
    step = (end - start) / num_points
    
    q = 0
    for i in range(num_points + 1):
        x_val = start + i * step
        q = max(q, abs(dg_num(x_val)))
    return q

def in_tieu_de_bang(tieu_de, g, dg, q, x0, a, b):
    """Hàm in tiêu đề, thông số và CHÚ THÍCH CỘT"""
    print("\n" + "="*110)
    print(f" {tieu_de}")
    print(f" Hàm số g(x)        = {g}")
    print(f" Đạo hàm g'(x)      = {dg}")
    print(f" Khoảng cách ly     = [{a}, {b}]")
    print(f" Hệ số co q         = {q:.6f}")
    if q >= 1:
        print(" [CẢNH BÁO]: q >= 1, điều kiện hội tụ không được đảm bảo!")
    
    # CHÚ THÍCH CÁC CỘT
    print("-" * 110)
    print(" * CHÚ THÍCH Ý NGHĨA CÁC CỘT TRONG BẢNG:")
    print("   - n            : Lần lặp hiện tại (Bắt đầu từ 0 với giá trị ban đầu x0).")
    print("   - x_n          : Giá trị xấp xỉ nghiệm ở bước thứ n.")
    print("   - g(x_n)       : Giá trị hàm tại x_n. Đây chính là x_{n+1} cho bước tiếp theo.")
    print("   - |x_n - x_n-1|: Khoảng cách giữa 2 bước lặp liên tiếp (Chỉ tính từ n = 1).")
    print("   - Sai số Δn    : Sai số hậu nghiệm tính theo công thức: (q / (1 - q)) * |x_n - x_{n-1}|.")
    print("="*110)
    
    # HEADER BẢNG
    print(f"| {'n':<4} | {'x_n':<22} | {'g(x_n)':<22} | {'|x_n - x_n-1|':<18} | {'Sai số Δn':<18} |")
    print("-" * 110)

def format_row(i, xn, g_xn, kc_epsilon, sai_so):
    """Hàm định dạng in từng dòng (dòng 0 sẽ in --- cho sai số)"""
    if i == 0 or kc_epsilon is None or sai_so is None:
        kc_str = "---"
        sai_so_str = "---"
    else:
        kc_str = f"{kc_epsilon:.9f}"
        sai_so_str = f"{sai_so:.9e}"
        
    print(f"| {i:<4} | {xn:<22.20f} | {g_xn:<22.20f} | {kc_str:<18} | {sai_so_str:<18} |")

def lap_don_so_vong(func_str, a, b, x0, max_iter):
    x = sp.Symbol('x')
    try:
        g = sp.sympify(func_str)
        dg = sp.diff(g, x)
    except Exception:
        print("Lỗi: Hàm số nhập vào không hợp lệ.")
        return None

    q = tim_q_lap_don(g, dg, x, a, b)
    g_num = sp.lambdify(x, g, 'math')

    in_tieu_de_bang("PHƯƠNG PHÁP LẶP ĐƠN (LẶP THEO SỐ VÒNG n)", g, dg, q, x0, a, b)

    xn = x0
    x_prev = None

    for i in range(max_iter + 1):
        try:
            g_xn = g_num(xn)
        except Exception as e:
            print(f"Lỗi tính toán tại x = {xn}: {e}")
            return None

        if i > 0:
            kc_epsilon = abs(xn - x_prev)
            sai_so = (q / (1 - q)) * kc_epsilon if q < 1 else kc_epsilon
        else:
            kc_epsilon = None
            sai_so = None

        format_row(i, xn, g_xn, kc_epsilon, sai_so)
        
        # Chuẩn bị cho vòng lặp tiếp theo
        x_prev = xn
        xn = g_xn 

    print("-" * 110)
    print(f"=> Kết luận: Xấp xỉ nghiệm sau {max_iter} lần lặp là x ≈ {x_prev:.9f}")
    return x_prev

def lap_don_epsilon(func_str, a, b, x0, epsilon, max_limit=1000):
    x = sp.Symbol('x')
    try:
        g = sp.sympify(func_str)
        dg = sp.diff(g, x)
    except Exception:
        print("Lỗi: Hàm số nhập vào không hợp lệ.")
        return None

    q = tim_q_lap_don(g, dg, x, a, b)
    g_num = sp.lambdify(x, g, 'math')

    in_tieu_de_bang(f"PHƯƠNG PHÁP LẶP ĐƠN (DỪNG KHI SAI SỐ <= {epsilon})", g, dg, q, x0, a, b)

    xn = x0
    x_prev = None
    i = 0

    while i <= max_limit:
        try:
            g_xn = g_num(xn)
        except Exception as e:
            print(f"Lỗi tính toán tại x = {xn}: {e}")
            return None

        if i > 0:
            kc_epsilon = abs(xn - x_prev)
            sai_so = (q / (1 - q)) * kc_epsilon if q < 1 else kc_epsilon
        else:
            kc_epsilon = None
            sai_so = None

        format_row(i, xn, g_xn, kc_epsilon, sai_so)

        if i > 0 and sai_so is not None and sai_so <= epsilon:
            print("-" * 110)
            print(f"-> Dừng thuật toán vì sai số Δ{i} = {sai_so:.9e} <= {epsilon}.")
            print(f"=> Kết luận: Xấp xỉ nghiệm là x ≈ {xn:.9f}")
            return xn
            
        x_prev = xn
        xn = g_xn
        i += 1

    print("-" * 110)
    print(f"-> [CẢNH BÁO] Không đạt được sai số yêu cầu sau {max_limit} lần lặp.")
    return x_prev

if __name__ == "__main__":
    print("=== TÌM NGHIỆM PHƯƠNG TRÌNH x = g(x) BẰNG LẶP ĐƠN ===")
    ham_so = input("Nhập hàm g(x) = ")
    
    try:
        a = float(input("Nhập đầu mút a: "))
        b = float(input("Nhập đầu mút b: "))
        x0 = float(input("Nhập giá trị x0 ban đầu: "))
    except ValueError:
        print("Lỗi: Dữ liệu nhập vào phải là số.")
        exit()

    print("\nChọn điều kiện dừng:")
    print(" 1. Lặp theo số vòng định trước (n)")
    print(" 2. Lặp theo Epsilon (Sai số)")
    lua_chon = input("Lựa chọn (1 hoặc 2): ")

    if lua_chon == '1':
        n = int(input("Nhập số vòng lặp n: "))
        lap_don_so_vong(ham_so, a, b, x0, n)
    elif lua_chon == '2':
        eps = float(input("Nhập Epsilon (VD: 1e-4, 0.001): "))
        lap_don_epsilon(ham_so, a, b, x0, eps)
    else:
        print("Lựa chọn không hợp lệ!")