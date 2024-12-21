from BaseTableWindow import BaseTableWindow
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QHeaderView
)
from PyQt6.QtCore import Qt
import MySQLdb as mdb

class AttendanceWindow(BaseTableWindow):
    def __init__(self):
        super().__init__("Học sinh có điểm danh")

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
        SELECT c.nameC, s.SId,s.nameSt ,ses.sessionName ,ses.sessionDate 
        FROM classes c
        JOIN sessions ses ON c.CId = ses.CId
        JOIN studentsInSessions ss ON ses.sessionId = ss.sessionId
        JOIN students s ON ss.SId = s.SId
        WHERE ss.attendance = 'present'
        ORDER BY c.CId, ss.sessionId, s.nameSt;

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
