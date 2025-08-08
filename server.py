from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route('/')
def download_file():
    file_path = "uploaded/file"  # всегда одно имя
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name="file.zip")
    else:
        return "Файл пока не загружен", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)