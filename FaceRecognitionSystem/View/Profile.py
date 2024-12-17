import sys
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, \
    QGraphicsDropShadowEffect, QLineEdit, QDateEdit, QGroupBox, QRadioButton, QMessageBox
import MySQLdb as mdb

class ProfileView(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setStyleSheet("color: black")
        self.loaddata()
        self.init_form_ui()
    def loaddata(self):
        # Kết nối cơ sở dữ liệu
        db = mdb.connect(
            host='localhost',
            user='root',
            passwd='',
            db='facerecognitionsystem'
        )
        cursor = db.cursor()
        query = "SELECT nameTc, FROM teachers WHERE nameTc = %s"
        cursor.execute(query, (user))
        cursor.fetchone()
        data = cursor.fetchall()  # Lấy tất cả kết quả truy vấn
        pwd = data.row[1]

def init_form_ui(self):
        # Tạo form
        self.form_widget = QWidget()
        self.form_widget.setStyleSheet("""
                  background-color: white;
                  padding: 10px;
              """)
        self.form_widget.setMinimumSize(400, 400)

        form_layout = QVBoxLayout(self.form_widget)

        # Nhãn và trường nhập liệu
        self.user_label = QLabel("Tài khoản ")
        self.user_label.setStyleSheet("font-size: 15px; font-weight: bold; ")

        self.username_field = QLineEdit()
        self.username_field.setStyleSheet("""
            border: 1px solid #cccccc; 
            border-radius: 5px;  /* Tùy chọn bo góc */
            padding: 5px;
            font-size: 14px;
        """)

        self.password_label = QLabel("Mật khẩu ")
        self.password_label.setStyleSheet("font-size: 15px; font-weight: bold; ")
        self.password_field = QLineEdit(self, echoMode=QLineEdit.EchoMode.Password)
        self.password_field.setStyleSheet("""
            border: 1px solid #cccccc; 
            border-radius: 5px; 
            padding: 5px;
            font-size: 14px;
        """)

        self.dob_label = QLabel("Năm sinh: ")
        self.dob_label.setStyleSheet("font-size: 15px; font-weight: bold;")
        self.dob_field = QDateEdit()
        self.dob_field.setStyleSheet("""
            border: 1px solid #cccccc; 
            border-radius: 5px;
            padding: 5px;
            font-size: 14px;
        """)
        self.dob_field.setDate(QDate.currentDate())
        self.dob_field.setMinimumDate(QDate(1900, 1, 1))
        self.dob_field.setMaximumDate(QDate.currentDate())

        self.gender_label = QLabel("Giới tính: ")
        self.gender_label.setStyleSheet("font-size: 15px; font-weight: bold;")

        gender_group = QGroupBox("Chọn giới tính")
        gender_layout = QHBoxLayout()
        self.rb_Male = QRadioButton('Nam')
        self.rb_Female = QRadioButton('Nữ')
        gender_layout.addWidget(self.rb_Male)
        gender_layout.addWidget(self.rb_Female)
        gender_group.setLayout(gender_layout)

        # Nút bấm
        self.update_button = QPushButton('Cập nhật')
        self.update_button.setStyleSheet("""
                      font-size: 15px;
                      padding: 10px;
                      background-color: white;
                      border-radius: 10px;
                      border: 3px solid #FFCD99;
                      margin-top: 20px;
                  """)

        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(10)
        shadow_effect.setXOffset(5)
        shadow_effect.setYOffset(5)
        shadow_effect.setColor(QColor(0, 0, 0, 50))
        self.update_button.setGraphicsEffect(shadow_effect)

        # Thêm vào bố cục
        form_layout.addWidget(self.user_label)
        form_layout.addWidget(self.username_field)
        form_layout.addWidget(self.password_label)
        form_layout.addWidget(self.password_field)
        form_layout.addWidget(self.dob_label)
        form_layout.addWidget(self.dob_field)
        form_layout.addWidget(self.gender_label)
        form_layout.addWidget(gender_group)
        form_layout.addWidget(self.update_button)

        self.form_widget.setLayout(form_layout)

        # Main layout
        login_layout = QVBoxLayout(self)
        login_layout.addWidget(self.form_widget)
        login_layout.setAlignment(self.form_widget, Qt.AlignmentFlag.AlignCenter)

    def go_to_recognitionView(self):
        self.stacked_widget.setCurrentIndex(2)
