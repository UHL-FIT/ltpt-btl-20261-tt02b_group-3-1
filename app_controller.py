from student import StudentManager

class AppController:
    def __init__(self):
        self.manager = StudentManager()

    def get_all_students(self):
        # Gọi Model để làm mới danh sách sinh viên
        self.manager.load_data()
        return self.manager.get_all_students()

    def get_stats(self):
        return self.manager.get_statistics()