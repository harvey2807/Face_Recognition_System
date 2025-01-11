import sys

from PyQt6.QtCore import Qt, QTimer,QDate
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit, \
    QGridLayout, QTextEdit, QStackedWidget, QTableWidget, QHeaderView, QTabWidget,QTableWidgetItem,QApplication
import cv2
import os
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import MySQLdb as mdb

from PyQt6.QtCore import  QTime

import Global


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'


class RecognitionStudentView(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = QStackedWidget()
        self.stacked_widget = stacked_widget
        self.init_ui()
        #must use absolute path
        db = mdb.connect(
            host='localhost',
            user='root',
            passwd='',
            db="facerecognitionsystem"
        )
        cursor = db.cursor()


        self.model = load_model("D:\\Python\\model.keras")

        self.start_recognition = False
        self.count = 0
        self.recognition_name =0
        self.fronter = []
        print(self.fronter)

        cursor.execute("select SId, nameSt from students")
        rows = cursor.fetchall()    
        ids = [item[0] for item in rows]
        names = [item[1] for item in rows]
        print(names)
        print(ids)

        self.mapIdtoName = {}

        for i in range(len(ids)):
            self.mapIdtoName[ids[i]] =  names[i]
        print(self.mapIdtoName)
        self.label_map = ids

    def init_ui(self):
        self.setStyleSheet("""
                QWidget {
                        background-color: white;
                        color: black;
                    }
                    QLabel {
                        font-size: 14px;
                    }
                    QLineEdit, QComboBox, QTableWidget {
                        border: 1px solid black;
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

        # Grid Layout cho các phần
        self.grid_layout = QGridLayout()

        # Groupbox cho màn hình nhận diện
        self.recognition_group = QGroupBox("Màn hình nhận diện")
        self.recognition_layout = QVBoxLayout()
        self.recognition_group.setLayout(self.recognition_layout)


        # Combobox để chọn lớp và loại điểm danh
        choose_layout = QHBoxLayout()
        self.course_label = QLabel("Lớp:")
        self.course_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.course_label.setStyleSheet("border: none")
        self.classname = QLabel("")
        # class_names = self.loadClassData()
        # self.classname.addItems(class_names)
        self.classname.setStyleSheet("padding:1px 2px; border: 1px solid gray;")
        self.classname.setFixedHeight(25)

        self.class_label = QLabel("Buổi:")
        self.class_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.class_label.setStyleSheet("border: none")
        self.sessionname = QLabel("")
        # session_name = self.loadSessionData("2024-12-04","11:00:00")
        # self.sessionname.addItems(session_name)
        self.sessionname.setStyleSheet("padding:1px 2px; border: 1px solid gray;")
        self.sessionname.setFixedHeight(25)

  
        self.timerzoro = QTimer(self)
        self.timerzoro.timeout.connect(
             lambda: self.loadSessionData(
                QDate.currentDate().toString("yyyy-MM-dd"),
                QTime.currentTime().toString("hh:mm:ss")
            )
        )
        self.timerzoro.start(1000)


        # Thêm vào layout chọn thông tin
        choose_layout.addWidget(self.course_label)
        choose_layout.addWidget(self.classname)
        choose_layout.addWidget(self.class_label)
        choose_layout.addWidget(self.sessionname)
        self.recognition_layout.addLayout(choose_layout)

        self.stack_widget = QWidget(self)
        self.stack_widget.setStyleSheet("background-color: white;")
        # self.stack_widget.setGeometry(0,50,700,450)

        self.stack_layout = QVBoxLayout(self.stack_widget)
        self.stack_widget.setLayout(self.stack_layout)

        self.tab = QTabWidget(self)
        self.tab.setStyleSheet("""
            QTabBar::tab:selected { 
                background: white; 
                border-bottom: 1px solid #0078D7;
                padding: 5px;
            }
        """)

    #Chứa danh sách các sinh viên đã điểm danh
        self.table = QTableWidget(0, 3)  # Bảng chứa kết quả tìm kiếm
        self.table.setHorizontalHeaderLabels(["ID","Tên sinh viên", "Thời gian"])  # Đặt tên các cột
        self.table.setFixedSize(700,360)
        # Điều chỉnh kích thước các cột trong bảng
        header = self.table.horizontalHeader()
        for i in range(self.table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        # Camera feed
        self.camera_feed = QLabel()
        self.camera_feed.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.camera_feed.setPixmap(QPixmap("../Image/img.png").scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio))
        self.camera_feed.setStyleSheet("border: 1px solid black; text-align: center; border-radius: 3px;")
        self.camera_feed.setFixedSize(700, 360)
        # self.recognition_layout.addWidget(self.camera_feed, alignment=Qt.AlignmentFlag.AlignCenter)

        self.tab.addTab(self.camera_feed,'Nhận diện')
        self.tab.addTab(self.table,'Thông tin điểm danh')

        self.recognition_layout.addWidget(self.tab, alignment=Qt.AlignmentFlag.AlignCenter)


        # Khởi tạo camera và timer
        self.camera = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.is_camera_active = False

        # Nút mở camera
        camera_buttons_layout = QHBoxLayout()
        self.open_camera_btn = QPushButton("Mở Camera")
        self.open_camera_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        self.open_camera_btn.clicked.connect(self.toggle_camera)

        #Nút đóng camera
        self.close_camera_btn = QPushButton("Đóng Camera")
        self.close_camera_btn.setStyleSheet("background-color: #F44336; color: white; padding: 10px;")
        self.close_camera_btn.clicked.connect(self.toggle_camera)

        # Nút điểm danh lại nếu có có điểm sai
        self.reset_recognition = QPushButton("Nhận diện lại")
        self.reset_recognition.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        self.reset_recognition.clicked.connect(self.remove_inf)

        # Nút Xem danh sách sinh viên đã điểm danh
        self.viewList = QPushButton("Lưu danh sách")
        self.viewList.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        self.viewList.clicked.connect(self.saveDataToDB)

        camera_buttons_layout.addWidget(self.open_camera_btn)
        camera_buttons_layout.addWidget(self.close_camera_btn)
        camera_buttons_layout.addWidget(self.reset_recognition)
        camera_buttons_layout.addWidget(self.viewList)
        
        self.recognition_layout.addLayout(camera_buttons_layout)

        # Thêm màn hình nhận diện vào main layout
        self.grid_layout.addWidget(self.recognition_group, 0, 0)

        # Thông tin điểm danh (Phần bên phải)
        self.infor_content = QWidget(self)
        self.infor_playout = QVBoxLayout(self.infor_content)


        # Nhận diện học sinh (Phần bên dưới)
        session_group = QGroupBox("Nhận diện sinh viên")
        session_layout = QGridLayout()
        session_group.setLayout(session_layout)
        session_group.setStyleSheet("""
            border: 1px solid gray;
            background-color: white; border-radius: 5px;
            padding-top: 5px;
            padding-bottom: 5px;""")
        self.label_image = QLabel()
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.label_image.setFixedSize(250, 200)
        session_layout.addWidget(self.label_image)

        # Thêm groupbox thông tin buổi học vào layout
        self.infor_playout.addWidget(session_group)


        self.attendance_group = QGroupBox("Điểm danh thành công")
        self.attendance_group.setStyleSheet("""
            border: 1px solid gray;
            background-color: white; border-radius: 5px;
            padding-top: 10px;
            padding-right: 5px;
            padding-bottom: 10px;
            margin-top: 10px;
            margin-bottom: 10px;""")
        self.attendance_layout = QGridLayout()
        self.attendance_group.setLayout(self.attendance_layout)

        self.id_label = QLabel("ID sinh viên:")
        self.id_label.setStyleSheet("border: none")
        self.id_input = QLineEdit()
        self.id_input.setReadOnly(True)
        self.id_input.setStyleSheet("""
                    border: 1px solid #CCCCCC;
                    border-radius: 4px;
                    padding: 5px;
                    margin-bottom: 10px;
                """)

        self.name_label = QLabel("Tên sinh viên:")
        self.name_label.setStyleSheet("border: none")
        self.name_input = QLineEdit()
        self.name_input.setReadOnly(True)
        self.name_input.setStyleSheet("""
                            border: 1px solid #CCCCCC;
                            border-radius: 4px;
                            padding: 5px;
                            margin-bottom: 10px;
                        """)

        self.time_label = QLabel("Thời gian:")
        self.time_label.setStyleSheet("border: none")
        self.time_input = QLineEdit()
        self.time_input.setReadOnly(True)
        self.time_input.setStyleSheet("""
                            border: 1px solid #CCCCCC;
                            border-radius: 4px;
                            padding: 5px;
                            margin-bottom: 10px;
                        """)
        self.attendance_layout.addWidget(self.id_label, 0, 0)
        self.attendance_layout.addWidget(self.id_input, 0, 1)
        self.attendance_layout.addWidget(self.name_label, 1, 0)
        self.attendance_layout.addWidget(self.name_input, 1, 1)
        self.attendance_layout.addWidget(self.time_label, 2, 0)
        self.attendance_layout.addWidget(self.time_input, 2, 1)

        # Thêm groupbox vào layout chính
        self.infor_playout.addWidget(self.attendance_group)

        # Thêm phần layout vào widget chính
        self.grid_layout.addWidget(self.infor_content, 0, 1)

        # Đặt tỷ lệ kích thước cho các cột
        self.grid_layout.setColumnStretch(0, 2)  # recognition_group chiếm 2 phần
        self.grid_layout.setColumnStretch(1, 1)  # infor_content chiếm 1 phần

        self.setLayout(self.grid_layout)


    def loadSessionData(self,date,time):
        # Mảng để chứa dữ liệu
        session_names = []
        print(Global.GLOBAL_ACCOUNTID, date, time)

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
                   select c.nameC, s.sessionName
                    from sessions s join classes c 
                        on s.CId = c.CId
                    where c.TId = %s AND s.sessionDate = %s AND (%s between s.startTime and s.endTime)
                    """
            input = (Global.GLOBAL_ACCOUNTID,date,time)
            cursor.execute(query, input)  # Lọc theo giáo viên
            results = cursor.fetchall()
            
            # Kiểm tra nếu không có kết quả
            if not results:
                print("Không có lớp học nào trong hệ thống.")
                session_names = ["",""]
                self.start_recognition = False
            else :   
                for data in results[0]:
                    session_names.append(data)
                self.start_recognition = True
            
            self.classname.setText(session_names[0])
            self.sessionname.setText(session_names[1])

        except Exception as e:
            print(f"Lỗi khi tải dữ liệu: {e}")

        finally:
            # Đóng kết nối và cursor
            cursor.close()
            db.close()

    

    def face_extractor(self, img):

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(img, 1.3, 5)
        if len(faces) == 0:
            return None

        for (x, y, w, h) in faces:
            # draw rectangle around face
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
            cropped_face = img[y:y + h, x:x + w]
            return cropped_face

        return None
    
    def toggle_camera(self):
        if not self.is_camera_active:
            # Bật camera
            self.camera = cv2.VideoCapture(0)  # 0 là camera mặc định
            if not self.camera.isOpened():
                self.camera_feed.setText("Không thể mở camera")
                return
            self.is_camera_active = True
            self.timer.start(10)  # Cập nhật khung hình mỗi 10ms
        else:
            # Tắt camera
            self.timer.stop()
            if self.camera:
                self.camera.release()
            self.camera_feed.clear()
            self.is_camera_active = False
    
    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
            # Chuyển đổi khung hình từ BGR (OpenCV) sang RGB (Qt)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(frame, 1.3, 5)
            
            for (x, y, w, h) in faces:
            #     # draw rectangle around face
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                height, width, channel = frame.shape
                step = channel * width
                q_image = QImage(frame.data, width, height, step, QImage.Format.Format_RGB888)
                # Hiển thị khung hình lên QLabel
                self.camera_feed.setPixmap(QPixmap.fromImage(q_image))

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face = self.face_extractor(gray)
                if self.start_recognition:
                    self.update_face_recognitioned(face, frame)

    
    def update_face_recognitioned(self, face_img, frame1):
        image_recognition = face_img
        size = self.label_image.size()
        t = size.width()
        g = size.height()
        
        if image_recognition is not None: 
            w, h = image_recognition.shape[:2]
            try:
                # Resize the face image to fit model input
                face_resized = cv2.resize(image_recognition, (224, 224))
                im = Image.fromarray(face_resized, 'RGB')
                img_array = np.array(im)
                img_array = np.expand_dims(img_array, axis=0) / 255.0

                pred = self.model.predict(img_array)
                predicted_class = np.argmax(pred, axis=1)
                name = self.label_map[predicted_class[0]]

                self.recognition_name = name
            
                #set org

                cv2.putText(frame1, self.mapIdtoName[int(name)-1], (0, 15), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 255, 0), 1)
                
                print(name,self.fronter)
                frame = cv2.cvtColor(face_resized, cv2.COLOR_BGR2RGB)
                height, width, channel = frame.shape
                step = channel * width
                q_image = QImage(frame.data, 224, 224, step, QImage.Format.Format_RGB888)
                if name not in self.fronter:
                    if self.count < 1:
                        #Hiển thị thông tin học sinh đã điểm danh lên màn hình
                        self.fronter.append(name)
                        self.id_input.setText(str(name-1))
                        self.name_input.setText(self.mapIdtoName[int(name)-1])
                        self.time_input.setText(QTime.currentTime().toString("hh:mm:ss"))
                        self.data = [str(name-1), self.mapIdtoName[int(name)-1], QTime.currentTime().toString("hh:mm:ss")]
                        self.saveData(self.data)

                        print("Thông tin học sinh", self.fronter)
                        # Hiển thị khung hình lên QLabel
                        self.label_image.setPixmap(QPixmap.fromImage(q_image))
                        self.count = 2
                else:
                    self.count = 0
            except Exception as e:
                print(f"Error during face processing: {e}")

    

    def remove_inf(self):
         # xóa trong bảng
        self.delete_last_row()

        # pass
        name = self.recognition_name  
    
        self.id_input.clear()
        self.name_input.clear()
        self.time_input.clear()
        self.label_image.setPixmap(QPixmap())

        if name in self.fronter:
            for i in self.fronter:
                if i == name:
                    self.fronter.remove(i)
                    print(self.fronter)
        self.count = 0
       

    
    def saveData(self,data_array):
        #Tạo một dòng mới
        current_row = self.table.rowCount() 
        self.table.insertRow(current_row)

        #Thêm dữ liệu vào dòng mới
        for col, value in enumerate(data_array):
            if col < self.table.columnCount():  # Đảm bảo không vượt quá số cột
                item =QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(current_row, col,item)
    
    def saveDataToDB(self):
        rows = self.table.rowCount()
        cols = self.table.columnCount()
        print("running...")
        data = []
        for row in range(rows):
            row_data = []
            for col in range(cols):
                item = self.table.item(row, col)
                row_data.append(item.text() if item else "")
            data.append(row_data)
        

        try:
            db = mdb.connect(
                host='localhost',
                user='root',
                passwd='',
                db="facerecognitionsystem"
            )
            cursor = db.cursor()
            query = """
                    update studentsinsessions
                    set attendance = "present",
                        attendancedTime = %s
                    where sessionId in (
                            select sessionId from sessions where sessionName = %s AND CId in (
                            select CId from classes where nameC = %s)) AND SId = %s;
                   """
            # attendanceTime = self.time_input.text()
            className = self.classname.text()
            sessionName = self.sessionname.text()

              # Kiểm tra xem data có phải là danh sách không
            if isinstance(data, list):
                for item in data:
                    # Giả sử item là tuple (có ít nhất 3 phần tử)
                    if len(item) >= 3:
                        dataneedsave = (item[2], sessionName, className,  int(item[0]))  # item[0] và item[2] phải là các giá trị hợp lệ
                        print(cursor.execute(query, dataneedsave))
                        db.commit()
                        print(f"Saved: {item[1]}")
                        
                    else:
                        print("Dữ liệu không hợp lệ trong item:", item)
            else:
                print("Data phải là một danh sách")

        except Exception as e:
            print(f"Lỗi khi lưu: {e}")
    #Xóa toàn bộ nội dung của bảng
        self.fronter.clear()
        self.start_recognition = True
        self.table.setRowCount(0)

    def delete_last_row(self):
        # Kiểm tra xem bảng có dòng nào không
        row_count = self.table.rowCount()
        print("Xóa rồi")
        if row_count > 0:
            self.table.removeRow(row_count - 1)  # Xóa dòng cuối cùng

    def closeEvent(self, event):
        # Giải phóng tài nguyên khi đóng cửa sổ
        if self.camera:
            self.camera.release()
        event.accept()

    # def process_frame(self, frame):
    #     face = self.face_extractor(frame)
    #     if face is not None:
    #         face_resized = cv2.resize(face, (224, 224))
    #         embedding = self.extract_embedding(self.model, face_resized)

    #         label, score = self.recognize_face(embedding)
    #         print(f"Detected: {label} (score: {score})")

    #         if label != "Unknown":
    #             cv2.putText(frame, f"{label} ({score:.2f})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
    #             self.update_face_recognitioned(label, frame)

    # def update_face_recognitioned(self, label, frame1):
    #     name = label
    #     if name != "Unknown":
    #         self.id_input.setText(str(name))
    #         self.name_input.setText(self.mapIdtoName[int(name)-1])  # Lấy tên từ `mapIdtoName`
    #         self.time_input.setText(QTime.currentTime().toString("hh:mm:ss"))
            
    #         if name not in self.fronter:
    #             self.fronter.append(name)
    #             print("name added:", self.fronter)

    #             face_resized = cv2.resize(frame1, (224, 224)) 
    #             frame_rgb = cv2.cvtColor(face_resized, cv2.COLOR_BGR2RGB)
    #             height, width, channel = frame_rgb.shape
    #             step = channel * width
    #             q_image = QImage(frame_rgb.data, width, height, step, QImage.Format.Format_RGB888)
    #             self.label_image.setPixmap(QPixmap.fromImage(q_image))

    #             self.count = 2  
    #         else:
    #             self.count = 0

    # def recognize_face(self, new_embedding, threshold = 0.8):
    #     embeddings, labels = self.load_embeddings()
    #     best_match = "Unknown"
    #     best_score = -1

    #     for embedding, label in zip(embeddings, labels):
    #         score = self.cosine(new_embedding, embedding)
    #         if (score > best_score):
    #             best_score = score
    #             best_match = label
            
    #     if best_score >= threshold:
    #             return best_match, best_score
          
    #     return "Unknown", best_score

    # def cosine(self, embedding1, embedding2):
    #     dotproduct = np.dot(embedding1, embedding2)
    #     norm1 = np.linalg.norm(embedding1)
    #     norm2 = np.linalg.norm(embedding2)
    #     return dotproduct/(norm1 * norm2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = RecognitionStudentView("My Recognition Window")
    main_window.show()
    sys.exit(app.exec())       