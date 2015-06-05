#!/usr/bin/python

import string

def OnlyInts(msg):
    all = string.maketrans('', '')
    noChars = all.translate(all, string.digits)
    return msg.translate(all, noChars)
