from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form["url"]
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'noplaylist': True,
                'quiet': False
            }

            if not os.path.exists('downloads'):
                os.makedirs('downloads')

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
                info_dict = ydl.extract_info(video_url, download=False)
                file_name = ydl.prepare_filename(info_dict)

            return send_file(file_name, as_attachment=True)

        except Exception as e:
            return f"Erro ao baixar o vídeo: {str(e)}"
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

