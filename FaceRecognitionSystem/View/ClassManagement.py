from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QComboBox, QTableWidget, QVBoxLayout,

    QHBoxLayout, QGroupBox, QGridLayout, QHeaderView, QDateTimeEdit, QTableWidgetItem, QMessageBox, QDialog


)
from PyQt6.QtCore import Qt, QDate
import MySQLdb as mdb

import Global

from Global import GLOBAL_ACCOUNTID



class ClassManagementView(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
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
        header_label = QLabel("Quản lý thông tin lớp học")
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
        student_group = QGroupBox("Thông tin buổi học")
        student_layout = QGridLayout()

        # Các ô nhập liệu thông tin
        self.id_input = QLineEdit()
        self.startTime = QLineEdit()
        self.end_time = QLineEdit()
        self.datetime = QDateTimeEdit(self, calendarPopup=True)
        self.datetime.setDate(QDate.currentDate())  # Ngày mặc định
        self.datetime.setDisplayFormat("dd/MM/yyyy")  # Định dạng hiển thị
        calendar = self.datetime.calendarWidget()
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
        self.sessionName = QLineEdit()
        self.classname = QComboBox()
        class_names = self.loadData()
        self.classname.addItems(class_names)

        # Thêm các thành phần nhập liệu vào lưới
        student_layout.addWidget(QLabel("ID Buổi học:"), 1, 0)
        student_layout.addWidget(self.id_input, 1, 1)
        student_layout.addWidget(QLabel("Tên Buổi học:"), 2, 0)
        student_layout.addWidget(self.sessionName, 2, 1)
        student_layout.addWidget(QLabel("Giờ bắt đầu:"), 3, 0)
        student_layout.addWidget(self.startTime, 3, 1)
        student_layout.addWidget(QLabel("Giờ kết thúc:"), 4, 0)
        student_layout.addWidget(self.end_time, 4, 1)
        student_layout.addWidget(QLabel("Ngày :"), 5, 0)
        student_layout.addWidget(self.datetime, 5, 1)
        student_layout.addWidget(QLabel("Lớp :"), 6, 0)
        student_layout.addWidget(self.classname, 6, 1)

        # Các nút chức năng (Lưu, Sửa, Xóa)
        button_layout = QHBoxLayout()

        self.addclass_button = QPushButton("Thêm lớp học")
        self.addclass_button.setStyleSheet("background-color: black; color: white;")

        self.save_button = QPushButton("Lưu")
        self.save_button.setStyleSheet("background-color: black; color: white;")
        self.edit_button = QPushButton("Sửa")
        self.edit_button.setStyleSheet("background-color: black; color: white;")
        self.delete_button = QPushButton("Xóa")
        self.delete_button.setStyleSheet("background-color: black; color: white;")

        button_layout.addWidget(self.addclass_button)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        student_layout.addLayout(button_layout, 7, 0, 1, 4)  # Thêm hàng nút vào layout lưới
        student_group.setLayout(student_layout)  # Đặt layout cho nhóm

        # ----------- Phần hệ thống tìm kiếm (bên phải) -----------
        table_group = QGroupBox("Hệ Thống Tìm kiếm")  # Nhóm chứa bảng và chức năng tìm kiếm
        table_layout = QVBoxLayout()  # Layout dạng dọc

        # Thanh tìm kiếm
        self.search_combo = QComboBox()
        self.search_combo.addItems(["Tên lớp học"])  # Thêm tiêu chí tìm kiếm
        self.search_input = QLineEdit()
        self.search_button = QPushButton("Tìm kiếm")
        self.view_all_button = QPushButton("Xem tất cả")
        self.table = QTableWidget(5, 5)  # Bảng chứa kết quả tìm kiếm
        self.table.setHorizontalHeaderLabels(["ID","Tên buổi học", "Lớp", "Ngày", "Giờ bắt đầu", "Giờ kết thúc"])  # Đặt tên các cột

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

        self.addclass_button.clicked.connect(self.add_class_popup)

        self.save_button.clicked.connect(self.save_student)
        self.edit_button.clicked.connect(self.edit_student)
        self.delete_button.clicked.connect(self.delete_student)
        self.search_button.clicked.connect(self.search_session)
        self.view_all_button.clicked.connect(self.view_all_students)



    def reset_fields(self):
        self.id_input.clear()
        self.sessionName.clear();
        self.classname.setCurrentIndex(0)  # Chọn lại giá trị mặc định đầu tiên
        self.datetime.setDate(QDate.currentDate())  # Đặt lại ngày hiện tại
        self.end_time.clear()
        self.startTime.clear()


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
        session_id = self.id_input.text()
        sessionName = self.sessionName.text()
        startTime = self.startTime.text()
        endTime = self.end_time.text()
        date = self.datetime.date().toString("yyyy-MM-dd")  # Convert date to the proper format
        className = self.classname.currentText()

        # Câu lệnh SQL để chèn dữ liệu
        try:
            query_class = "SELECT cId FROM classes WHERE nameC = %s"
            cursor.execute(query_class, (className,))
            class_result = cursor.fetchone()

            if class_result:
                class_id = class_result[0]
                query_check = """
                            SELECT sessionId FROM sessions
                            WHERE cId = %s AND sessionDate = %s AND startTime = %s
                            """
                cursor.execute(query_check, (class_id, date, startTime))
                existing_session = cursor.fetchone()

                if existing_session:
                    # Nếu buổi học đã tồn tại, thông báo cho người dùng
                    print("Lỗi: Buổi học này đã tồn tại vào ngày và giờ này!")
                    QMessageBox.warning(self, "Lỗi", "Buổi học đã tồn tại vào ngày và giờ này!")
                else:
                    # Nếu không có buổi học trùng, thực hiện chèn dữ liệu
                    query_session = """
                                INSERT INTO sessions (sessionId, cId, sessionName, sessionDate, startTime, endTime)
                                VALUES (%s, %s, %s, %s, %s, %s)
                                """
                    values = (session_id, class_id, sessionName, date, startTime, endTime)
                    cursor.execute(query_session, values)
                    db.commit()
                    print("Lưu buổi học thành công!")
                    QMessageBox.information(self, "Thành công", "Buổi học đã được lưu thành công!")
                    self.reset_fields()
            else:
                print("Không tìm thấy lớp học phù hợp.")

        except Exception as e:
            print(f"Lỗi khi lưu buổi học: {e}")

        cursor.close()
        db.close()

    def edit_student(self):
    # Kiểm tra dữ liệu ID
        session_id = self.id_input.text().strip()
        if not session_id:
            print("ID buổi học không được để trống!")
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
            sessionName = self.sessionName.text()
            startTime = self.startTime.text()
            endTime = self.end_time.text()
            date = self.datetime.date().toString("yyyy-MM-dd")  # Convert date to the proper format
            className = self.classname.currentText()

            # Kiểm tra dữ liệu đầu vào
            if not sessionName and not startTime and not endTime and not date and not className:
                print("Vui lòng nhập đầy đủ thông tin cần thiết!")
                return

            # Câu lệnh SQL để cập nhật dữ liệu
            query_class = "SELECT cId FROM classes WHERE nameC = %s"
            cursor.execute(query_class, (className,))
            class_result = cursor.fetchone()
            class_id = class_result[0]

            # Câu lệnh SQL để cập nhật dữ liệu buổi học
            query = """
                    UPDATE sessions
                    SET  CId = %s, sessionName = %s, sessionDate = %s, startTime = %s, endTime = %s
                    WHERE sessionId = %s
                    """
            values = (class_id, sessionName, date, startTime, endTime,session_id)

            # Thực thi câu lệnh
            cursor.execute(query, values)
            db.commit()

            # Kiểm tra số hàng bị ảnh hưởng
            if cursor.rowcount == 0:
                print(f"Không tìm thấy buổi học với ID {session_id} để sửa.")
                self.reset_fields()
            else:
                print(f"Sửa thông tin buổi học với ID {session_id} thành công!")
                self.reset_fields()

        except Exception as e:
            print(f"Lỗi khi sửa thông tin buổi học: {e}")
        finally:
            cursor.close()
            db.close()
# nút xóa
    def delete_student(self):
        session_id = self.id_input.text().strip()
        if not session_id:
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
            query = "DELETE FROM sessions WHERE sessionId = %s"
            cursor.execute(query, (session_id,))

            db.commit()
            print(f"Xóa thông tin Học sinh với ID {session_id} thành công!")

            self.reset_fields()  # Reset các ô nhập liệu
        except Exception as e:
            print(f"Lỗi khi xóa học sinh: {e}")
        finally:
            cursor.close()
            db.close()


# tìm kiếm
    def search_session(self):
        keyword = self.search_input.text().strip()

        # Kiểm tra nếu không có từ khóa tìm kiếm
        if not keyword:
            print("Cần nhập từ khóa để tìm kiếm!")

        # Kiểm tra nếu chưa có ID giáo viên (GLOBAL_ACCOUNTID)
        if not Global.GLOBAL_ACCOUNTID:
            print("Chưa đăng nhập hoặc không có ID giáo viên!" + Global.GLOBAL_ACCOUNTID)

        try:
            db = mdb.connect(
                host='localhost',
                user='root',
                passwd='',
                db="facerecognitionsystem"
            )
            cursor = db.cursor()
            print(Global.GLOBAL_ACCOUNTID)
            print("%"+keyword+"%")
            query = """
                   SELECT sessionId,sessionName, classes.nameC, sessionDate, startTime, endTime
                   FROM sessions
                   JOIN classes ON sessions.cId = classes.cId
                   JOIN teachers t ON classes.TId = t.TID
                   WHERE classes.nameC LIKE %s AND t.TID = %s
                   """
            cursor.execute(query, ("%" + keyword +"%", Global.GLOBAL_ACCOUNTID))  # Thêm dấu % vào từ khóa
            results = cursor.fetchall()

            if not results:
                print("Không tìm thấy buổi học nào với từ khóa này.")
                return

            # Cập nhật bảng
            self.table.setRowCount(len(results))
            for row_idx, row_data in enumerate(results):
                for col_idx, col_data in enumerate(row_data):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        except Exception as e:
            print(f"Lỗi khi tìm kiếm: {e}")


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
            query = """
                    SELECT sessionId,sessionName, classes.nameC, sessionDate, startTime, endTime
                    FROM sessions
                    JOIN classes ON sessions.cId = classes.cId
                    JOIN teachers t ON classes.TId = t.TID
                    WHERE t.TID = %s
                    """
            cursor.execute(query, (Global.GLOBAL_ACCOUNTID,))
            results = cursor.fetchall()

            # Kiểm tra nếu không có kết quả
            if not results:
                print("Không có buổi học nào trong hệ thống.")
                self.reset_fields()
                return

            # Cập nhật bảng
            self.table.setRowCount(len(results))  # Cập nhật số dòng trong bảng
            # Điền dữ liệu vào bảng
            for row_idx, row_data in enumerate(results):
                for col_idx, col_data in enumerate(row_data):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        except Exception as e:
            print(f"Lỗi khi xem tất cả: {e}")
            self.reset_fields()
        finally:
            cursor.close()
            db.close()

    def loadData(self):
        # Mảng để chứa dữ liệu
        class_names = []
        print(Global.GLOBAL_ACCOUNTID)

        try:
            # Kết nối đến cơ sở dữ liệu
            db = mdb.connect(
                host='localhost',
                user='root',
                passwd='',
                db="facerecognitionsystem"
            )
            cursor = db.cursor()

            # Truy vấn để lấy tên lớp học
            query = """
                    SELECT nameC
                    FROM classes 
                    JOIN teachers t ON classes.TId = t.TID
                    WHERE t.TID = %s
                    """
            cursor.execute(query, (Global.GLOBAL_ACCOUNTID,))  # Lọc theo giáo viên
            results = cursor.fetchall()

            # Kiểm tra nếu không có kết quả
            if not results:
                print("Không có lớp học nào trong hệ thống.")
                return class_names  # Trả về mảng rỗng

            # Lấy dữ liệu từ kết quả truy vấn và lưu vào mảng class_names
            class_names = [result[0] for result in results]  # result[0] là tên lớp học

        except Exception as e:
            print(f"Lỗi khi tải dữ liệu: {e}")

        finally:
            # Đóng kết nối và cursor
            cursor.close()
            db.close()


        return class_names

    def add_class_popup(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Thêm Lớp Học")
        dialog.setFixedSize(300, 150)

        layout = QVBoxLayout()

        # Nhãn và ô nhập tên lớp học
        label = QLabel("Nhập tên lớp học:")
        class_name_input = QLineEdit()
        class_name_input.setPlaceholderText("Tên lớp học...")

        # Tạo layout hàng ngang cho nút
        button_layout = QHBoxLayout()
        add_button = QPushButton("Thêm")
        cancel_button = QPushButton("Hủy")
        button_layout.addWidget(add_button)
        button_layout.addWidget(cancel_button)

        # Thêm các thành phần vào layout chính
        layout.addWidget(label)
        layout.addWidget(class_name_input)
        layout.addLayout(button_layout)

        dialog.setLayout(layout)

        # Hàm xử lý thêm lớp học
        def handle_add_class():
            class_name = class_name_input.text().strip()
            if not class_name:
                QMessageBox.warning(dialog, "Lỗi", "Tên lớp học không được để trống!")
                return

            try:
                db = mdb.connect(
                    host='localhost',
                    user='root',
                    passwd='',
                    db="facerecognitionsystem"
                )
                cursor = db.cursor()

                # Thực hiện truy vấn để thêm lớp học
                query = "INSERT INTO classes (nameC, TId) VALUES (%s, %s)"
                cursor.execute(query, (class_name, Global.GLOBAL_ACCOUNTID))
                db.commit()

                QMessageBox.information(dialog, "Thành công", "Lớp học đã được thêm thành công!")
                self.classname.addItem(class_name)  # Cập nhật combobox
                dialog.accept()  # Đóng popup

            except Exception as e:
                QMessageBox.critical(dialog, "Lỗi", f"Lỗi khi thêm lớp học: {e}")
            finally:
                cursor.close()
                db.close()

        # Kết nối sự kiện cho nút
        add_button.clicked.connect(handle_add_class)
        cancel_button.clicked.connect(dialog.reject)

        dialog.exec()

