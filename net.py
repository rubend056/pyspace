import pickle

class Net(object):
    current = None
    def __init__(self):
        Net.current = self
        self.pickler = pickle.Pickler()
        self.unpickler = pickle.Unpickler()
    
    def update(self, this_ship, other_ships):
        # Pickle the hell out of it and send it over
        
        
        return None # Must return a list of other ships for rendering and physics