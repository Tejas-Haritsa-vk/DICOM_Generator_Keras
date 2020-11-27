import numpy as np
from scipy.ndimage import interpolation

#load dicom from given path
def load_dicom(path, input_shape):
      '''Input:
      path: path to dicom folder
      input_shape: number_of_slices x height x width'''
      slices = [pydicom.dcmread(path + "/" + slice) for slice in os.listdir(path)]

      try:
            slices.sort(key=lambda x: float(x.ImagePositionPatient[2])
      except Exception as error:
      #       print(error)
            slices.sort(key=lambda x: float(x.InstanceNumber))

      try:
            slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
      except:
            slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)

      for slice in slices:
            slice.SliceThickness = slice_thickness

      hu_pix = get_pixels_hu(slices)
      hu_pix_resampled, spacing = resample(hu_pix, slices, input_shape)
      hu_pix_resampled = [np.reshape(i, (input_shape[1], input_shape[2], 1)) for i in hu_pix_resampled]

      z = [round(slice.ImagePositionPatient[2], 1) for slice in slices]
      pos_r = slices[0].ImagePositionPatient[1]
      spacing_r = slices[0].PixelSpacing[1]
      pos_c = slices[0].ImagePositionPatient[0]
      spacing_c = slices[0].PixelSpacing[0]
      pkg = [z, pos_r, pos_c, spacing_r, spacing_c, hu_pix.shape]

      return hu_pix_resampled, spacing, pkg

                        
def resample(image, input_shape, scan=False, new_spacing=[1,1,1]):
      if scan:
            spacing = np.array([scan[0].SliceThickness], dtype=np.float32)
      
      reslice = input_shape[0]/image.shape[0]
      rescale_height = input_shape[1]/image.shape[1]
      rescale_width = input_shape[2]/image.shape[2]   
                        
      resize_factor = np.array([reslice, rescale_height, rescale_width])
      new_real_shape = image.shape*resize_factor
      new_shape = np.round(new_real_shape)
      real_resize_factor = new_shape/image.shape
      new_spacing = spacing/real_resize_factor
      
      image = interpolation.zoom(image, real_resize_factor, mode="nearest")
                        
      return image, new_spacing
