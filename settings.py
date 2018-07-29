# import pickle
# import os
# import io
# 
# class Settings(object):
#     debug = False
#     fps = 60
#     s_dims = 1366, 768
#     a_dims = 2 ** 12, 2 ** 10
#     
# settings = Settings()
# 
# pickler = pickle.Pickler()
# unpickler = pickle.Unpickler()
# 
# r = open("settings.txt",'rw')
# 
# if not os.path.exists("settings.txt"):
#     r.write(pickler.dumps(settings))
# else:
#     unpickler.read("")
# 
# r.close()

DEBUG = False

FPS = 60

SCREEN_WIDTH, SCREEN_HEIGHT = 1366, 768
ARENA_WIDTH, ARENA_HEIGHT = 2 ** 9, 2 ** 9
