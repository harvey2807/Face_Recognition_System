from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QComboBox, QTableWidget, QVBoxLayout,
    QHBoxLayout, QGroupBox, QGridLayout, QHeaderView, QDateTimeEdit, QTableWidgetItem, QStackedWidget

)
from PyQt6.QtCore import Qt, QDate
import MySQLdb as mdb
from tensorflow.keras.models import Model
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from scipy.spatial.distance import cosine
import os

class StudentInformationManagement(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = QStackedWidget()
        self.stacked_widget = stacked_widget
        # Thiết lập tiêu đề và kích thước cửa sổ
        self.setWindowTitle("Quản lý thông tin Học sinh")
        self.setGeometry(100, 100, 1200, 700)

        # Định nghĩa CSS để tạo giao diện
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                color: black;
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit, QComboBox, QTableWidget, QDateTimeEdit {
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 6px;
            }
            QPushButton {
                border: 1px solid black;
                border-radius: 4px;
                padding: 8px;
                color white;           
            }
            QPushButton:hover {
                background-color: black;
                color: white;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid gray;
                margin-top: 10px;
                padding: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                padding: 4px;
            }
        """)

        # Layout ngoài cùng chứa toàn bộ nội dung
        outer_layout = QVBoxLayout()

        # Tiêu đề chính
        header_label = QLabel("Quản lý thông tin Học sinh")
        header_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # Căn giữa tiêu đề
        header_label.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: black; margin: 0px; padding: 0px;"
        )
        outer_layout.addWidget(header_label)  # Thêm tiêu đề vào layout ngoài

        # Spacer nhỏ để tạo khoảng cách giữa tiêu đề và nội dung
        outer_layout.addSpacing(10)

        # Layout chính (chứa hai phần: thông tin học sinh và hệ thống tìm kiếm)
        main_layout = QHBoxLayout()

        # ----------- Phần thông tin học sinh (bên trái) -----------
        student_group = QGroupBox("Thông tin Học sinh")  # Nhóm chứa thông tin học sinh
        student_layout = QGridLayout()  # Layout dạng lưới

        # Các ô nhập liệu thông tin
        self.id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.class_input = QLineEdit()
        self.cccd_input = QLineEdit()
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["male", "female", "other"])  # Thêm tùy chọn "Nam" và "Nữ
        self.dob_input = QDateTimeEdit(self, calendarPopup=True)
        self.dob_input.setDate(QDate.currentDate())  # Ngày mặc định
        self.dob_input.setDisplayFormat("dd/MM/yyyy")  # Định dạng hiển thị

        calendar = self.dob_input.calendarWidget()
        calendar.setStyleSheet("""
            QCalendarWidget QTableView {
                selection-background-color: lightblue; /* Màu nền khi chọn */
                selection-color: black; /* Màu chữ khi chọn */
            }

            QCalendarWidget QTableView::item {
                color: black; /* Màu chữ mặc định của các ngày */
                background-color: white; /* Màu nền mặc định của các ngày */
            }

            QCalendarWidget QHeaderView::section {
                background-color: #1E90FF; /* Màu nền của hàng thứ */
                color: white; /* Màu chữ của hàng thứ */
                font-weight: bold;
                border: 1px solid #CCCCCC;
                padding: 5px;
            }
        """)

        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.address_input = QLineEdit()

        # Thêm các thành phần nhập liệu vào lưới
        student_layout.addWidget(QLabel("ID Học sinh:"), 1, 0)
        student_layout.addWidget(self.id_input, 1, 1)
        student_layout.addWidget(QLabel("Tên Học sinh:"), 1, 2)
        student_layout.addWidget(self.name_input, 1, 3)
        student_layout.addWidget(QLabel("Lớp học:"), 2, 0)
        student_layout.addWidget(self.class_input, 2, 1)
        student_layout.addWidget(QLabel("CCCD:"), 2, 2)
        student_layout.addWidget(self.cccd_input, 2, 3)
        student_layout.addWidget(QLabel("Giới tính:"), 3, 0)
        student_layout.addWidget(self.gender_combo, 3, 1)
        student_layout.addWidget(QLabel("Ngày sinh:"), 3, 2)
        student_layout.addWidget(self.dob_input, 3, 3)
        student_layout.addWidget(QLabel("Email:"), 4, 0)
        student_layout.addWidget(self.email_input, 4, 1)
        student_layout.addWidget(QLabel("SĐT:"), 4, 2)
        student_layout.addWidget(self.phone_input, 4, 3)
        student_layout.addWidget(QLabel("Địa chỉ:"), 5, 0)
        student_layout.addWidget(self.address_input, 5, 1)

        # Các nút chức năng (Lưu, Sửa, Xóa)
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Lưu")
        self.save_button.setStyleSheet("background-color: black; color: white;")
        self.edit_button = QPushButton("Sửa")
        self.edit_button.setStyleSheet("background-color: black; color: white;")
        self.delete_button = QPushButton("Xóa")
        self.delete_button.setStyleSheet("background-color: black; color: white;")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        student_layout.addLayout(button_layout, 6, 0, 1, 4)  # Thêm hàng nút vào layout lưới
        student_group.setLayout(student_layout)  # Đặt layout cho nhóm

        # ----------- Phần hệ thống tìm kiếm (bên phải) -----------
        table_group = QGroupBox("Hệ Thống Tìm kiếm")  # Nhóm chứa bảng và chức năng tìm kiếm
        table_layout = QVBoxLayout()  # Layout dạng dọc

        # Thanh tìm kiếm
        self.search_combo = QComboBox()
        self.search_combo.addItems(["ID Học sinh"])  # Thêm tiêu chí tìm kiếm
        self.search_input = QLineEdit()
        self.search_button = QPushButton("Tìm kiếm")
        self.view_all_button = QPushButton("Xem tất cả")
        self.table = QTableWidget(5, 5)  # Bảng chứa kết quả tìm kiếm
        self.table.setHorizontalHeaderLabels(["ID Học sinh", "Họ tên", "CCCD", "Giới tính", "Lớp"])  # Đặt tên các cột

        # Điều chỉnh kích thước các cột trong bảng
        header = self.table.horizontalHeader()
        for i in range(self.table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        # Layout chứa thanh tìm kiếm
        table_search_layout = QHBoxLayout()
        table_search_layout.addWidget(QLabel("Tìm kiếm theo:"))
        table_search_layout.addWidget(self.search_combo)
        table_search_layout.addWidget(self.search_input)
        table_search_layout.addWidget(self.search_button)
        table_search_layout.addWidget(self.view_all_button)

        # Thêm thanh tìm kiếm và bảng vào layout
        table_layout.addLayout(table_search_layout)
        table_layout.addWidget(self.table)
        table_group.setLayout(table_layout)  # Đặt layout cho nhóm

        # ----------- Thêm các phần vào layout chính -----------
        main_layout.addWidget(student_group, 2)  # Phần bên trái (thông tin học sinh)
        main_layout.addWidget(table_group, 2)  # Phần bên phải (hệ thống tìm kiếm)

        # Thêm layout chính vào outer_layout
        outer_layout.addLayout(main_layout)

        # Đặt outer_layout làm layout chính của cửa sổ
        self.setLayout(outer_layout)

        self.save_button.clicked.connect(self.save_student)
        self.edit_button.clicked.connect(self.edit_student)
        self.delete_button.clicked.connect(self.delete_student)
        self.search_button.clicked.connect(self.search_student)
        self.view_all_button.clicked.connect(self.view_all_students)


    def reset_fields(self):
        self.id_input.clear()
        self.name_input.clear()
        self.class_input.clear()
        self.cccd_input.clear()
        self.gender_combo.setCurrentIndex(0)  # Chọn lại giá trị mặc định đầu tiên
        self.dob_input.setDate(QDate.currentDate())  # Đặt lại ngày hiện tại
        self.email_input.clear()
        self.phone_input.clear()
        self.address_input.clear()

    # nút lưu
    def save_student(self):
        db = mdb.connect(
            host='localhost',
            user='root',
            passwd='',
            db="facerecognitionsystem"
        )
        cursor = db.cursor()

        # Lấy dữ liệu từ giao diện
        student_id = self.id_input.text()
        name = self.name_input.text()
        student_class = self.class_input.text()
        cccd = self.cccd_input.text()
        gender = self.gender_combo.currentText()
        dob = self.dob_input.date().toString("yyyy-MM-dd")  # Convert date to the proper format
        email = self.email_input.text()
        phone = self.phone_input.text()
        address = self.address_input.text()

        # Câu lệnh SQL để chèn dữ liệu
        query = """
        INSERT INTO students (nameSt, dob, gender, CCCD, email, address, phone, class)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (name, dob, gender, cccd, email, address, phone, student_class)

        try:
            cursor.execute(query, values)
            db.commit()
            print("Lưu học sinh thành công!")
            self.reset_fields()
        except Exception as e:
            print(f"Lỗi khi lưu học sinh: {e}")
        cursor.close()
        db.close()

    def edit_student(self):

    # Kiểm tra dữ liệu ID

        student_id = self.id_input.text().strip()
        if not student_id:
            print("ID Học sinh không được để trống!")
            return

        try:
            db = mdb.connect(
                host='localhost',
                user='root',
                passwd='',
                db="facerecognitionsystem"
            )
            cursor = db.cursor()

            # Lấy dữ liệu từ giao diện
            name = self.name_input.text().strip()
            student_class = self.class_input.text().strip()
            cccd = self.cccd_input.text().strip()
            gender = self.gender_combo.currentText()
            dob = self.dob_input.date().toString("yyyy-MM-dd")  # Định dạng ngày sinh
            email = self.email_input.text().strip()
            phone = self.phone_input.text().strip()
            address = self.address_input.text().strip()

            # Kiểm tra dữ liệu đầu vào
            if not name or not student_class or not cccd:
                print("Vui lòng nhập đầy đủ thông tin cần thiết!")
                return

            # Câu lệnh SQL để cập nhật dữ liệu
            query = """
            UPDATE students
            SET nameSt = %s, dob = %s, gender = %s, CCCD = %s, email = %s, address = %s, phone = %s, class = %s
            WHERE SId = %s
            """
            values = (name, dob, gender, cccd, email, address, phone, student_class, student_id)

            # Thực thi câu lệnh
            cursor.execute(query, values)
            db.commit()

            # Kiểm tra số hàng bị ảnh hưởng
            if cursor.rowcount == 0:
                print(f"Không tìm thấy Học sinh với ID {student_id} để sửa.")
                self.reset_fields()
            else:
                print(f"Sửa thông tin Học sinh với ID {student_id} thành công!")
                self.reset_fields()

        except Exception as e:
            print(f"Lỗi khi sửa thông tin Học sinh: {e}")
        finally:
            cursor.close()
            db.close()

    # nút xóa
    def delete_student(self):
        student_id = self.id_input.text().strip()
        if not student_id:
            print("Cần nhập ID Học sinh để xóa!")
            return

        try:
            db = mdb.connect(
                host='localhost',
                user='root',
                passwd='',
                db="facerecognitionsystem"
            )
            cursor = db.cursor()

            # Câu lệnh SQL để xóa dữ liệu
            query = "DELETE FROM students WHERE SId = %s"
            cursor.execute(query, (student_id,))

            db.commit()
            print(f"Xóa thông tin Học sinh với ID {student_id} thành công!")
            self.reset_fields()  # Reset các ô nhập liệu
        except Exception as e:
            print(f"Lỗi khi xóa học sinh: {e}")
        finally:
            cursor.close()
            db.close()

# tìm kiếm

    def search_student(self):
        keyword = self.search_input.text()
        if not keyword:
            print("Cần nhập từ khóa để tìm kiếm!")
            return

        try:
            db = mdb.connect(
                host='localhost',
                user='root',
                passwd='',
                db="facerecognitionsystem"
            )
            cursor = db.cursor()
            query = "SELECT SId, nameSt, CCCD, gender, class FROM students WHERE SId = %s"
            cursor.execute(query, (keyword,))
            results = cursor.fetchall()


            # Cập nhật bảng
            self.table.setRowCount(len(results))
            for row_idx, row_data in enumerate(results):
                for col_idx, col_data in enumerate(row_data):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        except Exception as e:
            print(f"Lỗi khi tìm kiếm: {e}")
        finally:
            cursor.close()
            db.close()

        def extract_embeddings_from_foder(model, folder_path):
            embeddings =[]
            list_folder = []

            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if file_name.lower().endswith(('jpg', 'png', 'jpeg')):
                    try:
                        embedding = extract_embedding(model, file_path)
                        embeddings.append(embedding)
                        list_folder.append(file_path)
                    except Exception as e:
                        print(f'Error when process{file_path}:{e}')
            return embedding, list_folder
    # xem tất cả

    def view_all_students(self):
        try:
            db = mdb.connect(
                host='localhost',
                user='root',
                passwd='',
                db="facerecognitionsystem"
            )
            cursor = db.cursor()
            query = "SELECT SId, nameSt, CCCD, gender, class FROM students"
            cursor.execute(query)
            results = cursor.fetchall()

            if not results:
                print("Không có học sinh nào trong hệ thống.")
                self.reset_fields()
                return

            # Cập nhật bảng
            self.table.setRowCount(len(results))
            for row_idx, row_data in enumerate(results):
                for col_idx, col_data in enumerate(row_data):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        except Exception as e:
            print(f"Lỗi khi xem tất cả: {e}")
            self.reset_fields()
        finally:
            cursor.close()
            db.close()

