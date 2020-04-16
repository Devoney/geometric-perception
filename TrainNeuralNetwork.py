#region Imports
import math
import numpy as np
import os

import Libs.DataConverter as DataConverter
import Libs.DataHelper as DataHelper

import Libs.IO.DataReader as DataReader
import GlobalConfig
from Libs.DataConverter import ConvertToNetworkInput
from Libs.NeuralNetwork.Creator import CreateConvolutionNetwork
from Libs.NeuralNetwork.Training import TrainWithGenerator, Train

import tensorflow as tf
#endregion

#region constants
epochs = 32
lr = 0.001
batch_size = None
# img_gen_dir = os.getcwd() + '\\temp\\img_gen\\'
img_gen_dir = 'R:\\'
nr_of_val_samples = 16
train_with_generator = True
save_model = True
load_model = False
#endregion
(nr_of_imgs, datasets) = DataReader.ReadData(GlobalConfig.Paths.data_dir)

(height, width) = datasets[0][1][0].shape

if GlobalConfig.resize_factor != 1:
  height = int(height * GlobalConfig.resize_factor)
  width = int(width * GlobalConfig.resize_factor)
  
channels = 3
nr_of_labels = len(datasets)

if load_model:
  model = tf.keras.models.load_model(GlobalConfig.model_file)
  print('Model loaded from: ' + GlobalConfig.model_file)
else:
  model = CreateConvolutionNetwork((GlobalConfig.TargetImg.height, GlobalConfig.TargetImg.width, channels), nr_of_labels, lr)
  print('Model created by code')

networkInput = ConvertToNetworkInput(datasets)

TrainWithGenerator(model, epochs, networkInput, None, img_gen_dir)

if save_model:
  model.save(GlobalConfig.Paths.model_file)
  print('Model saved to: ' + GlobalConfig.Paths.model_file)

print('End')