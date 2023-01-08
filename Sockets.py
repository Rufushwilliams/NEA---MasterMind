from __future__ import annotations

import pickle
import socket
from abc import ABC
from enum import Enum


#####################
# CUSTOM EXCEPTIONS #
#####################
class MessageExchangeError(Exception):
    """
    An exception for errors in message exchange.
    """

    pass


class NoMessageError(MessageExchangeError):
    """
    An exception for when no message is received.
    """

    pass


class SocketManager(ABC):
    """
    An abstract class for handling sockets
    """

    ##############################################
    # GROUP A SKILL: COMPLEX CLIENT-SERVER MODEL #
    ##############################################
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket: socket.socket = self.__createUnboundSocket()
        # socket attribute should be set by the subclass

    def __createUnboundSocket(self) -> socket.socket:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(20)
        return s

    def _createServerSocket(self) -> socket.socket:
        s = self.__createUnboundSocket()
        # Bind to the address
        s.bind((self.host, self.port))
        s.listen(1)
        # wait for client connection.
        conn, addr = s.accept()
        # close the listening socket
        s.close()
        # return the client connection socket
        return conn

    def _createClientSocket(self) -> socket.socket:
        s = self.__createUnboundSocket()
        # connect to the server
        s.connect((self.host, self.port))
        return s

    def __send(self, msg: bytes):
        """
        Sends a message to the socket.
        """
        self.socket.sendall(msg)

    def __receiveData(self) -> bytes:
        """
        Receives a message from the socket.
        """
        return self.socket.recv(2048)

    def __sendMessage(self, msg: bytes):
        """
        Sends a message to the socket.
        Waits for a confirmation message from the socket.
        Sets the timeout to be 5 seconds while waiting for the confirmation message.
        """
        # send the message
        self.__send(msg)
        # change the timeout to 5 seconds
        timeout = self.socket.gettimeout()
        self.socket.settimeout(5)
        try:
            # wait for the confirmation message
            c = self.__receiveData()
        finally:
            # reset the timeout
            self.socket.settimeout(timeout)
        # if the confirmation message is not the expected one, raise an exception
        if not c or c.decode() != self.possibleMessages.CONFIRM.value:
            raise MessageExchangeError("Did not receive confirmation")

    def __receiveMessage(self) -> bytes:
        """
        Receives a message from the socket.
        Sends a confirmation message to the socket.
        """
        msg = self.__receiveData()
        if not msg:
            raise NoMessageError("No message received")
        # send the confirmation message
        self.__send(self.possibleMessages.CONFIRM.value.encode())
        return msg

    def sendMessage(self, msg: possibleMessages, *args):
        """
        Sends data to the socket.
        The data is pickled and then sent.
        The primary message will be in the form of:
        <message type><delimiter><no. of subsequent messages>
        It will then wait for a confirmation message.
        Any subsequent messages will be in the form of:
        <pickled data>
        Finally, it should receive a confirmation message.
        """
        primaryMsg = msg.value + self.possibleMessages.DELIMITER.value + str(len(args))
        # send the primary message
        self.__sendMessage(primaryMsg.encode())
        # send the subsequent messages
        for arg in args:
            self.__sendMessage(self.__pickleData(arg))

    def receiveMessage(self, timeout: bool = True) -> tuple[possibleMessages, list]:
        """
        Receives a message from the socket.
        Sends a confirmation message.
        Splits it according to the delimiter.
        The message should be in the form of:
        <message type><delimiter><no. of subsequent messages>
        It then receives the subsequent pickled data.
        It returns a tuple of the message type and the list of data.
        """
        # if we do not want the socket to timeout, we set the timeout to None
        if not timeout:
            oldTimeout = self.socket.gettimeout()
            self.socket.settimeout(None)
        # receive the primary msg
        primaryMsg = self.__receiveMessage()
        # split the primary msg into the message type and the number of subsequent messages
        msg, numData = self.splitData(primaryMsg.decode())
        encData = []
        # receive the subsequent data
        for _ in range(int(numData[0])):
            d = self.__receiveMessage()
            encData.append(d)
        # unpickle the data
        data = [self.__unpickleData(d) for d in encData]
        if not timeout:
            # set the timeout back to the old value
            self.socket.settimeout(oldTimeout)
        return msg, data

    def splitData(self, data: str) -> tuple[possibleMessages, list]:
        """
        Splits the data received from the socket.
        Returns a tuple of the message and a list of the data.
        """
        msg = data.split(self.possibleMessages.DELIMITER.value)
        return self.getEnumFromStr(msg[0]), msg[1:]

    def getEnumFromStr(self, msg: str) -> possibleMessages:
        """
        Convert a string value into its enum equivalent from the enum possibleMessages.
        """
        for member in self.possibleMessages:
            if msg == member.value:
                return member
        raise ValueError(f"Invalid Enum: {msg}")

    def __pickleData(self, data) -> bytes:
        """
        Pickles the data and returns it as bytes
        """
        return pickle.dumps(data)

    def __unpickleData(self, data: bytes):
        """
        Unpickles the data and returns it
        """
        return pickle.loads(data)

    def close(self):
        """
        Closes the socket.
        """
        self.socket.close()

    def __del__(self):
        self.close()

    class possibleMessages(Enum):
        """
        An enum for possible messages by the server.
        """

        DELIMITER = "#"
        GET_MOVE = "getMove"
        RETURN_MOVE = "returnMove"
        GET_CODE = "getCode"
        RETURN_CODE = "returnCode"
        DISPLAY_BOARD = "displayBoard"
        DISPLAY_ROUND_WINNER = "displayRoundWinner"
        DISPLAY_WINNER = "displayWinner"
        DISPLAY_ROUND_NUMBER = "displayRoundNumber"
        DISCONNECT = "disconnect"
        CONFIRM = "confirm"
