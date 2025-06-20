import sys
import socket
import threading
import time

HOST = "192.168.219.116"
SEND_PORT = 10002
RECV_PORT = 10001
BUF_SIZE = 1024

def recv_data(sock):
    while True:
        try:
            data = sock.recv(BUF_SIZE)

            if not data:
                print("Disconnected by no data")
                break

            str = data.decode()
            if str[0] == '<':
                print("{0}".format(str))
            else:
                print("<< {0}".format(str))

            if str == "<quit>":
                print("Thread exit by server")
                break

        except socket.error as e:
            print("Thread exit by socket error")
            break

        except ConnectionResetError as e:
            print("Disconnected by exception")
            break

def main(argc, argv):
    try:
        PORT = SEND_PORT
        sendsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sendsocket.connect((HOST, PORT))
        print("sendsocket connected {0}".format(PORT))

        PORT = RECV_PORT
        recvsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        recvsocket.connect((HOST, PORT))

        recvsocket_thread = threading.Thread(target=recv_data, args=(recvsocket,))
        recvsocket_thread.start()
        print("recvsocket connected {0}".format(PORT))

    except socket.error as e:
        print("Exit by socket error : host {0}, port {1}".format(HOST, PORT))
        sys.exit(1)

    while True:
        try:
            msg = input()
            if not recvsocket_thread.is_alive():
                break

            sendsocket.send(msg.encode())

            if msg == "<q>" or msg == "<quit>":
                break

        except KeyboardInterrupt as e:
            break

        except socket.error as e:
            print("Thread exit by socket error : "+ e)
            break

    sendsocket.close()
    recvsocket.close()
    print("Socket closed")

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)