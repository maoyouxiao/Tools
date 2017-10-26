#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import requests
from optparse import OptionParser

def update():
    import execjs
    url = "https://www.wireshark.org/assets/js/manuf.js"
    headers = {
        "User-Agent": "Mozilia/5.0 (Windows NT 10.0)"
    }
    res = requests.get(url, headers=headers)
    context = execjs.compile(res.content.decode("utf-8"))
    res.close()
    with open("./oui.json", "w") as f:
        json.dump(context.eval("oui"), f)

def get_oui():
    if not os.path.exists("./oui.json"):
        update()
    with open("./oui.json", "rb") as f:
        data = json.load(f)
    return data

def find_by_mac(value):
    oui = get_oui()
    pfx = "".join(value.split(":")).lower()[:6]
    for o in oui:
        if o['pfx'] == pfx:
            pfx = "".join(["%s:" % o['pfx'][x:x+2] for x in range(0, len(o['pfx']), 2)])[:-1]
            print("%s\t%s" % (pfx, o['desc']))
            return
    print("Not Found.")

def find_by_name(value):
    oui = get_oui()
    pfx = None
    for o in oui:
        if value.lower() in o['desc'].lower():
            pfx = "".join(["%s:" % o['pfx'][x:x+2] for x in range(0, len(o['pfx']), 2)])[:-1]
            print("%s\t%s" % (pfx, o['desc']))
    if not pfx:
        print("Not Found.")

def main():
    parser = OptionParser(usage="Usage: %prog <-k keyword> <-m mac address> <-u update>")
    parser.add_option("-k", "--key", dest="key", type="string", help="specify keyword")
    parser.add_option("-m", "--mac", dest="mac", type="string", help="specify mac address")
    parser.add_option("-u", "--update", dest="update", action="store_true", default=False, help="update OUI file")
    opts, args = parser.parse_args()
    if not (opts.key or opts.mac) and not opts.update:
        parser.print_help()
        sys.exit(1)
    if opts.update:
        update()
    if opts.key:
        find_by_name(opts.key)
    if opts.mac:
        find_by_mac(opts.mac)

if __name__ == "__main__":
    main()
    



    


