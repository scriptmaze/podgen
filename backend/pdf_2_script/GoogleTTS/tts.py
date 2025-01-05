"""
Module to create podcasts from text using Google Text-to-Speech.
"""
import os
import shutil
import uuid
from datetime import datetime
from gtts import gTTS
from pydub import AudioSegment
from django.conf import settings
from backend.models import Podcast

def create_podcast(pdf_name):
    """
    Create a podcast from the text extracted from a PDF.
    
    Args:
        pdf_name (str): The name of the PDF file (used for naming the output folder and file).
    """
    try:
        print("Initializing podcast creation...")
        # Initialize characters with playback speed
        character1 = Character(accent='co.uk', speed=1.2)  # 1.2x faster
        character2 = Character(accent='com', speed=1.3)  # 1.3x faster

        media_root = os.path.join(settings.BASE_DIR, 'media')  # Media directory for dynamic content
        podcast_folder = os.path.join(
            media_root,
            "podcast_output_folder", 
            "GoogleTTS", 
            "full_audio_output")
        if not os.path.exists(podcast_folder):
            os.makedirs(podcast_folder)

        # Initialize file reader with script path
        script_path = os.path.join(
            settings.BASE_DIR,
            "TEMPORARY_FILES_FOLDER", 
            "scripts_output_folder", 
            pdf_name,
            f"{pdf_name}_script.txt")
        print(f"Script file path: {script_path}")

        # Check if script file exists
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"Script file not found: {script_path}")

        file_reader = FileReader(character1, character2)
        print("Reading script file...")
        file_reader.read_file(script_path)

        print("Merging audio files...")
        file_reader.merge_audio(
            output_folder=podcast_folder,
            pdf_name=pdf_name,
            speed=1.1)  # Adjust final podcast speed to 1.1x
        print(f"Podcast created successfully and saved to {podcast_folder}/podcast.mp3")
        shutil.rmtree(os.path.join(settings.BASE_DIR, "TEMPORARY_FILES_FOLDER"))

    except Exception as e:
        print(f"Error in create_podcast: {e}")
        raise

class Character:
    """
    Class representing a character with specific accent and speed for TTS.
    """
    counter = 0

    def __init__(self, accent, speed=1.0):  # Default speed is normal (1.0x)
        """
        Initialize a Character instance.
        
        Args:
            accent (str): The accent for the TTS.
            speed (float): The playback speed for the TTS. Default is 1.0 (normal speed).
        """
        self.accent = accent
        self.speed = speed

    def increment_counter(self):
        """
        Increment the counter for the number of audio files created.
        """
        Character.counter += 1

    def create_audio(self, text):
        """
        Create an audio file from the given text using Google TTS.
        
        Args:
            text (str): The text to convert to audio.
        
        Returns:
            str: The path to the created audio file.
        """
        try:
            tts = gTTS(text, lang='en', tld=f"{self.accent}")
            self.increment_counter()
            output_folder = os.path.join(
                settings.BASE_DIR,
                "podcast_output_folder",
                "GoogleTTS",
                "raw_audio_output")
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
                print(f"Created output folder for raw audio: {output_folder}")
            raw_output_path = os.path.join(
                output_folder,
                f"{Character.counter}_{self.accent}_raw.mp3")
            print(f"Saving raw audio to: {raw_output_path}")
            tts.save(raw_output_path)

            # Adjust playback speed using pydub
            audio = AudioSegment.from_file(raw_output_path, format="mp3")
            adjusted_audio = audio.speedup(playback_speed=self.speed)

            # Save adjusted audio
            adjusted_output_path = os.path.join(
                output_folder,
                f"{Character.counter}_{self.accent}.mp3")
            adjusted_audio.export(adjusted_output_path, format="mp3")
            print(f"Adjusted audio saved to: {adjusted_output_path}")

            # Remove raw audio after adjustment
            os.remove(raw_output_path)

            return adjusted_output_path
        except Exception as e:
            print(f"Error in create_audio: {e}")
            raise

class FileReader:
    """
    Class to read text files and create audio files using Character instances.
    """

    def __init__(self, c1, c2):
        """
        Initialize a FileReader instance.
        
        Args:
            c1 (Character): The first character instance.
            c2 (Character): The second character instance.
        """
        self.files = []
        self.c1 = c1
        self.c2 = c2

    def read_file(self, path):
        """
        Read a text file and create audio files for each line.
        
        Args:
            path (str): The path to the text file.
        """
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
        """
        Clean up temporary audio files.
        """
        try:
            for file_path in self.files:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"Removed temporary file: {file_path}")
        except Exception as e:
            print(f"Error during cleanup: {e}")
            raise

    def merge_audio(self, output_folder, pdf_name, speed=1.0):
        """
        Merge all created audio files into a single podcast file.
        
        Args:
            output_folder (str): The directory where the final podcast file will be saved.
            pdf_name (str): The name of the PDF file (used for naming the output file).
            speed (float): The playback speed for the final podcast. Default is 1.0 (normal speed).
        """
        try:
            if not self.files:
                raise ValueError("No audio files to merge.")

            combined = AudioSegment.from_file(self.files[0], format="mp3")
            print(f"Starting merge with file: {self.files[0]}")

            for file in self.files[1:]:
                print(f"Merging file: {file}")
                audio = AudioSegment.from_file(file, format="mp3")
                combined += audio

            # Adjust playback speed of the final merged podcast
            if speed != 1.0:
                print(f"Adjusting playback speed of merged audio to {speed}x")
                combined = combined.speedup(playback_speed=speed)

            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
                print(f"Created output folder for final podcast: {output_folder}")

            # Generate a unique podcast filename
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            podcast_filename = f"{pdf_name}_{timestamp}_{unique_id}.mp3"
            output_path = os.path.join(output_folder, podcast_filename)

            # Export the final podcast file
            combined.export(output_path, format="mp3")
            print(f"Podcast exported to: {output_path}")

            # Update the database
            Podcast.objects.filter(
                file_name=pdf_name,
                status="processing").delete()  # Remove the processing record
            podcast_url = f"{settings.MEDIA_URL}podcast_output_folder/GoogleTTS/full_audio_output/{podcast_filename}"

            Podcast.objects.create(
                file_name=pdf_name,
                podcast_path=podcast_url,
                status="completed"
            )
            print(f"Podcast metadata saved to the database for {pdf_name}")

            # Clean up temporary files
            self.cleanup()

        except Exception as e:
            print(f"Error in merge_audio: {e}")
            raise
