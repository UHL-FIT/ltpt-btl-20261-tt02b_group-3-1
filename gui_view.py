import tkinter as tk
from tkinter import ttk, messagebox

class GUIView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("SmartAttend - PHÂN TÍCH KẾT QUẢ HỌC TẬP")
        self.root.geometry("1100x600")

        # Cấu hình tự động co giãn theo kích thước cửa sổ
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        # 1. Thanh bộ lọc tìm kiếm
        search_frame = tk.LabelFrame(self.root, text=" Tìm kiếm & Bộ lọc ")
        search_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=10)
        
        tk.Label(search_frame, text="Tìm theo:").pack(side=tk.LEFT, padx=5)
        self.cb_search = ttk.Combobox(search_frame, values=["Mã SV", "Họ tên"], width=10, state="readonly")
        self.cb_search.set("Họ tên")
        self.cb_search.pack(side=tk.LEFT, padx=5)
        
        self.ent_search = tk.Entry(search_frame, width=30)
        self.ent_search.pack(side=tk.LEFT, padx=5)
        
        tk.Button(search_frame, text="🔍 Tìm Kiếm", command=self.search_data).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="🔄 Làm Mới", command=self.reset_table).pack(side=tk.LEFT, padx=5)

        # 2. Bảng dữ liệu chính Treeview
        center_frame = tk.Frame(self.root)
        center_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=5)

        columns = ("msv", "ho_ten", "gioi_tinh", "sdt", "diem_kt1", "diem_kt2", "diem_thi", "gpa")
        self.table = ttk.Treeview(center_frame, columns=columns, show="headings")
        
        headers = {
            "msv": "Mã SV", "ho_ten": "Họ và Tên", "gioi_tinh": "Giới Tính", "sdt": "Số ĐT",
            "diem_kt1": "KT1 (20%)", "diem_kt2": "KT2 (30%)", "diem_thi": "Điểm Thi (50%)", "gpa": "ĐTB Học Phần"
        }
        for col, text in headers.items():
            self.table.heading(col, text=text)
            self.table.column(col, anchor=tk.CENTER, width=110)
        self.table.column("ho_ten", width=160, anchor=tk.W)
        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 3. Thanh trạng thái hiển thị Thống kê NumPy
        stats_frame = tk.LabelFrame(self.root, text=" Thống kê số liệu hệ thống (NumPy & Pandas) ")
        stats_frame.grid(row=2, column=0, sticky="ew", padx=15, pady=5)
        
        self.lbl_si_so = tk.Label(stats_frame, text="Sĩ số: 0 SV", font=("Arial", 10, "bold"), fg="blue")
        self.lbl_si_so.pack(side=tk.LEFT, padx=20, pady=5)
        self.lbl_gpa = tk.Label(stats_frame, text="GPA Hệ thống: 0.0", font=("Arial", 10, "bold"), fg="green")
        self.lbl_gpa.pack(side=tk.LEFT, padx=20, pady=5)
        self.lbl_co_cau = tk.Label(stats_frame, text="Cơ cấu: 0 Nam - 0 Nữ", font=("Arial", 10, "bold"), fg="purple")
        self.lbl_co_cau.pack(side=tk.LEFT, padx=20, pady=5)

        # 4. Khu vực nút bấm chức năng CRUD
        btn_frame = tk.Frame(self.root, pady=10)
        btn_frame.grid(row=3, column=0, sticky="ew", padx=15)
        
        tk.Button(btn_frame, text="➕ Thêm Mới Sinh Viên", bg="#28a745", fg="white", font=("Arial", 9, "bold"), command=self.open_add_window).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✏️ Sửa Thông Tin", bg="#ffc107", font=("Arial", 9, "bold"), command=self.open_edit_window).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="❌ Xóa Bản Ghi", bg="#dc3545", fg="white", font=("Arial", 9, "bold"), command=self.delete_data).pack(side=tk.LEFT, padx=5)

    def refresh_table(self, df_data=None):
        for item in self.table.get_children(): 
            self.table.delete(item)
            
        df = df_data if df_data is not None else self.controller.get_all_students()
        for _, r in df.iterrows():
            gpa = round((float(r['diem_kt1']) * 0.2) + (float(r['diem_kt2']) * 0.3) + (float(r['diem_thi']) * 0.5), 2)
            self.table.insert("", tk.END, values=(r['msv'], r['ho_ten'], r['gioi_tinh'], r['sdt'], r['diem_kt1'], r['diem_kt2'], r['diem_thi'], gpa))
        
        stats = self.controller.get_stats()
        self.lbl_si_so.config(text=f"Sĩ số: {stats['si_so']} SV")
        self.lbl_gpa.config(text=f"GPA Trung bình hệ thống: {stats['gpa_tb']}")
        self.lbl_co_cau.config(text=f"Cơ cấu: {stats['nam']} Nam - {stats['nu']} Nữ")

    def search_data(self):
        res = self.controller.search_students(self.ent_search.get(), self.cb_search.get())
        self.refresh_table(res)

    def reset_table(self):
        self.ent_search.delete(0, tk.END)
        self.refresh_table()

    def delete_data(self):
        sel = self.table.selection()
        if not sel: 
            return messagebox.showwarning("Lỗi", "Vui lòng chọn 1 sinh viên trên bảng để xóa!")
        msv = self.table.item(sel[0])['values'][0]
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa sinh viên mang mã {msv}?"):
            # 1. Gọi lệnh xóa dữ liệu trong file CSV
            self.controller.delete_student(msv)
            
            # 2. ĐỂ HẾT LỖI: Ép buộc hệ thống nạp lại file CSV mới sau khi xóa vào bộ nhớ
            self.controller.get_all_students()
            
            # 3. Làm mới và vẽ lại bảng Treeview chính
            self.refresh_table()
            messagebox.showinfo("Thành công", "Đã xóa bản ghi thành công!")
    # --- CỬA SỔ THỨ 2: THÊM MỚI ---
    def open_add_window(self):
        win = tk.Toplevel(self.root)
        win.title("Thêm Sinh Viên")
        win.geometry("380x450")
        win.grab_set()

        fields = ["Mã SV", "Họ Tên", "SĐT", "Điểm KT1", "Điểm KT2", "Điểm Thi"]
        ents = {}
        for f in fields:
            f_frame = tk.Frame(win)
            f_frame.pack(fill="x", padx=20, pady=8)
            tk.Label(f_frame, text=f, width=12, anchor="w").pack(side=tk.LEFT)
            e = tk.Entry(f_frame)
            e.pack(side=tk.RIGHT, expand=True, fill="x")
            ents[f] = e
        
        gen_frame = tk.Frame(win)
        gen_frame.pack(fill="x", padx=20, pady=8)
        tk.Label(gen_frame, text="Giới Tính", width=12, anchor="w").pack(side=tk.LEFT)
        gen = ttk.Combobox(gen_frame, values=["Nam", "Nữ"], state="readonly")
        gen.set("Nam")
        gen.pack(side=tk.RIGHT, expand=True, fill="x")

        def save():
            if not ents["Mã SV"].get() or not ents["Họ Tên"].get():
                messagebox.showwarning("Cảnh báo", "Không được để trống Mã SV và Họ Tên!")
                return
            try:
                data = {
                    'msv': ents["Mã SV"].get(), 'ho_ten': ents["Họ Tên"].get(),
                    'sdt': ents["SĐT"].get(), 'gioi_tinh': gen.get(),
                    'diem_kt1': float(ents["Điểm KT1"].get() if ents["Điểm KT1"].get() else 0),
                    'diem_kt2': float(ents["Điểm KT2"].get() if ents["Điểm KT2"].get() else 0),
                    'diem_thi': float(ents["Điểm Thi"].get() if ents["Điểm Thi"].get() else 0)
                }
                self.controller.add_student(data)
                self.refresh_table()
                win.destroy()
                messagebox.showinfo("Thành công", "Đã thêm sinh viên mới thành công!")
            except ValueError: 
                messagebox.showerror("Lỗi", "Các ô điểm phải nhập số thực!")

        tk.Button(win, text="💾 Lưu Lại", bg="#28a745", fg="white", font=("Arial", 10, "bold"), width=12, command=save).pack(pady=20)

    # --- CỬA SỔ THỨ 3: SỬA (Đã tối ưu làm mới bảng ngay khi bấm cập nhật) ---
    def open_edit_window(self):
        sel = self.table.selection()
        if not sel: 
            return messagebox.showwarning("Lỗi", "Vui lòng click chọn 1 sinh viên trên bảng trước khi bấm nút Sửa!")
        
        # Lấy chính xác dữ liệu của dòng đang chọn
        v = self.table.item(sel[0])['values']

        win = tk.Toplevel(self.root)
        win.title("Sửa Thông Tin Sinh Viên")
        win.geometry("380x450")
        win.grab_set()

        fields = ["Họ Tên", "SĐT", "Điểm KT1", "Điểm KT2", "Điểm Thi"]
        ents = {}
        curr_vals = [v[1], v[3], v[4], v[5], v[6]]
        
        tk.Label(win, text=f"Chỉnh sửa dữ liệu Mã SV: {v[0]}", font=("Arial", 11, "bold"), fg="blue").pack(pady=15)

        for i, f in enumerate(fields):
            f_frame = tk.Frame(win)
            f_frame.pack(fill="x", padx=20, pady=8)
            tk.Label(f_frame, text=f, width=12, anchor="w").pack(side=tk.LEFT)
            e = tk.Entry(f_frame)
            e.insert(0, curr_vals[i]) # Điền sẵn dữ liệu cũ vào ô nhập
            e.pack(side=tk.RIGHT, expand=True, fill="x")
            ents[f] = e

        gen_frame = tk.Frame(win)
        gen_frame.pack(fill="x", padx=20, pady=8)
        tk.Label(gen_frame, text="Giới Tính", width=12, anchor="w").pack(side=tk.LEFT)
        gen = ttk.Combobox(gen_frame, values=["Nam", "Nữ"], state="readonly")
        gen.set(v[2])
        gen.pack(side=tk.RIGHT, expand=True, fill="x")

        def update():
            if not ents["Họ Tên"].get():
                messagebox.showwarning("Cảnh báo", "Không được để trống Họ Tên!")
                return
            try:
                data = {
                    'ho_ten': ents["Họ Tên"].get(), 
                    'sdt': ents["SĐT"].get(),
                    'gioi_tinh': gen.get(),
                    'diem_kt1': float(ents["Điểm KT1"].get()),
                    'diem_kt2': float(ents["Điểm KT2"].get()),
                    'diem_thi': float(ents["Điểm Thi"].get())
                }
                # 1. Ghi dữ liệu mới vào file CSV thông qua Controller
                self.controller.update_student(v[0], data)
                
                # 2. Ép buộc nạp lại dữ liệu mới từ file CSV vào bộ nhớ phần mềm
                self.controller.get_all_students() 
                
                # 3. Làm mới và vẽ lại bảng Treeview chính
                self.refresh_table() 
                
                # 4. Đóng cửa sổ sửa
                win.destroy()
                messagebox.showinfo("Thành công", f"Đã cập nhật thông tin mới cho SV {v[0]}!")
            except ValueError: 
                messagebox.showerror("Lỗi", "Điểm số phải đúng định dạng số thực (Ví dụ: 8.5)!")

        tk.Button(win, text="🛠️ Cập Nhật", bg="#ffc107", font=("Arial", 10, "bold"), width=12, command=update).pack(pady=20)