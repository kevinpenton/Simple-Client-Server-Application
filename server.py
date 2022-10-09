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


try:
    host = '0.0.0.0'
    port = int(sys.argv[1])
    fileDir = sys.argv[2]

    counter = 0

    # Creates the socket instance
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Opening listening socket
        sock.bind((host, port))
        numOfConn = 10
        sock.listen(numOfConn)


        # Function to accept a connection and process it accordingly
        def setConn(conn_counter):
            try:
                # Accepts connection
                clientSocket, clientAddress = sock.accept()
                clientSocket.settimeout(10)

                with clientSocket:
                    # Creates variable for command
                    cmd = b'accio\r\n'

                    # Send first accio\r\n command
                    cmd1Send = clientSocket.send(cmd)

                    # Receives data for the first time
                    bytesRecv1 = clientSocket.recv(1024)

                    # Sends second accio\r\n command
                    cmd2Send = clientSocket.send(cmd)

                    # Receives data for the second time
                    bytesRecv2 = clientSocket.recv(1024)

                    # Creates binary file
                    newFile = open((fileDir + "%i.file" %conn_counter), 'wb')

                    while True:
                        recvFile = clientSocket.recv(1024)
                        if not recvFile:
                            break
                        newFile.write(recvFile)

                    newFile.close()

            except socket.error:
                sys.stderr.write("ERROR: Failed to connect to functioning server\n")
                newFile = open((fileDir + "%i.file" %conn_counter), 'w')
                newFile.write("ERROR")
                newFile.close()


        threads = []

        # Creates a thread for each connection
        for _ in range(numOfConn):
            counter += 1
            t = threading.Thread(target=setConn, args= [counter])
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()

except OverflowError:
    sys.stderr.write("ERROR: Invalid port number")
    exit(1)
