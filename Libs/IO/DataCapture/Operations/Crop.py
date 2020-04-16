import GlobalConfig

class Crop:
  apply = GlobalConfig.Defaults.crop

  y = GlobalConfig.Cropping.Y
  x = GlobalConfig.Cropping.X
  
  def __call__(self, img):
    if not Crop.apply:
      return img

    return img[self.y.start:self.y.end, self.x.start:self.x.end]
    
