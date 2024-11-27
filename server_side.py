import socket
import threading 

#Multi threading so it will simultaneously handle 3 connections 
def connection_thread(sock, id):
    print(">> Start of thread #" + str(id))
    data = sock.recv(1024).decode('ascii')
    print("Thread no #{} has received: {}".format(id, data))
    print ('The connection has ended with with client: ', sock_name[0])
    print(">> End of Thread no.", id)
    print(50*'-')


with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as ss: 

    print("The server has started and wiating for clients to connect..." )
    
    ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    ss.bind(("127.0.0.1", 49999)) 
    
    #So it will be able to handle atleast 3 connections
    ss.listen(3)

    #To accept connections from clients 
    sock_add, sock_name = ss.accept()

    threads = []
    while True: 
        #To accept connections from clients 
        sock_add, sock_name = ss.accept()

        the_thread= threading.Thread(target=connection_thread, args=(sock_add,len(threads)+1))
        threads.append(the_thread)
        the_thread.start()    
        if len(threads) > 4:
            break

        print('The request has been accepted from ', sock_name[0], "That has this port number: ", sock_name[1])

ss.close()

