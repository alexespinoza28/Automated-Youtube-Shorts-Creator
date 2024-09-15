from moviepy.editor import VideoFileClip, AudioFileClip
from elevenlabs import Voice, VoiceSettings, save, play
from elevenlabs.client import ElevenLabs
import random
import os
from mutagen.mp3 import MP3

class Editor:
  
    def createVids(self, title, description, output_path):
        count = 0
        footages = ['backgroundFootage/GTA.mp4', 'backgroundFootage/minecraft.mp4', 'backgroundFootage/subwaySurf.mp4']

        for i in footages:
            if not os.path.exists(i):
                print(f"file not found: {i}")
                exit()

        client = ElevenLabs(
            api_key="enter_key_here",
        )

        # Setup a voice from just first entry column
        audio = client.generate(
            text=title + description,
            voice=Voice(
                voice_id='pNInz6obpgDQGcFmaJgB',
                settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
            )
        )
        save(audio, "audio.mp3")
        audioLen = MP3("audio.mp3")

        # Open up the video clip and subclip it
        clip1 = VideoFileClip(random.choice(footages)).subclip(10, audioLen.info.length + 10)

        # Calculate the aspect ratio of the video
        aspect_ratio = 9 / 16
        clip_aspect_ratio = clip1.w / clip1.h

        # Resize and add padding to fit 9:16 aspect ratio
        if clip_aspect_ratio > aspect_ratio:
            new_height = clip1.h
            new_width = int(clip1.h * aspect_ratio)
            padding = (clip1.w - new_width) / 2
            clip1 = clip1.crop(x1=padding, x2=clip1.w-padding)
        else:
            new_width = clip1.w
            new_height = int(clip1.w / aspect_ratio)
            padding = (clip1.h - new_height) / 2
            clip1 = clip1.crop(y1=padding, y2=clip1.h-padding)

        # Open up an audio clip, grab elevenlabs voice
        audioClip = AudioFileClip("audio.mp3")

        # Set audio of the video clip to the audio clip
        clip1 = clip1.set_audio(audioClip)

        # Write the file
        clip1.write_videofile(output_path, codec='libx264')
    