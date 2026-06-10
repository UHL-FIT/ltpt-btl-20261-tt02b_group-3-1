from models.student import Student, StudentManager

class AppController:
    def __init__(self):
        self.manager = StudentManager()

    def get_all_students(self):
        return self.manager.get_all_students()

    def add_student(self, msv, ho_ten, gioi_tinh, sdt, diem_kt1=0.0, diem_kt2=0.0, diem_thi=0.0, phat_bieu=0.0, bai_tap=0.0, attendance=None):
        student = Student(msv, ho_ten, gioi_tinh, sdt, diem_kt1, diem_kt2, diem_thi, phat_bieu, bai_tap, attendance)
        self.manager.add_student(student)

    def update_student(self, msv, data):
        return self.manager.update_student(msv, data)

    def delete_student(self, msv):
        return self.manager.delete_student(msv)

    def search_students(self, keyword, search_by):
        return self.manager.search_students(keyword, search_by)

    def import_csv(self, file_path):
        return self.manager.import_from_csv(file_path)

    def export_csv(self, file_path):    
        return self.manager.export_to_csv(file_path)
