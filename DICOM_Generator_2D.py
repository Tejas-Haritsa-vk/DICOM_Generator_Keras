from keras.utils import Sequence
import pydicom
import os
import glob

class DICOM_Generator(Sequence):
    def __init__(self, root_path, dicom_folder=None, dicom_labels=None, batch_size=16, num_classes=None, shuffle=True, _2D=False):
        self.root_path = root_path
        self.dicom_folder = self.dicom_folder
        self.dicom_labels = self.dicom_labels
        self.batch_size = batch_size
        self.num_classes = num_classes
        self.shuffle = shuffle
        self._2D = _2D
        self.on_epoch_end()

    def __len__(self):
        return len(self.indices) // self.batch_size)

    def __getitem__(self, index):
    
        if dicom_folder == "None":
            folders = os.path.listdir(self.root_path)[-1] #-1 to remove thumbs.db in windows 10
            self.batch_size = self.batch_size/len(folders)
            index = self.index[index * self.batch_size:(index + 1) * self.batch_size]
            dcm_batch_files = os.path.join(self.root_path, folders[0])
            batch = [dcm_batch_files[k] for k in index]
            X, Y = self.get_batch(batch, folders)
            return X, Y
    
        else:
            index = self.index[index * self.batch_size:(index + 1) * self.batch_size]
            dcm_batch_files = os.path.join(self.root_path, self.dicom_folder)
            batch = [dcm_batch_files[k] for k in index]
            X, Y = self.get_batch(batch)
            return X, Y

    def on_epoch_end(self):
        self.index = np.arange(len(self.indices))
        if self.shuffle == True:
            np.random.shuffle(self.index)

    def load_dicoms(self, batch):
        dcm_files = [pydicom.read(dcm) for dcm in glob.glob(batch+"\*.dcm")]
        
    def load_dicoms_labels(self, batch):
        if not _2D:
            dcm_labels = [pydicom.read(dcm) for dcm in glob.glob(batch+"\*.png")] + [pydicom.read(dcm) for dcm in glob.glob(batch+"\*.jpg")] + [pydicom.read(dcm) for dcm in glob.glob(batch+"\*.jpeg")]
        
        else:
            batch
            
    def get_batch(self, batch, foldes=None):
        
        if folder != "None":
            dcm_files = []
            dcm_labels = []
            for i, folder in enumrate(folders):
                files = load_dicoms(batch.replace(folders[0], folders[i]))
                labels = load_dicom_labels(batch)
                dcm_files.append(files)
                dcm_labels.append(labels)
        else:
            dcm_files = load_dicoms(batch)
            
        if dicom_labels == "None":
            pass
        else:
            dcm_labels = load_dicom_labels(batch)
            
        
        for i, id in enumerate(batch):
            X[i,] = # logic
            y[i] = # labels

        return X, y
