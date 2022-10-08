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

counter = 0

try:
    host = '0.0.0.0'
    port = int(sys.argv[1])
    fileDir = sys.argv[2]

    # Creates the socket instance
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(10)

        # Opening listening socket
        sock.bind((host, port))
        numOfConn = 10
        sock.listen(numOfConn)


        def accept_conn(conn_Socket, conn_fileDir, conn_counter):
            try:
                sock.settimeout(10)
                # Accepts connection
                clientSocket, clientAddress = sock.accept()

                with conn_Socket:

                    # Creates variable for command
                    cmd = b'accio\r\n'

                    # Sends accio\r\n command
                    clientSocket.send(cmd)

                    #Creates binary file
                    newFile = open("%s/s%.file" %(conn_fileDir,  conn_counter), 'wb')

                    while True:
                        recvFile = clientSocket.recv(1024)
                        if not recvFile:
                            break
                        newFile.write(recvFile)

                    newFile.close()

            except socket.error:
                sys.stderr.write("ERROR: Failed to connect to functioning server\n")
                newFile = open("%s/s%.file" % (conn_fileDir, conn_counter), 'w')
                newFile.write("ERROR")
                newFile.close()
        
        threads = []
        # Creates a thread for each connection
        for _ in range(numOfConn):
            counter += 1
            t = threading.Thread(target=accept_conn, args=(clientSocket, fileDir, counter))
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()


except OverflowError:
    sys.stderr.write("ERROR: Invalid port number")
    exit(1)
