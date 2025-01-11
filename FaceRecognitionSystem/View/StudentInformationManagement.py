from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QComboBox, QTableWidget, QVBoxLayout,
    QHBoxLayout, QGroupBox, QGridLayout, QHeaderView, QDateTimeEdit, QTableWidgetItem, QStackedWidget, QFileDialog

)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap
import MySQLdb as mdb
import sys
import os
import shutil
from PIL import Image
import numpy as np
import MySQLdb as mdb
from tensorflow.keras.models import Model
import numpy as np
from tensorflow.keras.models import load_model

from tensorflow.keras.preprocessing.image import img_to_array, load_img
from scipy.spatial.distance import cosine
import os
from PyQt6.QtCore import  QTime

import Global


class StudentInformationManagement(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = QStackedWidget()
        self.stacked_widget = stacked_widget
        # Thiết lập tiêu đề và kích thước cửa sổ
        self.setWindowTitle("Quản lý thông tin Học sinh")
        self.setGeometry(100, 100, 1200, 700)

        self.model = load_model("D:\\Python\\model.keras")


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

        # Nhãn để hiển thị hình ảnh hoặc nút tải ảnh
        self.photo_label = QLabel("Click để tải ảnh")
        self.photo_label.setFixedSize(200, 200)
        self.photo_label.setStyleSheet("border: 1px solid black; background-color: #F0F0F0; border-radius: 5px;")
        self.photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.photo_label.setCursor(Qt.CursorShape.PointingHandCursor)  # Thêm con trỏ tay khi di chuột lên

        # Kết nối sự kiện nhấp chuột của QLabel để tải ảnh
        self.photo_label.mousePressEvent = self.upload_photo  # Gắn sự kiện nhấp chuột vào QLabel

        # Các ô nhập liệu thông tin
        self.id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.class_input = QLineEdit()
        self.cccd_input = QLineEdit()
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["nam", "nữ"])  # Thêm tùy chọn "Nam" và "Nữ
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

        # Thêm nhãn và nút vào layout
        student_layout.addWidget(self.photo_label, 0, 0, 1, 2)  # Tạo khoảng trống cho ảnh

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

    # tải ảnh lên
    def upload_photo(self, event):
        try:
            # Mở hộp thoại để chọn file ảnh
            file_dialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
            file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.gif)")

            # Nếu người dùng chọn ảnh, lấy đường dẫn và hiển thị ảnh
            if file_dialog.exec():
                selected_files = file_dialog.selectedFiles()
                if selected_files:
                    photo_path = selected_files[0]

                    # Lấy tên file ảnh và tách tên trước dấu - và phần mở rộng
                    file_name = os.path.basename(photo_path)
                    name_without_extension = os.path.splitext(file_name)[0]  # Lấy tên file mà không có phần mở rộng

                    # Kiểm tra xem tên file có chứa dấu "-" không
                    if ' -' in name_without_extension:
                        folder_name = name_without_extension.split(' -')[0]  # Lấy phần trước dấu " -"
                    else:
                        folder_name = name_without_extension  # Nếu không có dấu "-", dùng toàn bộ tên file

                    # Thư mục lưu ảnh sử dụng tên thư mục tương đối
                    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Thư mục cha
                    image_folder = os.path.join(project_root, 'Data', 'Train',folder_name)  # Đường dẫn thư mục con từ tên file
                    if not os.path.exists(image_folder):
                        os.makedirs(image_folder, exist_ok=True)  # Tạo thư mục nếu chưa có

                    # Tạo đường dẫn cho ảnh mới
                    relative_path = os.path.join(image_folder, file_name)

                    # Kiểm tra xem ảnh đã tồn tại trong thư mục đích chưa
                    if not os.path.exists(relative_path):
                        shutil.copy(photo_path, relative_path)  # Sao chép ảnh vào thư mục
                        print(f"Đã sao chép ảnh đến: {relative_path}")
                    else:
                        print(f"Ảnh đã tồn tại tại {relative_path}")

                    # Cập nhật ảnh lên UI
                    self.photo_label.setPixmap(
                        QPixmap(relative_path).scaled(self.photo_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
                    self.photo_label.setText("")  # Xóa chữ khi đã có ảnh
                    self.photo_path = relative_path  # Lưu đường dẫn ảnh tương đối

                    # Không cần trả về giá trị
                    # Chỉ cần cập nhật UI và lưu đường dẫn
        except Exception as e:
            print(f"Đã xảy ra lỗi trong quá trình tải ảnh: {e}")

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

        # Lấy đường dẫn thư mục chứa ảnh (phần đường dẫn thư mục)
        photo_path = getattr(self, "photo_path", None)  # Lấy đường dẫn ảnh nếu có
        if photo_path:
            # Chuyển đường dẫn thành tương đối
            photo_path = os.path.dirname(photo_path)  # Lấy thư mục chứa ảnh
            photo_path = os.path.relpath(photo_path, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
            print(f"photo_path:{photo_path}")
            # photo_path = '\\' + photo_path  # Thêm dấu "\" ở đầu để có dạng "\Data\Train\tên thư mục chứa ảnh"

            images= self.list_file_in_folder(photo_path)
            for img in images:
                try:
                    embedding = self.extract_embedding(self.model, img)
                    self.save_embedding(name, embedding)
                except Exception as e:
                    print(f"Error when processing {img}:{e}")
        else:
            photo_path= None # nếu không có ảnh trả về giá trị None

        query = """
        INSERT INTO students (nameSt, dob, gender, CCCD, email, address, phone, class, photo_path)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (name, dob, gender, cccd, email, address, phone, student_class, photo_path)

        try:
            cursor.execute(query, values)
            db.commit()
            print("Lưu học sinh thành công!")
            # Đặt lại khung ảnh như ban đầu, xóa hình
            self.photo_label.setPixmap(QPixmap())  # xóa hình
            self.photo_label.setText("Click để tải ảnh")  # hiện chữ
            self.photo_path = None  # xóa đường dẫn hình
            self.reset_fields()
        except Exception as e:
            print(f"Lỗi khi lưu học sinh: {e}")
        finally: #để đóng kết nối đến database, đảm bảo không có kết nối bị bỏ sót.
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

    # xem tất cả
    def load_embeddings(self):
        embeddigs = []
        labels = []
        
        try:
            db = mdb.connect(
                host='localhost',
                user='root',
                passwd='',
                db="facerecognitionsystem"
            )
            cursor = db.cursor()

            query = """
                    SELECT label, vector
                    FROM embedding
                    """
            cursor.execute(query)
            db.commit()
            result = cursor.fetchall()

            for row in result:
                label = row[0]
                vector = np.frombuffer(row[1], dtype=np.float32)
                labels.append(label)
                embeddigs.append(vector)

        except Exception as e:
            print(f"Error when loading embeddings:{e}")
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close
        return embeddigs, labels

    def save_embedding(self, label, embedding):
      
        try:
            db = mdb.connect(
                host='localhost',
                user='root',
                passwd='',
                db="facerecognitionsystem"
            )
            cursor = db.cursor()

            query = """
                    INSERT INTO embedding (label, vector)
                    VALUES (%s, %s)
                    """
            cursor.execute(query, (label, embedding.tobytes()))
            db.commit()
            result = cursor.fetchall()
            print(f"Embedding for label '{label}' saved successfully!")


                
        except Exception as e:
            print(f"Error when saving embeddings:{e}")
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close


    # # get from student db field img_path
    def extract_embeddings_from_foder(self, model, folder_path, id):
        embeddings =[]
        list_folder = []

        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if file_name.lower().endswith(('jpg', 'png', 'jpeg')):
                try:
                    embedding = self.extract_embedding(model, file_path)
                    embeddings.append(embedding)
                    list_folder.append(file_path)
                except Exception as e:
                    print(f'Error when process{file_path}:{e}')
        for embedding in embeddings:
            self.save_embedding(self.get_file_name(folder_path), embedding)
        return embedding, list_folder
    
    def extract_embedding(self, model, file_path):
        img = load_img(file_path, target_size = (224,224))
        img_arr = img_to_array(img)
        img_arr = np.expand_dims(img_arr, axis=0)
        embedding = model.predict(img_arr)
        return embedding.flatten()
    
    def get_folder(self):
        list_folder = []
        try:
            db = mdb.connect(
                host='localhost',
                user='root',
                passwd='',
                db="facerecognitionsystem"
            )
            cursor = db.cursor()
            query = """
                    select photo_path
                    from students
                    where students.SId = %s
                    """ 
            cursor.execute(query, (Global.GLOBAL_ACCOUNTID,))  # Lọc theo giáo viên
            results = cursor.fetchall()

            for row in results:
                 list_folder.append(row[0])
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu: {e}")

        finally:
            # Đóng kết nối và cursor
            cursor.close()
            db.close()
        return list_folder
    
    def get_file_name(self, folder_path):
        file_name = os.path.basename(folder_path)
        return file_name

    import os

    def list_file_in_folder(self, folder_path):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        absolute_path = os.path.join(base_dir, folder_path)

        if not os.path.exists(absolute_path):
            raise FileNotFoundError(f"File path not exist: {absolute_path}")

        files = [f for f in os.listdir(absolute_path) if os.path.isfile(os.path.join(absolute_path, f))]
        file_paths = [os.path.join(absolute_path, f) for f in files]

        return file_paths

    
    def add_new_class(self, label, image_paths, model):
        try:
            folder_name =self.get_file_name(label)
            embedding = self.extract_embedding(model, image_paths)
            self.save_embedding(folder_name, embedding)
            
            folder_paths = self.get_folder(folder_name)
            for path in folder_paths:
                print(f"Proccessing image at:{path}")
                embedding = self.extract_embedding(model, path)
                self.save_embedding(label, embedding)

        except Exception as e:
            print(f"Error adding new image:{e}")

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = StudentInformationManagement(" ")
    main_window.show()
    sys.exit(app.exec())