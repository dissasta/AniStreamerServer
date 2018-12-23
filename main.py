import os, sys, threading, socket

homeDir = os.getcwd()
tempDir = os.path.join(homeDir, 'TEMP')
outputDir = os.path.join(homeDir, 'OUTPUT')
archiveDir = os.path.join(homeDir, 'ARCHIVE')

class Server(object):
    clientSocks = []
    clientThreads = []
    def __init__(self, jobThreads):
        self.host = ''
        self.port = 6666
        self.buffSize = 1024
        self.jobThreads = jobThreads
        self.createSocket()
        self.listenForClients()

    def createSocket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket Created @port %s." % str(self.port))

        try:
            self.socket.bind((self.host, self.port))
        except socket.error as msg:
            print("Bind failed. Error code: " + str(msg))
            sys.exit()

    def listenForClients(self):
        self.socket.listen()
        print("Listening for incoming connections.")

        while True:
            conn, addr = self.socket.accept()
            print("Connection from: " + addr[0])
            clientThread = threading.Thread(self.handleClient(conn))
            Server.clientSocks.append(conn)
            Server.clientThreads.append(clientThread)
            print(Server.clientSocks, Server.clientThreads)
        self.socket.close()

    def handleClient(self, socket):
        while True:
            header = socket.recv(self.buffSize)
            header = header.decode('utf-8').split('|')
            fsize = int(header[0])
            fname = header[1]
            rsize = 0

            file = open(os.path.join(tempDir, fname), 'wb')

            while True:
                data = socket.recv(self.buffSize)
                file.write(data)
                rsize = rsize + len(data)
                if rsize >= fsize:
                    print('received a file')
                    break

            file.close()

def main():

    if not os.path.exists(tempDir):
        os.mkdir(tempDir)
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    if not os.path.exists(archiveDir):
        os.mkdir(archiveDir)

    appServer = Server(4)


if __name__ == "__main__":
    main()