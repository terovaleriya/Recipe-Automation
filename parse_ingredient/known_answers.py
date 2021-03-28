import json
from copy import deepcopy


class Answers:
    def __init__(self, fileName):
        self.fileName = fileName
        self.answers = None

    def load_answers(self):
        with open(self.fileName) as f:
            self.answers = json.load(f)

    def save_answers(self):
        with open(self.fileName, 'w') as f:
            json.dump(self.answers, f)

    def has_answer(self, question):
        if self.answers is None:
            self.load_answers()
        return question in self.answers

    def get_answer(self, question):
        if self.answers is None:
            self.load_answers()
        return deepcopy(self.answers.get(question, None))

    def add_answer(self, question, answer):
        if self.answers is None:
            self.load_answers()
        self.answers[question] = deepcopy(answer)
        self.save_answers()
