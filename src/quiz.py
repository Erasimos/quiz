import re
import subprocess
import os

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
        # Extracting each attribute using regex
        self.title = re.search(title_pattern, question).group(1)
        self.quiz_type = re.search(type_pattern, question).group(1)
        self.body = re.search(body_pattern, question).group(1)
        self.answer = re.search(answer_pattern, question).group(1)
        self.points = re.search(points_pattern, question).group(1)
    
    def __repr__(self):
        return f"Title: {self.title}, Type: {self.quiz_type}, Body: {self.body}, Answer: {self.answer}, Points: {self.points})"

class Quiz:

    def __init__(self, quiz_file_pth):
        self.questions = []
        self.parse(quiz_file_pth=quiz_file_pth)

    def parse(self, quiz_file_pth):
        f = open(quiz_file_pth, 'r')
        content = f.read()
        f.close()

        for question in content.split('\n\n'):
            self.questions.append(Question(question=question))

    def generate_answer_sheet(self):
        pass

    def generate_question_sheet(self):

        with open("latex/question_template.tex", "r") as template:
            latex_template = template.read()

        with open("latex/question_sheet.tex", "w") as question_sheet:

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
        
        pth = os.path.join(os.getcwd(), "latex", "question_sheet.tex")
        print(pth)
        subprocess.run(["pdflatex", pth])

    def generate_presentation(self):
        pass

    def generate(self):
        self.generate_question_sheet()
        self.generate_answer_sheet()
        self.generate_presentation()
        print(self.questions)        

    