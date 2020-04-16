import keyboard
import time

class KeyboardHelper:
  listening = True
  listen_key = None

  def __init__(self, pause, listen_key=None):
    self.pause = pause
    self.lastRelease = time.time()
    if not listen_key is None:
      self.listening = False
      def startListening():
        # print('Listening')
        self.listening = True
      self.OnRelease(listen_key, startListening)
      self.listen_key = listen_key

  def OnRelease(self, key, callback):
    if not self.listen_key is None and key == self.listen_key:
      raise Exception('This key has been reserved as listen key.')

    l = lambda argKey: self._debounce(callback, key)
    keyboard.on_release_key(key, l)

  def _debounce(self, callback, key):
    if key != self.listen_key and not self.listening:
      return
    
    now = time.time()
    elapsed = now - self.lastRelease
    if elapsed > self.pause:
      # print('Debounce passed: ' + str(key))
      if not self.listen_key is None:
        # print('Not listening anymore')
        self.listening = False
      # print('callback start')
      callback()
      # print('callback end')

if __name__ == "__main__":
  kbh = KeyboardHelper(1)
  kbh.OnRelease('R', lambda : print('OnRelease R'))
  kbh.OnRelease('P', lambda : print('OnRelease P'))
  input()    