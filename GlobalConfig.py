from Libs.IO.KeyboardHelper import KeyboardHelper as kbh
import os

histogram_mode = 0

class Paths:
  model_file = '3dperception_model.h5'
  data_dir = os.getcwd() + '\\data\\'

#region Image retrieval
class Img:
  width = 640
  height = 480
  bytes_per_pixel = 2

pipe_name = '\\\\.\\pipe\\occipital-structure-core'
#endregion

#region Image processing
resize_factor = 1
background_margin = 15
class Cropping:
  class Y:
    start = 8
    end = -30
  class X:
    start = 10
    end = -95

  height_cropped = Img.height - Y.start + Y.end
  width_cropped = Img.width - X.start + X.end
#endregion

class TargetImg:
  width = 128
  height = 128
  depth = 128

class Filtering:
  median_size = 7
  gaussian_sigma = 0.5

class ShortKeys:
  Quit = 'q' # Mnemonic: Quit
  ToggleNormalize = 'n' # Mnemonic: Normalize

class Defaults:
  capture_subject = 'capture'
  normalize = True
  crop = True
  _kbh = kbh(0.5, '|')
  def KeyboardHelper():
    return Defaults._kbh