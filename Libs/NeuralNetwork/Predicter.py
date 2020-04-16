from Libs.DataConverter import ConvertImg
import math
import numpy as np
import os
import tensorflow as tf

class Predicter:
  model = None
  labels = []
  last_prediction = None

  def __init__(self, model_file, data_dir):
    self.model = tf.keras.models.load_model(model_file)
    cwd = os.getcwd()
    self.labels = [f.name for f in os.scandir(data_dir) if f.is_dir()]

  def Predict(self, img):
    img_nn = ConvertImg(img)
    shape = img_nn.shape
    img_nn = np.reshape(img_nn, (1, shape[0], shape[1], shape[2]))
    prediction = self.model.predict(img_nn)[0]
    
    index = np.argmax(prediction)
    label = self.labels[index]

    output = ''
   
    summed = np.sum(prediction)
    true_prediction = np.true_divide(prediction, summed)
    percentage = math.floor(true_prediction[index] * 1000) / 10
    # if label != self.last_prediction:
    #   output = "Percentages of prediction:\r\n"
    #   for i in range(len(true_prediction)):
    #     output = output + "\t" + self.labels[i] + ": " + str(math.floor(true_prediction[i] * 1000) / 10) + "\r\n"
      
    #   print(output)

    self.last_prediction = label
    return label + ' (' + str(percentage) + '%)'