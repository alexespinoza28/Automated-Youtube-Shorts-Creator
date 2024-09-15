import whisper
import os
import shutil
import cv2
from moviepy.editor import ImageSequenceClip, AudioFileClip, VideoFileClip
from tqdm import tqdm
import ssl
from moviepy.video.fx.all import speedx

ssl._create_default_https_context = ssl._create_unverified_context

FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 1.5  # Increased font size
FONT_THICKNESS = 3
TEXT_DELAY_OFFSET = -0.15  # Offset to make text appear slightly ahead of audio

class VideoTranscriber:
    def __init__(self):
        self.model = whisper.load_model("base")
        self.video_path = ""
        self.audio_path = ''
        self.text_array = []
        self.fps = 0
        self.char_width = 0

    def transcribe_video(self):
        print('Transcribing video')
        result = self.model.transcribe(self.audio_path)
        cap = cv2.VideoCapture(self.video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        asp = width / height
        ret, frame = cap.read()
        if not ret:
            raise ValueError("Failed to read video frame")
        width = frame[:, int((width - 1 / asp * height) / 2):width - int((width - 1 / asp * height) / 2)].shape[1]
        width = width - (width * 0.1)
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        text_size = cv2.getTextSize(result["segments"][0]["text"], FONT, FONT_SCALE, FONT_THICKNESS)[0]
        self.char_width = int(text_size[0] / len(result["segments"][0]["text"]))

        for segment in tqdm(result["segments"]):
            text = segment["text"]
            end = segment["end"] + TEXT_DELAY_OFFSET  # Adjusted delay
            start = segment["start"] + TEXT_DELAY_OFFSET
            total_frames = int((end - start) * self.fps)
            start_frame = int(start * self.fps)
            total_chars = len(text)
            words = text.split(" ")
            i = 0

            while i < len(words):
                words[i] = words[i].strip()
                if words[i] == "":
                    i += 1
                    continue

                # Single word or two words if spoken quickly
                line = words[i]
                if i + 1 < len(words):
                    next_word_duration = (len(words[i]) + len(words[i + 1]) + 1) / total_chars * total_frames
                    if next_word_duration < self.fps * 0.5:  # Quick speech check
                        line += " " + words[i + 1]
                        i += 1

                length_in_pixels = (len(line) + 1) * self.char_width
                line_array = [line, start_frame, int(len(line) / total_chars * total_frames) + start_frame]
                start_frame = int(len(line) / total_chars * total_frames) + start_frame
                self.text_array.append(line_array)
                i += 1
        
        cap.release()
        print('Transcription complete')

    def extract_audio(self):
        print('Extracting audio')
        audio_path = os.path.join(os.path.dirname(self.video_path), "audio.mp3")
        video = VideoFileClip(self.video_path)
        audio = video.audio 
        audio.write_audiofile(audio_path)
        self.audio_path = audio_path
        print('Audio extracted')

    def extract_frames(self, output_folder):
        print('Extracting frames')
        cap = cv2.VideoCapture(self.video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        asp = width / height
        N_frames = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = frame[:, int((width - 1 / asp * height) / 2):width - int((width - 1 / asp * height) / 2)]

            for text, start_frame, end_frame in self.text_array:
                if N_frames >= start_frame and N_frames <= end_frame:
                    text_size, _ = cv2.getTextSize(text, FONT, FONT_SCALE, FONT_THICKNESS)
                    text_x = int((frame.shape[1] - text_size[0]) / 2)
                    text_y = int(height / 2)
                    # Draw black border
                    cv2.putText(frame, text, (text_x, text_y), FONT, FONT_SCALE, (0, 0, 0), FONT_THICKNESS + 2)
                    # Draw white text
                    cv2.putText(frame, text, (text_x, text_y), FONT, FONT_SCALE, (255, 255, 255), FONT_THICKNESS)
                    break
            
            cv2.imwrite(os.path.join(output_folder, f"{N_frames}.jpg"), frame)
            N_frames += 1
        
        cap.release()
        print('Frames extracted')

    def create_video(self, output_video_path):
        print('Creating video')
        image_folder = os.path.join(os.path.dirname(self.video_path), "frames")
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
        
        self.extract_frames(image_folder)
        
        images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
        images.sort(key=lambda x: int(x.split(".")[0]))
        
        clip = ImageSequenceClip([os.path.join(image_folder, img) for img in images], fps=self.fps)
        audio = AudioFileClip(self.audio_path)
        clip = clip.set_audio(audio)
        clip = speedx(clip, factor=1.2)
        clip.write_videofile(output_video_path, codec='libx264')
        shutil.rmtree(image_folder)
        os.remove(os.path.join(os.path.dirname(self.video_path), "audio.mp3"))
        
    def transcribe(self, video_path, output_path):
        self.video_path = video_path
        output_video_path = output_path
        self.extract_audio()
        self.transcribe_video()
        self.create_video(output_video_path)
        return output_path


tran = VideoTranscriber()
tran.transcribe(f'precaption/aita7.mp4', 'bruh.mp4')