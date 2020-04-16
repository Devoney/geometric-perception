from Libs.NeuralNetwork.Predicter import Predicter
import cv2
import GlobalConfig

class Predict:
  apply = False
  predicter = None

  def __call__(self, img, boundingBox, img_original):
    if Predict.apply:
      if self.predicter is None:
        self.predicter = Predicter(GlobalConfig.Paths.model_file, GlobalConfig.Paths.data_dir)

      prediction = self.predicter.Predict(img)

      ((yStart, yEnd), (xStart, xEnd)) = boundingBox

      cv2.putText(
        img=img_original, 
        text=prediction, 
        org=(yStart, xStart), 
        fontFace=0, 
        fontScale=1, 
        color=(0,0,255)
      )
    
    return img_original


