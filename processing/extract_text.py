# this is just Miranda playing around. Not actually used in the project

import moviepy.editor as mp 
import speech_recognition as sr 

video_path = "test.mp4"
# load the video 
video = mp.VideoFileClip(video_path) 

# extract audio from video
audio_file = video.audio 
audio_file.write_audiofile("test.wav") 

r = sr.Recognizer() 

# load the audio file 
with sr.AudioFile("test.wav") as source: 
	data = r.record(source) 

# convert the speech to text
text = r.recognize_google(data) 
print("\nThe resultant text from video is: \n") 
print(text) 
