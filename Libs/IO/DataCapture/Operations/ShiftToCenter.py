from Libs.Image.MiscOperations import CropToBoundingBox, ScaleToSize
import GlobalConfig
import numpy as np

class ShiftToCenter:
  apply = False

  def __call__(self, img):
    if not ShiftToCenter.apply:
      return img

    maxValue = np.amax(img)
    if maxValue != 0:
      # there is no object in the scene, so cropping to a boudning box makes no sense
      img = CropToBoundingBox(img)

    img = ScaleToSize(
      img,
      GlobalConfig.TargetImg.height,
      GlobalConfig.TargetImg.width,
      GlobalConfig.TargetImg.depth
    )

    return img