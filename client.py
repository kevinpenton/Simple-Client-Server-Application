"""================================================================================
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
 *  Description: Accio client is a relatively simple application that connects to the specified server and port,
 *               receives two accio\r\n commands from the server, sends correct confirmations to the server, then
 *               transfers the specified file, and gracefully terminates the connection.
 *
 *  Usage: client.py <HOSTNAME-OR-IP> <PORT> <FILENAME>
 *================================================================================"""

import sys
import socket


try:
      # Command-line parameter processing
      host = sys.argv[1]
      port = int(sys.argv[2])
      fileName = sys.argv[3]


      # Creates the socket instance
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.settimeout(10)

      # Connects to specified host and port
      sock.connect((host, port)) #Fix to put connection time
      print("Connection established successfully")

      #Receives data for the first time
      data = b''
      while True:
            try:
                  bytesRecv = sock.recv(1)
                  data += bytesRecv

                  if data == b'accio\r\n':
                        break

            except socket.timeout:
                  sys.stderr.write("ERROR: Data reception timeout")
                  exit(1)

      #Amount of bytes received
      if data:
            print("Received bytes:", len(data))

      #Checks if first command was received
      if data ==  b'accio\r\n':
            print("First command received successfully")

            #Creates first command
            cmd1 = b'confirm-accio\r\n'

            #Sends first command
            cmd1Send = sock.send(cmd1)
            print("Sent bytes: %d" %cmd1Send)

            # Receives data for the second time
            data = b''
            while True:
                  try:
                        bytesRecv = sock.recv(1)
                        data += bytesRecv

                        if data == b'accio\r\n':
                              break

                  except socket.timeout:
                        sys.stderr.write("ERROR: Data reception timeout")
                        exit(1)

            # Amount of bytes received
            if data:
                  print("Received bytes:", len(data))

            #Checks if second command was received
            if data == b'accio\r\n':
                  print("Second command received successfully")
                  
                  #Creates second command
                  cmd2 = b'confirm-accio-again\r\n\r\n'
                  
                  #Sends second command
                  cmd2Send = sock.send(cmd2)
                  print("Sent bytes: %d" % cmd2Send)

                  #Writing provided file to binary file
                  binaryFile = open(fileName, 'rb')

                  fileBytes = 0

                  while True:
                        bytesRead = binaryFile.read(10000)
                        
                        if not bytesRead:
                              break

                        #Check how many bytes from the file are being sent
                        fileBytes += len(bytesRead)
                        print("File bytes sent:", fileBytes)

                        sock.sendall(bytesRead)

                  print("File Sent Successfully")

                  #Close file
                  binaryFile.close()

                  #Exit with no errors
                  exit(0)

except socket.timeout:
      sys.stderr.write("ERROR: Failed to connect to a functioning server")
      exit(1)

except socket.gaierror:
      sys.stderr.write("ERROR: Invalid hostname or IP address")
      exit(1)
except OverflowError:
      sys.stderr.write("ERROR: Invalid port number")
      exit(1)

#Closes socket
sock.close()
