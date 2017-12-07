from socket import *

import re

from scripts.better_base64 import BetterBase64


class EmailClient:
    """
    Email client
    """
    def __init__(self, smtp_address, pop3_address, smtp_port, pop3_port, username, password):
        self._smtp_address = smtp_address
        self._pop3_address = pop3_address
        self._smtp_port = smtp_port
        self._pop3_port = pop3_port
        self._username = username
        self._password = password
        self._client_socket = socket(AF_INET, SOCK_STREAM)

    def receive_email(self):
        """
        Receive email
        """
        self._initialize_connection(self._pop3_address, self._pop3_port)
        self._authentication()

        list = "LIST\r\n"
        recv = self._send(list)
        last_email = recv[len(recv)-12:-10]
        take_one = "RETR {number}\r\n".format(number=last_email)
        recv = self._send(take_one)
        searchObj = re.search(r'Subject: (.*)\.', recv)

        if searchObj:
            print("Subject:     ", searchObj.group(1))
        else:
            print("Nothing found!!")
        self._close_connection()

    def send_email(self, subject, msg):
        """
        Send message

        :param str subject: Subject
        :param str msg  : Message
        """
        self._initialize_connection(self._smtp_address, self._smtp_port)
        self._send('EHLO  ehlo\r\n')
        self._authentication()

        self._send("MAIL FROM:<{}>\r\n".format(self._username))
        self._send("RCPT TO:<{}>\r\n".format(self._username))
        self._send("DATA\r\n")

        subject = "Subject: {subject}\r\n\r\n".format(subject=subject)
        self._client_socket.send(subject.encode())
        msg = "\r\n {msg}".format(msg=msg)
        endmsg = "\r\n.\r\n"
        self._client_socket.send(msg.encode())
        self._client_socket.send(endmsg.encode())

        self._close_connection()

    def _send(self, data):
        """
        Send
        :param data:
        """
        self._client_socket.send(data.encode())
        recv = self._client_socket.recv(1024)
        recv = recv.decode()
        return recv

    def _initialize_connection(self, address, port):
        """
        Initialize connection
        """
        self._client_socket.connect((address, port))
        recv = self._client_socket.recv(1024)
        recv = recv.decode()
        if recv[:3] != '220' and recv[:3] != '+OK':
            raise Exception

    def _close_connection(self):
        """
        Close connection
        """
        quit = "QUIT\r\n"
        self._client_socket.send(quit.encode())
        recv = self._client_socket.recv(1024)
        # print(recv.decode())
        self._client_socket.close()

    def _authentication(self):
        """
        Authentication
        """
        self._client_socket.send(self._parse_auth_msg())
        recv_auth = self._client_socket.recv(1024)
        recv_auth = recv_auth.decode()
        print(recv_auth)
        if recv_auth[:3] != '235' and recv_auth[:3] != '+OK':
            raise Exception

    def _parse_auth_msg(self):
        """
        Parse auth msg

        :return: str
        """
        base64_str = "\x00"+self._username + "\x00" + self._password
        base64_str = BetterBase64.encode(base64_str)
        auth_msg = "AUTH PLAIN ".encode()+base64_str.encode()+"\r\n".encode()

        return auth_msg
