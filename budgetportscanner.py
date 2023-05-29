import socket
import time
import threading

#prep stuff here: check for proper range for starting and ending ports
ip = input("Enter an ip: ") #enter an ip to scan

firstport = int(input("Enter a starting port for the range: "))
while firstport < 0 or firstport > 65535:
    firstport = int(input("Port must be 0-65535: "))
lastport = int(input("Enter an ending port for the range: "))
while lastport < 0 or lastport > 65535:
    lastport = int(input("Port must be 0-65535: "))
while lastport < firstport:
    lastport = int(input("Ending port cannot be smaller than starting port: "))

portrange = range(firstport,lastport + 1) #set range of ports to scan here
open_ports = [] #Display all open ports in this list
threadslist = []
maxthreads = threading.BoundedSemaphore(value=1000) #make a max of 1000 threads instead of 1 thread per port incase of high port range
starttime = time.time()


#function for making a socket so that function can be called later to make a socket for each individual thread
def portscan(port):
    try:
        s = socket.socket()
        s.settimeout(1)
        if s.connect_ex((ip, port)) == 0:
            print(f"{port} OPEN")
            open_ports.append(port)
        #else:                                  #   UNCOMMENT HERE TO SEE ALL PORTS THAT ARE CLOSED   #
        #    print(f"{port} closed")            #                   FLOODS CLI                        #
    except Exception as error:
        print(f"Error: {error}")
    finally:
        s.close()
        maxthreads.release()


#for every port in the port range, make a new thread up to 1000 and call function for each one, start it, and add the thread to thread list to call later
for everyport in portrange:
    maxthreads.acquire()
    thread = threading.Thread(target=portscan, args=(everyport,))
    thread.start()
    threadslist.append(thread)


#makes every thread in threadslist stop main thread from executing so that they can finish executing
for everythread in threadslist:
    thread.join()


#Display open ports, closed ports, and time taken to finish process
closed_ports = lastport - firstport - len(open_ports)
print(f"Open ports are: {open_ports}")
print(f"There are {closed_ports} ports closed")
endtime = time.time()
timepassed = round(endtime - starttime, 2)
print(f"Process took {timepassed}s to complete")