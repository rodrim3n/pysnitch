import os
import time


def run(*args):
    socket = 'viene por args'
    file_name = 'viene por args'

    try:
        f = open(os.getcwd()+"/"+file_name, "rb")

        while True:
            data = f.read(4096)
            if not data:
                break
            socket.sendall(data)
        f.close()
        time.sleep(0.8)
        socket.sendall("EOFX")
        time.sleep(0.8)

        return "File transfered."
    except:
        socket.sendall("EOFX")
        time.sleep(0.8)
        return "Failed to transfer a file."
