import sys
from PyQt6.QtCore import QTimer, QTime, QDate, Qt
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtWidgets import QApplication, QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, \
    QGraphicsDropShadowEffect, QLineEdit, QFormLayout


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle('Face Recognition System')
        self.setGeometry(50, 50, 1200, 700)        # Show the window
        self.setFixedSize(1200, 700)
        self.setStyleSheet("background-color: lightblue;")

        # Create a white panel (QFrame)
        self.panel = QFrame(self)
        self.panel.setGeometry(25, 25, 1150, 650)
        self.panel.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
        """)

        # Create a header panel (QFrame)
        self.header_panel = QFrame(self.panel)
        self.header_panel.setGeometry(0, 0, 1150, 50)
        self.header_panel.setStyleSheet("""
            background-color: white;
            border-top-right-radius: 10px;
            border-top-left-radius: 10px;
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

        self.title_label = QLabel("Hệ thống nhận diện khuôn mặt")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(self.title_label)

        # Tạo menu bên trái
        self.menu_widget = QWidget(self.panel)
        menu_layout = QVBoxLayout(self.menu_widget)
        self.menu_widget.setGeometry(5, 65, 120, 570)

        buttons = ["Trang chủ", "Quản lý", "Nhận diện", "Mật khẩu", "Thoát"]
        for button in buttons:
            # Tạo hiệu ứng shadow thật
            shadow_effect_btn = QGraphicsDropShadowEffect()
            shadow_effect_btn.setBlurRadius(10)  # Độ nhòe của bóng
            shadow_effect_btn.setXOffset(5)  # Độ dịch ngang
            shadow_effect_btn.setYOffset(5)  # Độ dịch dọc
            shadow_effect_btn.setColor(QColor(0, 0, 0, 50))  # Màu của bóng (đen mờ)

            btn = QPushButton(button)
            btn.setFixedSize(110, 110)
            btn.setStyleSheet(
                "font-size: 15px; "
                "padding: 10px; "
                "background-color: white; "
                "border-radius: 10px;"
                "border: 3px solid #FFCD99;"
                "margin:5px"
            )
            btn.setGraphicsEffect(shadow_effect_btn)
            menu_layout.addWidget(btn)

        # Tạo main frame chính
        self.main_frame = QFrame(self.panel)
        self.main_frame.setGeometry(130, 65, 1000, 570)
        self.main_frame.setStyleSheet("""
            background-color: #FFCC99;
           """)

        # Tạo hiệu ứng shadow thật
        shadow_effect = QGraphicsDropShadowEffect(self.main_frame)
        shadow_effect.setBlurRadius(10)  # Độ nhòe của bóng
        shadow_effect.setXOffset(5)  # Độ dịch ngang
        shadow_effect.setYOffset(5)  # Độ dịch dọc
        shadow_effect.setColor(QColor(0, 0, 0, 50))  # Màu của bóng (đen mờ)
        self.main_frame.setGraphicsEffect(shadow_effect)

        # Tạo form
        self.form_widget = QWidget(self.main_frame)
        # self.form_widget.setGeometry(130, 65, 120, 570)
        self.form_widget.setStyleSheet("""
                  background-color: white;
                 """)

        form_layout = QVBoxLayout (self.form_widget)
        # Tạo layout cho main_frame
        main_layout = QVBoxLayout(self.main_frame)
        main_layout.addWidget(self.form_widget)
        main_layout.setAlignment(self.form_widget, Qt.AlignmentFlag.AlignCenter)

        # Tạo các trường nhập liệu
        self.user_label = QLabel("Tài khoản")
        self.user_label.setStyleSheet("font-size: 15px; font-weight: bold;")

        self.password_old_label = QLabel("Mật khẩu cũ")
        self.password_old_label.setStyleSheet("font-size: 15px; font-weight: bold;")

        self.password_new_label = QLabel("Mật khẩu mới")
        self.password_new_label.setStyleSheet("font-size: 15px; font-weight: bold;")

        self.password_repeat_label = QLabel("Nhập lại mật khẩu")
        self.password_repeat_label.setStyleSheet("font-size: 15px; font-weight: bold;")

        self.username_field = QLineEdit()
        self.password_old_field = QLineEdit(self, echoMode=QLineEdit.EchoMode.Password)
        self.password_new_field = QLineEdit(self, echoMode=QLineEdit.EchoMode.Password)
        self.password_repeat_field = QLineEdit(self, echoMode=QLineEdit.EchoMode.Password)

        # Tạo nút Xác nhận
        self.confirm_button = QPushButton('Xác nhận')
        self.confirm_button.setStyleSheet("""
              font-size: 15px;
              padding: 10px;
              background-color: white;
              border-radius: 10px;
              border: 3px solid #FFCD99;
          """)
        # Áp dụng hiệu ứng bóng (shadow) cho nút
        shadow_effect = QGraphicsDropShadowEffect(self.confirm_button)
        shadow_effect.setBlurRadius(10)
        shadow_effect.setXOffset(5)
        shadow_effect.setYOffset(5)
        shadow_effect.setColor(QColor(0, 0, 0, 50))
        self.confirm_button.setGraphicsEffect(shadow_effect)


        # place the widget on the window
        form_layout.addWidget(self.user_label)
        form_layout.addWidget(self.username_field)
        form_layout.addWidget(self.password_old_label)
        form_layout.addWidget(self.password_old_field)
        form_layout.addWidget(self.password_new_label)
        form_layout.addWidget(self.password_new_field)
        form_layout.addWidget(self.password_repeat_label)
        form_layout.addWidget(self.password_repeat_field)
        form_layout.addWidget(self.confirm_button)
        self.form_widget.setLayout(form_layout)

        # Tạo layout cho main_frame và thêm form_widget vào
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.form_widget)
        main_layout.setAlignment(self.form_widget, Qt.AlignmentFlag.AlignCenter)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create the main window
    window = MainWindow()

    # Start the event loop
    sys.exit(app.exec())
