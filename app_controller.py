from student import StudentManager

class AppController:
    def __init__(self):
        self.manager = StudentManager()

    def get_all_students(self):
        self.manager.load_data()
        return self.manager.get_all_students()

    def add_student(self, data):
        self.manager.add_student(data)

    def update_student(self, msv, data):
        self.manager.update_student(msv, data)

    def delete_student(self, msv):
        self.manager.delete_student(msv)

    def search_students(self, keyword, search_by):
        return self.manager.search_students(keyword, search_by)

    def get_stats(self):
        return self.manager.get_statistics()