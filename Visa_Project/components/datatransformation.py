import os,sys
import pandas as pd
import numpy as np
from Visa_Project.exception import CustomException
from Visa_Project.logger import logging
from Visa_Project.entity.config_entity import DataTransformationConfig
from Visa_Project.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from sklearn.compose import ColumnTransformer
from Visa_Project.constant import *
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, OneHotEncoder, PowerTransformer
from Visa_Project.utils.utils import read_yaml_file, load_data, save_numpy_array_data, save_object
from imblearn.combine import SMOTEENN

class DataTransformation:
    def __init__(self,data_transformation_config: DataTransformationConfig,
                 data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_artifact: DataValidationArtifact):
        try:
            logging.info(
                f"{'>>' * 30}Data Transformation log started.{'<<' * 30} \n\n")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            
        except Exception as e:
            raise CustomException(e,sys) from e
        
    def get_data_transformer_object(self)-> ColumnTransformer:
        try:
            schema_file_path = self.data_validation_artifact.schema_file_path
            dataset_schema = read_yaml_file(file_path = schema_file_path)

            numerical_columns = dataset_schema[NUMERICAL_COLUMN_KEY]
            ordinal_columns = dataset_schema[ORIDINAL_COLUMN_KEY]
            onehot_columns = dataset_schema[ONE_HOT_COLUMN_KEY]
            transformation_columns = dataset_schema[TRANSFORM_COLUMN_KEY]

            num_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler',StandardScaler())
            ])

            onehot_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy= 'most_frequent')),
                ('ordinal_encoder', OrdinalEncoder()),
                ('scaler',StandardScaler(with_mean=False))
            ])

            ordianal_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy= 'most_frequent')),
                ('one_hot_encoder', OneHotEncoder()),
                ('scaler',StandardScaler(with_mean=False))
            ]) 

            transform_pipeline = Pipeline(steps=[
                ('scaler', StandardScaler()),
                ('transformer',PowerTransformer())
            ])

            preprocessor = ColumnTransformer([
                ('num_pipeline', num_pipeline,numerical_columns),
                ('onehot_pipeline',onehot_pipeline,onehot_columns),
                ('ordinal_pipeline',ordianal_pipeline,ordinal_columns),
                ('transform_pipeline',transform_pipeline,transformation_columns)
            ])

            return preprocessor

        except Exception as e:
            raise CustomException(e,sys) from e
        
    def remove_outliers_IQR(self,col,df):
        try:
            percentile25 = df[col].quantile(0.25)
            percentile75 = df[col].quantile(0.75)
            iqr = percentile75 - percentile25
            upper_limit = percentile75 + 1.5 * iqr
            lower_limit = percentile25 - 1.5 * iqr
            df.loc[(df[col]> upper_limit),col] = upper_limit
            df.loc[(df[col]< lower_limit),col] = lower_limit

            return df
        except Exception as e:
            raise CustomException(e,sys) from e
        
    def initiate_data_transformation(self)-> DataTransformationArtifact:
        try:
            preprocessing_obj = self.get_data_transformer_object()

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            schema_file_path = self.data_validation_artifact.schema_file_path

            train_df = load_data(file_path = train_file_path, schema_file_path=schema_file_path)
            test_df = load_data(file_path = test_file_path, schema_file_path=schema_file_path)

            schema = read_yaml_file(file_path=schema_file_path)

            target_column_name = schema[TARGET_COLUMN_KEY]
            numerical_columns = schema[NUMERICAL_COLUMN_KEY]

            continous_columns = [feature for feature in numerical_columns if len(train_df[feature].unique())>=25]

            for col in continous_columns:
                self.remove_outliers_IQR(col = col, df = train_df)
            logging.info(f"Outlier capped in train df")

            for col in continous_columns:
                self.remove_outliers_IQR(col = col, df = test_df)
            logging.info(f"Outlier capped in test df")

            logging.info(f"")
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]
            
            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            smt = SMOTEENN(random_state=42, sampling_strategy='minority')
            input_feature_train_arr,target_feature_train_df = smt.fit_resample(input_feature_train_arr,target_feature_train_df)
            input_feature_test_arr, target_feature_test_df = smt.fit_resample(input_feature_test_arr,target_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            transformed_train_dir = self.data_transformation_config.transformed_train_dir
            transformed_test_dir = self.data_transformation_config.transformed_test_dir

            train_file_name = os.path.basename(train_file_path).replace(".csv",".npz")
            test_file_name = os.path.basename(test_file_path).replace(".csv",".npz")
        
            transformed_train_file_path = os.path.join(transformed_train_dir, train_file_name)
            transformed_test_file_path = os.path.join(transformed_test_dir, test_file_name)

            save_numpy_array_data(file_path=transformed_train_file_path, array=train_arr)
            save_numpy_array_data(file_path= transformed_test_file_path, array=test_arr)

            preprocessing_obj_file_path = self.data_transformation_config.preprocessed_object_file_path

            save_object(file_path= preprocessing_obj_file_path, obj=preprocessing_obj)

            data_transformation_artifact = DataTransformationArtifact(is_transformed=True,
                                                                      message="Data transformation successfull.",
                                                                      transformed_train_file_path=transformed_train_file_path,
                                                                      transformed_test_file_path=transformed_test_file_path,
                                                                      preprocessed_object_file_path=preprocessing_obj_file_path
                                                                      )
            logging.info(f"Data transformation artifact: {data_transformation_artifact}")
            return data_transformation_artifact

        except Exception as e:
            raise CustomException(e,sys) from e
        
    def __del__(self):
            logging.info(f"{'>>' * 30}Data Transformation log completed.{'<<' * 30} \n\n")