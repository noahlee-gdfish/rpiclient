import sys
import socket
import threading
import time

#DEFAULT_HOST = "192.168.219.116"
#DEFAULT_PORT = 9999
DEFAULT_HOST = "192.168.219.113"
DEFAULT_PORT = 9000
BUF_SIZE = 1024

def recv_data(client_socket):
    while True:
        try:
            data = client_socket.recv(BUF_SIZE)

            if not data:
                print("Disconnected by no data")
                break

            str = data.decode()
            print("{0}\n".format(str))

            if str == "OpenChatRequest":
                print("Open chat sockets here")

            with condition:
                condition.notify_all()

            if str == "<quit>":
                print("Thread exit by server")
                break

        except socket.error as e:
            print("Thread exit by socket error")
            break

        except ConnectionResetError as e:
            print("Disconnected by exception")
            break
    
    with condition:
        condition.notify_all()

def main(argc, argv):
    if argc >= 2:
        arg = argv[1].split(":")
        HOST = arg[0]
        if arg[1].isdigit():
            PORT = int(arg[1])
        else:
            PORT = DEFAULT_PORT
    else:
        HOST = DEFAULT_HOST
        PORT = DEFAULT_PORT

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))

        client_thread = threading.Thread(target=recv_data, args=(client_socket,))
        client_thread.start()
        print("Connect to server")

        # Wait for "connected" msg
        with condition:
            condition.wait()

    except socket.error as e:
        print("Exit by socket error : host {0}, port {1}".format(HOST, PORT))
        sys.exit(1)

    while True:
        try:
            msg = input(">> ")
            if not client_thread.is_alive():
                break

            if msg.strip() == "":
                continue

            client_socket.send(msg.encode())

            with condition:
                condition.wait()

            if msg == "q":
                break

        except KeyboardInterrupt as e:
            break

        except socket.error as e:
            print("Thread exit by socket error : "+ e)

    client_socket.close()

if __name__ == '__main__':
    condition=threading.Condition()
    main(len(sys.argv), sys.argv)