import sys
from PyQt6.QtCore import  Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, \
    QGraphicsDropShadowEffect, QLineEdit


class ResetPasswordView(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setStyleSheet("color: black")
        self.init_ui()

    def init_ui(self):
        # Tạo form
        self.form_widget = QWidget()
        self.form_widget.setStyleSheet("""
                  background-color: white;
                 """)
        self.form_widget.setMinimumSize(400, 400)

        form_layout = QVBoxLayout (self.form_widget)
        # Tạo layout cho main_frame
        resetpw_layout = QVBoxLayout()
        resetpw_layout.addWidget(self.form_widget)
        resetpw_layout.setAlignment(self.form_widget, Qt.AlignmentFlag.AlignCenter)

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
              margin: 20px
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
        resetpw_layout = QVBoxLayout(self)
        resetpw_layout.addWidget(self.form_widget)
        resetpw_layout.setAlignment(self.form_widget, Qt.AlignmentFlag.AlignCenter)


    def go_to_recognitionView(self):
        self.stacked_widget.setCurrentIndex(2)
