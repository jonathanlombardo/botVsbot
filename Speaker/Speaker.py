import threading, queue, pyttsx3, json
from threading import Thread
from pyttsx3.voice import Voice
from time import sleep

class StopThread(): pass

class Speaker:
    def __init__(self, voice: int = 0, speed: int = 200):
        self._on: bool = True
        self._voiceId: int = voice
        self._speed: int = speed
        self._thread: Thread = threading.Thread(target=self._worker, daemon=True)
        self._initEngine()

    def _initEngine(self):
        self._engine = pyttsx3.init()
        self._voices: list[Voice] = self._engine.getProperty('voices')
        self._initEngineProps()

    def _initEngineProps(self):
      self._engine.setProperty('voice', self._voices[self._voiceId].id)
      self._engine.setProperty('rate', self._speed)

    def _say(self, message: dict):
      if not self._on: return
      self._engine.setProperty('voice', self._voices[message.get('voice')].id)
      self._engine.setProperty('rate', message.get('speed'))
      self._engine.say(message.get('text'))
      self._engine.runAndWait()
      self._initEngineProps()

    def _worker(self):
        self._queue: queue.Queue = queue.Queue()
        self._initEngine()
        while True:
            message: dict = self._queue.get()
            if isinstance(message, StopThread): self._queue.task_done(); break
            self._say(message)

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
        self._engine = self._initEngine() # reset engine
        self._thread = threading.Thread(target=self._worker, daemon=True) # reset thread
        self._thread.start() # restart thread

    def switchPlayState(self, wait: bool = False):
        if self._on: self.stop(wait)
        else: self.resume()

    @staticmethod
    def play(text, voice=0, speed=200):
        if not isinstance(text, list): text = [text]
        engine: pyttsx3.Engine = None
        engine = pyttsx3.init()
        voices: list[Voice] = engine.getProperty('voices')
        engine.setProperty('rate', speed)
        engine.setProperty('voice', voices[voice].id)
        for t in text: engine.say(text)
        engine.runAndWait()

    @staticmethod
    def getVoices(dump=False):
        engine: pyttsx3.Engine = None
        engine = pyttsx3.init()
        voices: list[Voice] = engine.getProperty('voices')
        voicesData = [{'id': i, 'name': voice.name, 'lang': voice.languages } for i, voice in enumerate(voices)]
        if dump: json.dumps(print(voicesData), indent=2)
        return voicesData
    