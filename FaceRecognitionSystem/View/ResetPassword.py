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


from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QTabWidget
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from MySQLdb import connect
from AttendanceWindow import AttendanceWindow
from NoAttendanceWindow import NoAttendanceWindow

class SystemStatistics(QMainWindow):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setWindowTitle("Thống kê hệ thống")
        self.setGeometry(100, 100, 1200, 700)
        self.setup_ui()  # Gọi hàm thiết lập giao diện
        self.setStyleSheet("background-color: white; color:black;")  # Đặt màu nền và màu chữ


    def setup_ui(self):
        # Tạo layout chính
        main_layout = QVBoxLayout()

        # Tạo QTabWidget và thêm các tab vào
        tab_widget = QTabWidget(self)


        self.password_old_label = QLabel("Mật khẩu cũ")
        self.password_old_label.setStyleSheet("font-size: 15px; font-weight: bold;")

        tab_widget.clear()  # Xóa các tab cũ
        tab_widget.addTab(self.create_statistics_tab(), "Thống kê")
        tab_widget.addTab(self.create_no_attendance_tab(), "Học sinh vắng")
        tab_widget.addTab(self.create_attendance_tab(), "Học sinh đã điểm danh")

        # Thêm QTabWidget vào layout chính
        main_layout.addWidget(tab_widget)


        # Tạo widget trung tâm và đặt layout chính cho nó
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)  # Đặt widget trung tâm cho cửa sổ chính

    def create_statistics_tab(self):
        """Tạo tab thống kê chứa biểu đồ"""
        statistics_tab = QWidget()
        layout = QVBoxLayout()


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

        # Thêm biểu đồ với viền
        chart_widget = self.create_chart_with_border()
        layout.addWidget(chart_widget)

        statistics_tab.setLayout(layout)
        return statistics_tab


    def create_attendance_tab(self):
        """Tạo tab cho học sinh có điểm danh"""
        attendance_tab = QWidget()
        layout = QVBoxLayout()

        # Tạo đối tượng AbsentWindow và thêm vào layout
        self.attendance_window_widget = AttendanceWindow()  # Đảm bảo rằng AbsentWindow là một QWidget hoặc kế thừa QWidget
        layout.addWidget(self.attendance_window_widget)

        attendance_tab.setLayout(layout)
        return attendance_tab

    def create_no_attendance_tab(self):
        """Tạo tab cho học sinh đã điểm danh"""
        no_attendance_tab = QWidget()
        layout = QVBoxLayout()

        # Tạo đối tượng NoAttendanceWindow và thêm vào layout
        self.no_attendance_window_widget = NoAttendanceWindow()  # Đảm bảo rằng NoAttendanceWindow là một QWidget hoặc kế thừa QWidget
        layout.addWidget(self.no_attendance_window_widget)

        no_attendance_tab.setLayout(layout)
        return no_attendance_tab

    def create_chart_with_border(self):
        """Tạo một container chứa biểu đồ với viền và hiệu ứng."""
        # Tạo một QFrame để chứa biểu đồ
        chart_container = QFrame()
        chart_container.setStyleSheet(""" 
            QFrame {
                background-color: #ffffff; /* Nền trắng */
                border: 2px solid #4faaff; /* Viền xanh dương */
                border-radius: 10px;      /* Bo góc */
                padding: 10px;           /* Khoảng cách nội dung */
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); /* Hiệu ứng bóng */
            }
        """)

        # Thêm biểu đồ vào container
        chart_layout = QVBoxLayout()
        chart = self.create_area_chart()  # Gọi hàm tạo biểu đồ
        chart_layout.addWidget(chart)
        chart_container.setLayout(chart_layout)

        return chart_container  # Trả về container chứa biểu đồ

    def create_area_chart(self):
        figure = Figure(figsize=(10, 6))
        ax = figure.add_subplot(111)


        db = connect(
            host='localhost',
            user='root',
            passwd='',
            db="facerecognitionsystem"
        )
        cursor = db.cursor()


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

        query1 = """
        SELECT c.nameC, COUNT(ss.SId) AS present_students_count
        FROM classes c
        JOIN sessions s ON c.CId = s.CId
        JOIN studentsInSessions ss ON s.sessionId = ss.sessionId
        WHERE ss.attendance = 'present'
        GROUP BY c.CId;
        """
        cursor.execute(query1)
        data1 = cursor.fetchall()
        hoc_sinh_co_diem_danh = {row[0]: row[1] for row in data1}

        query2 = """
        SELECT c.nameC, COUNT(ss.SId) AS absent_students_count
        FROM classes c
        JOIN sessions s ON c.CId = s.CId
        JOIN studentsInSessions ss ON s.sessionId = ss.sessionId
        WHERE ss.attendance = 'absent'
        GROUP BY c.CId;

        """
        cursor.execute(query2)
        data2 = cursor.fetchall()
        hoc_sinh_vang = {row[0]: row[1] for row in data2}

        query4 = """
        SELECT c.CId, c.nameC
        FROM classes c
        ORDER BY c.CId;
        """
        cursor.execute(query4)
        data4 = cursor.fetchall()
        class_names = {row[0]: row[1] for row in data4}

        cursor.close()
        db.close()

        # Xử lý dữ liệu cho biểu đồ
        x = [class_names.get(c, str(c)) for c in hoc_sinh_co_diem_danh.keys()]
        sumst = [hoc_sinh_co_diem_danh.get(c, 0) for c in hoc_sinh_co_diem_danh.keys()]
        miss = [hoc_sinh_vang.get(c, 0) for c in hoc_sinh_vang.keys()]

        width = 0.35
        indices = range(len(x))

        ax.bar([i - width / 2 for i in indices], sumst, width=width, color="#F29CA3", label="Số học sinh điểm danh")
        ax.bar([i + width / 2 for i in indices], miss, width=width, color="#64113F", label="Số học sinh vắng")

        ax.set_xticks(indices)
        ax.set_xticklabels(x, rotation=0, ha="right")

        ax.set_title("Thống kê học sinh theo lớp học", fontsize=18, fontweight="bold", pad=20)
        ax.set_ylabel("Số học sinh", fontsize=12, labelpad=10)
        ax.set_xlabel("Lớp học", fontsize=12, labelpad=10)
        ax.tick_params(axis="both", labelsize=10)

        # Di chuyển chú thích ra bên ngoài
        ax.legend(
        loc="upper right",  # Đặt chú thích ở góc trên bên phải
        bbox_to_anchor=(1.0, -0.2),  # Điều chỉnh vị trí chú thích ra ngoài
        ncol=1,  # Sắp xếp theo chiều dọc
        fontsize=10,
        frameon=True  # Tạo khung cho chú thích (tùy chọn)
        )

        ax.set_facecolor("#ffffff")
        # Tăng khoảng cách giữa biểu đồ và rìa dưới
        figure.subplots_adjust(bottom=0.15, left=0.1, right=0.9, top=0.9)
        figure.set_facecolor("#ffffff")
        ax.grid(color="#0E131F", linestyle="--", linewidth=0.5, alpha=0.3)

        # Tự động điều chỉnh khoảng cách
        figure.tight_layout()

        canvas = FigureCanvas(figure)
        return canvas

