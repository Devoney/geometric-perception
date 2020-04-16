from PIL import Image
import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import signal
import struct
import subprocess
import sys
import time
import time
import win32pipe, win32file, pywintypes

# Occipital Structure Core data comes in via a pipe, this is the client for it
class StructureCoreClient:
  def __init__(self, pipe_name, width, height, bytes_per_pixel):
    self.pipe_name = pipe_name
    self.width = width
    self.height = height
    self.nrOfBytes = height * width * bytes_per_pixel
    self.subprocess = None

  def Connect(self):
    self._startServer()

    self.handle = win32file.CreateFile(
      self.pipe_name,
      win32file.GENERIC_READ | win32file.GENERIC_WRITE,
      0,
      None,
      win32file.OPEN_EXISTING,
      0,
      None
    )
    
    if self.handle == win32file.INVALID_HANDLE_VALUE:
      return False

    self._setPipeMode()
    return True

  def Disconnect(self):
    try:
      os.kill(self.subprocess.pid, signal.SIGTERM)
    except Exception as inst:
      print('Error while closing server process')
      print(type(inst))
      print(inst.args)
      print(inst)
    
  def ReadImage(self):
    resp = win32file.ReadFile(self.handle, self.nrOfBytes)
    buffer = bytearray(resp[1])
    datatype = np.dtype(np.uint16)
    datatype = datatype.newbyteorder('<')
    imgbuffer = np.frombuffer(buffer, datatype)
    return np.reshape(imgbuffer, (self.height, self.width))

  def _startServer(self):
    self.subprocess = subprocess.Popen(
      ["D:\\Data\\Software\\Occipital Skanect Structore Core\\StructureSDK-CrossPlatform-0.7.3-ROS\\StructureSDK-CrossPlatform-0.7.3-ROS\\build\\Samples\\SimpleStreamer\\Debug\\SimpleStreamer.exe"],
      creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    time.sleep(0.5)

  def _setPipeMode(self):
    res = win32pipe.SetNamedPipeHandleState(self.handle, win32pipe.PIPE_READMODE_BYTE, None, None)
    if res == 0:
      print(f"SetNamedPipeHandleState return code: {res}")