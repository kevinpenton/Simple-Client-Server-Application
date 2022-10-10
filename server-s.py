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
 *  Description: The simplified Accio server is a relatively simple application that waits for clients to connect,
 *               accepts a connection, sends the accio\r\n command, afterwards receives confirmation, sends the
 *               accio\r\n command again, receives the second confirmation, and then receives binary file that client
 *               sends,counts the number of bytes received, and prints it out as a single number (number of bytes
 *               received not including the header size).
 *
 *  Usage: server-s.py <PORT>
 *==================================================================================================================="""

import sys
import socket


try:
    host = '0.0.0.0'
    port = int(sys.argv[1])

    # Creates the socket instance
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(10)

        # Opening listening socket
        sock.bind((host, port))
        numOfConn = 10
        sock.listen(numOfConn)

        #It iterates through all the connections
        for x in range(numOfConn):
            try:
                # Accepts connection
                clientSocket, clientAddress = sock.accept()

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

                    # Receives file
                    l = 0
                    while True:
                        recvFile = clientSocket.recv(1024)

                        if not recvFile:
                            break
                        l += len(recvFile)

                    print(l)

            except socket.error:
                sys.stderr.write("ERROR: Failed to connect to functioning server\n")
                continue

except OverflowError:
    sys.stderr.write("ERROR: Invalid port number")
    exit(1)
