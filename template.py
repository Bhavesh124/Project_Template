import os
from pathlib import Path
import logging

logging.basicConfig(
    level = logging.INFO,
    format= "[%(asctime)s:%(levelname)s]: %(message)s"
)

while True:
    project_name = input("Enter Your project name: ")
    if project_name != '':
        break

logging.info(f"Creating project by name: {project_name} ")
list_of_files = [
    ".github/workflows/.gitignore",
    ".github/workflows/main.yaml",
    "{project_name}/__init__.py",
    "{project_name}/components/__init__.py",
    "{project_name}/config/__init__.py",
    "{project_name}/constant/__init__.py",
    "{project_name}/entity/__init__.py",
    "{project_name}/exception/__init__.py",
    "{project_name}/logger/__init__.py",
    "{project_name}/pipeline/__init__.py",
    "{project_name}/utils/__init__.py",
    f"config/config.yaml",
    "requirements.txt",
    "setup.py",
    "main.py",
    "schema.yaml"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir,filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"Creating a new directory at : (filedir) for file: {filename}")

    if(not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
        with open(filepath, "w") as f:
            pass
        logging.info(f"Create a new file: {filename} for path: {filepath}")

    else:
        logging.info(f"file is already present at: {filepath}")
