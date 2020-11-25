#load dicom from given path
def load_dicom(path, input_shape):
'''Input:
      path: path to dicom folder
      input_shape: number_of_slices x height x width'''
  slices = [pydicom.dcmread(path + "/" + slice) for slice in os.listdir(path)]
  
  return
