import numpy as np

def fixed_point_iteration(G, x0, mode, tol=1e-6, num_iters=10):
    """
    Giải hệ phương trình phi tuyến bằng phương pháp lặp đơn.
    """
    x = np.array(x0, dtype=float)
    
    print(f"\n{'Vòng lặp':<10} | {'Giá trị X (Nghiệm dự đoán)'}")
    print("-" * 60)
    print(f"{0:<10} | {x}")

    for k in range(1, num_iters + 1):
        x_new = G(x)
        print(f"{k:<10} | {x_new}")

        if mode == 2:
            sai_so_hien_tai = np.linalg.norm(x_new - x, np.inf)
            if sai_so_hien_tai < tol:
                print("-" * 60)
                print(f"[*] Thuật toán HỘI TỤ đạt chuẩn epsilon sau {k} vòng lặp.")
                return x_new, k

        x = x_new

    print("-" * 60)
    if mode == 1:
        print(f"[*] Đã hoàn thành đúng {num_iters} vòng lặp theo yêu cầu.")
    elif mode == 2:
        print(f"[!] Dừng do đạt giới hạn {num_iters} vòng lặp mà chưa đạt epsilon.")
        
    return x, num_iters

# ==========================================
# CHƯƠNG TRÌNH CHÍNH
# ==========================================
if __name__ == "__main__":
    np.set_printoptions(precision=12, floatmode='fixed')
    print("--- BƯỚC 1: THIẾT LẬP HỆ PHƯƠNG TRÌNH ---")
    try:
        num_vars = int(input("Nhập số lượng ẩn (VD: 2): "))
        var_names = input("Nhập tên các ẩn, cách nhau bởi khoảng trắng (VD: x y): ").split()
        
        if len(var_names) != num_vars:
            print("Lỗi: Số lượng tên ẩn không khớp với số lượng ẩn đã nhập!")
            exit()
            
        print("\nNhập các hàm G(X) sao cho X = G(X).")
        print("Lưu ý cú pháp Python: Dùng sin(), cos(), exp(), sqrt(), x**2 (thay vì x^2).")
        
        expressions = []
        for var in var_names:
            expr = input(f"{var} = ")
            expressions.append(expr)
            
        # Định nghĩa các hàm toán học cho phép người dùng nhập trực tiếp
        math_env = {
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "exp": np.exp, "log": np.log, "log10": np.log10, "sqrt": np.sqrt,
            "pi": np.pi, "e": np.e
        }
        
        # Hàm G(X) động, được tạo từ chuỗi người dùng nhập
        def G_dynamic(vars_values):
            # Ghép tên biến với giá trị hiện tại của nó (VD: x=0, y=0)
            local_env = {name: val for name, val in zip(var_names, vars_values)}
            # Kết hợp các hàm toán học và giá trị biến để tính toán
            env = {**math_env, **local_env}
            
            results = []
            for expr in expressions:
                # Dùng eval để tính giá trị của chuỗi biểu thức
                val = eval(expr, {"__builtins__": {}}, env)
                results.append(val)
            return np.array(results, dtype=float)

        print("\n--- BƯỚC 2: NHẬP GIÁ TRỊ KHỞI TẠO ---")
        x_ban_dau = []
        for var in var_names:
            val = float(input(f"Nhập giá trị dự đoán ban đầu cho {var} (X0): "))
            x_ban_dau.append(val)

        print("\n--- BƯỚC 3: CHỌN CHẾ ĐỘ LẶP ---")
        print("1. Lặp theo số vòng (N)")
        print("2. Lặp theo sai số (epsilon)")
        
        lua_chon = int(input("Nhập lựa chọn của bạn (1 hoặc 2): "))
        
        if lua_chon == 1:
            n_vong = int(input("Nhập số vòng lặp mong muốn: "))
            nghiem, so_vong = fixed_point_iteration(G_dynamic, x0=x_ban_dau, mode=1, num_iters=n_vong)
            
        elif lua_chon == 2:
            epsilon = float(input("Nhập sai số epsilon (VD: 0.0001): "))
            max_n = int(input("Nhập số vòng lặp tối đa (VD: 100): "))
            nghiem, so_vong = fixed_point_iteration(G_dynamic, x0=x_ban_dau, mode=2, tol=epsilon, num_iters=max_n)
            
        else:
            print("Lựa chọn không hợp lệ.")
            exit()
            
        print("\nKẾT QUẢ CUỐI CÙNG:")
        for name, val in zip(var_names, nghiem):
            print(f"{name} ≈ {val:.12f}")
            
    except Exception as e:
        print(f"\nĐã xảy ra lỗi trong quá trình nhập liệu hoặc tính toán: {e}")
        print("Vui lòng kiểm tra lại cú pháp biểu thức toán học.")