import tensorflow as tf

# Tải mô hình Keras
model = tf.keras.models.load_model("model.keras")

# Kiểm tra cấu trúc mô hình
model.summary()

# Sử dụng mô hình để dự đoán
import numpy as np

input_data = np.random.random((1, 224, 224, 3))  # Dữ liệu đầu vào mẫu
output = model.predict(input_data)
print("Dự đoán:", output)
