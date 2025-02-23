import threading, queue, pyttsx3
from threading import Thread
from pyttsx3.voice import Voice
from time import sleep

class StopThread(): pass

class Speaker:
    def __init__(self, voice: int = 0, speed: int = 200):
        self.voiceId: int = voice
        self.speed: int = speed
        self.on: bool = True
        self.thread: Thread = threading.Thread(target=self.worker, daemon=True)

    def initEngine(self):
        self.engine = pyttsx3.init()
        voices: list[Voice] = self.engine.getProperty('voices')
        self.engine.setProperty('rate', self.speed)
        self.engine.setProperty('voice', voices[self.voiceId].id)

    def worker(self):
        self.queue: queue.Queue = queue.Queue()
        self.initEngine()
        while True:
            text = self.queue.get()
            if isinstance(text, StopThread): self.queue.task_done(); break
            if self.on:
              self.engine.say(text)
              self.engine.runAndWait()
            self.queue.task_done()

    def start(self):
      self.on = True
      self.thread.start()
      return self
    
    def add(self, text: str):
        self.queue.put(text)

    def waitAndStop(self):
        self.queue.put(StopThread())
        self.thread.join()
    
    def togglePause(self):
        self.on = not self.on # toggle pause
        if not self.on:
            # if paused, worker will skip the next items in queue
            self.queue.put(StopThread()) # add stop item to queue
            self.engine.stop() # stop current speaking
            self.thread.join() # wait for worker to stop
            self.queue = queue.Queue() # reset queue
            self.engine = self.initEngine() # reset engine
            self.thread = threading.Thread(target=self.worker, daemon=True) # reset thread
            self.thread.start() # restart thread

    @staticmethod
    def test(text):
        engine: pyttsx3.Engine = None
        engine = pyttsx3.init()
        voices: list[Voice] = engine.getProperty('voices')
        engine.setProperty('rate', 200)
        engine.setProperty('voice', voices[0].id)
        engine.say(text)
        engine.runAndWait()