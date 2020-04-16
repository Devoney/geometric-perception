from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as pyplot
import numpy as np
from Libs.NeuralNetwork.Plotting import PlotHistory

def Train(model, training, validation, epochs, batchSize):
  trainingData, trainingLabels = training

  history = model.fit(
    trainingData
    ,trainingLabels
    ,validation_data=validation
    ,epochs=epochs 
    ,batch_size=batchSize
  )

  # PlotHistory(history)

def TrainWithGenerator(model, epochs, training, validation, dirToSaveImages):
  datagen = ImageDataGenerator(
    featurewise_std_normalization=False,
    featurewise_center=False,
    samplewise_std_normalization=False,
    samplewise_center=False,
    rotation_range=1.2,
    width_shift_range=0.00,
    height_shift_range=0.00,
    horizontal_flip=False,
    vertical_flip=False,
    fill_mode='nearest',
    zoom_range=[0.97, 1.03],
    zca_whitening=False,
    #rescale=1/255
  )

  trainingData, trainingLabels = training

  #region Debug ImageDataGenerator
  if False:
    it = datagen.flow(trainingData, batch_size=1)
    # generate samples and plot
    for a in range(4):
      for i in range(9):
        # define subplot
        pyplot.subplot(330 + 1 + i)
        # generate batch of images
        batch = it.next()
        # convert to unsigned integers for viewing
        image = batch[0].astype('uint8')
        image = np.squeeze(image)
        # plot raw pixel data
        pyplot.imshow(image)
      # show the figure
      pyplot.show()
  #endregion
  
  datagen.fit(trainingData)
  flow = datagen.flow(
    trainingData, 
    trainingLabels, 
    batch_size=4, 
    save_to_dir=dirToSaveImages, 
    save_format='jpeg'
  )
  
  history = model.fit_generator(
    flow, 
    steps_per_epoch=len(trainingData) / 4, 
    epochs=epochs, 
    validation_data=validation,
    callbacks=[]
  )
  
  # PlotHistory(history)
