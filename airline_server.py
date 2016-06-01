from socket import *
import thread
import fcntl
import time


# Handler function to handle all incoming service request for query, reservation and  cancellation
def handler(clientsocket, clientaddr): 
    print "Accepted connection from: ", clientaddr
    
    # authentication module
    auth = 1
    i = 100
    user = clientsocket.recv(1024)
    print user +" is trying to log in"
    while 1:
        passwd = clientsocket.recv(1024)
        if passwd != None:
            break
    #print passwd
    try:
        i = username.index(user) # find the index of the username from the list username
        print i
        if password[i] != passwd: #compare each username with the respective password 
            auth = 0
            print "wrong password"
    except ValueError:
        print "No such username"
        auth = 0
    if auth == 0:
        clientsocket.send("Bad username/password combination")
        clientsocket.close()
    else:
        clientsocket.send("!!!Authentication successful!!!")
    # authentication off

    #if authentication is successful allowed in to make query, reservation and cancellation
    
    while auth == 1:
        data = clientsocket.recv(1024) # receive incoming command from the client
        # reading from file
        f = open('flight.txt', 'r') # extracts data from the database file flight.txt
        element = []            # list to hold the flight status
        temp = f.read().splitlines()   # create a 
        f.close()
        for i in range(len(temp)):
            #element.append([])
            element.append(temp[i].split('\t')) # create two dimensional list to store flight status 
        if not data:
            break
        else:
            #print data
            #print data[0].lower()
            
            #Query module: It is responsible for handling the query request from the customer

            if data[0].lower() == 'q' and len(data.split(' ')) > 1:  # query section
                sq = "Flight\tSeat\tE/R\tName\n"
                #f = open('flight.txt', 'r')
                #print "query request"
                que = data.split(' ') # split the query string to find the flight number
                print que
                if que[1] == '1': # for flight 1
                    for q in range(0,5):
                        #print element[q][2]
                        if element[q][2] =='0':   # append the matched flight to the reply string sq sent back to the client
                            sq = sq + '\t'.join(element[q]) + '\n'  
                elif que[1] =='2': # for flight 2  
                    for q in range(5,7):
                        if element [q][2] =='0':  # append the matched flight to the reply string sq sent back to the client
                            sq = sq + '\t'.join(element[q]) + '\n'
                elif que[1] =='3': # for flight 3
                    for q in range(7,17):
                        if element [q][2] =='0':   # append the matched flight to the reply string sq sent back to the client
                            sq = sq + '\t'.join(element[q]) + '\n'
                elif que[1] =='4': # for flight 4
                    for q in range(17,27):
                        if element [q][2] =='0':   # append the matched flight to the reply string sq sent back to the client
                            sq = sq + '\t'.join(element[q]) + '\n'
                else:
                    sq ="Wrong flight number enter. Please enter eithe 1 or 2 or 3 or 4"
                if sq =="":
                    sq = "No seat available on flight"
                sq = sq + "\n Note: If E/R = 0, seat is empty or If E/R = 1, seat is Reserved"
                print "Flight\tSeat\tE/R\tName\n"
                for i in range(len(element)):
                    text = '\t'.join(element[i]) + '\n'
                    print text


            elif data[0].lower() =='r'and len(data.split(' ')) > 1: # Reserve section
                sq = "Reservation of flight "
                #print "Reserve seat"
                reserve = data.split(' ') # split the reserve command to list so seat number can be extracted
                flight = que[1]
                sq = sq+flight+" done Successfully!!!"
                for a in range(1, len(reserve)-1): # loop until all stated seats are reserved
                    
                    if flight == '1':  # for flight 1 
                        for b in range(0,5):
                            if reserve[a] == element[b][1]:
                                element[b][2]= '1'         # change empty/reserve bit to 1
                                element[b][3]= reserve [len(reserve)-1] # change name to username that reserved it
                
                    if flight == '2':  # for flight 2
                        for b in range(5,7):
                            if reserve[a] == element[b][1]:
                                element[b][2]= '1'         # change empty/reserve bit to 1
                                element[b][3]= reserve [len(reserve)-1] # change name to username that reserved it

                    if flight == '3':  # for flight 3
                        for b in range(7,17):
                            if reserve[a] == element[b][1]:
                                element[b][2]= '1'          # change empty/reserve bit to 1
                                element[b][3]= reserve [len(reserve)-1] # change name to username that reserved it

                    if flight == '4':  # for flight 4
                        for b in range(17,27):
                            if reserve[a] == element[b][1]:
                                element[b][2]= '1'          # change empty/reserve bit to 1
                                element[b][3]= reserve [len(reserve)-1] # change name to username that reserved it

                print element
                # writing into file using flock UNIX file lock write module
                '''f = open('flight.txt', 'w')
                for i in range(len(element)):
                    text = '\t'.join(element[i]) + '\n'
                    f.write(text)
                f.close()
                '''
                f = open('flight.txt', 'w')
                try:
                    fcntl.flock(f,fcntl.LOCK_EX | fcntl.LOCK_NB)   # locking of file so no other thread can access concurrently
                except IOError:             # if already lock error 
                    wr = '0'
                    print "\ncannot be written in file\n"
                else:                       # if locking successful update the database
                    wr = '1'
                    "Flight\tSeat\tE/R\tName\n"
                    for i in range(len(element)):
                        text = '\t'.join(element[i]) + '\n'
                        f.write(text)
                        print text
                    #time.sleep(8)
                    fcntl.flock(f, fcntl.LOCK_UN)       #unlock the file so other process can access it
                    f.close()
                if wr == '0':
                    sq = "Reservation in process by other client.\nTry after sometime "


            elif data[0].lower() == 'c' and len(data.split(' ')) > 1: #cancel reservation
                print "Cancel reservation"
                cancel = data.split(' ')  # split the cancel command to list so flight number and username can be extracted
                sq = "Reservation of flight "+cancel[1]+" calcelled for "+cancel[2]
                if cancel[1] == '1':  # for flight 1
                    for e in range(0,5):
                        if element[e][2]=='1' and element[e][3]==cancel[2]: # if reserved and match username change empty/reserve bit back to 0 and username back to non
                            element[e][2]= '0'
                            element[e][3]= "non"

                if cancel[1] == '2': # for flight 2
                    for e in range(5,7):
                        if element[e][2]=='1' and element[e][3]==cancel[2]: # if reserved and match username change empty/reserve bit back to 0 and username back to non
                            element[e][2]= '0'
                            element[e][3]= "non"

                if cancel[1] == '3':  # for flight 3
                    for e in range(7,17):
                        if element[e][2]=='1' and element[e][3]==cancel[2]: # if reserved and match username change empty/reserve bit back to 0 and username back to non
                            element[e][2]= '0'
                            element[e][3]= "non"

                if cancel[1] == '4':  #for flight 4
                    for e in range(17,27):
                        if element[e][2]=='1' and element[e][3]==cancel[2]: # if reserved and match username change empty/reserve bit back to 0 and username back to non
                            element[e][2]= '0'
                            element[e][3]= "non"

                #writing to file
                '''f = open('flight.txt', 'w')
                for i in range(len(element)):
                    text = '\t'.join(element[i]) + '\n'
                    f.write(text)
                f.close()
                '''

                f = open('flight.txt', 'w')
                try:
                    fcntl.flock(f,fcntl.LOCK_EX | fcntl.LOCK_NB)  # locking of file so no other thread can access concurrently
                except IOError:      # if already lock error 
                    wr = '0'
                    print "\ncannot be written in file\n"
                else:      # if locking successful update the database
                    wr = '1'
                    "Flight\tSeat\tE/R\tName\n"
                    for i in range(len(element)):
                        text = '\t'.join(element[i]) + '\n'
                        f.write(text)
                        print text
                    #time.sleep(8)
                    fcntl.flock(f, fcntl.LOCK_UN)  #unlock the file so other process can access it
                    f.close()
                if wr == '0':
                    sq = "Reservation/Cancellation in process by other client.\nTry after sometime "
                    print sq

            else:
                sq = "Wrong Command entered. Please enter a valid command"
                            
            msg = "You send me % s" % data
            clientsocket.send(sq)
    clientsocket.close()
# main function
if __name__ == "__main__":

    host = 'localhost' #server address
    port = 44129   # port number for server
    buf = 1024
    #auth = 1
    username = ['shubham', 'balram']  # username list
    password = ['1234', '5678']         # password list

    addr = (host, port)

    serversocket = socket(AF_INET, SOCK_STREAM) # create TCp socket

    serversocket.bind(addr)

    serversocket.listen(5)

    while 1:
        print "Server is listening for connections\n"

        clientsocket, clientaddr = serversocket.accept()
        thread.start_new_thread(handler, (clientsocket, clientaddr))
    serversocket.close()
