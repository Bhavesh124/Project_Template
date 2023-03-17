from Visa_Project.exception import CustomException
from Visa_Project.logger import logging
from flask import Flask
import os,sys

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    try:
        raise Exception("we are testing custom exception")
    except Exception as e:
        Visa = CustomException(e,sys)
        logging.info(Visa.error_message)
        logging.info("we are testing logging file")

if __name__ == "__main__":
    app.run(debug=True)