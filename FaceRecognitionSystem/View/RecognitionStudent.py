from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit, \
    QGridLayout, QTextEdit
import cv2
import os
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'


class RecognitionStudentView(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui()
        #must use absolute path
        # self.model = load_model("D:\python\FaceRecognitionSystem\model.keras")
        self.model = load_model("../model.keras")
        self.label_map = ['Dang Tran Tan Luc', 'Nguyen Thi Ngoc Diem', 'Phung Khanh Duy',
                          'Vo Nguyen Thanh Dieu',
                          'Vo Thi Cam Tu']

    def init_ui(self):
        # Định nghĩa CSS để tạo giao diện
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
        self.course_label = QLabel("Chọn Lớp:")
        self.course_label.setStyleSheet("border: none")
        self.course_combo = QComboBox()
        self.course_combo.addItems(["Cấu trúc dữ liệu", "Python"])
        self.course_combo.setStyleSheet("padding: 5px; border: 1px solid gray;")

        self.class_label = QLabel("Chọn Buổi:")
        self.class_label.setStyleSheet("border: none")
        self.class_combo = QComboBox()
        self.class_combo.addItems(["1", "2", "3"])
        self.class_combo.setStyleSheet("padding: 5px; border: 1px solid gray;")

        self.attendance_label = QLabel("Loại Điểm Danh:")
        self.attendance_label.setStyleSheet("border: none")
        self.attendance_combo = QComboBox()
        self.attendance_combo.addItems(["Vào", "Ra"])
        self.attendance_combo.setStyleSheet("padding: 5px; border: 1px solid gray;")

        # Thêm vào layout chọn thông tin
        choose_layout.addWidget(self.course_label)
        choose_layout.addWidget(self.course_combo)
        choose_layout.addWidget(self.class_label)
        choose_layout.addWidget(self.class_combo)
        choose_layout.addWidget(self.attendance_label)
        choose_layout.addWidget(self.attendance_combo)
        self.recognition_layout.addLayout(choose_layout)

        # Camera feed
        self.camera_feed = QLabel()
        self.camera_feed.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.camera_feed.setPixmap(QPixmap("../Image/img.png").scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio))
        # self.camera_feed.setStyleSheet("border: 1px solid blue; text-align: center;")
        self.camera_feed.setFixedSize(700, 360)
        self.recognition_layout.addWidget(self.camera_feed, alignment=Qt.AlignmentFlag.AlignCenter)

        # Khởi tạo camera và timer
        self.camera = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.is_camera_active = False

        # Nút mở và đóng camera
        camera_buttons_layout = QHBoxLayout()
        self.open_camera_btn = QPushButton("Mở Camera")
        self.open_camera_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        self.open_camera_btn.clicked.connect(self.toggle_camera)

        self.close_camera_btn = QPushButton("Đóng Camera")
        self.close_camera_btn.setStyleSheet("background-color: #F44336; color: white; padding: 10px;")
        self.close_camera_btn.clicked.connect(self.toggle_camera)

        camera_buttons_layout.addWidget(self.open_camera_btn)
        camera_buttons_layout.addWidget(self.close_camera_btn)
        self.recognition_layout.addLayout(camera_buttons_layout)

        # Thêm màn hình nhận diện vào main layout
        self.grid_layout.addWidget(self.recognition_group, 0, 0)

        # Thông tin điểm danh (Phần bên phải)
        self.infor_content = QWidget(self)
        self.infor_playout = QVBoxLayout(self.infor_content)

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

        self.id_label = QLabel("ID Học sinh:")
        self.id_label.setStyleSheet("border: none")
        self.id_input = QLineEdit()
        self.id_input.setStyleSheet("""
                    border: 1px solid #CCCCCC;
                    border-radius: 4px;
                    padding: 5px;
                    margin-bottom: 10px;
                """)

        self.name_label = QLabel("Tên Học sinh:")
        self.name_label.setStyleSheet("border: none")
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet("""
                            border: 1px solid #CCCCCC;
                            border-radius: 4px;
                            padding: 5px;
                            margin-bottom: 10px;
                        """)

        self.time_label = QLabel("Thời gian:")
        self.time_label.setStyleSheet("border: none")
        self.time_input = QLineEdit()
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

        # Thông tin buổi học (Phần bên dưới)
        session_group = QGroupBox("Thông tin buổi học")
        session_group.setStyleSheet("""
            border: 1px solid gray;
            background-color: white; border-radius: 5px;
            padding-top: 5px;
            padding-bottom: 5px;""")
        session_layout = QGridLayout()
        session_group.setLayout(session_layout)

        self.class_label = QLabel("Lớp:")
        self.class_label.setStyleSheet("border: none")
        self.infor_class_input = QLabel("Cấu trúc dữ liệu")
        self.infor_class_input.setStyleSheet("border: none; color: red")

        self.id_session_label = QLabel("ID buổi học: ")
        self.id_session_label.setStyleSheet("border: none")
        self.id_session_input = QLabel("1")
        self.id_session_input.setStyleSheet("border: none; color: red")

        self.time_label = QLabel("Thời gian")
        self.time_label.setStyleSheet("border: none")
        self.time_input = QLabel("7:00:00 - 11:30:00")
        self.time_input.setStyleSheet("border: none; color: red")

        session_layout.addWidget(self.class_label, 0, 0)
        session_layout.addWidget(self.infor_class_input, 0, 1)
        session_layout.addWidget(self.id_session_label, 1, 0)
        session_layout.addWidget(self.id_session_input, 1, 1)
        session_layout.addWidget(self.time_label, 2, 0)
        session_layout.addWidget(self.time_input, 2, 1)

        # Thêm groupbox thông tin buổi học vào layout
        self.infor_playout.addWidget(session_group)

        # Thêm phần layout vào widget chính
        self.grid_layout.addWidget(self.infor_content, 0, 1)

        # Đặt tỷ lệ kích thước cho các cột
        self.grid_layout.setColumnStretch(0, 2)  # recognition_group chiếm 2 phần
        self.grid_layout.setColumnStretch(1, 1)  # infor_content chiếm 1 phần

        self.setLayout(self.grid_layout)

    def face_extractor(self, img):
        classifier = load_model("D:\Project\Face_Recognition_System\FaceRecognitionSystem\model.keras")
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
            self.timer.start(30)  # Cập nhật khung hình mỗi 30ms
        else:
            # Tắt camera
            self.timer.stop()
            if self.camera:
                self.camera.release()
            self.camera_feed.clear()
            self.is_camera_active = False

    # def update_frame(self):
    #     ret, frame = self.camera.read()
    #     if ret:
    #         # Chuyển đổi khung hình từ BGR (OpenCV) sang RGB (Qt)
    #         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #         height, width, channel = frame.shape
    #         step = channel * width
    #         q_image = QImage(frame.data, width, height, step, QImage.Format.Format_RGB888)
    #         # Hiển thị khung hình lên QLabel
    #         self.camera_feed.setPixmap(QPixmap.fromImage(q_image))

    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
            # Convert frame from BGR (OpenCV) to RGB (Qt)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Call face_extractor to get face region
            face = self.face_extractor(frame_rgb)
            if face is not None:
                try:
                    # Resize the face image to fit model input
                    face_resized = cv2.resize(face, (224, 224))
                    im = Image.fromarray(face_resized, 'RGB')
                    img_array = np.array(im)
                    img_array = np.expand_dims(img_array, axis=0) / 255.0

                    pred = self.model.predict(img_array)
                    predicted_class = np.argmax(pred, axis=1)
                    name = self.label_map[predicted_class[0]]

                    #set org
                    cv2.putText(frame_rgb, name, (30, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                except Exception as e:
                    print(f"Error during face processing: {e}")
            else:
                cv2.putText(frame_rgb, "No face detected", (30, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

            height, width, channel = frame_rgb.shape
            step = channel * width
            q_image = QImage(frame_rgb.data, width, height, step, QImage.Format.Format_RGB888)
            self.camera_feed.setPixmap(QPixmap.fromImage(q_image))

    def closeEvent(self, event):
        # Giải phóng tài nguyên khi đóng cửa sổ
        if self.camera:
            self.camera.release()
        event.accept()


