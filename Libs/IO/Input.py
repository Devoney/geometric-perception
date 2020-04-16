def TakeNumericInput(default = 0):
  try:
    userInput = input()
    nrInput = ''
    chars = [i for i in userInput if i.isdigit()]
    for char in chars:
      nrInput = nrInput + char
    return int(nrInput)
  except:
    return default