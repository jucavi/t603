import pickle
import os

class Manager:
    def __init__(self, filename='default.pck', path=None):
        if not path:
            path = os.getcwd()
            
        self.file = os.path.join(os.path.dirname(path), filename)
    
    
    def load(self):
        print(f'Loading data from {self.file}...')
        try:
            with open(self.file, 'rb') as bf:
                data = pickle.load(bf)
        except Exception:
            print(f'Unable to load {self.file}')
            return []
        else:
            print('File successfully loaded')
            return data
    
    def write(self, data):
        with open(self.file, 'wb') as bf:
            print(f'Writing data into {self.file}')
            pickle.dump(data, bf)
            
