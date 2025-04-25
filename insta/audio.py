from flask import Blueprint, render_template, request, send_file, redirect, url_for, flash
import yt_dlp
import os
import uuid

audio_bp = Blueprint('audio', __name__, template_folder='templates')

# Ensure downloads folder exists
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def download_instagram_audio(url, download_folder=DOWNLOAD_FOLDER):
    # Create a unique filename using uuid
    unique_id = str(uuid.uuid4())
    outtmpl = os.path.join(download_folder, unique_id + '.%(ext)s')
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': outtmpl,
        # No postprocessor is set up here, so FFmpeg is not required.
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        # The file is saved with its native extension (e.g., .m4a or .webm)
        filename = ydl.prepare_filename(info_dict)
    return filename

@audio_bp.route("/audio", methods=['GET', 'POST'])
def download_audio():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            flash("Please provide a valid URL.", "error")
            return redirect(url_for('audio.download_audio'))
        try:
            audio_file = download_instagram_audio(url)
            return send_file(audio_file, as_attachment=True)
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            return render_template("audio.html", error=error_message)
    return render_template("audio.html")
