import logging
import sys, getopt
import socket
import time

Log_Format = "%(levelname)s %(asctime)s - %(message)s"


if __name__ == "__main__":
    my_argv = sys.argv[1:]
    opts, args = getopt.getopt(my_argv, "", ["host-ip=", "host-port=", "log-interval="])
    hostIp = "10.0.0.2"
    hostPort = 8081
    logInterval = 10
    for opt, arg in opts:
        if opt in ("--host-ip",):
            hostIp = arg
        elif opt in ("--host-port",):
            hostPort = int(arg)
        elif opt in ("--log-interval",):
            logInterval = int(arg)

    logging.basicConfig(filename = "log-{}.log".format(hostIp),
                    format = Log_Format, 
                    level = logging.DEBUG)

    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((hostIp, hostPort))
    
    bufferSize  = 1024
    estimatedRate = dict()
    t = time.time()
    while(True):
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1][0]
        if address not in estimatedRate:
            estimatedRate[address] = 0
        estimatedRate[address] += 1
        if time.time() - t >= logInterval:
            for address in estimatedRate:
                estimatedRate[address] /= logInterval
            logging.info(str(estimatedRate))
            t = time.time()
            estimatedRate = dict()
        # clientMsg = "Message from Client:{}".format(message)
        # clientIP  = "Client IP Address:{}".format(address)    
        # print(clientMsg)
        # print(clientIP)