import os
import sys

import numpy as np
import pandas as pd 
import dill

from src.exepection import CustomExpection
from src.logger import logging

def save_object(file_path,obj):
    try:
        logging.info("Obect save initalize")
        dir_path = os.path.dirname(file_path)
        
        os.makedirs(dir_path,exist_ok=True)
        
        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)
        
    except Exception as e:
        raise CustomExpection(e,sys)