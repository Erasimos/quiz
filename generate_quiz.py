from quiz import Quiz
import sys

if __name__ == '__main__':
    quiz_file_pth = sys.argv[1]
    quiz = Quiz(quiz_file_pth=quiz_file_pth)
    quiz.generate()
    