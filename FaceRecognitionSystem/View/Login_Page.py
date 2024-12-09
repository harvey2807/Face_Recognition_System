import sys

from PyQt6.QtCore import Qt, QTimer, QDate, QTime
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtWidgets import QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout, QApplication, QGraphicsDropShadowEffect, \
    QLineEdit, QPushButton


class MainWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        # Set the window title
        self.setWindowTitle('Face Recognition System')
        self.setGeometry(0, 0, 1200, 700)        # Show the window
        self.setStyleSheet("color: black")
        self.init_ui()

    def init_ui(self):
        # Tạo một widget trung tâm
        central_widget = QWidget(self)
        central_widget.setFixedSize( 1200, 700)
        central_widget.setStyleSheet("background-color: lightblue;")

        # Tạo layout chính
        main_layout = QVBoxLayout(central_widget)

        # Tạo panel (QFrame)
        self.panel = QFrame(central_widget)  # Đặt central_widget làm parent
        self. panel.setFixedSize(1100, 650)
        self.panel.setStyleSheet("""
                   background-color: white;
                   border-radius: 10px;
               """)

        # Thêm panel vào layout
        main_layout.addWidget(self.panel)
        main_layout.setAlignment(self.panel, Qt.AlignmentFlag.AlignCenter)

        # Create a header panel (QFrame)
        self.header_panel = QFrame(self.panel)
        self.header_panel.setGeometry(0, 0, 1100, 50)
        self.header_panel.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
            border-bottom: 1px solid black;;
        """)

        # Create a panel to hold the clock icon (QFrame)
        self.clock_panel = QFrame(self.header_panel)
        self.clock_panel.setGeometry(5, 5, 50, 40)  # Adjust the size and position as needed
        self.clock_panel.setStyleSheet("border: none;")

        # Create a label to hold the clock icon inside the clock panel
        self.clock_icon = QLabel(self.clock_panel)
        self.clock_icon.setPixmap(QPixmap('../Image/clock-icon.png').scaled(35, 30))  # Adjust icon size as needed
        self.clock_icon.setGeometry(5, 5, 35, 30)

        # Create a panel to hold the time and date labels (QFrame)
        self.time_date_panel = QFrame(self.header_panel)
        self.time_date_panel.setGeometry(50, 5, 150, 40)
        self.time_date_panel.setStyleSheet("border: none;")


        # Create a vertical layout to hold the time and date labels
        time_date_layout = QVBoxLayout(self.time_date_panel)
        time_date_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for better alignment

        # Create a label to display the time
        self.time_label = QLabel(self.time_date_panel)
        self.time_label.setStyleSheet("font-size: 12px; font-weight: bold;")
        self.time_label.setStyleSheet("border: none;")
        time_date_layout.addWidget(self.time_label)  # Add time_label to layout

        # Create a label to display the date
        self.date_label = QLabel(self.time_date_panel)
        self.date_label.setStyleSheet("font-size: 12px; font-weight: bold;")
        self.date_label.setStyleSheet("border: none;")
        time_date_layout.addWidget(self.date_label)  # Add date_label to layout


        # Title panel (Centered)
        self.title_panel = QFrame(self.header_panel)
        self.title_panel.setGeometry(300, 5, 550, 40)
        self.title_panel.setStyleSheet("border: none;")
        title_layout = QHBoxLayout(self.title_panel)
        title_layout.setContentsMargins(0, 0, 0, 0)

        self.title_label = QLabel("Đăng nhập")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(self.title_label)

        # Tạo form
        self.form_widget = QWidget(self.panel)
        self.form_widget.setStyleSheet("""
                  background-color: white;
                 """)
        self.form_widget.setMinimumSize(350, 250)

        form_layout = QVBoxLayout (self.form_widget)
        # Tạo layout cho main_frame
        login_layout = QVBoxLayout(self.panel)
        login_layout.addWidget(self.form_widget)
        login_layout.setAlignment(self.form_widget, Qt.AlignmentFlag.AlignCenter)

        # Tạo các trường nhập liệu
        self.user_label = QLabel("Tài khoản ")
        self.user_label.setStyleSheet("font-size: 15px; font-weight: bold;")

        self.password_old_label = QLabel("Mật khẩu ")
        self.password_old_label.setStyleSheet("font-size: 15px; font-weight: bold;")

        self.username_field = QLineEdit()
        self.password_old_field = QLineEdit(self, echoMode=QLineEdit.EchoMode.Password)

        # Tạo nút Xác nhận
        self.login_button = QPushButton('Đăng nhập')
        self.login_button.setStyleSheet("""
              font-size: 15px;
              padding: 10px;
              background-color: white;
              border-radius: 10px;
              border: 3px solid #FFCD99;
              margin: 20px
          """)
        self.login_button.clicked.connect(self.go_to_homepage)

        # Áp dụng hiệu ứng bóng (shadow) cho nút
        shadow_effect = QGraphicsDropShadowEffect(self.login_button)
        shadow_effect.setBlurRadius(10)
        shadow_effect.setXOffset(5)
        shadow_effect.setYOffset(5)
        shadow_effect.setColor(QColor(0, 0, 0, 50))
        self.login_button.setGraphicsEffect(shadow_effect)

        # place the widget on the window
        form_layout.addWidget(self.user_label)
        form_layout.addWidget(self.username_field)
        form_layout.addWidget(self.password_old_label)
        form_layout.addWidget(self.password_old_field)
        form_layout.addWidget(self.login_button)
        self.form_widget.setLayout(form_layout)

        # Tạo layout cho main_frame và thêm form_widget vào
        login_layout = QVBoxLayout(self)
        login_layout.addWidget(self.form_widget)
        login_layout.setAlignment(self.form_widget, Qt.AlignmentFlag.AlignCenter)

        # Timer to update time and date every second
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)

        self.update_time()
        self.show()

    def update_time(self):
        # Get current time and date
        current_time = QTime.currentTime().toString("hh:mm:ss")
        current_date = QDate.currentDate().toString("dd/MM/yyyy")

        # Update labels
        self.time_label.setText(current_time)
        self.date_label.setText(current_date)

    def go_to_homepage(self):
        # Chuyển sang trang chủ
        self.stacked_widget.setCurrentIndex(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create the main window
    window = MainWindow()

    # Start the event loop
    sys.exit(app.exec())
