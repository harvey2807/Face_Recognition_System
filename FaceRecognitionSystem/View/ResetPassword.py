import sys
from PyQt6.QtCore import  Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, \
    QGraphicsDropShadowEffect, QLineEdit, QMessageBox
import MySQLdb as mdb

class ResetPasswordView(QWidget):
    def __init__(self,stacked_widget):
        super().__init__()
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

        self.password_old_label = QLabel("Mật khẩu cũ")
        self.password_old_label.setStyleSheet("font-size: 15px; font-weight: bold;")

        self.password_new_label = QLabel("Mật khẩu mới")
        self.password_new_label.setStyleSheet("font-size: 15px; font-weight: bold;")

        self.password_repeat_label = QLabel("Nhập lại mật khẩu")
        self.password_repeat_label.setStyleSheet("font-size: 15px; font-weight: bold;")

        self.password_old_field = QLineEdit(self, echoMode=QLineEdit.EchoMode.Password)
        self.password_old_field.setPlaceholderText("Mật khẩu cũ")
        self.password_old_field.setStyleSheet("""
            border: 1px solid #CCCCCC;
            border-radius: 4px;
            padding: 5px;
            margin-bottom: 10px;
        """)
        self.password_new_field = QLineEdit(self, echoMode=QLineEdit.EchoMode.Password)
        self.password_new_field.setPlaceholderText("Mật khẩu mới")
        self.password_new_field.setStyleSheet("""
            border: 1px solid #CCCCCC;
            border-radius: 4px;
            padding: 5px;
            margin-bottom: 10px;
        """)
        self.password_repeat_field = QLineEdit(self, echoMode=QLineEdit.EchoMode.Password)
        self.password_repeat_field.setPlaceholderText("Nhập lại mật khẩu mới")
        self.password_repeat_field.setStyleSheet("""
            border: 1px solid #CCCCCC;
            border-radius: 4px;
            padding: 5px;
            margin-bottom: 10px;
        """)

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
        self.confirm_button.clicked.connect(self.resertpassword)

        # place the widget on the window
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

    def resertpassword(self):
        old_pwd = self.password_old_field.text()
        new_pwd = self.password_new_field.text()
        repeat_new_pwd = self.password_repeat_field.text()
        # Kết nối cơ sở dữ liệu
        db = mdb.connect(
            host='localhost',
            user='root',
            passwd='',
            db='facerecognitionsystem'
        )
        cursor = db.cursor()
        # query = "SELECT * FROM teachers WHERE nameTc = %s AND tpassword = %s"
        # cursor.execute(query, (user, pwd))
        kt = cursor.fetchone()
        if kt:
            QMessageBox.information(self, "Reset password", "Update password sucess!")
        else:
            QMessageBox.information(self, "Reset password", "Update password failed!")
        cursor.close()
        db.close()
