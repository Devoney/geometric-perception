import numpy as np

def GetWidthHeight(img_array):
  width = np.size(img_array, 0)
  height = np.size(img_array, 1)
  return (width, height)

def ShuffleInUnison(a, b):
    rng_state = np.random.get_state()
    np.random.shuffle(a)
    np.random.set_state(rng_state)
    np.random.shuffle(b)

def SplitTrainingValidation(dataset, nr_of_val_samples):
  training = []
  validation = []
  nrOfLabels = len(dataset)

  for i in range(nrOfLabels):
    (label, data) = dataset[i]
    training.append((label, data[:-nr_of_val_samples]))
    validation.append((label, data[-nr_of_val_samples:]))
  
  return (training, validation)