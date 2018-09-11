# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 13:06:23 2018

@author: fahad

@contributor: Lianxin Zhang
"""

import threading
import tcpPC


if __name__ == '__main__':
    
    t1 = threading.Thread(target= tcpPC.tcpPC)
    
    t1.start()
    
    t1.join()