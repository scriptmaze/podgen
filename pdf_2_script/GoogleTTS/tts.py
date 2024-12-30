from gtts import gTTS
from pydub import AudioSegment
import os

def create_podcast(pdf_name):
    character1 = Character(accent='co.uk')
    character2 = Character(accent='com')
    file_reader = FileReader(character1, character2)
    file_reader.read_file(f'pdf_2_script/scripts/{pdf_name}/{pdf_name}_script.txt')
    file_reader.merge_audio()
    print('Podcast saved to pdf_2_script/GoogleTTS/full_audio_output/podcast.mp3')

class Character:
    counter = 0
    def __init__(self, accent):
        self.accent = accent


    def increment_counter(self):
        Character.counter += 1  
        
    def create_audio(self, text):
        tts = gTTS(text, lang='en', tld=f"{self.accent}")
        self.increment_counter()
        tts.save(f"pdf_2_script/GoogleTTS/raw_audio_output/{Character.counter}_{self.accent}.mp3")
        return f"pdf_2_script/GoogleTTS/raw_audio_output/{Character.counter}_{self.accent}.mp3"
        
        
class FileReader:
    
    def __init__(self, c1, c2):
        self.files = []
        self.c1 = c1
        self.c2 = c2
    
    def read_file(self, path):
        with open(path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            if line.startswith('[1]'):
                self.files.append(self.c1.create_audio(text=line[3:].strip()))
                 
            elif line.startswith('[2]'): 
                self.files.append(self.c2.create_audio(text=line[3:].strip()))
            else:
                continue
            
    def cleanup(self):
        for file_path in self.files:
            if os.path.exists(file_path):
                os.remove(file_path)
            
    def merge_audio(self):
        combined = AudioSegment.from_file(self.files[0], format="mp3")

        for file in self.files[1:]:
            audio = AudioSegment.from_file(file, format="mp3")
            combined += audio

        combined.export("pdf_2_script/GoogleTTS/full_audio_output/podcast.mp3", format="mp3")
        self.cleanup()
        

        
        