from flask import Flask, render_template, request, jsonify, send_from_directory
from ultralytics import YOLO
import hashlib, cv2, os

#import hashlib, os
#from ultralytics import YOLO

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
weights_path = os.path.join(BASE_DIR, 'best.pt') 

with open(weights_path, 'rb') as f:
    print(">> Loaded weights sha256:", hashlib.sha256(f.read()).hexdigest())

model = YOLO(weights_path)
#verify > print hash


app = Flask(__name__)
##消失先 model = YOLO('/Users/soniasu/Desktop/app/best.pt')

UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
OUTPUT_FOLDER = os.path.join(app.root_path, 'outputs')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            file = request.files['image']
            img_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(img_path)

            # 推論
            results = model(img_path)  
            annotated = results[0].plot()

            # 儲存
            out_path = os.path.join(OUTPUT_FOLDER, file.filename)
            cv2.imwrite(out_path, annotated)

            # 除錯用印一次看看
            print("DEBUG -> out_path:", out_path, "exists?", os.path.exists(out_path))

            # 回傳圖片
            return send_from_directory(OUTPUT_FOLDER, file.filename, mimetype='image/jpeg')

        except Exception as e:
            app.logger.error("Detection error", exc_info=e)
            return jsonify({'error': str(e)}), 500

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
