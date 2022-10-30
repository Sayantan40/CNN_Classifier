from DeepClassifier.config.configuration import ConfigurationManager
from DeepClassifier.components.data_ingestion import DataIngestion
from DeepClassifier.logger.logger import logger

STAGE_NAME = "Data Ingestion stage"

try:
    def main():
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config = data_ingestion_config)
        data_ingestion.download_file()
        data_ingestion.unzip_and_clean()

except Exception as e:
    raise e


if __name__ == '__main__':
    
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    
    except Exception as e:
        logger.exception(e)
        raise e
