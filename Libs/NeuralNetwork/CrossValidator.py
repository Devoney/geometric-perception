import numpy as np
import Libs.DataConverter as DataConverter
import Libs.DataHelper as DataHelper

def AvgModelWeights(list_of_weights):
  weights_avg = list()

  for weights_list_tuple in zip(*list_of_weights):
    weights_avg.append(
      np.array([np.array(weights_).mean(axis=0) \
      for weights_ in zip(*weights_list_tuple)]))
    
  return weights_avg

def KfoldCrossValidation(model, datasets, nr_of_val_samples, train_method):
  #region Validations
  data_length = len(datasets[0][1])

  # Check that data is equally divideable
  mod = data_length % nr_of_val_samples
  if mod != 0:
    raise Exception('Length of data (' + str(data_length) + ') should be dividable by nr_of_val_samples (' + str(nr_of_val_samples) + ').')

  # Check that all data sets are equal in length
  for dataset in datasets:
    (label, data) = dataset
    if len(data) != data_length:
      raise Exception('Each dataset should have equal number of samples.')
  #endregion

  nr_of_bins = data_length // nr_of_val_samples

  weights_initial = model.get_weights()
  list_of_weights = []

  for bin_index in range(nr_of_bins):
    # TODO: Check why values are negative in the data
    (training, validation) = SplitTrainingValidation(datasets, bin_index, nr_of_val_samples)
    
    training = DataConverter.ConvertToNetworkInput(training)
    validation = DataConverter.ConvertToNetworkInput(validation)
    
    model.set_weights(weights_initial)

    # Randomize data
    (d, l) = training
    d = d[:]
    l = l[:]
    DataHelper.ShuffleInUnison(d, l)
    for i in range(10):
      training = (d, l)

    train_method(model, training, validation)
    
    list_of_weights.append(model.get_weights())

  weights_avg = AvgModelWeights(list_of_weights)
  model.set_weights(weights_avg)

def SplitTrainingValidation(dataset, bin_index, nr_of_val_samples):
  training = []
  validation = []
  nrOfLabels = len(dataset)

  start = nr_of_val_samples * bin_index
  end = start + nr_of_val_samples
  for i in range(nrOfLabels):
    (label, data) = dataset[i]
    validation_data = data[start:end]
    
    training_data = data[:]
    del training_data[start:end]

    validation.append((label, validation_data))
    training.append((label, training_data))
  
  return (training, validation)
  