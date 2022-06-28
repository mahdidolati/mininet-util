import sys, getopt
import socket

if __name__ == "__main__":
    my_argv = sys.argv[1:]
    opts, args = getopt.getopt(my_argv, "", ["host-ip=", "host-port="])
    hostIp = "10.0.0.2"
    hostPort = 8081
    for opt, arg in opts:
        if opt in ("--host-ip",):
            hostIp = arg
        elif opt in ("--host-port",):
            hostPort = int(arg)

    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((hostIp, hostPort))
    
    bufferSize  = 1024
    while(True):
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        # message = bytesAddressPair[0]
        # address = bytesAddressPair[1]
        # clientMsg = "Message from Client:{}".format(message)
        # clientIP  = "Client IP Address:{}".format(address)    
        # print(clientMsg)
        # print(clientIP)