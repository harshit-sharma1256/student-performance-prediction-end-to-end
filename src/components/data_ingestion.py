# IN THIS WE HAVE TO PERFORM TWO DIFFERENT TASKS:-
# 1. READING THE DATA
# 2. SPLITTING THE DATA INTO TRAIN AND TEST SET

import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

@dataclass     # THIS IS A DECORATOR.YOU CAN DIRECTLY DEFINE YOUR VARIABLES OF CLASS WITHOUT WRITING THE __init__ METHOD.
class DataIngestionConfig:
    """
    This has inputs like:-
    1. Where i have to save the train data
    2. Where i have to save the test data
    3. Where i have to save the raw data (actual csv file downloaded from kaggle ....)
    
    This has outputs like:-
    1. Numpy arrays
    2. Files saved at a particular location

    """
    # TRAINING DATA WILL BE SAVED IN 'artifacts' FOLDER IN FORM OF A .CSV FILE NAMED AS 'train.csv'.
    train_data_path : str = os.path.join('artifacts','train.csv')  
    test_data_path : str = os.path.join('artifacts','test.csv')
    raw_data_path : str = os.path.join('artifacts','data.csv')
    

# NOT:- IF YOU ONLY DEFINING VARIABLES INSIDE THE CLASS ---> USE @dataclass 
# IF YOU HAVE SOME OTHER FUNCTIONS INSIDE THE CLASS ---> USE CONSTRUCTOR('__init__' method)

class DataIngestion:
    def __init__(self) -> None:
        # WHEN I CALL THIS 'DataIngestion' CLASS THE ABOVE ALL 3 PATHS WILL  SAVED INSIDE THIS CLASS VARIABLE.
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        """
        WHAT THIS FUNCTION(METHOD) WILL DO:-
        IF YOUR DATA STORED IN SOME DATABASES LIKE- MONGODB OR MYSQL, THEN I WILL CREATE A MONGODB CLIENT OR MYSQL
        CLIENT IN UTILS.PY AND I CAN READ IT.THIS WILL BE COMPLEX PROCESS.

        HERE WE READING THE DATA IN A VERY SIMPLE MANNER.
         """
        logging.info("Entered the data ingestion part or component")

        try:
            df = pd.read_csv('notebook/data/stud.csv')
            logging.info('Read the dataset as dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            # os.path.dirname GIVES DIRECTORY NAME, IF IT EXISTS ALREADY THEN WE DON'T NEED TO DELETE IT
            # AND CREATE IT AGAIN.
            
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            logging.info("train test split initiated")
            train_set,test_set = train_test_split(df,random_state=42,test_size=0.2)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header =True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info('Ingestion of the data is completed')

            return (
                # I WILL RETURN THESE 2 INFORMATIONS BECAUSE I NEED THESE 2 INFOS IN DATATRANSFORMATION STAGE.
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
             
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()

    data_transformation=DataTransformation()
    train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)
    


