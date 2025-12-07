#Class to represent dataset metadata 
class Dataset:

    #Constructor to initialize the dataset 
    def __init__(self, id, dataset_name, category, source, last_updated, record_count, file_size_mb, created_at=None):
        self._id = id #ID for the dataset
        self.dataset_name = dataset_name 
        self.category = category 
        self.source = source 
        self.last_updated = last_updated 
        self.record_count = record_count 
        self.file_size_mb = file_size_mb 
        self.created_at = created_at 

    #Function to get the dataset ID
    def get_id(self):
        return self._id

    #Function to convert object data to a dictionary to be used in dataframe
    def to_dict(self):
        """Helper for Streamlit DataFrame display"""
        return {
            "id": self._id,
            "dataset_name": self.dataset_name,
            "category": self.category,
            "source": self.source,
            "last_updated": self.last_updated,
            "record_count": self.record_count,
            "file_size_mb": self.file_size_mb
        }

    #Dataset details
    def __str__(self):
        return f"Dataset {self._id}: {self.dataset_name} , {self.file_size_mb} MB)"