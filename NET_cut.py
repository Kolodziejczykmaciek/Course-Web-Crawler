#!/usr/bin/env python

import netfilterqueue
import subprocess
import sys



# execute the command in terminal:
# iptables -I FORWARD -j NFQUEUE --queue-num 0


def create_queue():
    subprocess.call(["iptables", "-I", "FORWARD", "-j", "NFQUEUE", "--queue", "--num", "0"])
    # this command creates the queue to trap incoming traffic

def restore_defaults():
    subprocess.call(["iptables", "--flush"])
    #come back to initial configuration

def process_packet(packet):
    packet.drop()        #we know what it does :)

########################################################################################################################

try:
    create_queue()

    queue = netfilterqueue.NetFilterQueue() #create the netfilter object
    queue.bind(0, process_packet)           #connect the queue object to the queue created with termianl command as arguments specify
                                            # the queue number and the callback function which will be executed on every incoming packet
    droped_packet_count = 0

    while True:
        queue.run(block=False)                             #start the queue
        droped_packet_count += 1
        print ("\nDroped {} packets".format(droped_packet_count))
        sys.stdout.flush()

except KeyboardInterrupt
    print ("\n [+] Ctr+C detected ... Quiting")
    restore_defaults()
    print ("\n [+] Defaults restored.")