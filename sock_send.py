import sys, getopt
import socket
import time
import numpy as np


if __name__ == "__main__":
    my_argv = sys.argv[1:]
    opts, args = getopt.getopt(my_argv, "", ["dst-ip=", "dst-port=", "scale="])
    dstIp = "10.0.0.1"
    dstPort = 8081
    scale = 1.0
    for opt, arg in opts:
        if opt in ("--dst-ip",):
            dstIp = arg
        elif opt in ("--dst-port",):
            dstPort = int(arg)
        elif opt in ("--scale",):
            scale = float(arg)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        message = "0" * 100
        sock.sendto(bytes(message, "utf-8"), (dstIp, dstPort))
        sc = np.random.exponential(scale=scale)
        print(sc)
        time.sleep(sc)