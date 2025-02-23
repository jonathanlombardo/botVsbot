import threading, queue, pyttsx3
from threading import Thread
from pyttsx3.voice import Voice
from time import sleep

class StopThread(): pass

class Speaker:
    def __init__(self, voice: int = 0, speed: int = 200):
        self._on: bool = True
        self._voiceId: int = voice
        self._speed: int = speed
        self._thread: Thread = threading.Thread(target=self.worker, daemon=True)

    def initEngine(self):
        self._engine = pyttsx3.init()
        self._voices: list[Voice] = self._engine.getProperty('voices')
        self.initEngineProps()

    def initEngineProps(self):
      self._engine.setProperty('voice', self._voices[self._voiceId].id)
      self._engine.setProperty('rate', self._speed)

    def say(self, message: dict):
      if not self._on: return
      self._engine.setProperty('voice', self._voices[message.get('voice')].id)
      self._engine.setProperty('rate', message.get('speed'))
      self._engine.say(message.get('text'))
      self._engine.runAndWait()
      self.initEngineProps()

    def worker(self):
        self._queue: queue.Queue = queue.Queue()
        self.initEngine()
        while True:
            message: dict = self._queue.get()
            if isinstance(message, StopThread): self._queue.task_done(); break
            self.say(message)

    def start(self):
      self._on = True
      self._thread.start()
      return self
    
    def play(self, text: str, voice: int = None, speed: int = None):
        self._queue.put({'text': text, 'voice': voice or self._voiceId, 'speed': speed or self._speed})

    def stop(self, wait: bool = False):
        if not wait: self._on = False
        self._queue.put(StopThread()) # add stop item to queue
        if not wait: self._engine.stop() # stop current speaking
        self._thread.join() # wait for worker to stop
        if wait: self._on = False

    def resume(self):
        self._on = True
        self._queue = queue.Queue() # reset queue
        self._engine = self.initEngine() # reset engine
        self._thread = threading.Thread(target=self.worker, daemon=True) # reset thread
        self._thread.start() # restart thread

    def switchPlayState(self, wait: bool = False):
        if self._on: self.stop(wait)
        else: self.resume()

    @staticmethod
    def test(text):
        engine: pyttsx3.Engine = None
        engine = pyttsx3.init()
        voices: list[Voice] = engine.getProperty('voices')
        engine.setProperty('rate', 200)
        engine.setProperty('voice', voices[0].id)
        engine.say(text)
        engine.runAndWait()