import socket
import sys
import threading

class Chat:
    def __init__(self, host=socket.gethostname(), port=5000):
        s = socket.socket(type=socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.bind((host, port))
        self.__myadress = (host, port)
        self.__clientpseudo = 'anonymous'
        self.__s = s
        print('Listen to {}:{}'.format(host, port))


    def run(self):
        handlers = {
            '/exit': self._exit,
            '/quit': self._quit,
            '/join': self._join,
            '/register': self._register,
            '/connected': self._connected,
            '/list': self._list,
            '/send': self._send,
            '/help': self._help,
            '/chat': self._startchat

        }
        self.__serveradress = (socket.gethostname(), 5000)
        self.__running = True
        self.__address = None
        self.__clientlist= []
        self.__clientpseudo = ''
        threading.Thread(target=self._receive).start()
        while self.__running:
            line = sys.stdin.readline().rstrip() + ' '
            if line.startswith( '/' ):
                # Extract the command and the param
                command = line[:line.index(' ')]
                param = line[line.index(' ')+1:].rstrip()
                # Call the command handler
                if command in handlers:
                    try:
                        handlers[command]() if param == '' else handlers[command](param)
                    except:
                         print ("Unexpected error:", sys.exc_info()[0])
                else:
                    print('Command inconnue:', command)
            else:
                self._sendpeermessage(line)
    def _sendpeermessage(self, line):
        if self.__backadress is not None:
            reply = ('chat;{};{};{};{}'.format(self.__myadress[0],self.__myadress[1], self.__clientpseudo, line))
            msgreply = reply.encode()
            totalsent = 0
            while totalsent < len(msgreply):
                sent = self.__s.sendto(msgreply[totalsent:], self.__backadress)
                totalsent += sent
            print('Waiting reply...')
    def _list(self):
        print(self.__clientlist)
    def _exit(self):
        self.__running = False
        self.__address = None
        self.__s.close()
    def _add(self, host, port, pseudo):
        self.__clientlist.append((host, port, pseudo))
    def _help(self):
        print('Usage for the server:')
        print(' - /list :list all the connected clients on the server')
        print(' - /join [adress]: set the adress to contact when using /send.')
        print('          The adress, seperated by a space, contain the IP and the PORT.')
        print(' - /send [message]: send the message to the adress of /join.')
        print('Usage for the clients:')
        print(' - /register [pseudo] : add the client to the list of the server.')
        print(' - /connected :list all the connected clients on the server.')
        print(' - /chat [pseudo] : start peer to peer with pseudo name.')
        print('Usage for  both:')
        print(' - /exit : close the instance and exit.')
    def _quit(self):
        self.__address = None
    def _send(self, param):
        if self.__address is not None:
            try:
                message = param.encode()
                totalsent = 0
                while totalsent < len(message):
                    sent = self.__s.sendto(message[totalsent:], self.__address)
                    totals__serevraddressent += sent
            except OSError:
                print('Error during the reception of the message')
    def _connectedlist(self, host, port):
        addressClient = (host, int(port))
        if addressClient is not None:
            try:
                param = str(self.__clientlist)
                message = param.encode()
                totalsent = 0
                while totalsent < len(message):
                    sent = self.__s.sendto(message[totalsent:], addressClient)
                    totalsent += sent
            except OSError:
                print('Error during the reception of the message')
    def _join(self, param):
        tokens = param.split(' ')
        if len(tokens) == 2:
            try:
                #rm socket__serevraddress.gethostbyaddr()[0] because adding .home to the name
                self.__address = (tokens[0], int(tokens[1]))
                print('Connected to {}:{}'.format(*self.__address))
            except OSError:
                print('Error during the sending of the message')

        self.__serveradress = (socket.gethostname(), 5000)

    def _receive(self):
        while self.__running:
            try:
                data, address = self.__s.recvfrom(1024)
                message = data.decode()
                #print(message)
                addmsg = message.split(';')
                if addmsg[0] == 'register':
                    self._add(addmsg[1], addmsg[2], addmsg[3])
                if  addmsg[0] == 'connected':
                    self._connectedlist(addmsg[1], addmsg[2])
                if addmsg[0] == 'startchat':
                    receiver = addmsg[3]
                    for client in self.__clientlist:
                        if client[2] == receiver:
                            receiveradress= (client[0], client[1])
                    self._clientadresschat = (addmsg[1], addmsg[2])
                    #print(addmsg[1])
                    #print(addmsg[2])
                    #print(addmsg[3])
                    #print(receiveradress[0], receiveradress[1])
                    clientadresschat = (receiveradress[0], int(receiveradress[1]))
                    self.__backadress =(addmsg[1], int(addmsg[2])) #the adress of the client that asked to chat
                    #reply = input("Reply:  ")
                    reply = ('chat;{};{};{};{}'.format(receiveradress[0], int(receiveradress[1]), receiver, 'hi!'))
                    msgreply = reply.encode()
                    totalsent = 0
                    while totalsent < len(msgreply):
                        sent = self.__s.sendto(msgreply[totalsent:], self.__backadress)
                        totalsent += sent
                if addmsg[0] == 'chat':

                    self.__backadress = addmsg[1], int(addmsg[2])
                    print('> {} : {}'.format(addmsg[3], addmsg[4]))

                    #self._clientadresschat = (addmsg[1], addmsg[2])
                    #clientadresschat = (receiveradress[0], int(receiveradress[1]))
                    #clientadresschat =(addmsg[1])

                    print("Reply:  ")
                    #inmsg = 'lolo'



            except socket.timeout:
                pass
            except OSError:
                return

    def _startchat(self, receiver):
        if self.__serveradress is not None:
            try:
                param = 'startchat;{};{};{}'.format(self.__myadress[0], self.__myadress[1], receiver)
                message = param.encode()
                totalsent = 0

                while totalsent < len(message):
                    sent = self.__s.sendto(message[totalsent:], self.__serveradress)
                    totalsent += sent
            except OSError:
                print('Error during the reception of the message')



    def _register(self, pseudo):
        if self.__serveradress is not None:
            try:
                param = 'register;{};{};{}'.format(self.__myadress[0], self.__myadress[1],pseudo)
                self.__clientpseudo = pseudo
                message = param.encode()
                totalsent = 0
                while totalsent < len(message):
                    sent = self.__s.sendto(message[totalsent:], self.__serveradress)
                    totalsent += sent
                print('Client registered to the server')
            except OSError:
                print('Error during the reception of the message')


    def _connected(self):
        if self.__serveradress is not None:
            try:
                param = 'connected;{};{}'.format(*self.__myadress)
                message = param.encode()
                totalsent = 0
                while totalsent < len(message):
                    sent = self.__s.sendto(message[totalsent:], self.__serveradress)
                    totalsent += sent
            except OSError:
                print('Error during the reception of the message')

if __name__ == '__main__':
    if len(sys.argv) == 3:
        Chat(sys.argv[1], int(sys.argv[2])).run()
    else:
        Chat().run()
