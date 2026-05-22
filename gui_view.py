import tkinter as tk
from tkinter import ttk, messagebox

class GUIView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("SmartAttend - Khung Giao Diện Tuần 2")
        self.root.geometry("1000x550")
        
        # Cấu hình tự động co giãn (Auto-resize) khi kéo to cửa sổ
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        # --- Thanh tìm kiếm giả định ---
        top_frame = tk.LabelFrame(self.root, text=" Bộ lọc tìm kiếm ")
        top_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=10)
        tk.Label(top_frame, text="Tìm kiếm nhanh:").pack(side=tk.LEFT, padx=5, pady=5)
        tk.Entry(top_frame, width=30).pack(side=tk.LEFT, padx=5, pady=5)

        # --- Bảng hiển thị dữ liệu chính ---
        center_frame = tk.Frame(self.root)
        center_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=5)

        columns = ("msv", "ho_ten", "gioi_tinh", "sdt", "diem_kt1", "diem_kt2", "diem_thi", "gpa")
        self.table = ttk.Treeview(center_frame, columns=columns, show="headings")
        
        headers = {"msv": "Mã SV", "ho_ten": "Họ và Tên", "gioi_tinh": "Giới Tính", "sdt": "Số ĐT",
                   "diem_kt1": "KT1 (20%)", "diem_kt2": "KT2 (30%)", "diem_thi": "Điểm Thi (50%)", "gpa": "ĐTB Học Phần"}
        for col, text in headers.items():
            self.table.heading(col, text=text)
            self.table.column(col, anchor=tk.CENTER, width=110)
        self.table.column("ho_ten", width=160, anchor=tk.W)

        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # --- KHU VỰC THỐNG KÊ TUẦN 2 (Hiện số liệu từ NumPy) ---
        stats_frame = tk.LabelFrame(self.root, text=" Thống kê số liệu hệ thống (Ứng dụng NumPy & Pandas) ")
        stats_frame.grid(row=2, column=0, sticky="ew", padx=15, pady=5)
        
        self.lbl_si_so = tk.Label(stats_frame, text="Sĩ số: 0 SV", font=("Arial", 10, "bold"), fg="blue")
        self.lbl_si_so.pack(side=tk.LEFT, padx=20, pady=5)
        self.lbl_gpa = tk.Label(stats_frame, text="GPA Hệ thống: 0.0", font=("Arial", 10, "bold"), fg="green")
        self.lbl_gpa.pack(side=tk.LEFT, padx=20, pady=5)
        self.lbl_co_cau = tk.Label(stats_frame, text="Cơ cấu Nam/Nữ: 0/0", font=("Arial", 10, "bold"), fg="purple")
        self.lbl_co_cau.pack(side=tk.LEFT, padx=20, pady=5)

        # --- Các nút bấm chờ tiến độ tuần sau ---
        btn_frame = tk.Frame(self.root, pady=10)
        btn_frame.grid(row=3, column=0, sticky="ew", padx=15)
        tk.Button(btn_frame, text="➕ Thêm Mới Sinh Viên", bg="#28a745", fg="white", font=("Arial", 9, "bold"), command=self.wait_week3).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✏️ Sửa Thông Tin", bg="#ffc107", font=("Arial", 9, "bold"), command=self.wait_week3).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="❌ Xóa Bản Ghi", bg="#dc3545", fg="white", font=("Arial", 9, "bold"), command=self.wait_week3).pack(side=tk.LEFT, padx=5)

    def refresh_table(self):
        for item in self.table.get_children(): 
            self.table.delete(item)
            
        students = self.controller.get_all_students()
        for s in students:
            gpa = round((s.diem_kt1 * 0.2) + (s.diem_kt2 * 0.3) + (s.diem_thi * 0.5), 2)
            self.table.insert("", tk.END, values=(s.msv, s.ho_ten, s.gioi_tinh, s.sdt, s.diem_kt1, s.diem_kt2, s.diem_thi, gpa))
        
        # Cập nhật nhãn thống kê từ NumPy
        stats = self.controller.get_stats()
        self.lbl_si_so.config(text=f"Sĩ số: {stats['si_so']} SV")
        self.lbl_gpa.config(text=f"GPA Trung bình hệ thống: {stats['gpa_tb']}")
        self.lbl_co_cau.config(text=f"Cơ cấu: {stats['nam']} Nam - {stats['nu']} Nữ")

    def wait_week3(self):
        messagebox.showinfo("Tiến độ BTL", "Mở các cửa sổ phụ (Sub Windows) thuộc nội dung tiến độ Tuần 3!")