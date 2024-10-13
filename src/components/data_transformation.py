import sys
import os

from dataclasses import dataclass
# data manupulation lib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.pipeline import Pipeline

# custom made lib for logging and expection
from src.exception import  CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
    
    def get_transformation_object(self):
        """
            This function is for data tranformation 
        Raises:
            CustomExpection: to raise a error when system running

        Returns:
            _type_: preprocessor pipline combined
        """
        logging.info("Entered the data transformation block")
        try:
            numerical_features = ['reading_score','writing_score']
            catgorical_features = [
                "gender",
                "race_ethnicity", 
                "parental_level_of_education",	
                "lunch",
                "test_preparation_course"
                ]
            num_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='median')),
                    ('scaler',StandardScaler())
                ]
            )
            
            logging.info('numerical standard scaling completed')
            
            catgorical_pipeline = Pipeline(
                steps =[
                     ('imputer',SimpleImputer(strategy='most_frequent')),
                     ('one_hot_encoder',OneHotEncoder()),
                     ('scaler',StandardScaler(with_mean=False))
                ]
            )
            logging.info(f"Categorical columns: {numerical_features}")
            logging.info(f"Numerical columns: {catgorical_features}")
            logging.info('catgorical columns encoding  completed')
            
            preprocessor = ColumnTransformer(
                [
                    ('numerical_pipline',num_pipeline,numerical_features),
                    ('catgorical_pipline',catgorical_pipeline,catgorical_features),
                ]
            )
            
            logging.info('data transfromation completed')
            
            return preprocessor
        except  Exception as e:
            raise CustomExpection(e,sys)
    
    def initate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("Read train and test data is completed")
            
            logging.info("Obtaning preprocessor object")
            preprocessor_obj = self.get_transformation_object()
            
            target_column = 'math_score'
            
            input_feature_train_df = train_df.drop(columns=[target_column],axis=1)
            target_feature_train_df = train_df[target_column]
            
            input_feature_test_df = test_df.drop(columns=[target_column],axis=1)
            target_feature_test_df = test_df[target_column]
            
            logging.info(f'Apply preprocessing traing and testing dataframe')
            
            input_feature_train_arr =  preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)
            
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]
            
            
            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessor_obj
            )
            logging.info(f'Saved preprocessing object')
            
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
        except Exception as e:
            raise CustomExpection(e,sys)