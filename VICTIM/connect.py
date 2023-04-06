from utils import Connect

def connect(R_HOST, R_PORT):
    while True:
        connection = Connect(R_HOST, R_PORT)
        connection.connect()
        connection = None
        continue
    return
