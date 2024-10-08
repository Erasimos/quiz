import os 
import shutil
from datetime import datetime

def new_quiz():

    date = datetime.now().date().strftime("%m_%d_%Y")
    folder_path = os.getcwd() + '/' + date
    os.mkdir(folder_path)
    quiz_template_file = os.getcwd() + '/src/templates/quiz_template.txt'
    new_quiz_file = folder_path + '/quiz.txt' 
    shutil.copy(quiz_template_file, new_quiz_file)


if __name__ == '__main__':
    new_quiz()