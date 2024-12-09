import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QTabWidget
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from FaceRecognitionSystem.View.AbsentWindow import AbsentWindow
from FaceRecognitionSystem.View.NoAttendanceWindow import NoAttendanceWindow

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

        tab_widget.clear()  # Xóa các tab cũ
        tab_widget.addTab(self.create_statistics_tab(), "Thống kê")
        tab_widget.addTab(self.create_no_attendance_tab(), "Học sinh vắng")
        tab_widget.addTab(self.create_absent_tab(), "Học sinh đã điểm danh")

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


    def create_absent_tab(self):
        """Tạo tab cho học sinh vắng"""
        absent_tab = QWidget()
        layout = QVBoxLayout()

        # Tạo đối tượng AbsentWindow và thêm vào layout
        self.absent_window_widget = AbsentWindow()  # Đảm bảo rằng AbsentWindow là một QWidget hoặc kế thừa QWidget
        layout.addWidget(self.absent_window_widget)

        absent_tab.setLayout(layout)
        return absent_tab

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
        """Tạo biểu đồ dạng vùng (area chart) với phong cách mềm mại."""
        # Tạo đối tượng Figure từ matplotlib
        figure = Figure(figsize=(10, 6))
        ax = figure.add_subplot(111)

        # Dữ liệu mẫu
        x = ["Buổi 1", "Buổi2", "Buổi 3", "Buổi 4", "Buổi 5"]
        sumst = [10, 30, 25, 20, 15]  # Tổng số học sinh
        miss = [15, 25, 20, 30, 10]   # Số lần vắng
        dd = [40, 15, 10, 25, 20]     # Số bản điểm danh

        # Vẽ biểu đồ dạng vùng
        ax.fill_between(x, sumst, color="#F8E71C", alpha=0.7, label="Số học sinh")
        ax.fill_between(x, miss, color="#F5A623", alpha=0.7, label="Số lần vắng")
        ax.fill_between(x, dd, color="#80B354", alpha=0.7, label="Số bản điểm danh")

        # Hiển thị giá trị lên các điểm dữ liệu
        for i, value in enumerate(sumst):
            ax.text(i, value + 2, f"{value}", color="#ffffff", fontsize=9, ha="center", va="bottom")
        for i, value in enumerate(miss):
            ax.text(i, value + 2, f"{value}", color="#ffffff", fontsize=9, ha="center", va="bottom")
        for i, value in enumerate(dd):
            ax.text(i, value + 2, f"{value}", color="#ffffff", fontsize=9, ha="center", va="bottom")

        # Cài đặt tiêu đề, trục và phong cách
        ax.set_title("Thống kê hệ thống", fontsize=18, fontweight="bold", color="#ffffff", pad=20)
        ax.set_ylabel("Số lần", fontsize=12, color="#ffffff", labelpad=10)
        ax.set_xlabel("Buổi", fontsize=12, color="#ffffff", labelpad=10)
        ax.tick_params(axis="both", colors="#ffffff", labelsize=10)
        ax.legend(loc="upper right", fontsize=10, facecolor="#4a4a4a", edgecolor="none", labelcolor="white")

        # Cài đặt nền và lưới
        ax.set_facecolor("#838CC7")  # Nền cho biểu đồ
        figure.set_facecolor("#838CC7")  # Nền cho toàn bộ figure
        ax.grid(color="#ffffff", linestyle="--", linewidth=0.5, alpha=0.3)

        # Căn chỉnh khoảng cách và bo góc
        figure.subplots_adjust(top=0.85, bottom=0.15, left=0.1, right=0.9)

        # Nhúng biểu đồ vào PyQt
        canvas = FigureCanvas(figure)
        return canvas


