import os 
import shutil
from datetime import datetime

def new_quiz():

    date = datetime.now().date().strftime("%m_%d_%Y")
    folder_path = os.getcwd() + '/' + date
    os.mkdir(folder_path)
    template_quiz_file = os.getcwd() + '/quiz_template.txt'
    new_quiz_file = folder_path + '/quiz.txt' 
    shutil.copy(template_quiz_file, new_quiz_file)


if __name__ == '__main__':
    new_quiz()