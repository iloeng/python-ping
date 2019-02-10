#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File:    pings.py  
   Desc:    pings
   Author:  Liangz
   Contact: liangz.org@gmail.com
   Date:    2019/2/9 21:30
-------------------------------------------------
   Change:  2019/2/9
-------------------------------------------------
"""

import os

DEFAULT_COUNT = 4
DEFAULT_TIMEOUT = 2


class Pings(object):
    """

    """

    def __init__(self): #, target_host, count=DEFAULT_COUNT, timeout=DEFAULT_TIMEOUT):
        # self.target_host = target_host
        # self.count = count
        # self.timeout = timeout
        pass
        
    def checksum(self, source_string):
        """

        :param source_string:
        :return:
        """
        sum = 0
        max_count = (len(source_string)/2)*2
        count = 0
        while count < max_count:
            val = ord(source_string[count + 1]) * 256 + ord(source_string[count])
            sum = sum + val
            sum = sum & 0xffffffff
            count = count + 2

        if max_count < len(source_string):

            sum = sum + ord(source_string[len(source_string) - 1])
            sum = sum & 0xffffffff

        sum = (sum >> 16) + (sum & 0xffff)  # 将高16位与低16位相加直到高16位为0
        sum = sum + (sum >> 16)
        answer = ~sum
        answer = answer & 0xffff
        answer = answer >> 8 | (answer << 8 & 0xff00)
        return answer  # 返回的是十进制整数


if __name__ == '__main__':
    ping = Pings()
    val = ping.checksum('5A6D7C12457D56AB7FC')
    print(val)
