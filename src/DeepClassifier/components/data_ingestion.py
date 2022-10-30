## The Data Ingestion Component
import os
import urllib.request as request
from zipfile import ZipFile
from DeepClassifier.entity.config_entity import DataIngestionConfig
from DeepClassifier.utils import get_size
from tqdm import tqdm ## This helps to create a progress bar 
from pathlib import Path
from DeepClassifier.logger.logger import logger

class DataIngestion:
    
    def __init__(self, config: DataIngestionConfig):
        
        self.config = config

    ## To download the zip file
    def download_file(self):
        
        if not os.path.exists(self.config.local_data_file):

            logger.info("Download started...")
            
            filename, headers = request.urlretrieve(
                                                   
                                                   url = self.config.source_URL,
                                                   filename = self.config.local_data_file
                                                    
                                                    )
            logger.info(f"{filename} download! with following info: \n{headers}")
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")

   
    ## This method performs a cleansing action removes unwanted files like files with other extensions
    ## And selects the required files . 
    def _get_updated_list_of_files(self, list_of_files):
        return [file for file in list_of_files if file.endswith(".jpg") and ("Cat" in file or "Dog" in file)]

    
    
    
    ## This extracts the zipfile  and removes files that have file size 0 kb.
    def _preprocess(self, zf: ZipFile, file: str, working_dir: str):
        
        target_filepath = os.path.join(working_dir, file)
        
        if not os.path.exists(target_filepath):
            zf.extract(file, working_dir)

        if os.path.getsize(target_filepath) == 0:
            
            logger.info(f"removing file:{target_filepath} of size: {get_size(Path(target_filepath))}")
            
            os.remove(target_filepath)


    
    
    ## To unzip and extract the downloaded zip file and perform cleansing action to remove unwanted files.
    def unzip_and_clean(self):

        logger.info(f"unzipping file and removing unawanted files")
        
        with ZipFile(file = self.config.local_data_file, mode="r") as zf: ## zf means zipfile
            
            list_of_files = zf.namelist()
            
            updated_list_of_files = self._get_updated_list_of_files(list_of_files)
            
            for file in tqdm(updated_list_of_files):
                self._preprocess(zf, file, self.config.unzip_dir)

    
    def create_test_data(self):
        """
        separte 30% of data into test data
        """
        pass