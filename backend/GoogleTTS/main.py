from tts import FileReader
from tts import Character

def main():
    character1 = Character(accent='co.uk')
    character2 = Character(accent='com')
    file_reader = FileReader(character1, character2)
    file_reader.read_file('backend/GoogleTTS/text_files/script1.txt')
    file_reader.merge_audio()

if __name__ == "__main__":
    main()