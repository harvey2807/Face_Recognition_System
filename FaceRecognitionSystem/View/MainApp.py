import sys

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QApplication
from Login_Page import LoginView
from SignUp_Page import SignUpView
from Home import HomeView

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget()
        # Set the window title
        self.setWindowTitle('Face Recognition System')
        self.setGeometry(50, 40, 1200, 700)
        self.setFixedSize(1200, 700)
        self.setStyleSheet("color: black")
        self.init_ui()

    def init_ui(self):
        # Thêm các trang
        self.login_page = LoginView(self.stacked_widget)
        self.signup_page = SignUpView(self.stacked_widget)
        self.view_page = HomeView()

        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.signup_page)
        self.stacked_widget.addWidget(self.view_page)


        # Thiết lập trang đầu tiên
        self.stacked_widget.setCurrentIndex(0)

        # Layout chính
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec())