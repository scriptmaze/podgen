from gtts import gTTS
from pydub import AudioSegment
from django.conf import settings
import os
import shutil

def create_podcast(pdf_name):
    try:
        print("Initializing podcast creation...")
        
        # Initialize characters
        character1 = Character(accent='co.uk')
        character2 = Character(accent='com')
        
        MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'media')  # Media directory for dynamic content
        podcast_folder = os.path.join(MEDIA_ROOT, "podcast_output_folder", "GoogleTTS", "full_audio_output")
        if not os.path.exists(podcast_folder):
            os.makedirs(podcast_folder)

        # Initialize file reader with script path
        script_path = os.path.join(
            settings.BASE_DIR, 
            "TEMPORARY_FILES_FOLDER", 
            "scripts_output_folder", 
            pdf_name, 
            f"{pdf_name}_script.txt"
        )
        print(f"Script file path: {script_path}")

        # Check if script file exists
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"Script file not found: {script_path}")

        file_reader = FileReader(character1, character2)
        print("Reading script file...")
        file_reader.read_file(script_path)

        print("Merging audio files...")
        file_reader.merge_audio(podcast_folder)  # Pass podcast folder as an argument
        print(f"Podcast created successfully and saved to {podcast_folder}/podcast.mp3")
        shutil.rmtree(os.path.join(settings.BASE_DIR, "TEMPORARY_FILES_FOLDER"))

    except Exception as e:
        print(f"Error in create_podcast: {e}")
        raise

class Character:
    counter = 0

    def __init__(self, accent):
        self.accent = accent

    def increment_counter(self):
        Character.counter += 1  

    def create_audio(self, text):
        try:
            tts = gTTS(text, lang='en', tld=f"{self.accent}")
            self.increment_counter()
            
            output_folder = os.path.join(settings.BASE_DIR, "podcast_output_folder", "GoogleTTS", "raw_audio_output")
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
                print(f"Created output folder for raw audio: {output_folder}")
            
            output_path = os.path.join(output_folder, f"{Character.counter}_{self.accent}.mp3")
            print(f"Saving audio to: {output_path}")
            tts.save(output_path)
            return output_path
        except Exception as e:
            print(f"Error in create_audio: {e}")
            raise

class FileReader:

    def __init__(self, c1, c2):
        self.files = []
        self.c1 = c1
        self.c2 = c2

    def read_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            for line in lines:
                if line.startswith('[1]'):
                    self.files.append(self.c1.create_audio(text=line[3:].strip()))
                elif line.startswith('[2]'): 
                    self.files.append(self.c2.create_audio(text=line[3:].strip()))
                else:
                    print(f"Skipping unsupported line format: {line.strip()}")
        except Exception as e:
            print(f"Error in read_file: {e}")
            raise

    def cleanup(self):
        try:
            for file_path in self.files:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"Removed temporary file: {file_path}")
        except Exception as e:
            print(f"Error during cleanup: {e}")
            raise

    def merge_audio(self, output_folder):
        try:
            if not self.files:
                raise ValueError("No audio files to merge.")

            combined = AudioSegment.from_file(self.files[0], format="mp3")
            print(f"Starting merge with file: {self.files[0]}")

            for file in self.files[1:]:
                print(f"Merging file: {file}")
                audio = AudioSegment.from_file(file, format="mp3")
                combined += audio

            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
                print(f"Created output folder for final podcast: {output_folder}")

            output_path = os.path.join(output_folder, "podcast.mp3")
            combined.export(output_path, format="mp3")
            print(f"Podcast exported to: {output_path}")

            self.cleanup()

        except Exception as e:
            print(f"Error in merge_audio: {e}")
            raise