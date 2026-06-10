import sys
import tkinter as tk
from controllers.app_controller import AppController
from views.gui_view import GUIView  

def main():
    controller = AppController()
    
    # Kiểm tra xem người dùng có muốn chạy CLI không
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        try:
            from views.cli_view import CLIView
            cli = CLIView(controller)
            cli.display_menu()
        except ImportError:
            print("Lỗi: Module CLI chưa được tạo hoặc đã bị xóa.")
    else:
        # Mặc định chạy GUI
        root = tk.Tk()
        app = GUIView(root, controller)
        root.mainloop()

if __name__ == "__main__":
    main()
