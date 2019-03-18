#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File:    ping.py
   Desc:    python 3.x ping
   Author:  Liangz
   Contact: liangz.org@gmail.com
   Date:    2019/2/9 21:30
-------------------------------------------------
   Change:  2019/3/18
-------------------------------------------------
"""

"""
1. 把校验和字段置为0
2. 对首部中的每16 bit（位）进行二进制反码求和（整个首部看成是由一串16 bit 的字组成）， 结果存在校验和字段中
"""

import sys
import struct
import socket
import select
import time

DEFAULT_COUNT = 4
DEFAULT_TIMEOUT = 2


def checksum(data):
    n = len(data)
    m = n % 2
    sum = 0
    for i in range(0, n - m, 2):
        sum += (data[i]) + ((data[i+1]) << 8)

    if m:
        sum += (data[-1])
    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)
    answer = ~sum & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def raw_socket(dst_addr, icmp_packet):
    rawsocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
    send_request_ping_time = time.time()
    rawsocket.sendto(icmp_packet, (dst_addr, 80))
    return send_request_ping_time, rawsocket, dst_addr


def request_ping(data_type, data_code, data_checksum, data_id, data_sequence, payload_body):
    icmp_packet = struct.pack('>BBHHH32s', data_type, data_code, data_checksum, data_id, data_sequence, payload_body)
    icmp_checksum = checksum(icmp_packet)
    icmp_packet = struct.pack('>BBHHH32s', data_type, data_code, icmp_checksum, data_id, data_sequence, payload_body)
    return icmp_packet


def reply_ping(send_request_ping_time, rawsocket, data_sequence, timeout=2):
    while True:
        started_select = time.time()
        what_ready = select.select([rawsocket], [], [], timeout)
        wait_time = (time.time() - started_select)
        if what_ready[0] is []:
            return -1
        time_received = time.time()
        received_packet, addr = rawsocket.recvfrom(2014)
        icmp_header = received_packet[20:28]
        type, code, checksum, packet_id, sequence = struct.unpack(">BBHHH", icmp_header)
        if type == 0 and sequence == data_sequence:
            return time_received - send_request_ping_time
        timeout = timeout - wait_time
        if timeout <= 0:
            return -1


def ping(host):
    data_type = 8
    data_code = 0
    data_checksum = 0
    data_id = 0
    data_sequence = 1
    payload_body = b'abcdefghijklmnopqrstuvwabcdefghi'
    dst_addr = socket.gethostbyname(host)
    print(u"正在 Ping {} [{}] 具有 32 字节的数据:".format(host, dst_addr))
    for i in range(0, 4):
        icmp_packet = request_ping(data_type, data_code, data_checksum, data_id, data_sequence + i, payload_body)
        send_request_ping_time, rawsocket, addr = raw_socket(dst_addr, icmp_packet)
        times = reply_ping(send_request_ping_time, rawsocket, data_sequence + i)
        if times > 0:
            print("来自 {} 的回复: 字节=32 时间={}ms".format(addr, int(times*1000)))
            time.sleep(0.7)
        else:
            print("Timeout")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Usage: ping.py <host>")

    ping(sys.argv[1])

    # ping('www.baidu.com')
