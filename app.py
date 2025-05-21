import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 🔸 ฟังก์ชันวิเคราะห์สีภาพแล้วแยกประเภทขยะเบื้องต้นจากความสว่าง
def classify_by_color(image_path):
    img = Image.open(image_path).resize((100, 100)).convert('RGB')
    pixels = np.array(img).reshape(-1, 3)

    # คำนวณความสว่างเฉลี่ย
    avg_brightness = np.mean(pixels)

    if avg_brightness < 80:
        return "ขยะอินทรีย์ (เช่น เศษอาหาร)"
    elif avg_brightness < 140:
        return "ขยะทั่วไป (เช่น ซองขนม)"
    elif avg_brightness < 200:
        return "ขยะรีไซเคิล (เช่น ขวดพลาสติก)"
    else:
        return "ขยะรีไซเคิล (เช่น ขวดแก้ว, โลหะ)"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    image_path = None

    if request.method == 'POST':
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            result = classify_by_color(filepath)
            image_path = filepath

    return render_template('index.html', result=result, image=image_path)

# ✅ รองรับทั้ง Render และ localhost
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # อ่านพอร์ตจาก env (Render ใช้)
    app.run(host='0.0.0.0', port=port)
