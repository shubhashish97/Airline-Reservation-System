from socket import *
import getpass

#main function
if __name__ == '__main__':

    host = 'localhost'  # server address
    port = 44129        # server port
    buf = 1024
    auth = 1
    addr = (host, port)

    clientsocket = socket(AF_INET, SOCK_STREAM)

    clientsocket.connect(addr)
    print "\nWelcome to Akondilac Air\n"
    username = raw_input("Username:")
    clientsocket.send(username)
    password = getpass.getpass("Password:")
    clientsocket.send(password)
    print "Authenticating...."
    while 1: # waiting for authentication process and reply from server
        rep = clientsocket.recv(buf)
        if rep != None:
            break
    print rep
    if rep == "Bad username/password combination":  # if authentication fails, TCP connection is closed
        auth = 0;
        clientsocket.close()
    f = open('input1.dat', 'r')
    element = []
    temp = f.read().splitlines()
    f.close()
    for i in range(len(temp)):
        element.append(temp[i])
    for s in range(len(element)):    
    #while auth ==  1:  # if authentication succeed main menu is shown
        print "\n ***Main Menu***"
        print "\nEnter command in the format:\na)Query for number of seats available on flight x:       Q x"
        print "\nb)Reserve seats I, j, etc. user name nm:                   R I j ..  nm"
        print "\nc) Cancel seats for flight x under name n:                C x n"
        print "\n Else type exit to quit"
        #data = raw_input(">> ")
        data = element[s]
        if data == "exit":
            break
        else:
            clientsocket.send(data)
            data = clientsocket.recv(buf)
            if data.lower() == "exit":   # if exit is typed TCP connection is closed
                break
            else:
                print data  #print data send by server for respective request
    clientsocket.close()
