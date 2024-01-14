from flask import Flask, request, render_template
from moviepy.editor import *
import moviepy.video.fx.all as vfx
import speech_recognition as sr
import os

from get_theme import theme_prompts

# ML stuff
# from transformers import pipeline
# from audiocraft.models import musicgen
# import torchaudio
# import torch
# from scipy.io import wavfile
# from PIL import Image
# from diffusers import StableDiffusionUpscalePipeline
import subprocess


# if torch.cuda.is_available():
#     device = torch.device('cuda')
# elif torch.backends.mps.is_available():
#     device = torch.device('mps')
# else:
#     device = torch.device('cpu')

# MusicGen Model
# model = musicgen.MusicGen.get_pretrained('medium', device=device)
# model.set_generation_params(duration=150)

# ViT2GPT2 Caption Model
# image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")

# Upscaler Model
# model_id = "stabilityai/stable-diffusion-x4-upscaler"
# pipeline = StableDiffusionUpscalePipeline.from_pretrained(
#     model_id, revision="fp16", torch_dtype=torch.float16
# )
# pipeline = pipeline.to("cuda")

app = Flask(__name__)

uploads_dir = os.path.join(app.instance_path, 'uploads')
static_dir = os.path.join(app.root_path, 'static')
os.makedirs(uploads_dir, exist_ok=True)


@app.route('/upload')
def index():
    return render_template('upload.html')


@app.route('/')
def page():
    return render_template('page.html')


def convert_video_format(input_path, output_path):
    """Convert video to a compatible format using FFmpeg."""
    try:
        command = ['ffmpeg', '-i', input_path, '-c:v', 'libx264', '-strict', '-2', output_path]
        subprocess.run(command, check=True)
        return output_path
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Error converting video format: {e}")


def extract_audio(video_path):
    """Extract audio from video and return the path to the audio file."""
    try:
        video_clip = VideoFileClip(video_path)
        audio_path = video_path + '.wav'
        video_clip.audio.write_audiofile(audio_path)
        return audio_path
    except Exception as e:
        error_message = f"Error extracting audio: {e}"
        print(error_message)
        raise ValueError(error_message)


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
    """Mix theme soundtrack with video audio and apply additional audio effects."""
    soundtrack_path = os.path.join('soundtracks', theme + '.mp3')
    if not os.path.exists(soundtrack_path):
        print(f"Soundtrack not found: {soundtrack_path}")
        return video_clip

    try:
        soundtrack = AudioFileClip(soundtrack_path).fx(afx.audio_normalize).fx(afx.audio_fadein, 1.0)

        # if the original video has audio, mix it with the soundtrack
        if video_clip.audio:
            original_audio = video_clip.audio.fx(afx.audio_normalize).volumex(1)
            soundtrack = soundtrack.volumex(0.3)  # Adjust the soundtrack volume
            final_audio = CompositeAudioClip([original_audio, soundtrack.set_duration(video_clip.duration)])
        else:
            final_audio = soundtrack.set_duration(video_clip.duration)

        video_clip.audio = final_audio.fx(afx.audio_fadeout, 1.0)
    except Exception as e:
        print(f"Error mixing soundtrack: {e}")
        return video_clip

    return video_clip

# def get_caption(image):
#     image = Image.fromarray(image)
#     return image_to_text(image)[0]['generated_text']

# def generate_music(transcript, caption):
#     model = None
#     res = model.generate([
#         transcript,
#         caption,
#     ],
#     progress=True)
#     wavfile.write(f"./soundtracks/custom.wav", rate=32000, data=res[0, 0].cpu().numpy())

# def upscale_video(video_clip):
#     for i in range(0, int(video_clip.duration), 5):
#         frame = video_clip.get_frame(i)
#         frame = Image.fromarray(frame)
#         prompt = ''
#         upscale_frame = pipeline(propmt=prompt, image=frame).images[0]
#         video_clip = video_clip.set_frame(i, upscale_frame)

def apply_filters(video_clip, theme):
    if theme == 'vibey':
        video_clip = video_clip.fx(vfx.colorx, 1.5).fx(vfx.adjust_contrast, 1.4)
    elif theme == 'modern':
        video_clip = video_clip.fx(vfx.colorx, 1.3).fx(vfx.adjust_contrast, 1.5)
    elif theme == 'cinematic':
        video_clip = video_clip.fx(vfx.crop, x1=0.1, y1=0.1, x2=-0.1, y2=-0.1).fx(vfx.colorx, 0.8)
    elif theme == 'jazz':
        video_clip = video_clip.fx(vfx.color_balance, midtones=[0.3, 0.3, 0.5], shadows=[0.2, 0.2, 0.3])
    elif theme == 'retro':
        video_clip = video_clip.fx(vfx.colorx, 0.9).fx(vfx.old_film, color=True)
    elif theme == 'ambient':
        video_clip = video_clip.fx(vfx.color_balance, midtones=[0.8, 0.8, 1.0], highlights=[0.9, 0.9, 1.1]).fx(vfx.painting, saturation=1.2)
    else:
        pass
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

    # Generate Custom BGM
    # caption = get_caption(video_clip.get_frame(5))
    # generate_music(transcript, caption)

    # Upscale the resolution of the video
    # upscale_video(video_clip)

    # save the edited video
    edited_video_filename = 'edited_' + os.path.splitext(video.filename)[0] + '.mp4'
    edited_video_path = os.path.join(static_dir, edited_video_filename)
    video_clip.write_videofile(edited_video_path, codec='libx264')

    return render_template('result.html', transcript=transcript, video_filename=edited_video_filename, theme_prompt=theme_prompt)


if __name__ == '__main__':
    app.run(debug=False)
