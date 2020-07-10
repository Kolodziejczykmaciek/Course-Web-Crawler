#!bin cos tam

import netfilterqueue
import scapy.all as scapy

# and subprossecc to automate that
# execute the command in terminal:
# iptables -I OUTPUT -j NFQUEUE --queue-num 0   only this when attacing a remote comp
# and
# # iptables -I INPUT -j NFQUEUE --queue-num 0  add this when testing in virtualbox
# this command creates the queue to trap incaming traffic


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    packet.accept()     #must be to forward to the GW


queue = netfilterqueue.NetFilterQueue() #create the netfilter object
queue.bind(0, process_packet)   #connect the queue object to the queue created with termianl command as arguments specify
                                # the queue number and the callback function which will be executed on every incoming packet
queue.run()

