#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import tftpy
import struct
import time
import socket
import hashlib
import threading
import logging

logger = logging.getLogger(__name__)

udp_port = 6004
file_update_allowed_ext = ['bin', 'cfg']

update_progress = 0.0


class Object_Dict(dict):
    def __init__(self, *args, **kw):
        dict.__init__(self, *args, **kw)
        self.__dict__ = self


class ObjectDict(dict):
    """Makes a dictionary behave like an object."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


def get_md5(file_body):
    md5 = hashlib.md5()
    md5.update(file_body)
    return md5.hexdigest()


def fw_md5(file_body):
    '''
        根据文件内容计算md5值
    '''
    return get_md5(file_body)[-4:]  # only the last 4 bytes are needed


def is_valid_fw(filename):
    '''
        校验文件名中的md5值是否与文件对应
    '''
    try:
        name, ext = filename.split('.')
        assert ext in file_update_allowed_ext
    except (ValueError, AssertionError):
        return False
    if '_m' in name:
        with open(filename, 'r') as bin:
            fbody = bin.read()
        m = fw_md5(fbody)
        return True if name.endswith('_m%s' % m) else False
    return False


def updatefile(host, filename):
    '''
        对文件进行md5校验，一个文件对应一个线程
    '''
    file_valid_flag = is_valid_fw(filename)
    # print filename, u'文件md5校验正确:', file_valid_flag
    if file_valid_flag:
        tftp_client = TftpUpdateClient(host, filename)
        tftp_client.join()


def enter_update_mode(host, port):
    '''
        开启升级模式
    '''
    MAX_UDP_ATTEMPT = 5
    MSG_START_UPDATE = struct.pack('BBBBBB', 0, 0, 0x0e, 0, 0, 0)
    MSG_READY_FOR_UPDATE = struct.pack('BBBBBB', 0, 0, 0x1e, 0, 0, 0)
    timeout = 20  # default timeout (second)

    udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_client.settimeout(timeout)
    attempt = 0
    ready = False
    while True:
        try:
            udp_client.sendto(
                MSG_START_UPDATE,
                (host, port)
            )
            res, addr = udp_client.recvfrom(8192)
        except:
            attempt += 1
            if attempt < MAX_UDP_ATTEMPT:
                # print u'第%d次开启升级模式升级失败' % attempt
                logger.info('第%d次开启升级模式升级失败' % attempt)
                continue
            else:
                return False
        if res and addr[0] == host:
            if res == MSG_READY_FOR_UPDATE:
                ready = True
                break
        udp_client.close()

    return ready


class TftpUpdateClient(threading.Thread):

    MAX_TFTP_ATTEMPT = 5

    def __init__(self, host, filename):
        super(TftpUpdateClient, self).__init__()
        self._uploaded_bytes = 0.0
        self._total_bytes = 0.0

        info = {}

        info['progress'] = 0.0
        info['update_flag'] = False

        self.info = info

        self.host = str(host)
        self.filename = filename
        self.ready = False

        self._tftpclient = tftpy.TftpClient(self.host, 69)
        # self.daemon = True
        self.start()

    def run(self):
        # print u'开始升级%s' % self.filename
        self.upload()
        # print u'升级最后成功与否', self.info

    def upload(self):
        f = open(self.filename, 'r').read()
        self._total_bytes = len(f)

        # calculate md5
        m = fw_md5(f)
        fname, ext = os.path.basename(self.filename).split('.')
        if '_m' in fname:  # md5 is provided
            remote_filename = '%s.%s' % (fname, ext)
        else:
            remote_filename = '%s_m%s.%s' % (fname, m, ext)

        def try_tftp(attempt):
            try:
                self._tftpclient.upload(
                    str(remote_filename),
                    str(self.filename),
                    self.set_progress
                )
                self.info['update_flag'] = True
            except TypeError:
                attempt += 1
                if attempt < self.MAX_TFTP_ATTEMPT:
                    try_tftp(attempt)
                else:
                    self.info['update_flag'] = False
        attempt = 0
        try_tftp(attempt)

    def set_progress(self, pack):
        if isinstance(pack, tftpy.TftpPacketDAT):
            self._uploaded_bytes += len(pack.data)
            percent = self._uploaded_bytes / self._total_bytes * 100
            self.info['progress'] = percent
            global update_progress
            update_progress = percent


def upgrade(bin_file, cfg_file, ip, port):
    global udp_port
    udp_port = port
    back = " "
    ready = enter_update_mode(ip, udp_port)
    # print u'下位机是否准备就绪：', ready
    if ready:
        # print "ifififif"
        if bin_file:
            # print "bin_file"
            updatefile(ip, bin_file)
        if cfg_file:
            # print "cfg_file"
            updatefile(ip, cfg_file)
        back = "OK"
    else:
        back = u'下位机是否准备就绪:否'
    time.sleep(25)
    # print '所有固件升级成功'
    # print back
    return back
