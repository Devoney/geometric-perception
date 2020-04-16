from tensorflow.keras import optimizers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Dropout, Flatten, Dense

def CreateConvolutionNetwork(inputShape, nr_of_classes, learning_rate):
  kernelSize = 3
  kernel = (kernelSize, kernelSize)

  model = Sequential()
  model.add(Conv2D(16, kernel_size=kernel, padding='same', input_shape=inputShape, activation='relu'))
  model.add(MaxPooling2D(pool_size=(2, 2)))

  model.add(Conv2D(32, kernel_size=kernel, padding='same', activation='relu'))
  model.add(MaxPooling2D(pool_size=(2, 2)))

  model.add(Conv2D(64, kernel_size=kernel, padding='same', activation='relu'))
  model.add(MaxPooling2D(pool_size=(2, 2)))

  model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors
  model.add(Dense(32, activation='relu'))
  model.add(Dropout(0.3))
  model.add(Dense(32, activation='relu'))
  model.add(Dropout(0.3))
  model.add(Dense(nr_of_classes, activation='softmax'))

  sgd = optimizers.SGD(lr=learning_rate, decay=1e-6, momentum=0.1, nesterov=True)
  model.compile(loss='categorical_crossentropy', 
              optimizer=sgd,
              metrics=['accuracy'])
  
  return model