import os 
import shutil
from datetime import datetime

def new_quiz():

    date = datetime.now().date().strftime("%m_%d_%Y")
    script_directory = os.path.dirname(os.path.abspath(__file__))
    folder_path = script_directory + '/../quizes/' + date
    os.mkdir(folder_path)
    quiz_template_file = script_directory + '/templates/quiz_template.txt'
    new_quiz_file = folder_path + '/quiz.txt' 
    shutil.copy(quiz_template_file, new_quiz_file)
    print(new_quiz_file)


if __name__ == '__main__':
    new_quiz()