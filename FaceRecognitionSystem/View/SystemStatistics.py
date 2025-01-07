import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QTabWidget, QStackedWidget
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from MySQLdb import connect
from AttendanceWindow import AttendanceWindow
from NoAttendanceWindow import NoAttendanceWindow

class SystemStatistics(QMainWindow):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = QStackedWidget()
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

    # tạo biểu đồ
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

        # Lấy dữ liệu từ database
        query1 = """
        SELECT c.nameC, COUNT(ss.SId) AS present_students_count
        FROM classes c
        JOIN sessions s ON c.CId = s.CId
        JOIN studentsinsessions ss ON s.sessionId = ss.sessionId
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

        cursor.close()
        db.close()

        # In ra dữ liệu kiểm tra
        print("Dữ liệu điểm danh:", hoc_sinh_co_diem_danh)
        print("Dữ liệu vắng:", hoc_sinh_vang)

        # Nếu cả hai cột đều trống, không vẽ biểu đồ
        if not hoc_sinh_co_diem_danh and not hoc_sinh_vang:
            print("Không có dữ liệu để vẽ biểu đồ!")
            return FigureCanvas(figure)  # Trả về biểu đồ trống

        # Chuẩn bị dữ liệu để vẽ biểu đồ
        x = list(set(hoc_sinh_co_diem_danh.keys()).union(hoc_sinh_vang.keys()))
        sumst = [hoc_sinh_co_diem_danh.get(class_name, 0) for class_name in x]
        miss = [hoc_sinh_vang.get(class_name, 0) for class_name in x]

        # Thiết lập các tham số cho biểu đồ
        width = 0.35
        indices = list(range(len(x)))

        # Vẽ các cột dữ liệu
        if any(sumst):  # Nếu có dữ liệu điểm danh
            ax.bar([i - width / 2 for i in indices], sumst, width=width, color="#F29CA3", label="Số học sinh điểm danh")

        if any(miss):  # Nếu có dữ liệu vắng
            ax.bar([i + width / 2 for i in indices], miss, width=width, color="#64113F", label="Số học sinh vắng")

        # Cài đặt trục và nhãn
        ax.set_xticks(indices)
        ax.set_xticklabels(x, rotation=0, ha="right")
        ax.set_title("Thống kê học sinh theo lớp học", fontsize=18, fontweight="bold", pad=20)
        ax.set_ylabel("Số học sinh", fontsize=12, labelpad=10)
        ax.set_xlabel("Lớp học", fontsize=12, labelpad=10)
        ax.tick_params(axis="both", labelsize=10)

        # Di chuyển chú thích ra bên ngoài
        ax.legend(
            loc="upper right",
            bbox_to_anchor=(1.0, -0.2),
            ncol=1,
            fontsize=10,
            frameon=True
        )

        ax.set_facecolor("#ffffff")
        figure.subplots_adjust(bottom=0.15, left=0.1, right=0.9, top=0.9)
        figure.set_facecolor("#ffffff")
        ax.grid(color="#0E131F", linestyle="--", linewidth=0.5, alpha=0.3)
        figure.tight_layout()

        canvas = FigureCanvas(figure)
        return canvas


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = SystemStatistics("")
    main_window.show()
    sys.exit(app.exec())