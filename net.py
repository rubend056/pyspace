import pickle

from objects import *

import socket
import threading

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 60000              # Arbitrary non-privileged port

class Player(object):
    couter = 1
    def __init__(self, conn, addr):
        self.name = "Player {}".format(self.couter)
        self.couter += 1
        self.conn = conn
        self.addr = addr
        self.ship = None
        
    def __str__(self):
        return "{} on {}".format(self.name, self.addr)



class Net(object):
    current = None
    def __init__(self):
        Net.current = self
        self.pickler = pickle.Pickler()
        self.unpickler = pickle.Unpickler()
        
        self.ships = []

        self.s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_socket.bind((HOST, PORT))
        self.s_socket.listen(5)

        self.player_list = []

        self.s_thread = threading.Thread(None, Net.accept, "server_thread", [self])
        self.s_thread.start()

        print "Created server thread on port ", PORT

    def accept(self):
        while 1:
            conn, addr = self.s_socket.accept()
            player = Player(conn, addr)
            self.player_list.append(player)
            print player, ' connected'
    
    def update(self, this_ship, other_ships):
        # Pickle the hell out of it and send it over
        for player in self.player_list:
            if player.ship == None:  # Create a ship for any non-existent one
                ship = Ship()
                player.ship = ship
                ship.synced = True
                
        
        return None # Must return a list of other ships for rendering and physics
    
    def shutdown(self):
        del self.s_thread
        self.s_socket.close()
        for player in self.player_list:
            player.conn.close()