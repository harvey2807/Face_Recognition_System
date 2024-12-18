from BaseTableWindow import BaseTableWindow
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QHeaderView
)
from PyQt6.QtCore import Qt
import MySQLdb as mdb

class NoAttendanceWindow(BaseTableWindow):
    def __init__(self):
        super().__init__("Học sinh không điểm danh")

        # Kết nối đến cơ sở dữ liệu
        db = mdb.connect(
            host='localhost',
            user='root',
            passwd='',
            db="facerecognitionsystem"
        )
        cursor = db.cursor()

        # Truy vấn dữ liệu
        query = """
        SELECT s.SId, s.nameSt, c.nameC, c.dateC
        FROM classes c
        LEFT JOIN students s 
            ON s.SId NOT IN (
                SELECT SId FROM studentsofclass WHERE CId = c.CId
            )
        WHERE s.SId IS NOT NULL
        ORDER BY s.SId ASC
        """
        cursor.execute(query)
        data = cursor.fetchall()

        # Điền dữ liệu vào bảng
        self.table.setRowCount(len(data))
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

        # Đóng kết nối
        cursor.close()
        db.close()
