from Libs.Image.MiscOperations import NormalizeFor8Bit
import GlobalConfig
import numpy as np

class Normalize:
  apply = GlobalConfig.Defaults.normalize

  def _toggle(self):
    Normalize.apply = not Normalize.apply

  def __call__(self, img, img_original):
    if self.apply:
      img = NormalizeFor8Bit(img)
      img_original = NormalizeFor8Bit(img_original)
    else:
      img = (img / 256).astype(np.uint16)
      img_original = (img_original / 256).astype(np.uint16)

    return (img, img_original)