from flask import Flask, render_template, request, send_file
from pytubefix import YouTube
import os

app = Flask(__name__)

# Certifique-se de que a pasta downloads existe
if not os.path.exists("downloads"):
    os.makedirs("downloads")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form["url"]
        try:
            yt = YouTube(video_url)
            stream = yt.streams.get_highest_resolution()
            file_path = stream.download(output_path="downloads")  # Especifique o caminho de download
            response = send_file(file_path, as_attachment=True)
            os.remove(file_path)  # Remove o arquivo após o download
            return response
        except Exception as e:
            return f"Erro ao baixar o vídeo: {str(e)}"
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)



