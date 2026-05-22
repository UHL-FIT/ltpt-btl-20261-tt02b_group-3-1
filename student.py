import csv
import os
import pandas as pd
import numpy as np

class Student:
    def __init__(self, msv, ho_ten, gioi_tinh, sdt, diem_kt1=0.0, diem_kt2=0.0, diem_thi=0.0):
        self.msv = msv
        self.ho_ten = ho_ten
        self.gioi_tinh = gioi_tinh
        self.sdt = sdt
        self.diem_kt1 = float(diem_kt1) if diem_kt1 else 0.0
        self.diem_kt2 = float(diem_kt2) if diem_kt2 else 0.0
        self.diem_thi = float(diem_thi) if diem_thi else 0.0

class StudentManager:
    def __init__(self, file_path="students.csv"):
        self.file_path = file_path
        self.students = []
        self.load_data()

    def load_data(self):
        self.students = []
        if os.path.exists(self.file_path):
            with open(self.file_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    s = Student(
                        row['msv'], 
                        row['ho_ten'], 
                        row['gioi_tinh'], 
                        row['sdt'],
                        row.get('diem_kt1', 0.0), 
                        row.get('diem_kt2', 0.0), 
                        row.get('diem_thi', 0.0)
                    )
                    self.students.append(s)

    def get_all_students(self):
        return self.students

    # 🛠️ DÙNG NUMPY & PANDAS TÍNH THỐNG KÊ (Đáp ứng yêu cầu tuần 2)
    def get_statistics(self):
        if not os.path.exists(self.file_path) or len(self.students) == 0:
            return {"si_so": 0, "gpa_tb": 0.0, "nam": 0, "nu": 0}
        
        # Sử dụng Pandas đọc nhanh file để lấy mảng dữ liệu
        df = pd.read_csv(self.file_path)
        si_so = len(df)
        
        # Chuyển đổi các cột sang mảng NumPy để xử lý tính toán
        kt1 = pd.to_numeric(df['diem_kt1'], errors='coerce').fillna(0.0).to_numpy()
        kt2 = pd.to_numeric(df['diem_kt2'], errors='coerce').fillna(0.0).to_numpy()
        thi = pd.to_numeric(df['diem_thi'], errors='coerce').fillna(0.0).to_numpy()
        
        # Dùng mảng NumPy tính điểm trung bình môn học (Hệ số: 20%, 30%, 50%)
        weights = np.array([0.2, 0.3, 0.5])
        all_scores = np.vstack((kt1, kt2, thi))
        gpa_per_student = np.dot(weights, all_scores)
        gpa_tb = np.round(np.mean(gpa_per_student), 2)
        
        nam = int((df['gioi_tinh'].str.lower() == 'nam').sum())
        nu = si_so - nam
        
        return {"si_so": si_so, "gpa_tb": gpa_tb, "nam": nam, "nu": nu}