import numpy as np
import os
import glob
from keras.utils import Sequence
from DICOM_Utilities import *

class DICOM_Generator(Sequence):
    def __init__(self, root_path, dicom_folder, dicom_labels, input_shape=(256, 512, 512), batch_size=16, num_classes=None, shuffle=True, preprocess_fun=None):
        '''Note: Input_shape takes 3 values: number_of_slices x image_height x image_width'''
        self.root_path = root_path
        self.dicom_folder_name = dicom_folder
        self.mask_folder_name = dicom_labels
        self.input_shape = input_shape
        self.batch_size = batch_size
        self.num_classes = num_classes
        self.shuffle = shuffle
        self.preprocess_func = preprocess_func
        self.on_epoch_end()

    def __len__(self):
        return len(self.indices) // self.batch_size

    def __getitem__(self, index):
        return self.get_batch()

    def on_epoch_end(self):
        self.files = glob.glob(self.rooth_path + "/" + self.dicom_folder_name + "/*")
        self.files = [os.path.join(self.root_path, file) for file in self.files]
        self.files = np.random.choice(self.files, self.batch_size)
        if self.shuffle:
            self.files = np.random.choice(self.siles, self.batch_size)
            np.random.shuffle(self.files)

    def load_dicom_masks(self, mask_file, dcm_file, pkg):
        mask_file = glob.glob(mask_file+"\*.dcm")[0]
        structure = pydicom.read_file(mask_file)
        contours = read_structure(structure)
        dcm_masks, colors = get_mask(contours, dcm_file, pkg)
        
        dcm_masks = np.array(dcm_masks)
        dcm_masks = resample_2d(dcm_masks, self.input_shape)
        dcm_masks = np.reshape(dcm_masks, dcm_masks.shape+(1,))
        
        return dcm_masks
            
            
    def get_batch(self, batch):
        batch_dicoms = []
        batch_labels = []
        for file in self.files:

            mask_file = file.replace(self.dicom_folder_name, self.mask_folder_name)

            dcm_file, spacing, pkg = load_dicom(file, self.input_shape)
            dcm_masks = self.load_dicom_masks(mask_file, dcm_file, pkg)

            if self.preprocess_func != None:
                dcm_file = self.preprocess_func(dcm_file)

            #data augmentation
            dcm_file = np.array(dcm_file)
            dcm_masks = np.array(dcm_masks)

            #rescaling HU values to 0-1
            dcm_file = (dcm_file+abs(dcm_file.min()))*(1/(abs(dcm_file.min())+dcm_file.max()))
            dcm_masks = (dcm_masks+abs(dcm_masks.min()))*(1/(abs(dcm_masks.min())+dcm_masks.max()))

            batch_dicoms+=[dcm_file]
            batch_labels+=[dcm_masks]

            batch_dicoms = np.array(batch_dicoms)
            batch_labels = np.array(batch_labels)

        return batch_dicoms, batch_labels
