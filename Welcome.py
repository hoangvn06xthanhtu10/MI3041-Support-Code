import os
import subprocess
import sys

SCRIPTS = {
    "1": os.path.join("Equation", "PhuongPhapChiaDoi (Hybrid).py"),
    "2": os.path.join("Equation", "PhuongPhapDayCung (Hybrid).py"),
    "3": os.path.join("Equation", "PhuongPhapLapDon(Hybrid).py"),
    "4": os.path.join("Equation", "PhuongPhapTiepTuyen (Hybrid).py"),
    "5": os.path.join("MoreEquation", "PhuongPhapLapDonGiaiHPTPhiTuyenTinh(Hybrid).py"),
    "6": os.path.join("MoreEquation", "PhuongPhapTiepTuyenGiaiHPTPhiTuyenTinh(Hybrid).py")
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    while True:
        clear_screen()
        print("=" * 75)
        print("    HỆ THỐNG TÌM NGHIỆM GIẢI TÍCH SỐ (HYBRID - TÍNH TOÁN LAI)    ")
        print("=" * 75)
        print(" [I] PHƯƠNG TRÌNH PHI TUYẾN 1 ẨN: f(x) = 0")
        print("   1. Phương pháp Chia Đôi")
        print("   2. Phương pháp Dây Cung")
        print("   3. Phương pháp Lặp Đơn")
        print("   4. Phương pháp Tiếp Tuyến (Newton)")
        print("-" * 75)
        print(" [II] HỆ PHƯƠNG TRÌNH PHI TUYẾN: F(X) = 0")
        print("   5. Phương pháp Lặp Đơn (Hệ Phương Trình)")
        print("   6. Phương pháp Tiếp Tuyến - Newton (Hệ Phương Trình)")
        print("-" * 75)
        print("   0. Thoát chương trình")
        print("=" * 75)
        
        # ---> DÒNG BẠN MUỐN THÊM VÀO ĐÂY <---
        print(" Current Version: v1.0.0(240326)")
        print(" Dự kiến bản cập nhật tiếp theo: v1.0.1(310326)")
        print("=" * 75)

        choice = input(" Nhập số thứ tự phương pháp bạn muốn sử dụng (0-6): ")

        if choice == "0":
            print("\n Cảm ơn bạn đã sử dụng hệ thống! Tạm biệt.")
            break
            
        elif choice in SCRIPTS:
            script_name = SCRIPTS[choice]
            
            if os.path.exists(script_name):
                clear_screen()
                print(f"[*] Đang khởi chạy module: {script_name}...\n")
                try:
                    subprocess.run([sys.executable, script_name])
                except Exception as e:
                    print(f"\n[!] Lỗi trong quá trình chạy file: {e}")
                
                print("\n" + "." * 75)
                input(" [Enter] Nhấn phím Enter để quay lại Menu chính...")
            else:
                print(f"\n[!] Lỗi: Không tìm thấy file '{script_name}'!")
                print("    Vui lòng kiểm tra lại xem tên file có khớp chính xác không.")
                input("\n [Enter] Nhấn phím Enter để quay lại Menu chính...")
                
        else:
            print("\n[!] Lựa chọn không hợp lệ. Vui lòng nhập số từ 0 đến 6.")
            input(" [Enter] Nhấn phím Enter để thử lại...")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n Đã ép buộc dừng chương trình. Tạm biệt!")
        sys.exit(0)