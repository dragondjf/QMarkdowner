# -*- coding: utf-8 -*-
import os
import shutil
import hashlib
import platform
import tempfile
import math
from app import settings
import urllib2
import os.path

file_update_allowed_ext = ['bin', 'cfg']


def undbref(ref):
    from db import connection
    from mongokit import ObjectId
    db = getattr(connection, ref.database)
    col = getattr(db, ref.collection)
    return col.find_one({'_id': ObjectId(ref.id)})


def requests(url, method='GET', body=None):
    try:
        request = urllib2.Request(url, body)
        request.get_method = lambda: method
        response = urllib2.urlopen(request, timeout=3)
    except urllib2.HTTPError, e:
        from log import logger
        logger.warn('Push HTTPError: %s %s ' % e.code, e.reason)
    except urllib2.URLError, e:
        from log import logger
        logger.warn('Push URLError: %s ' % e.reason)
    else:
        from log import logger
        logger.warn('Push success: %s ' % response.code)
        return response


def unix_socket_client(address, message):
    import socket
    import sys

    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    server_address = "/tmp/" + address
    try:
        sock.connect(server_address)
    except socket.error, msg:
        print >>sys.stderr, msg
        return

    try:
        sock.sendall(message)

    finally:
        sock.close()


def header_id(header, to_response=False):
    hid = '%s%s' % (header.channel, header.seq)
    return str(header.cmd | 0x10) + hid if to_response else hid


def ip2bin(dot_ip_str):
    if not dot_ip_str:
        return ''
    assert len(dot_ip_str.split('.')) == 4
    dot_ip_str = dot_ip_str.strip()
    return ''.join([chr(int(s)) for s in dot_ip_str.split('.')])


def bin2ip(s):
    return "%d.%d.%d.%d" % (ord(s[0]), ord(s[1]), ord(s[2]), ord(s[3]))


def to_objdict(obj):
    from tornado.util import ObjectDict
    wrapped = ObjectDict(dict(obj))
    if hasattr(obj, '_global_no'):
        wrapped._global_no = obj._global_no
    return wrapped


def get_ip_address(ifname=settings.default_ifname):
    import socket
    if platform_is('windows', 'cygwin'):
        ip = '127.0.0.1'
    else:
        myname = socket.getfqdn(socket.gethostname())
        ip = socket.gethostbyname(myname)
    if ip.startswith('127'):  # makes no sense
        import netifaces
        ip = netifaces.ifaddresses(ifname)[netifaces.AF_INET][0]['addr']
    return ip


def get_attr_from_dot_notation(obj, notation):
    """get_attr_from_dot_notation(
         {'a': {'c': 1, 'd': 2}, 'b': 3}, 'a.c.1'
    ) == {'a': {'c': 1}}"""
    r = notation.split('.', 1)
    att_name = r[0]
    other_notations = r[1] if len(r) > 1 else None
    if obj and att_name in obj:
        att_value = obj[att_name]
        if not other_notations:
            return {att_name: att_value}
        return {
            att_name: get_attr_from_dot_notation(att_value, other_notations)
        }
    else:
        return None


def merge(d1, d2):
    """merge two dict with their in common keys merged too"""
    r = dict(d1.items() + d2.items())
    for k, v in d1.iteritems():
        if k in d2:
            v2 = d2[k]
            if isinstance(v, dict) and isinstance(v2, dict):
                r[k] = merge(v, v2)
    return r


def platform_is(*test_strs):
    current_platform = platform.system().lower()
    for s in test_strs:
        if s in current_platform:
            return True


def bin_path(bin_file_name):
    path = os.path.join(os.getcwd(), 'bin', bin_file_name)
    if os.path.isfile(path):
        return path
    else:
        from log import logger
        logger.warn('binary path does not exist: %s' % path)


def sensitivitybreak(A):
    from log import logger
    sn = [0, 0]
    flag = 0
    cnt = 0
    if A >= 2 and A < 65536:
        if A == 2:
            sn = [2, 1]
            return sn
        elif 2 < A <= 512:
            sn = [A, 1]
            return sn
        else:
            while(1):
                for i in range(A / 255 + 1, int(math.sqrt(A))):
                    if (i > 1):
                        if (A % i):
                            pass
                        else:
                            sn[0] = max(i, A / i)
                            sn[1] = min(i, A / i)
                            return sn

                cnt = cnt + 1
                if (cnt % 2):
                    flag = flag + 1
                    A += flag
                else:
                    flag = flag + 1
                    A -= flag
    else:
        logger.info("Invalid digitalsensitivity number!")


def sensitivitycompound(A):
    from log import logger
    sn = sensitivitybreak(A)
    logger.info(
        "The first level N1=%d and the second level N2=%d" % (sn[0], sn[1]))
    if sn[1] > 1:
        return (sn[0] - 1) * 256 + (sn[1] - 2)
    else:
        return (sn[0] / 2 - 1) * 256 + (sn[1] - 1)


class TempDir(object):
    def __init__(self):
        self.path = tempfile.mkdtemp()

    def add(self, name, content):
        path = os.path.join(self.path, name)
        with open(path, 'w') as item_file:
            item_file.write(str(content))

    def delete(self):
        if os.path.isdir(self.path):
            shutil.rmtree(self.path)


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
    name = ""
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


def delext(pwd, ext):
    for dirpath, dirnames, filenames in os.walk(pwd):
        for filename in filenames:
            if os.path.splitext(filename)[1] == '.' + ext:
                filepath = os.path.join(dirpath, filename)
                os.remove(filepath)


def backhadbin_cfg(pwd, ext):
    for dirpath, dirnames, filenames in os.walk(pwd):
        for filename in filenames:
            if os.path.splitext(filename)[1] == '.' + ext:
                filepath = os.path.join(dirpath, filename)
                filesimplename = os.path.basename(filepath)
                return filesimplename
    return " "


def delfile(pwd, filename):
    try:
        name, ext = filename.split('.')
        assert ext in file_update_allowed_ext
        delext(pwd, ext)
        return True
    except (ValueError, AssertionError):
        return False
