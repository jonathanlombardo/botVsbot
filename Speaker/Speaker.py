import threading, queue, pyttsx3
from threading import Thread
from pyttsx3.voice import Voice

class StopThread(): pass

class Speaker:
    def __init__(self, voice: int = 0, speed: int = 200):
        self.voiceId: int = voice
        self.speed: int = speed
        self.queue: queue.Queue = queue.Queue()
        self.thread: Thread = threading.Thread(target=self.play)
        self.thread.start()
        self.engine: pyttsx3.Engine = None

    def initEngine(self):
        self.engine = pyttsx3.init()
        voices: list[Voice] = self.engine.getProperty('voices')
        self.engine.setProperty('rate', self.speed)
        self.engine.setProperty('voice', voices[self.voiceId].id)

    def play(self):
        self.initEngine()
        while True:
            text = self.queue.get()
            if isinstance(text, StopThread): break
            self.engine.say(text)
            self.engine.runAndWait()

    def add(self, text: str):
        self.queue.put(text)

    def stop(self):
        self.queue.put(StopThread())
        self.thread.join()

    def breakOut(self):
        self.queue = queue.Queue()
        self.queue.put(StopThread())
        self.engine.stop()
        self.thread.join()