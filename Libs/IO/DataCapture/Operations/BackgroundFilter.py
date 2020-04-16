from Libs.IO.Input import TakeNumericInput
import GlobalConfig
import Libs.IO.DataCapture.Operations.Crop as Crop
import math
import numpy as np

class BackgroundFilter:
  apply = False
  recording = False

  background = None

  def __init__(self):
    self._resetBackground()
  
  def __call__(self, img):
    if BackgroundFilter.recording:
      self._establishBackground(img)
    elif BackgroundFilter.apply:
      return self._subtractBackground(img)

    return img

  def _resetBackground(self):
    height = 0
    width = 0
    if Crop.Crop.apply:
      height = GlobalConfig.Cropping.height_cropped
      width = GlobalConfig.Cropping.width_cropped
    else:
      height = GlobalConfig.Img.height
      width = GlobalConfig.Img.width

    self.background = np.full(
      shape=(height, width),
      fill_value=int(math.pow(2, 16)-1)
    ).astype(np.uint16)
    print('Background reset')

  def _establishBackground(self, img):
    zeroFiltered = np.where(img == 0, 65535, img)
    self.background = np.where(zeroFiltered < self.background, zeroFiltered, self.background)

  def _subtractBackground(self, img):
    background_margin = GlobalConfig.background_margin
    background = np.where(self.background <= background_margin, background_margin, self.background)
    background = background - background_margin
    return np.where(img < background, img, 0)

  def _toggleRecording(self):
    BackgroundFilter.recording = not BackgroundFilter.recording
    if BackgroundFilter.recording:
        self._resetBackground()
    print('Background recording set to: ' + str(BackgroundFilter.recording))

  def _toggleUseBackgroundFilter(self):
    if self.background is None:
      return
    BackgroundFilter.apply = not BackgroundFilter.apply
    print('Using background filter set to: ' + str(BackgroundFilter.apply))