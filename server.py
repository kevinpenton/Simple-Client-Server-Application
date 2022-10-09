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
                print("Connection accepted successfully\n")
                clientSocket.settimeout(10)

                with clientSocket:
                    # Creates variable for command
                    cmd = b'accio\r\n'

                    # Send first accio\r\n command
                    try:
                        cmd1Send = clientSocket.send(cmd)
                        print("First command sent successfully\n")

                        try:
                            # Receives data for the first time
                            bytesRecv1 = clientSocket.recv(1024)
                            if bytesRecv1:
                                print("First command received successfully\n")

                            try:
                                # Sends second accio\r\n command
                                cmd2Send = clientSocket.send(cmd)
                                print("Second command sent successfully\n")
                                try:
                                    # Receives data for the second time
                                    bytesRecv2 = clientSocket.recv(1024)
                                    if bytesRecv2:
                                        print("Second command sent successfully\n")

                                    # Creates binary file
                                    try:
                                        newFile = open("%s/%s.file" % (fileDir, conn_counter), 'wb')
                                        print("File created successfully\n")

                                        while True:
                                            try:
                                                recvFile = clientSocket.recv(1024)
                                                if not recvFile:
                                                    break
                                                print("%d bytes received successfully" %len(recvFile))
                                                newFile.write(recvFile)
                                                print("Filed edited successfully")

                                            except socket.error:
                                                sys.stderr.write("ERROR: File failed to receive data\n")
                                                newFile.write("ERROR")
                                                print("File received ERROR message successfully\n")
                                                break

                                        newFile.close()

                                    except socket.error:
                                        sys.stderr.write("ERROR: There was a problem creating the file\n")

                                except socket.error:
                                    sys.stderr.write("ERROR: Failed to receive second command\n")

                            except socket.error:
                                sys.stderr.write("ERROR: Failed to send second command\n")

                        except socket.error:
                            sys.stderr.write("ERROR: Failed to receive first command\n")


                    except socket.error:
                        sys.stderr.write("ERROR: Failed to send first command\n")

            except socket.error:
                sys.stderr.write("ERROR: Failed to connect to functioning server\n")

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


