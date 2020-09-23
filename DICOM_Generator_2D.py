class DICOM_Generator(tf.keras.utils.Sequence):
    def __init__(self, root_path, dicom_folder, dicom_labels, batch_size=16, num_classes=None, shuffle=True):
        self.root_path = root_path
        self.dicom_folder = self.dicom_folder
        self.dicom_labels = self.dicom_labels
        self.batch_size = batch_size
        self.num_classes = num_classes
        self.shuffle = shuffle
        self.on_epoch_end()

    def __len__(self):
        return len(self.indices) // self.batch_size)

    def __getitem__(self, index):
        index = self.index[index * self.batch_size:(index + 1) * self.batch_size]
        batch = [self.indices[k] for k in index]
        
        X, Y = self.get_batch(batch)
        return X, Y

    def on_epoch_end(self):
        self.index = np.arange(len(self.indices))
        if self.shuffle == True:
            np.random.shuffle(self.index)

    def get_batch(self, batch):
        X = # logic
        y = # logic
        
        for i, id in enumerate(batch):
            X[i,] = # logic
            y[i] = # labels

        return X, y
