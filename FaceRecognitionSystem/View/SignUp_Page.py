import sys

from PyQt6.QtCore import Qt, QTimer, QDate, QTime
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtWidgets import QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect, \
    QLineEdit, QPushButton, QMessageBox, QDateEdit, QRadioButton
import MySQLdb as mdb

class SignUpView(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.central_widget = QWidget(self)

        # Tạo layout chính
        self.main_layout = QVBoxLayout(self.central_widget)
        self.panel = QFrame(self.central_widget)
        self.header_panel = QFrame(self.panel)
        self.clock_panel = QFrame(self.header_panel)

        self.stacked_widget = stacked_widget

        # Set the window title
        self.setWindowTitle('Face Recognition System')
        self.setGeometry(0, 0, 1200, 700)        # Show the window
        self.setStyleSheet("color: black")
        self.init_ui()

    def init_ui(self):
        # Tạo một widget trung tâm
        self.central_widget.setFixedSize( 1200, 700)
        self.central_widget.setStyleSheet("background-color: lightblue;")

        # Tạo panel (QFrame)
        self.panel.setFixedSize(600, 500)
        self.panel.setStyleSheet("""
                   background-color: white;
                   border-radius: 10px;
               """)

        # Thêm panel vào layout
        self.main_layout.addWidget(self.panel)
        self.main_layout.setAlignment(self.panel, Qt.AlignmentFlag.AlignCenter)

        # Create a header panel (QFrame)
        self.header_panel.setGeometry(0, 0, 600, 50)
        self.header_panel.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
            border-bottom: 1px solid black;;
        """)

        # Create a panel to hold the clock icon (QFrame)
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
        self.title_panel.setGeometry(200, 5, 200, 40)
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
        self.form_widget.setMinimumSize(350, 350)

        form_layout = QVBoxLayout (self.form_widget)
        # Tạo layout cho main_frame
        login_layout = QVBoxLayout(self.panel)
        login_layout.addWidget(self.form_widget)
        login_layout.setAlignment(self.form_widget, Qt.AlignmentFlag.AlignCenter)

        # Tạo các trường nhập liệu
        self.user_label = QLabel("Tài khoản ")
        self.user_label.setStyleSheet("font-size: 15px; font-weight: bold;")

        self.password_label = QLabel("Mật khẩu ")
        self.password_label.setStyleSheet("font-size: 15px; font-weight: bold;")

        self.dob_label =QLabel ("Năm sinh: ")
        self.dob_label.setStyleSheet("font-size: 15px; font-weight: bold;")

        self.gender_label = QLabel("Giới tính: ")
        self.gender_label.setStyleSheet("font-size: 15px; font-weight: bold;")

        self.username_field = QLineEdit()
        self.dob_field = QDateEdit()
        self.dob_field.setDate(QDate.currentDate())
        self.rb_Male = QRadioButton('Male', self)
        self.rb_Female = QRadioButton('Female', self)
        self.password_field = QLineEdit(self, echoMode=QLineEdit.EchoMode.Password)

        # Tạo nút Xác nhận
        self.signup_button = QPushButton('Đăng kí')
        self.signup_button.setStyleSheet("""
              font-size: 15px;
              padding: 10px;
              background-color: white;
              border-radius: 10px;
              border: 3px solid #FFCD99;
              margin-top: 20px
          """)

        # Áp dụng hiệu ứng bóng (shadow) cho đăng nhập
        shadow_effect = QGraphicsDropShadowEffect(self.signup_button)
        shadow_effect.setBlurRadius(10)
        shadow_effect.setXOffset(5)
        shadow_effect.setYOffset(5)
        shadow_effect.setColor(QColor(0, 0, 0, 50))
        self.signup_button.setGraphicsEffect(shadow_effect)

        # Tạo nút Đăng ký (Sign up)
        self.goback_button = QPushButton('Quay lại')
        self.goback_button.setStyleSheet("""
                    font-size: 15px;
                    font-style: italic;
                    text-decoration: underline;
                    background: transparent;
                    border: none;
                    padding: 0px;
                """)
        self.goback_button.setFixedHeight(40)
        self.goback_button.setFixedWidth(330)

        # place the widget on the window
        form_layout.addWidget(self.user_label)
        form_layout.addWidget(self.username_field)
        form_layout.addWidget(self.password_label)
        form_layout.addWidget(self.password_field)
        form_layout.addWidget(self.dob_label)
        form_layout.addWidget(self.dob_field)
        form_layout.addWidget(self.gender_label)
        form_layout.addWidget(self.rb_Male)
        form_layout.addWidget(self.rb_Female)
        form_layout.addWidget(self.signup_button)
        form_layout.addWidget(self.goback_button)
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
        self.signup_button.clicked.connect(self.sign_up)
        self.goback_button.clicked.connect(self.go_back_login)
        self.show()

    def sign_up(self):
        user = self.username_field.text()
        pwd = self.password_field.text()
        dob = str(self.dob_field.date().toPyDate())

        # Kiểm tra giới tính đã chọn
        gender = None
        if self.rb_Male.isChecked():
            gender = 'male'
        elif self.rb_Female.isChecked():
            gender = 'female'

        # Kết nối cơ sở dữ liệu
        db = mdb.connect(
            host='localhost',
            user='root',
            passwd='',
            db='facerecognitionsystem'
        )
        cursor = db.cursor()
        query = "SELECT * FROM teachers WHERE nameTc = %s AND tpassword = %s"
        cursor.execute(query, (user, pwd))
        kt = cursor.fetchone()
        if kt:
            QMessageBox.information(self, "Signup output", "Account already exists")
            self.reset_form()
        else:
            QMessageBox.information(self, "Signup output", "Account already exists")
            query = "INSERT INTO teachers(nameTc, dob, tpassword, gender) values (%s,%s,%s,%s)"
            cursor.execute(query, (user, dob, pwd, gender))
            db.commit()
            QMessageBox.information(self, "Signup output", "Signup success")


    def go_back_login(self):
        print("dang nhập")
        self.stacked_widget.setCurrentIndex(0)

    def update_time(self):
        # Get current time and date
        current_time = QTime.currentTime().toString("hh:mm:ss")
        current_date = QDate.currentDate().toString("dd/MM/yyyy")

        # Update labels
        self.time_label.setText(current_time)
        self.date_label.setText(current_date)

    def reset_form(self):
        self.username_field.clear()
        self.password_field.clear()
        self.dob_field.setDate(QDate.currentDate())
        self.rb_Male.setChecked(False)
        self.rb_Female.setChecked(False)
