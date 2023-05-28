import socket
import time
import threading

#prep stuff here
port = range(1,1000) #set range of ports to scan here
ip = input("Enter an ip: ") #enter an ip to scan
open_ports = [] #Display all open ports in this list
threadslist = []
starttime = time.time()

#function for making a socket so that function can be called later to make a socket for each individual thread
def portscan(port):
    try:
        s = socket.socket()
        s.settimeout(1)
        if s.connect_ex((ip, port)) == 0:
            print(f"{port} OPEN")
            open_ports.append(port)
        #else:                                  #   UNCOMMENT HERE TO SEE ALL PORTS THAT ARE CLOSED #
        #    print(f"{port} closed")            #                   FLOODS CLI                      #
    except Exception as error:
        print(f"Error: {error}")
    finally:
        s.close()

#for every port in the port range, make a new thread and call function for each one, start it, and add the thread to thread list to call later
for everyport in port:
    thread = threading.Thread(target=portscan, args=(everyport,))
    thread.start()
    threadslist.append(thread)

#makes every thread in threadslist stop main thread from executing so that they can finish executing
for everythread in threadslist:
    thread.join()

#Display open ports and time taken to finish process
print(f"Open ports are: {open_ports}")
endtime = time.time()
timepassed = round(endtime - starttime, 2)
print(f"Process took {timepassed}s to complete")
