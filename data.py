class Data:
    def __init__(self, file):
        with open(file) as the_file:
            paths = the_file.read().split("\n")
        
    def parse(file):
        with open(file) as the_file:
            paths = the_file.read().split("\n")
        return paths[0], paths[1:]