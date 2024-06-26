from flask import current_app
import pymysql
import speech_recognition as sr
import wave
import nltk
from contextlib import contextmanager
from pydub import AudioSegment
import io

# Ensure necessary NLTK data is downloaded
nltk.download('punkt')

def transcribe_audio(audio_file_path: str) -> str:
    recognizer = sr.Recognizer()
    # Convert audio to a compatible format (wav) if it's in ogg format
    if audio_file_path.endswith('.ogg'):
        sound = AudioSegment.from_ogg(audio_file_path)
        buffer = io.BytesIO()
        sound.export(buffer, format="wav")
        buffer.seek(0)
        audio_file = sr.AudioFile(buffer)
    else:
        audio_file = sr.AudioFile(audio_file_path)
    
    with audio_file as source:
        audio_data = recognizer.record(source)
    try:
        transcript = recognizer.recognize_google(audio_data, language='pt-BR')
        return transcript
    except Exception as e:
        print(f"Error in speech recognition: {e}")
        return None

def get_audio_duration(audio_file_path: str) -> float:
    with wave.open(audio_file_path, 'rb') as file:
        frames = file.getnframes()
        rate = file.getframerate()
        duration = frames / float(rate)
        return duration

def calculate_word_accuracy(transcript: str, reference_text: str) -> float:
    words_transcript = nltk.word_tokenize(transcript.lower())
    words_reference = nltk.word_tokenize(reference_text.lower())
    correct_words = [word for word in words_transcript if word in words_reference]
    accuracy = (len(correct_words) / len(words_reference)) * 100 if words_reference else 0
    return accuracy

def calculate_words_per_minute(transcript: str, audio_duration: float) -> float:
    words_transcript = nltk.word_tokenize(transcript.lower())
    wpm = (len(words_transcript) / audio_duration) * 60
    return wpm

def get_word_count(transcript: str) -> int:
    words_transcript = nltk.word_tokenize(transcript.lower())
    return len(words_transcript)

def determine_reading_level(crdi: float) -> str:
    if crdi >= 0.75:
        return "Nível 4 - Leitor Fluente"
    elif crdi >= 0.50:
        return "Nível 3 - Silabou ao realizar a leitura das palavras"
    elif crdi > 0.25:
        return "Nível 2 - Pré-leitor - aluno tem dificuldade em ler"
    else:
        return "Nível 1 - Leitor iniciante"

def calculate_crdi(transcript: str, reference_text: str, audio_duration: float) -> float:
    wpm = calculate_words_per_minute(transcript, audio_duration)
    accuracy = calculate_word_accuracy(transcript, reference_text)
    accuracy_weight = 0.5
    wpm_weight = 0.5
    crdi = (accuracy_weight * accuracy) + (wpm_weight * (wpm / 100))  # Normalizing WPM by assuming 100 WPM as normal
    return crdi

@contextmanager
def get_db_connection():
    connection = pymysql.connect(host=current_app.config['DB_HOST'],
                         user=current_app.config['DB_USER'],
                         password=current_app.config['DB_PASSWORD'],
                         db=current_app.config['DB_NAME'],
                         cursorclass=pymysql.cursors.DictCursor)
    try:
        yield connection
    finally:
        connection.close()

# Example usage (within a Flask route or command)
# audio_file_path = "path/to/audio/file.wav"
# transcript = transcribe_audio(audio_file_path)
# reference_text = "Your reference text here"
# audio_duration = get_audio_duration(audio_file_path)
# crdi_score = calculate_crdi(transcript, reference_text, audio_duration)
# print(f"Comprehensive Reading Difficulty Index (CRDI): {crdi_score:.2f}")
