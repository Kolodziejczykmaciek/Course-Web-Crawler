#!/user/bin/env python

import scapy.all as scapy #every time i want to use scapy.all i just write scapy
import optparse

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="targeted_ip", help="Specify the ip, network or subnet address")
    (options, arguments) = parser.parse_args()
    if not options.targeted_ip:
        parser.error("IP address must be specified use --help for more info")
    return options

def scan(ip):           #gets the mac of the specified ip (also ip ranges)

    arp_request = scapy.ARP(pdst=ip) #create an objact of an arp packet
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") #creats a ethernet frame
    arp_request_broadcast = broadcast/arp_request #combining these two packets

    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0] #tells to return ONLY one list !!!


    clients_list = []   #empty list

    for element in answered_list:
        client_dict = {"IP" : element[1].psrc, "MAC" : element[1].hwsrc} #every time new object is created
        clients_list.append(client_dict) #this creates the list of dictionaries which store a couple
    return clients_list

def return_print(clients_list):
    print("IP\t\t\tMAC address\n----------------------------------------")
    for i in clients_list:
        print(i["IP"] + "\t\t" + i["MAC"])



options = get_arguments()
return_print(scan(options.targeted_ip))
