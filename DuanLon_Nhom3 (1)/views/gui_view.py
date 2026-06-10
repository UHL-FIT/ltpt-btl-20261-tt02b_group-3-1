import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class GUIView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("SmartAttend - Hệ Thống Quản Lý Sinh Viên")
        self.root.geometry("1000x700")

        # Variables for form
        self.var_msv = tk.StringVar()
        self.var_hoten = tk.StringVar()
        self.var_gioitinh = tk.StringVar(value="Nam")
        self.var_sdt = tk.StringVar()
        self.var_kt1 = tk.DoubleVar()
        self.var_kt2 = tk.DoubleVar()
        self.var_thi = tk.DoubleVar()
        self.var_phatbieu = tk.DoubleVar()
        self.var_baitap = tk.DoubleVar()
        
        # Variables for attendance (7 sessions)
        self.var_att = [tk.StringVar(value="") for _ in range(7)]
        
        # Search variables
        self.var_search_by = tk.StringVar(value="Tất cả")
        self.var_search_keyword = tk.StringVar()

        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        # --- Top Frame: Search & Actions ---
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(top_frame, text="Tìm kiếm theo:").pack(side=tk.LEFT, padx=5)
        search_cb = ttk.Combobox(top_frame, textvariable=self.var_search_by, values=["Tất cả", "MSV", "Họ tên", "Giới tính", "SĐT"], state="readonly", width=10)
        search_cb.pack(side=tk.LEFT, padx=5)
        
        tk.Entry(top_frame, textvariable=self.var_search_keyword, width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Tìm kiếm", command=self.search_students, bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Làm mới", command=self.refresh_table, bg="#9E9E9E", fg="white").pack(side=tk.LEFT, padx=5)
        
        tk.Button(top_frame, text="Xem KQ Học Tập", command=self.show_study_results, bg="#009688", fg="white").pack(side=tk.RIGHT, padx=5)
        tk.Button(top_frame, text="Giới thiệu", command=self.show_about, bg="#9C27B0", fg="white").pack(side=tk.RIGHT, padx=5)
        tk.Button(top_frame, text="Export CSV", command=self.export_csv, bg="#4CAF50", fg="white").pack(side=tk.RIGHT, padx=5)
        tk.Button(top_frame, text="Import CSV", command=self.import_csv, bg="#FF9800", fg="white").pack(side=tk.RIGHT, padx=5)

        # --- Stats Frame ---
        stats_frame = tk.LabelFrame(self.root, text="Thống kê chung", fg="#0d47a1", font=("Arial", 9, "bold"))
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.lbl_siso = tk.Label(stats_frame, text="Sĩ số: 0", font=("Arial", 10, "bold"))
        self.lbl_siso.pack(side=tk.LEFT, padx=15, pady=5)
        
        self.lbl_namnu = tk.Label(stats_frame, text="Nam/Nữ: 0/0", font=("Arial", 10, "bold"))
        self.lbl_namnu.pack(side=tk.LEFT, padx=15, pady=5)

        # --- Middle Frame: Treeview ---
        mid_frame = tk.Frame(self.root)
        mid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        scroll_y = tk.Scrollbar(mid_frame)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ("MSV", "HoTen", "GioiTinh", "SDT", "KP", "CP", "TongVang", "PhatBieu", "BaiTap", "CC", "KT1", "KT2", "Thi", "DTB")
        self.tree = ttk.Treeview(mid_frame, columns=columns, show="headings", yscrollcommand=scroll_y.set)
        
        self.tree.heading("MSV", text="MSV")
        self.tree.heading("HoTen", text="Họ tên")
        self.tree.heading("GioiTinh", text="Giới tính")
        self.tree.heading("SDT", text="SĐT")
        self.tree.heading("KP", text="Không Phép")
        self.tree.heading("CP", text="Có Phép")
        self.tree.heading("TongVang", text="Tổng Vắng")
        self.tree.heading("PhatBieu", text="Phát Biểu")
        self.tree.heading("BaiTap", text="Bài Tập")
        self.tree.heading("CC", text="CC")
        self.tree.heading("KT1", text="KT 1")
        self.tree.heading("KT2", text="KT 2")
        self.tree.heading("Thi", text="Thi")
        self.tree.heading("DTB", text="ĐTB")

        self.tree.column("MSV", width=80, anchor=tk.CENTER)
        self.tree.column("HoTen", width=140, anchor=tk.W)
        self.tree.column("GioiTinh", width=60, anchor=tk.CENTER)
        self.tree.column("SDT", width=90, anchor=tk.CENTER)
        self.tree.column("KP", width=80, anchor=tk.CENTER)
        self.tree.column("CP", width=60, anchor=tk.CENTER)
        self.tree.column("TongVang", width=80, anchor=tk.CENTER)
        self.tree.column("PhatBieu", width=80, anchor=tk.CENTER)
        self.tree.column("BaiTap", width=70, anchor=tk.CENTER)
        self.tree.column("CC", width=40, anchor=tk.CENTER)
        self.tree.column("KT1", width=40, anchor=tk.CENTER)
        self.tree.column("KT2", width=40, anchor=tk.CENTER)
        self.tree.column("Thi", width=40, anchor=tk.CENTER)
        self.tree.column("DTB", width=50, anchor=tk.CENTER)

        # Tag configuration for colors
        self.tree.tag_configure("normal", background="white")
        self.tree.tag_configure("banned", background="black", foreground="white")

        self.tree.pack(fill=tk.BOTH, expand=True)
        scroll_y.config(command=self.tree.yview)
        
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # --- Bottom Frame: Form ---
        bot_frame = tk.LabelFrame(self.root, text="Thông tin chi tiết")
        bot_frame.pack(fill=tk.X, padx=10, pady=10)

        # Row 0: Basic Info
        tk.Label(bot_frame, text="MSV:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Entry(bot_frame, textvariable=self.var_msv, width=15).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(bot_frame, text="Họ tên:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        tk.Entry(bot_frame, textvariable=self.var_hoten, width=25).grid(row=0, column=3, padx=5, pady=5)

        tk.Label(bot_frame, text="Giới tính:").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        ttk.Combobox(bot_frame, textvariable=self.var_gioitinh, values=["Nam", "Nữ"], state="readonly", width=8).grid(row=0, column=5, padx=5, pady=5)

        tk.Label(bot_frame, text="SĐT:").grid(row=0, column=6, padx=5, pady=5, sticky=tk.W)
        tk.Entry(bot_frame, textvariable=self.var_sdt, width=15).grid(row=0, column=7, padx=5, pady=5)

        # Row 1: Scores
        tk.Label(bot_frame, text="Điểm KT1:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Entry(bot_frame, textvariable=self.var_kt1, width=15).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(bot_frame, text="Điểm KT2:").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        tk.Entry(bot_frame, textvariable=self.var_kt2, width=15).grid(row=1, column=3, padx=5, pady=5)

        tk.Label(bot_frame, text="Điểm Thi:").grid(row=1, column=4, padx=5, pady=5, sticky=tk.W)
        tk.Entry(bot_frame, textvariable=self.var_thi, width=15).grid(row=1, column=5, padx=5, pady=5)

        # Row 2: Attendance & Additional Points
        tk.Label(bot_frame, text="Phát biểu:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Entry(bot_frame, textvariable=self.var_phatbieu, width=15).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(bot_frame, text="Bài tập:").grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
        tk.Entry(bot_frame, textvariable=self.var_baitap, width=15).grid(row=2, column=3, padx=5, pady=5)

        att_frame = tk.Frame(bot_frame)
        att_frame.grid(row=2, column=4, columnspan=4, pady=5, sticky=tk.W)
        tk.Label(att_frame, text="Điểm danh:").pack(side=tk.LEFT, padx=5)
        for i in range(7):
            tk.Label(att_frame, text=f"B{i+1}").pack(side=tk.LEFT)
            ttk.Combobox(att_frame, textvariable=self.var_att[i], values=["", "M", "P", "K"], state="readonly", width=3).pack(side=tk.LEFT, padx=2)

        # Row 3: Action Buttons
        btn_frame = tk.Frame(bot_frame)
        btn_frame.grid(row=3, column=0, columnspan=8, pady=10)
        
        tk.Button(btn_frame, text="Thêm Mới", command=self.add_student, bg="#4CAF50", fg="white", width=12).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Cập Nhật", command=self.update_student, bg="#2196F3", fg="white", width=12).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Xóa", command=self.delete_student, bg="#f44336", fg="white", width=12).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Clear Form", command=self.clear_form, bg="#9E9E9E", fg="white", width=12).pack(side=tk.LEFT, padx=10)

    def refresh_table(self, students=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        if students is None:
            students = self.controller.get_all_students()
            
        siso = len(students)
        nam = 0
        nu = 0

        for s in students:
            # Thống kê
            if s.gioi_tinh == "Nam":
                nam += 1
            else:
                nu += 1
            
            dtb = s.get_dtb()
            
            kp = s.attendance.count('K')
            cp = s.attendance.count('P')
            tong_vang = kp + cp

            if tong_vang > 3:
                tag = "banned"
                self.tree.insert("", tk.END, values=(
                    s.msv, s.ho_ten, s.gioi_tinh, s.sdt,
                    kp, cp, tong_vang, "", "", "", "", "", "", ""
                ), tags=(tag,))
            else:
                tag = "normal"
                self.tree.insert("", tk.END, values=(
                    s.msv, s.ho_ten, s.gioi_tinh, s.sdt,
                    kp, cp, tong_vang, 
                    s.phat_bieu, s.bai_tap,
                    f"{s.get_diem_chuyen_can():.1f}", 
                    s.diem_kt1, s.diem_kt2, s.diem_thi, f"{dtb:.2f}"
                ), tags=(tag,))

        # Cập nhật UI thống kê
        if hasattr(self, 'lbl_siso'):
            self.lbl_siso.config(text=f"Sĩ số: {siso}")
            self.lbl_namnu.config(text=f"Nam/Nữ: {nam}/{nu}")

    def on_select(self, event):
        selected = self.tree.focus()
        if not selected:
            return
            
        values = self.tree.item(selected, 'values')
        if not values:
            return
            
        msv = values[0]
        students = self.controller.search_students(msv, "MSV")
        if students:
            s = students[0]
            self.var_msv.set(s.msv)
            self.var_hoten.set(s.ho_ten)
            self.var_gioitinh.set(s.gioi_tinh)
            self.var_sdt.set(s.sdt)
            self.var_kt1.set(s.diem_kt1)
            self.var_kt2.set(s.diem_kt2)
            self.var_thi.set(s.diem_thi)
            self.var_phatbieu.set(s.phat_bieu)
            self.var_baitap.set(s.bai_tap)
            for i in range(7):
                if i < len(s.attendance):
                    self.var_att[i].set(s.attendance[i])

    def clear_form(self):
        self.var_msv.set("")
        self.var_hoten.set("")
        self.var_gioitinh.set("Nam")
        self.var_sdt.set("")
        self.var_kt1.set(0.0)
        self.var_kt2.set(0.0)
        self.var_thi.set(0.0)
        self.var_phatbieu.set(0.0)
        self.var_baitap.set(0.0)
        for i in range(7):
            self.var_att[i].set("")

    def add_student(self):
        msv = self.var_msv.get().strip()
        ho_ten = self.var_hoten.get().strip()
        sdt = self.var_sdt.get().strip()
        
        if not msv:
            messagebox.showwarning("Cảnh báo", "Mã sinh viên không được để trống!")
            return
            
        if not (sdt.isdigit() and len(sdt) == 10):
            messagebox.showwarning("Cảnh báo", "Số điện thoại phải bao gồm đúng 10 chữ số!")
            return
            
        try:
            k1 = self.var_kt1.get()
            k2 = self.var_kt2.get()
            thi = self.var_thi.get()
            pb = self.var_phatbieu.get()
            bt = self.var_baitap.get()
            if not (0 <= k1 <= 10 and 0 <= k2 <= 10 and 0 <= thi <= 10):
                messagebox.showwarning("Cảnh báo", "Điểm số phải nằm trong khoảng từ 0 đến 10!")
                return
        except tk.TclError:
            messagebox.showwarning("Cảnh báo", "Điểm số không hợp lệ!")
            return
            
        try:
            self.controller.add_student(
                msv=msv,
                ho_ten=ho_ten,
                gioi_tinh=self.var_gioitinh.get(),
                sdt=sdt,
                phat_bieu=pb,
                bai_tap=bt
            )
            
            # Immediately update the attendance and scores if provided
            att_data = [var.get() for var in self.var_att]
            data = {
                'diem_kt1': k1,
                'diem_kt2': k2,
                'diem_thi': thi,
                'phat_bieu': pb,
                'bai_tap': bt,
                'attendance': att_data
            }
            self.controller.update_student(msv, data)
            
            self.refresh_table()
            messagebox.showinfo("Thành công", "Đã thêm sinh viên mới!")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def update_student(self):
        msv = self.var_msv.get()
        sdt = self.var_sdt.get().strip()
        
        if not msv:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sinh viên để cập nhật!")
            return
            
        if not (sdt.isdigit() and len(sdt) == 10):
            messagebox.showwarning("Cảnh báo", "Số điện thoại phải bao gồm đúng 10 chữ số!")
            return
            
        try:
            k1 = self.var_kt1.get()
            k2 = self.var_kt2.get()
            thi = self.var_thi.get()
            pb = self.var_phatbieu.get()
            bt = self.var_baitap.get()
            if not (0 <= k1 <= 10 and 0 <= k2 <= 10 and 0 <= thi <= 10):
                messagebox.showwarning("Cảnh báo", "Điểm số phải nằm trong khoảng từ 0 đến 10!")
                return
        except tk.TclError:
            messagebox.showwarning("Cảnh báo", "Điểm số không hợp lệ!")
            return
            
        try:
            att_data = [var.get() for var in self.var_att]
            data = {
                'ho_ten': self.var_hoten.get(),
                'gioi_tinh': self.var_gioitinh.get(),
                'sdt': sdt,
                'diem_kt1': k1,
                'diem_kt2': k2,
                'diem_thi': thi,
                'phat_bieu': pb,
                'bai_tap': bt,
                'attendance': att_data
            }
            if self.controller.update_student(msv, data):
                self.refresh_table()
                messagebox.showinfo("Thành công", "Cập nhật thành công!")
            else:
                messagebox.showerror("Lỗi", "Không tìm thấy sinh viên.")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def delete_student(self):
        msv = self.var_msv.get()
        if not msv:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sinh viên để xóa!")
            return
            
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa SV {msv}?"):
            if self.controller.delete_student(msv):
                self.clear_form()
                self.refresh_table()
                messagebox.showinfo("Thành công", "Đã xóa sinh viên.")
            else:
                messagebox.showerror("Lỗi", "Không tìm thấy sinh viên.")

    def search_students(self):
        keyword = self.var_search_keyword.get()
        search_by = self.var_search_by.get()
        results = self.controller.search_students(keyword, search_by)
        self.refresh_table(results)

    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            count, error = self.controller.import_csv(file_path)
            if error:
                messagebox.showerror("Lỗi Import", str(error))
            else:
                self.refresh_table()
                messagebox.showinfo("Thành công", f"Đã import {count} sinh viên.")

    def export_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            success, error = self.controller.export_csv(file_path)
            if success:
                messagebox.showinfo("Thành công", "Xuất file thành công!")
            else:
                messagebox.showerror("Lỗi Export", str(error))

    def show_about(self):
        about_text = (
            "PHẦN MỀM: SMARTATTEND\n"
            "-------------------------\n"
            "Phiên bản: 1.0.0\n"
            "Tác giả: ThS. Vũ Duy Sơn\n"
            "Đơn vị: Trường Đại học Hạ Long (UHL)\n"
            "Ngày phát hành: 03/05/2026\n"
            "-------------------------\n"
            "Phần mềm hỗ trợ quản lý sinh viên và điểm danh chuyên cần tự động."
        )
        messagebox.showinfo("Giới thiệu", about_text)

    def show_study_results(self):
        students = self.controller.get_all_students()
        if not students:
            messagebox.showinfo("Thông báo", "Đang cập nhật thông tin")
            return
            
        has_scores = any(s.diem_thi > 0 or s.get_dtb() > 0 for s in students)
        if not has_scores:
            messagebox.showinfo("Thông báo", "Đang cập nhật thông tin")
            return

        try:
            import matplotlib.pyplot as plt
            import numpy as np
        except ImportError:
            messagebox.showerror("Lỗi", "Yêu cầu cài đặt thư viện 'matplotlib' (pip install matplotlib) để xem biểu đồ.")
            return

        bin_labels = [f"{i}-{i+1}" for i in range(10)]
        thi_counts = [0] * 10
        dtb_counts = [0] * 10
        
        tong_thi = 0.0
        tong_dtb = 0.0

        for s in students:
            # Điểm thi
            thi = s.diem_thi
            tong_thi += thi
            if thi > 0:
                thi_idx = min(int(thi), 9) if thi < 10 else 9
                thi_counts[thi_idx] += 1
            
            # Điểm trung bình
            dtb = s.get_dtb()
            tong_dtb += dtb
            if dtb > 0:
                dtb_idx = min(int(dtb), 9) if dtb < 10 else 9
                dtb_counts[dtb_idx] += 1
            
        total = len(students)
        thi_pct = [(c / total) * 100 for c in thi_counts]
        dtb_pct = [(c / total) * 100 for c in dtb_counts]

        tb_thi = (tong_thi / total) if total > 0 else 0.0
        tb_dtb = (tong_dtb / total) if total > 0 else 0.0

        x = np.arange(len(bin_labels))
        width = 0.35

        fig, ax = plt.subplots(figsize=(10, 6))
        rects1 = ax.bar(x - width/2, thi_pct, width, label='Điểm Thi', color='#2196F3')
        rects2 = ax.bar(x + width/2, dtb_pct, width, label='Điểm Trung Bình', color='#4CAF50')

        ax.set_ylabel('Phần trăm (%)')
        ax.set_title(f'Phổ điểm Thi và Điểm Trung Bình\n(Trung bình Điểm Thi: {tb_thi:.2f} - ĐTB Học phần: {tb_dtb:.2f})')
        ax.set_xticks(x)
        ax.set_xticklabels(bin_labels)
        ax.legend()

        fig.tight_layout()
        plt.show()
