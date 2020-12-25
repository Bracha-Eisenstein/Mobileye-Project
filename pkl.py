import pickle

class Pkl:
    def __init__(self, file_path):
        data = pickle.load(file_path, encoding='latini')
        self.EM =
