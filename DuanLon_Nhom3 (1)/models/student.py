import csv
import os

class Student:
    def __init__(self, msv, ho_ten, gioi_tinh, sdt, diem_kt1=0.0, diem_kt2=0.0, diem_thi=0.0, phat_bieu=0.0, bai_tap=0.0, attendance=None):
        self.msv = msv
        self.ho_ten = ho_ten
        self.gioi_tinh = gioi_tinh
        self.sdt = sdt
        self.diem_kt1 = float(diem_kt1)
        self.diem_kt2 = float(diem_kt2)
        self.diem_thi = float(diem_thi)
        self.phat_bieu = float(phat_bieu)
        self.bai_tap = float(bai_tap)
        # 7 buổi điểm danh, mặc định rỗng
        self.attendance = attendance if attendance else [''] * 7

    def get_diem_chuyen_can(self):
        # Mỗi K trừ 1 điểm, P trừ 0.5 điểm. Cộng điểm phát biểu, bài tập.
        score = 7.0
        count_k = self.attendance.count('K')
        count_p = self.attendance.count('P')
        score -= (count_k * 1.0)
        score -= (count_p * 0.5)
        score += self.phat_bieu
        score += self.bai_tap
        return min(10.0, max(0.0, score))

    def get_dtb(self):
        # Trọng số: Chuyên cần 10%, KT1 20%, KT2 20%, Thi 50%
        cc = self.get_diem_chuyen_can()
        return cc * 0.1 + self.diem_kt1 * 0.2 + self.diem_kt2 * 0.2 + self.diem_thi * 0.5

    def to_dict(self):
        return {
            'msv': self.msv,
            'ho_ten': self.ho_ten,
            'gioi_tinh': self.gioi_tinh,
            'sdt': self.sdt,
            'diem_kt1': self.diem_kt1,
            'diem_kt2': self.diem_kt2,
            'diem_thi': self.diem_thi,
            'phat_bieu': self.phat_bieu,
            'bai_tap': self.bai_tap,
            'attendance': ",".join(self.attendance)
        }

    @classmethod
    def from_dict(cls, data):
        attendance_str = data.get('attendance', '')
        if not attendance_str:
            attendance = [''] * 7
        else:
            attendance = attendance_str.split(',')
        
        # Đảm bảo độ dài là 7
        while len(attendance) < 7:
            attendance.append('')
        attendance = attendance[:7]
        
        return cls(
            msv=data['msv'],
            ho_ten=data['ho_ten'],
            gioi_tinh=data['gioi_tinh'],
            sdt=data['sdt'],
            diem_kt1=data.get('diem_kt1', 0),
            diem_kt2=data.get('diem_kt2', 0),
            diem_thi=data.get('diem_thi', 0),
            phat_bieu=data.get('phat_bieu', 0),
            bai_tap=data.get('bai_tap', 0),
            attendance=attendance
        )


class StudentManager:
    def __init__(self, data_file="d:/moi/duancuatoi/data/students.csv"):
        self.students = []
        self.data_file = data_file
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        self.load_data()

    def add_student(self, student):
        for s in self.students:
            if s.msv == student.msv:
                raise ValueError("Mã sinh viên đã tồn tại!")
            if s.sdt == student.sdt:
                raise ValueError("Số điện thoại đã tồn tại ở sinh viên khác!")
        self.students.append(student)
        self.save_data()

    def update_student(self, msv, updated_data):
        # Kiểm tra trùng SĐT trước khi cập nhật
        if 'sdt' in updated_data:
            for s in self.students:
                if s.msv != msv and s.sdt == updated_data['sdt']:
                    raise ValueError("Số điện thoại đã tồn tại ở sinh viên khác!")

        for idx, s in enumerate(self.students):
            if s.msv == msv:
                # Update attributes
                s.ho_ten = updated_data.get('ho_ten', s.ho_ten)
                s.gioi_tinh = updated_data.get('gioi_tinh', s.gioi_tinh)
                s.sdt = updated_data.get('sdt', s.sdt)
                s.diem_kt1 = float(updated_data.get('diem_kt1', s.diem_kt1))
                s.diem_kt2 = float(updated_data.get('diem_kt2', s.diem_kt2))
                s.diem_thi = float(updated_data.get('diem_thi', s.diem_thi))
                s.phat_bieu = float(updated_data.get('phat_bieu', s.phat_bieu))
                s.bai_tap = float(updated_data.get('bai_tap', s.bai_tap))
                s.attendance = updated_data.get('attendance', s.attendance)
                self.save_data()
                return True
        return False

    def delete_student(self, msv):
        original_len = len(self.students)
        self.students = [s for s in self.students if s.msv != msv]
        if len(self.students) < original_len:
            self.save_data()
            return True
        return False

    def search_students(self, keyword, search_by="Tất cả"):
        keyword = keyword.lower()
        results = []
        for s in self.students:
            match = False
            if search_by == "Tất cả":
                if (keyword in s.msv.lower() or 
                    keyword in s.ho_ten.lower() or 
                    keyword in s.gioi_tinh.lower() or 
                    keyword in s.sdt.lower()):
                    match = True
            elif search_by == "MSV" and keyword in s.msv.lower():
                match = True
            elif search_by == "Họ tên" and keyword in s.ho_ten.lower():
                match = True
            elif search_by == "Giới tính" and keyword in s.gioi_tinh.lower():
                match = True
            elif search_by == "SĐT" and keyword in s.sdt.lower():
                match = True
                
            if match:
                results.append(s)
        return results

    def get_all_students(self):
        return self.students

    def load_data(self):
        if not os.path.exists(self.data_file):
            return
        
        self.students = []
        try:
            with open(self.data_file, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.students.append(Student.from_dict(row))
        except Exception as e:
            print(f"Lỗi khi đọc file: {e}")

    def save_data(self):
        try:
            with open(self.data_file, mode='w', encoding='utf-8', newline='') as f:
                fieldnames = ['msv', 'ho_ten', 'gioi_tinh', 'sdt', 'diem_kt1', 'diem_kt2', 'diem_thi', 'phat_bieu', 'bai_tap', 'attendance']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for s in self.students:
                    writer.writerow(s.to_dict())
        except Exception as e:
            print(f"Lỗi khi lưu file: {e}")

    def import_from_csv(self, file_path):
        count = 0
        try:
            with open(file_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Bỏ qua nếu msv đã tồn tại
                    if any(s.msv == row['msv'] for s in self.students):
                        continue
                    self.students.append(Student.from_dict(row))
                    count += 1
            self.save_data()
            return count, ""
        except Exception as e:
            return 0, str(e)

    def export_to_csv(self, file_path):
        try:
            with open(file_path, mode='w', encoding='utf-8', newline='') as f:
                fieldnames = ['msv', 'ho_ten', 'gioi_tinh', 'sdt', 'diem_kt1', 'diem_kt2', 'diem_thi', 'phat_bieu', 'bai_tap', 'attendance']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for s in self.students:
                    writer.writerow(s.to_dict())
            return True, ""
        except Exception as e:
            return False, str(e)
