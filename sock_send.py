import sys, getopt
import socket
import time
import numpy as np


if __name__ == "__main__":
    my_argv = sys.argv[1:]
    opts, args = getopt.getopt(my_argv, "", ["dst-ip=", "dst-port=", "scale=", "timeslot="])
    dstIp = "10.0.0.1"
    dstPort = 8081
    scale = 1.0
    timeslot = 10
    for opt, arg in opts:
        if opt in ("--dst-ip",):
            dstIp = arg
        elif opt in ("--dst-port",):
            dstPort = int(arg)
        elif opt in ("--scale",):
            scale = float(arg)
        elif opt in ("--timeslot",):
            timeslot = int(timeslot)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    t1 = time.time()
    sc = np.random.exponential(scale=scale)
    print(sc)
    while True:
        message = "0" * 100
        sock.sendto(bytes(message, "utf-8"), (dstIp, dstPort))
        time.sleep(sc)
        if time.time() - t1 > timeslot:
            t1 = time.time()
            sc = np.random.exponential(scale=scale)
            print(sc)
