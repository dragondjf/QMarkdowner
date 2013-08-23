#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import pkg
import logging

logger = logging.getLogger(__name__)


def deal_pkg(dc_ip, raw, ver=2):
    header, body = pkg.unpack(raw, ver)
    back = {}
    if header.cmd == pkg.GET_SAMPLING_CTRL_RSP:
        back = body.apply_to_dc(back)
    if header.cmd == pkg.GET_CHANNEL_CTRL_RSP:
        # back = body.apply_to_pa(back)
        back = body
    elif header.cmd == pkg.GET_BASE_INFO_RSP:
        back = body.apply_to_dc(back)
    elif header.cmd == pkg.GET_COMM_INFO_RSP:
        back = body.apply_to_dc(back)
    elif header.cmd == pkg.GET_DEVICE_FUNCTION_RSP:
        back = body.apply_to_dc(back)
    return back


def send_cmd(sk, address, header=None, body=None):
    if body:
        buf = pkg.combine(header, body).pack()
    else:
        buf = header.pack()
    try:
        sk.sendto(buf, address)
    except Exception, e:
        logger.error(e)


def getinforsp(ip, port, cmd, channel=1, ver=2):
    back = "timeout check ip"
    try:
        address = (ip, port)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(5)
        header = pkg.Header(cmd=cmd, channel=channel)
        send_cmd(s, address, header)
        raw, address = s.recvfrom(1024)
        ip = address[0]
        back = deal_pkg(ip, raw, ver)
        s.close()
    except Exception, e:
        raise
        logger.error(e)
    return back


def setinforsp(ip, port, cmd, ver=2, body_dict=None):
    try:
        address = (ip, port)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)
        header, body = pkg.get_pair(cmd, ver)
        if body_dict:
            body.load_from_dict(body_dict)
        send_cmd(s, address, header, body)
        raw, address = s.recvfrom(1024)
        header, body = pkg.unpack(raw, ver)
        s.close()
        if header.ret == 0:
            return True
        else:
            return False
    except Exception, e:
        logger.error(e)
        return False


def save_reboot(ip, port, ver=2):
    try:
        address = (ip, port)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(5)
        header, save = pkg.get_pair(0x0d, ver)
        send_cmd(s, address, header, save)
        raw, address = s.recvfrom(1024)
        header, body = pkg.unpack(raw, 2)
        import time
        time.sleep(1)
        header, reboot = pkg.get_pair(0x0c, ver)
        send_cmd(s, address, header, reboot)
        raw, address = s.recvfrom(1024)
        header, body = pkg.unpack(raw, 2)
        s.close()
    except Exception, e:
        logger.error(e)
        return False
    else:
        return True
