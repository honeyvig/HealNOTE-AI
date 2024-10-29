import tkinter as tk
from tkinter import messagebox
import pyaudio
import wave
import speech_recognition as sr
import nltk
from nltk.tokenize import word_tokenize

# Ensure you have the necessary NLTK data files
nltk.download('punkt')

class HealNoteAI:
    def __init__(self, master):
        self.master = master
        self.master.title("HealNote AI")
        
        self.record_button = tk.Button(master, text="Record Audio", command=self.record_audio)
        self.record_button.pack()

        self.transcribe_button = tk.Button(master, text="Transcribe Audio", command=self.transcribe_audio)
        self.transcribe_button.pack()

        self.transcription_text = tk.Text(master, height=10, width=50)
        self.transcription_text.pack()

        self.audio_file = "session.wav"

    def record_audio(self):
        chunk = 1024
        format = pyaudio.paInt16
        channels = 1
        rate = 44100
        record_seconds = 10
        wf = wave.open(self.audio_file, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(format))
        wf.setframerate(rate)

        p = pyaudio.PyAudio()
        stream = p.open(format=format, channels=channels, rate=rate, input=True)
        print("Recording...")
        stream.start_stream()
        frames = []

        for _ in range(0, int(rate / chunk * record_seconds)):
            data = stream.read(chunk)
            frames.append(data)

        print("Finished recording.")
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf.writeframes(b''.join(frames))
        wf.close()

    def transcribe_audio(self):
        recognizer = sr.Recognizer()
        with sr.AudioFile(self.audio_file) as source:
            audio = recognizer.record(source)  # read the entire audio file

        try:
            transcription = recognizer.recognize_google(audio)
            self.transcription_text.delete(1.0, tk.END)  # Clear previous text
            self.transcription_text.insert(tk.END, transcription)  # Insert new transcription
            self.extract_medical_terms(transcription)
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            messagebox.showerror("Error", f"Could not request results from Google Speech Recognition service; {e}")

    def extract_medical_terms(self, text):
        # Simple medical terminology extraction (placeholder)
        words = word_tokenize(text)
        medical_terms = [word for word in words if word.lower() in {"aspirin", "diabetes", "hypertension"}]  # Example terms
        print("Extracted Medical Terms:", medical_terms)

if __name__ == "__main__":
    root = tk.Tk()
    app = HealNoteAI(root)
    root.mainloop()
