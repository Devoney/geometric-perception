import GlobalConfig
from Libs.IO.DataCapture.Operations.Crop import Crop
from Libs.IO.DataCapture.Operations.ShiftToCenter import ShiftToCenter
from Libs.IO.Input import TakeNumericInput
import numpy as np

class Average:
  apply = False
  avg_frames = 1
  frame_counter = 0
  frames = None
  initialising = False

  def _toggle(self):
    Average.apply = not Average.apply
    if Average.apply:
      Average.initialising = True
      print('Enter number of frames to average: ')
      Average.avg_frames = TakeNumericInput(1)
      height = 0
      width = 0
      if Crop.apply:
        height = GlobalConfig.Cropping.height_cropped
        width = GlobalConfig.Cropping.width_cropped
      else:
        height = GlobalConfig.Img.height
        width = GlobalConfig.Img.width
      Average.frames = np.zeros(shape=(Average.avg_frames, height, width)).astype(np.uint16)

      Average.frame_counter = 0
      Average.initialising = False

  def Set(avg_frames):
    Average.apply = True if avg_frames > 1 else False
    if Average.apply:
      Average.initialising = True
      Average.avg_frames = avg_frames
      height = 0
      width = 0
      if Crop.apply:
        height = GlobalConfig.Cropping.height_cropped
        width = GlobalConfig.Cropping.width_cropped
      else:
        height = GlobalConfig.Img.height
        width = GlobalConfig.Img.width
      Average.frames = np.zeros(shape=(Average.avg_frames, height, width)).astype(np.uint16)

      Average.frame_counter = 0
      Average.initialising = False

  def __call__(self, img):
    if Average.apply and not Average.initialising and Average.avg_frames > 1:
      if Average.frames[0].shape != img.shape:
        self._toggle()
        self._toggle()
      
      Average.frames[Average.frame_counter] = img[:]

      Average.frame_counter += 1

      if Average.frame_counter == Average.avg_frames:
        Average.frame_counter = 0
        Average.frames = np.where(Average.frames == 0, np.nan, Average.frames)
        img = np.nanmean(Average.frames, axis=0)
        img = np.where(np.isnan(img), 0, img)
      else:
        img = None # Not enough data yet. Caller should call again with a new image

    return img