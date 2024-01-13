from flask import Flask, request, render_template
from moviepy.editor import *
import moviepy.video.fx.all as vfx
import speech_recognition as sr
import os

from get_theme import theme_prompts

app = Flask(__name__)

uploads_dir = os.path.join(app.instance_path, 'uploads')
static_dir = os.path.join(app.root_path, 'static')
os.makedirs(uploads_dir, exist_ok=True)


@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/page')
def page():
    return render_template('page.html')


def extract_audio(video_path):
    """Extract audio from video and return the path to the audio file."""
    video_clip = VideoFileClip(video_path)
    audio_path = video_path + '.wav'
    video_clip.audio.write_audiofile(audio_path)
    return audio_path


def transcribe_audio(audio_path):
    """Transcribe audio to text and return the transcript."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            raise ValueError('Speech recognition could not understand audio')
        except sr.RequestError as e:
            raise ValueError(f'Google Speech Recognition service error: {e}')


def mix_soundtrack(video_clip, theme):
    """Mix theme soundtrack with video audio."""
    soundtrack_path = os.path.join('soundtracks', theme + '.mp3')
    if not os.path.exists(soundtrack_path):
        print(f"Soundtrack not found: {soundtrack_path}")
        return video_clip  # return original clip if soundtrack is missing
    try:
        soundtrack = AudioFileClip(soundtrack_path).volumex(0.5)  # reduce volume to 50%
        final_audio = CompositeAudioClip([video_clip.audio, soundtrack.set_duration(video_clip.duration)])
        video_clip.audio = final_audio
    except Exception as e:
        print(f"Error mixing soundtrack: {e}")
        return video_clip

    return video_clip


def apply_filters(video_clip, theme):
    if theme == 'cowboy':
        # Example: Applying a color filter for the cowboy theme
        video_clip = video_clip.fx(vfx.colorx, 0.7)
    # Add other themes and their corresponding filters
    return video_clip

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return 'No video file part', 400

    video = request.files['video']
    theme = request.form['theme']
    theme_prompt = "Ensure a professional tone, with appropriate marketing music"

    if video.filename == '':
        return 'No selected file', 400

    video_path = os.path.join(uploads_dir, video.filename)
    video.save(video_path)

    try:
        audio_path = extract_audio(video_path)
        transcript = transcribe_audio(audio_path)
    except ValueError as e:
        return str(e), 500

    if theme in theme_prompts:
        theme_prompt = theme_prompts[theme]

    video_clip = VideoFileClip(video_path)

    # mix the soundtrack with the original audio
    video_clip = mix_soundtrack(video_clip, theme)

    # apply filters based on theme
    video_clip = apply_filters(video_clip, theme)

    # save the edited video
    edited_video_filename = 'edited_' + os.path.splitext(video.filename)[0] + '.mp4'
    edited_video_path = os.path.join(static_dir, edited_video_filename)
    video_clip.write_videofile(edited_video_path, codec='libx264')

    return render_template('result.html', transcript=transcript, video_filename=edited_video_filename, theme_prompt=theme_prompt)


if __name__ == '__main__':
    app.run(debug=False)
