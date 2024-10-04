from typing import List

class Question:
    def __init__(self, question: str):
        pass

class Quiz:

    def __init__(self, quiz_file_pth):
        self.quesions = []
        self.parse(quiz_file_pth=quiz_file_pth)

    def parse(self, quiz_file_pth):
        f = open(quiz_file_pth, 'r')
        content = f.read()
        f.close()

        for question in content.split('\n\n'):
            self.quesions.append(Question(question=question))

    def generate(self):
        pass

    