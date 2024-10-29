import os
import re
import sys
import subprocess

# Regex patterns for each attribute
title_pattern = r'title\s*=\s*(.+)'
type_pattern = r'type\s*=\s*(.+)'
body_pattern = r'body\s*=\s*(.+)'
answer_pattern = r'answer\s*=\s*(.+)'
points_pattern = r'points\s*=\s*(\d+)'

latex_head = r"""
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\title{THE QUIZ}
\maketitle
"""

latex_tail = r"""
\end{document}
"""

class Question:
    def __init__(self, question: str):
        self.title = re.search(title_pattern, question).group(1)
        self.quiz_type = re.search(type_pattern, question).group(1)
        self.body = re.search(body_pattern, question).group(1)
        self.answer = re.search(answer_pattern, question).group(1)
        self.points = re.search(points_pattern, question).group(1)
    
    def __repr__(self):
        return f"Title: {self.title}, Type: {self.quiz_type}, Body: {self.body}, Answer: {self.answer}, Points: {self.points})"

class Quiz:

    def __init__(self, quiz_date: str):
        self.questions = []
        self.quiz_pth = os.getcwd() + '/' + quiz_date + '/'
        self.parse()

    def parse(self):

        quiz_file_pth = self.quiz_pth + '/quiz.txt'
        f = open(quiz_file_pth, 'r')
        content = f.read()
        f.close()

        for question in content.split('\n\n'):
            self.questions.append(Question(question=question))

    def cleanup(self):
        allowed_extensions = ['.pdf', '.txt', '.tex']

        for filename in os.listdir(self.quiz_pth):
            file_path = os.path.join(self.quiz_pth, filename)
            
            if os.path.isfile(file_path):
                file_extension = os.path.splitext(filename)[1].lower()

                if file_extension not in allowed_extensions:
                    print(f"Removing: {file_path}")
                    os.remove(file_path)

    def generate_answer_sheet(self):
        pass

    def generate_question_sheet(self):

        with open("src/templates/question_template.tex", "r") as template:
            latex_template = template.read()

        question_sheet_pth = self.quiz_pth + '/question_sheet.tex'
        with open(question_sheet_pth, "w") as question_sheet:

            question_sheet.write(latex_head)

            for question in self.questions:
                latex_filled = (latex_template
                .replace("<<TITLE>>", question.title)
                .replace("<<TYPE>>", question.quiz_type)
                .replace("<<BODY>>", question.body)
                .replace("<<ANSWER>>", question.answer)
                .replace("<<POINTS>>", question.points))

                question_sheet.write(latex_filled)

            question_sheet.write(latex_tail)
        
        subprocess.run(["pdflatex", f"-output-directory={self.quiz_pth}", question_sheet_pth], check=True)

    def generate_presentation(self):
        pass

    def generate(self):
        self.generate_question_sheet()
        self.generate_answer_sheet()
        self.generate_presentation()
        self.cleanup()
    
if __name__ == '__main__':
    quiz_date = sys.argv[1]
    quiz = Quiz(quiz_date=quiz_date)
    quiz.generate()
    