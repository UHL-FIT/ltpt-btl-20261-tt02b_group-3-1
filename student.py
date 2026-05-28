import pandas as pd
import numpy as np
import os

class StudentManager:
    def __init__(self, file_path="students.csv"):
        self.file_path = file_path
        self.columns = ['msv', 'ho_ten', 'gioi_tinh', 'sdt', 'diem_kt1', 'diem_kt2', 'diem_thi']
        self.df = pd.DataFrame(columns=self.columns)
        self.load_data()

    def load_data(self):
        if os.path.exists(self.file_path):
            try:
                self.df = pd.read_csv(self.file_path, dtype={'msv': str, 'sdt': str})
            except Exception:
                self.df = pd.DataFrame(columns=self.columns)
        else:
            self.df = pd.DataFrame(columns=self.columns)

    def save_data(self):
        self.df.to_csv(self.file_path, index=False, encoding='utf-8-sig')

    def get_all_students(self):
        return self.df

    def add_student(self, data):
        new_row = pd.DataFrame([data])
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        self.save_data()

    def update_student(self, msv, data):
        # Ép kiểu msv về chuỗi và thêm số 0 ở đầu (ví dụ: từ số 2 thành chuỗi "002") để khớp với file CSV
        msv_str = str(msv).zfill(3) if str(msv).isdigit() else str(msv)
        
        # Tìm vị trí index của sinh viên trong DataFrame
        idx = self.df[self.df['msv'] == msv_str].index
        
        # Nếu không tìm thấy bằng chuỗi "002", tìm thử bằng chuỗi thô "2"
        if idx.empty:
            idx = self.df[self.df['msv'] == str(msv)].index
            
        # Tiến hành ghi đè dữ liệu mới vào bộ nhớ và lưu lại file CSV
        if not idx.empty:
            for key, value in data.items():
                self.df.at[idx[0], key] = value
            self.save_data()
        else:
            print(f"Không tìm thấy Mã SV {msv} trong hệ thống để cập nhật!")

    def delete_student(self, msv):
        # Ép kiểu msv về dạng chuỗi chuẩn (ví dụ: từ số 2 thành "002" hoặc "2" thành "02") để trùng với file CSV
        msv_str = str(msv).zfill(3) if str(msv).isdigit() else str(msv)
        
        # Kiểm tra xem mã dạng "002" có trong danh sách không, nếu có thì xóa
        if msv_str in self.df['msv'].values:
            self.df = self.df[self.df['msv'] != msv_str]
        else:
            # Nếu file CSV lưu dạng chuỗi thô không có số 0 (ví dụ: "2", "6"), ta xóa theo kiểu chuỗi thô
            self.df = self.df[self.df['msv'] != str(msv)]
            
        # Lưu lại file CSV sau khi xóa
        self.save_data()

    def search_students(self, keyword, search_by):
        if not keyword: 
            return self.df
        if search_by == "Mã SV":
            return self.df[self.df['msv'].str.contains(keyword, case=False, na=False)]
        elif search_by == "Họ tên":
            return self.df[self.df['ho_ten'].str.contains(keyword, case=False, na=False)]
        return self.df

    def get_statistics(self):
        if self.df.empty:
            return {"si_so": 0, "gpa_tb": 0.0, "nam": 0, "nu": 0}
        
        si_so = len(self.df)
        kt1 = pd.to_numeric(self.df['diem_kt1'], errors='coerce').fillna(0).to_numpy()
        kt2 = pd.to_numeric(self.df['diem_kt2'], errors='coerce').fillna(0).to_numpy()
        thi = pd.to_numeric(self.df['diem_thi'], errors='coerce').fillna(0).to_numpy()
        
        weights = np.array([0.2, 0.3, 0.5])
        scores_matrix = np.vstack((kt1, kt2, thi))
        gpas = np.dot(weights, scores_matrix)
        
        nam = int((self.df['gioi_tinh'] == 'Nam').sum())
        nu = int((self.df['gioi_tinh'] == 'Nữ').sum())
        
        return {
            "si_so": si_so,
            "gpa_tb": np.round(np.mean(gpas), 2),
            "nam": nam,
            "nu": nu
        }