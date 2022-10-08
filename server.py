"""=====================================================================================================================
 * Project Info Header
 *================================================================================
 *================================================================================
 *  Author: Kevin Penton
 *  Panther ID: 6173069
 *
 *  Certification: I understand FIU's academic policies, and I certify
 *                 that this work is my own and that none of it is the work of any
 *                 other person.
 *
 *  Description: The Accio server is an extension of the simplified server that processes multiple simultaneous
 *               connections in parallel and saves the received data into the specified folder (following the format
 *               1.file, 2.file, etc.)
 *
 *  Usage:  server.py <PORT> <FILE-DIR>
 *==================================================================================================================="""

import threading
import sys
import socket


def accept_conn(host, port, conn_fileDir, conn_counter):
    # Creates the socket instance
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(10)

    try:
        # Opening listening socket
        sock.bind((host, port))
        sock.listen(1)

        try:
            while True:
                # Accepts connection
                clientSocket, clientAddress = sock.accept()

                with clientSocket:

                    # Creates variable for command
                    cmd = b'accio\r\n'

                    # Sends accio\r\n command
                    clientSocket.send(cmd)

                    # Receives data for the first time
                    bytesRecv1 = clientSocket.recv(1024)

                    # Sends second accio\r\n command
                    cmd2Send = clientSocket.send(cmd)

                    # Receives data for the second time
                    bytesRecv2 = clientSocket.recv(1024)

                    # Creates binary file
                    newFile = open("%s/%s.file" % (conn_fileDir, conn_counter), 'wb')

                    while True:
                        recvFile = clientSocket.recv(1024)
                        if not recvFile:
                            break
                        newFile.write(recvFile)

                    newFile.close()

        except socket.error:
            sys.stderr.write("ERROR: Failed to connect to functioning server\n")
            newFile = open("%s/%s.file" % (conn_fileDir, conn_counter), 'w')
            newFile.write("ERROR")
            newFile.close()

    except socket.error:
        sys.stderr.write("ERROR: Fail to bind / execute\n")
        exit(1)

def main():
    try:
        host = '0.0.0.0'
        port = int(sys.argv[1])
        fileDir = sys.argv[2]

        if port < 1023 or port > 65535:
            sys.stderr.write("ERROR: Out of range port number\n")
            exit(1)

    except OverflowError:
        sys.stderr.write("ERROR: Invalid port number")
        exit(1)

    try:
        counter = 1
        threads = []
        # Creates a thread for each connection
        for _ in range(1,11):
            t = threading.Thread(target=accept_conn, args=(host, port, fileDir, counter))
            t.start()
            threads.append(t)
            counter += 1

        for thread in threads:
            thread.join()

    except socket.error:
        sys.stderr.write("ERROR: Failed to connect to functioning server\n")

main()


