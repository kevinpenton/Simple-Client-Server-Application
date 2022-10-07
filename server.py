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
 *  Usage:  server.py <PORT> <FILE-DIR>
 *==================================================================================================================="""


