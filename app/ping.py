#!/usr/bin/python
# -*- coding: utf-8 -*-
import dpkt
import random
import socket
import time
import logging


logger = logging.getLogger(__name__)


def ping(host, count=1, data='dragondjf'):
    ping_flag = False
    ping_reslut = ''
    try:
        dst = socket.gethostbyname(host)
    except socket.gaierror, e:
        logger.error(e)
        ping_reslut = u'无法找到指定的ip地址'
        return ping_flag, ping_reslut

    echo = dpkt.icmp.ICMP.Echo()
    echo.id = random.randint(0, 0xffff)
    echo.seq = random.randint(0, 0xffff)
    echo.data = data
    icmp = dpkt.icmp.ICMP()
    icmp.type = dpkt.icmp.ICMP_ECHO
    icmp.data = echo
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, dpkt.ip.IP_PROTO_ICMP)
    s.settimeout(3)
    for i in range(0, count):
        start = time.time()
        s.sendto(str(icmp), (dst, 0))
        try:
            reply = s.recv(0xffff)
        except Exception, e:
            logger.error(e)
            ping_flag = False
            ping_reslut = e
            return ping_flag, u'timeout,连接超时'
        used = (time.time() - start) * 1000
        ip = dpkt.ip.IP(reply)
        if ip.icmp.type == 0 or (ip.icmp.type == 8 and host == "localhost"):
            ping_reslut = u'%d bytes from %s: icmp_seq=%d ip_id=%d ttl=%d time=%.3fms' % (len(ip.icmp), dst, ip.icmp.echo.seq, ip.id, ip.ttl, used)
            ping_flag = True
        else:
            ping_flag = False
            ping_reslut = ip.icmp.type
    s.close()
    return ping_flag, ping_reslut
