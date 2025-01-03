import sys
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, \
    QGraphicsDropShadowEffect, QLineEdit, QDateEdit, QGroupBox, QRadioButton, QMessageBox, QStackedWidget
import MySQLdb as mdb


class ProfileView(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = QStackedWidget()
        self.stacked_widget = stacked_widget
        self.username = ''
        self.dob = ''
        self.gender = ''
        self.setStyleSheet("color: black")
        self.loaddata()
        self.init_form_ui()

    def loaddata(self):
        # Kết nối cơ sở dữ liệu
        username = "PhamVanTinh"
        db = mdb.connect(
            host='localhost',
            user='root',
            passwd='',
            db='facerecognitionsystem'
        )
        cursor = db.cursor()
        query = "SELECT * FROM teachers WHERE nameTc = %s"
        cursor.execute(query, (username,))
        data = cursor.fetchone()

        if data:
            self.username = data[1]
            dob_date = data[2]
            self.gender = data[4]
            self.dob = QDate(dob_date.year, dob_date.month, dob_date.day)
        else:
            print("Không tìm thấy dữ liệu.")

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
        self.username_field.setText(self.username)
        print(self.username)

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
        self.dob_field.setDate(self.dob)

        self.gender_label = QLabel("Giới tính: ")
        self.gender_label.setStyleSheet("font-size: 15px; font-weight: bold;")

        gender_group = QGroupBox("Chọn giới tính")
        gender_layout = QHBoxLayout()
        self.rb_Male = QRadioButton('Nam')
        self.rb_Female = QRadioButton('Nữ')
        gender_layout.addWidget(self.rb_Male)
        gender_layout.addWidget(self.rb_Female)
        gender_group.setLayout(gender_layout)
        if self.gender.lower() == 'male':
            self.rb_Male.setChecked(True)
        elif self.gender.lower() == 'female':
            self.rb_Female.setChecked(True)

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
        self.update_button.clicked.connect(self.update)

        # Thêm vào bố cục
        form_layout.addWidget(self.user_label)
        form_layout.addWidget(self.username_field)
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

    def update(self):
        # Kết nối cơ sở dữ liệu
        db = mdb.connect(
            host='localhost',
            user='root',
            passwd='',
            db='facerecognitionsystem'
        )
        cursor = db.cursor()

        # Lấy dữ liệu từ form
        new_username = self.username_field.text()
        new_dob = self.dob_field.date().toString("yyyy-MM-dd")
        new_gender = "Male" if self.rb_Male.isChecked() else "Female"

        # Kiểm tra sự thay đổi
        is_changed = False

        # Kiểm tra từng trường
        if new_username != self.username:
            is_changed = True
        if new_dob != self.dob:
            is_changed = True
        if new_gender != self.gender:
            is_changed = True

        # Nếu không có gì thay đổi
        if not is_changed:
            QMessageBox.information(self, "Update", "No changes were made.")
            cursor.close()
            db.close()
            return
        else:
            # Câu lệnh SQL để cập nhật dữ liệu
            query = """UPDATE teachers SET nameTc = %s, dob = %s, gender = %s WHERE nameTc = %s"""
            values = (new_username, new_dob, new_gender, self.username)

            try:
                cursor.execute(query, values)
                db.commit()
                print("Cập nhật thành công!")
                QMessageBox.information(self, "Update information", "Update sucess!")
            except Exception as e:
                print(f"Lỗi khi cập nhật: {e}")
                QMessageBox.information(self, "Update information", "Update failed!")

            cursor.close()
            db.close()

