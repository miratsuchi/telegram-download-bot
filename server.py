from flask import Flask, Response
import requests
import json

API_TOKEN = "8168140620:AAHEL7fDn5vO_KsLuo-R1iC_tLCM4TTM918"

app = Flask(__name__)

def load_file_id():
    try:
        with open("files.json", "r") as f:
            data = json.load(f)
            return data.get("current_file")
    except Exception:
        return None

@app.route("/download")
def download_file():
    file_id = load_file_id()
    if not file_id:
        return "Файл не найден", 404

    # Получаем путь к файлу в Telegram
    r = requests.get(f"https://api.telegram.org/bot{API_TOKEN}/getFile?file_id={file_id}")
    if not r.ok:
        return "Ошибка получения файла", 500

    file_path = r.json()["result"]["file_path"]

    # Скачиваем файл с Telegram
    file_response = requests.get(f"https://api.telegram.org/file/bot{API_TOKEN}/{file_path}", stream=True)
    if not file_response.ok:
        return "Ошибка скачивания файла", 500

    headers = {
        "Content-Disposition": "attachment; filename=file"
    }
    return Response(file_response.iter_content(chunk_size=8192),
                    headers=headers,
                    content_type=file_response.headers.get('content-type'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)