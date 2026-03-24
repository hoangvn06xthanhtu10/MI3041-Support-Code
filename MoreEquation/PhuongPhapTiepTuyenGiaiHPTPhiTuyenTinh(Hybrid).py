import numpy as np

def numerical_jacobian(F, x, h=1e-5):
    """
    Tự động tính ma trận Jacobian bằng phương pháp sai phân tiến.
    Giúp người dùng không phải tự đạo hàm tay từng biến.
    """
    n = len(x)
    J = np.zeros((n, n))
    f_x = F(x)
    
    for j in range(n):
        x_step = np.copy(x)
        x_step[j] += h
        f_x_step = F(x_step)
        J[:, j] = (f_x_step - f_x) / h
        
    return J, f_x

def newton_raphson_system(F, x0, mode, tol=1e-6, num_iters=10):
    x = np.array(x0, dtype=float)
    
    print(f"\n{'Vòng lặp':<10} | {'Giá trị X (Nghiệm dự đoán)'}")
    print("-" * 65)
    print(f"{0:<10} | {x}")

    for k in range(1, num_iters + 1):
        # Tính Ma trận Jacobian và giá trị hàm F(X) hiện tại
        J, f_x = numerical_jacobian(F, x)
        
        try:
            # Giải hệ phương trình tuyến tính: J * delta_x = -F(X)
            delta_x = np.linalg.solve(J, -f_x)
        except np.linalg.LinAlgError:
            print("-" * 65)
            print("[!] Lỗi: Ma trận Jacobian suy biến (định thức = 0). Thuật toán dừng lại.")
            print("Gợi ý: Hãy thử chọn một giá trị khởi tạo (X0) khác.")
            return x, k

        # Cập nhật nghiệm mới: X_new = X_old + delta_x
        x_new = x + delta_x
        print(f"{k:<10} | {x_new}")

        # Lựa chọn 2: Kiểm tra điều kiện dừng theo epsilon
        if mode == 2:
            sai_so = np.linalg.norm(delta_x, np.inf)
            if sai_so < tol:
                print("-" * 65)
                print(f"[*] Thuật toán HỘI TỤ đạt chuẩn epsilon sau {k} vòng lặp.")
                return x_new, k

        x = x_new

    print("-" * 65)
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
    print("--- BƯỚC 1: THIẾT LẬP HỆ PHƯƠNG TRÌNH F(X) = 0 ---")
    try:
        num_vars = int(input("Nhập số lượng ẩn (VD: 2): "))
        var_names = input("Nhập tên các ẩn, cách nhau bởi khoảng trắng (VD: x y): ").split()
        
        if len(var_names) != num_vars:
            print("Lỗi: Số lượng tên ẩn không khớp!")
            exit()
            
        print("\nNhập các hàm F(X) sao cho F(X) = 0.")
        print("Ví dụ: Nếu pt là x^2 + y^2 = 4, hãy nhập: x**2 + y**2 - 4")
        
        expressions = []
        for i in range(num_vars):
            expr = input(f"F{i+1}({', '.join(var_names)}) = ")
            expressions.append(expr)
            
        # Thư viện toán học (đã fix lỗi {} thay vì None)
        math_env = {
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "exp": np.exp, "log": np.log, "log10": np.log10, "sqrt": np.sqrt,
            "pi": np.pi, "e": np.e
        }
        
        def F_dynamic(vars_values):
            local_env = {name: val for name, val in zip(var_names, vars_values)}
            env = {**math_env, **local_env}
            
            results = []
            for expr in expressions:
                val = eval(expr, {"__builtins__": {}}, env)
                results.append(val)
            return np.array(results, dtype=float)

        print("\n--- BƯỚC 2: NHẬP GIÁ TRỊ KHỞI TẠO ---")
        x_ban_dau = []
        for var in var_names:
            val = float(input(f"Nhập giá trị ban đầu cho {var} (X0): "))
            x_ban_dau.append(val)

        print("\n--- BƯỚC 3: CHỌN CHẾ ĐỘ LẶP ---")
        print("1. Lặp theo số vòng (N)")
        print("2. Lặp theo sai số (epsilon)")
        
        lua_chon = int(input("Nhập lựa chọn của bạn (1 hoặc 2): "))
        
        if lua_chon == 1:
            n_vong = int(input("Nhập số vòng lặp mong muốn: "))
            nghiem, so_vong = newton_raphson_system(F_dynamic, x0=x_ban_dau, mode=1, num_iters=n_vong)
        elif lua_chon == 2:
            epsilon = float(input("Nhập sai số epsilon (VD: 0.0001): "))
            max_n = int(input("Nhập số vòng lặp tối đa (VD: 100): "))
            nghiem, so_vong = newton_raphson_system(F_dynamic, x0=x_ban_dau, mode=2, tol=epsilon, num_iters=max_n)
        else:
            print("Lựa chọn không hợp lệ.")
            exit()
            
        print("\nKẾT QUẢ CUỐI CÙNG:")
        for name, val in zip(var_names, nghiem):
            print(f"{name} ≈ {val:.12f}")
            
    except Exception as e:
        print(f"\nĐã xảy ra lỗi: {e}")