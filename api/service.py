from custom.profile import ProfileReader

import multiprocessing
import socket
import os

class CfdiEngineError(Exception):
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

class CfdiEngine(object):

    __HOST = '' # Symbolic name meaning all available interfaces

    def __init__(self, logger, config_prof, port):
        self.logger = logger
        self.port = port

        try:
            reader = ProfileReader(self.logger)
            proftree = reader(config_prof)
        except:
            msg = 'Problems came up when reading configuration profile'
            raise CfdiEngineError(msg)


    def start(self):
        """start the service upon selected port"""

        def spawner():
            self.logger.debug("listening")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.hostname, self.port))
            self.socket.listen(1)

            while True:
                conn, address = self.socket.accept()
                self.logger.debug("Got connection")
                process = multiprocessing.Process(
                    target=self.handle, args=(conn, address))
                process.daemon = True
                process.start()
                self.logger.debug("Started process %r", process)

        def shutdown():
            self.logger.info("Shutting down")
            for process in multiprocessing.active_children():
                self.logger.info("Shutting down process %r", process)
                process.terminate()
                process.join()

        try:
            print('Use Control-C to exit')
            spawner()
        except KeyboardInterrupt:
            print('Exiting')
        except BbGumServerError as e:
            self.logger.error(e)
            raise
        finally:
            shutdown()

    def handle(self, connection, address):
        try:
            self.logger.debug("Connected %r at %r", connection, address)
            while True:
                data = connection.recv(1024)
                if data == "":
                    self.logger.debug("Socket closed remotely")
                    break
                self.logger.debug("Received data %r", data)
                connection.sendall(data)
                self.logger.debug("Sent data")
        except:
            self.logger.exception("Problem handling request")
        finally:
            self.logger.debug("Closing socket")
            connection.close()
