def string_process(oldValue):
    for elem in oldValue:
        if(elem == '.' or elem ==':' or elem ==' ' or elem ==','):
           oldValue = oldValue.replace(elem, '_')
    newString = oldValue + ".jpg"
    return newString