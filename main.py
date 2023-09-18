import socket
import time


def connect_to_blackbox():
    target_ip = '10.1.30.50'
    target_port = 23

    client_socket = None
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        timeout = 60
        client_socket.settimeout(timeout)

        client_socket.connect((target_ip, target_port))

    except socket.timeout:
        print("timeout")
        client_socket.close()
    except Exception as e:
        print("error: ", str(e))
        client_socket.close()

    finally:
        return client_socket


def listen_for_blackbox(client_socket):

    if client_socket is None:
        print("Could not connect to client...")
        exit()

    while True:
        try:
            response = client_socket.recv(1024)
            print(response.decode('utf-8'))
        except socket.timeout as st:
            print("timeout: ", str(st))
            client_socket.close()
            client_socket = connect_to_blackbox()
        except Exception as e:
            print("error: ", str(e))
            client_socket.close()
            client_socket = connect_to_blackbox()


def ping_blackbox(client_socket):

    if client_socket is None:
        print("Could not connect to client...")
        exit()

    while True:
        message = "#0:2\PING" + "\n"

        try:
            client_socket.send(message.encode('utf-8'))
            response = client_socket.recv(1024)
            print("RESPONSE: ", response.decode('utf-8'))
        except socket.timeout as st:
            print("timeout: ", str(st))
            client_socket.close()
            client_socket = connect_to_blackbox()
        except Exception as e:
            print("error: ", str(e))
            client_socket.close()
            client_socket = connect_to_blackbox()
        finally:
            time.sleep(3)


if __name__ == '__main__':
    client_socket = connect_to_blackbox()
    ping_blackbox(client_socket)
    # listen_for_blackbox(client_socket)

