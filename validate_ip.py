#!/usr/bin/python3
# Small script to validate a given IP address

import socket
import sys

def validate_ip(ip):
    try:
        socket.inet_pton(socket.AF_INET, ip)
        return (True,"IPv4")
    except socket.error:
        try:
            socket.inet_pton(socket.AF_INET6, ip)
            return(True,"IPv6")
        except socket.error:
            return(False,"")

if __name__ == "__main__":
    try:
        ip = sys.argv[1]
        state, version = validate_ip(ip)
        if state:
            print(ip + " is a valid " + version + " address")
    except IndexError:
        print("No IP given")
