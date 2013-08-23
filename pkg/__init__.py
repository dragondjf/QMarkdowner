#!/usr/bin/env python
# -*- coding: UTF8 -*-

# UDP-based app level communication protocol
import struct
import dpkt
import logging
import v22
from utils import sensitivitycompound


logger = logging.getLogger(__name__)

#返回码
#成功
RETURN_SUCCESS = 0x00
#命令字未实现
RETURN_NO_ACHIEVE = 0x01
#消息长度错误
RETURN_LENGTH_ERROR = 0x02
#参数不合法
RETURN_PARAMETER_ERROR = 0x03
#功能未实现
RETURN_FEATURE_IMPLEMENTED = 0x04
#业务执行失败
RETURN_BUSINESS_FAILS = 0x05
#未知错误
RETURN_UNKNOWN_ERROR = 0xff


#command id
#查询产品基本固化信息
GET_BASE_INFO_REQ = 0x01
GET_BASE_INFO_RSP = 0x11

#查询通信控制信息
GET_COMM_INFO_REQ = 0x02
GET_COMM_INFO_RSP = 0x12

#设置通讯控制信息
SET_COMM_INFO_REQ = 0x03
SET_COMM_INFO_RSP = 0x13

#查询采样控制信息
GET_SAMPLING_CTRL_REQ = 0x04
GET_SAMPLING_CTRL_RSP = 0x14

#设置采样控制信息
SET_SAMPLING_CTRL_REQ = 0x05
SET_SAMPLING_CTRL_RSP = 0x15

#查询通道控制信息
GET_CHANNEL_CTRL_REQ = 0x06
GET_CHANNEL_CTRL_RSP = 0x16

#设置通道控制信息
SET_CHANNEL_CTRL_REQ = 0x07
SET_CHANNEL_CTRL_RSP = 0x17

#查询设备功能控制信息
GET_DEVICE_FUNCTION_REQ = 0x08
GET_DEVICE_FUNCTION_RSP = 0x18

#设置设备功能控制信息
SET_DEVICE_FUNCTION_REQ = 0x09
SET_DEVICE_FUNCTION_RSP = 0x19

#开关控制命令
SET_SWITCH_CTRL_REQ = 0x0a
SET_SWITCH_CTRL_RSP = 0x1a

#恢复出场配置
SET_RESTORE_REQ = 0x0b
SET_RESTORE_RSP = 0x1b

#重启命令
SET_REBOOT_REQ = 0x0c
SET_REBOOT_RSP = 0x1c

#执行保存配置命令
SET_SAVE_CFG_REQ = 0x0d
SET_SAVE_CFG_RSP = 0x1d

#执行固件升级命令
SET_UPGRADE_REQ = 0x0e
SET_UPGRADE_RSP = 0x1e

#采样数据报文
#标准预处理后采样数据上报报文
NOTIFY_PREPARE_SIMPLING_DATA = 0x21
#原始采样数据上报报文
NOTIFY_RAW_DATA = 0x22

#系统故障
NOTIFY_SYS_FAIL = 0x31
#通道故障
NOTIFY_CHANNEL_FAIL = 0x32
#系统故障恢复
NOTIFY_SYS_FAIL_RECOVERY = 0x33
#通道故障恢复
NOTIFY_CHANNEL_FAIL_RECOVERY = 0x34


class ErrorUnknownType(Exception):
    pass


#包头格式
class Header(dpkt.Packet):
    length = 6
    __hdr__ = (
        ('length', 'H', 0),
        ('cmd', 'B', 0xff),
        ('ret', 'B', 0xff),
        ('channel', 'B', 0xff),
        ('seq', 'B', 0xff)
    )


class Empty(dpkt.Packet):
    __hdr__ = ()


#产品固化信息
class BaseInfo(dpkt.Packet):
    __hdr__ = (
        ('mac', '6s', '\xff\xff\xff\xff\xff\xff'),
        ('hwid', '6s', '\xff\xff\xff\xff\xff\xff'),
        ('hwcode', '2s', '\xff\xff'),
        ('hw_version', '2s', '\xff\xff'),
        ('sw_version', '2s', '\xff\xff'),
        ('sw_revision', 'H', 0xffff),
        ('proto_version', 'B', 0xff),
        ('proto_mode', 'B', 0xff),
        ('channel_num', 'B', 0xff),
        ('config_version', '2s', '\xff\xff'),
        ('boot_version', '2s', '\xff\xff'),
        ('ip_num', 'B', 0xff),
        ('machine_id', 'B', 0xff),
        ('slot_id', 'B', 0xff)
    )

    def apply_to_dc(self, dc):
        dc['mac'] = u':'.join(['%02x' % ord(t) for t in self.mac])
        dc['hw_version'] = u'.'.join(['%d' % ord(t) for t in self.hw_version])
        dc['sw_version'] = u'.'.join(['%d' % ord(t) for t in self.sw_version])
        dc['sw_version'] += u'-r%s' % str(self.sw_revision)
        dc['hwcode'] = u'%s %s' % (":".join(["%02x" % ord(t) for t in self.hwcode]), ":".join(["%02x" % ord(t) for t in self.hwid]))
        dc['slot_id'] = self.slot_id
        dc['ip_num'] = self.ip_num
        dc['proto_mode'] = self.proto_mode
        dc['boot_version'] = u'.'.join(['%d' % ord(t) for t in self.boot_version])
        dc['proto_version'] = self.proto_version
        dc['machine_id'] = self.machine_id
        dc['config_version'] = u'.'.join(['%d' % ord(t) for t in self.config_version])
        dc['channel_num'] = self.channel_num
        return dc


#产品固化信息V1.0
class BaseInfo_v1(dpkt.Packet):
    __hdr__ = (
        ('mac', '6s', '\xff\xff\xff\xff\xff\xff'),
        ('hwid', '6s', '\xff\xff\xff\xff\xff\xff'),
        ('hwcode', '2s', '\xff\xff'),
        ('hw_version', '2s', '\xff\xff'),
        ('sw_version', '2s', '\xff\xff'),
        ('sw_revision', 'H', 0xffff),
        ('proto_version', 'B', 0xff),
        ('proto_mode', 'B', 0xff),
        ('channel_num', 'B', 0xff)
    )


#通信控制信息
class CommInfo(dpkt.Packet):
    __hdr__ = (
        ('ip_mode', 'B', 0xff),
        ('ipaddr', '4s', '\xff\xff\xff\xff'),
        ('netmask', '4s', '\xff\xff\xff\xff'),
        ('gateway', '4s', '\xff\xff\xff\xff'),
        ('mgmt_ipaddr', '4s', '\xff\xff\xff\xff'),
        ('mgmt_port', 'H', 0xffff),
        ('syslog_ipaddr', '4s', '\xff\xff\xff\xff'),
        ('syslog_port', 'H', 0xffff),
        ('syslog_priority', 'B', 0xff),
        ('log_priority', 'B', 0xff)
    )

    def load_from_dc(self, dc):
        from utils import ip2bin
        self.ip_mode = dc.ip_mode
        self.ipaddr = ip2bin(dc.ip)
        self.netmask = ip2bin(dc.subnet_mask)
        self.gateway = ip2bin(dc.gateway)
        self.mgmt_ipaddr = ip2bin(dc.host_ip)
        self.mgmt_port = dc.host_port
        self.syslog_ipaddr = ip2bin(dc.syslog_ip)
        self.syslog_port = dc.syslog_port
        self.syslog_priority = dc.syslog_priority
        self.log_priority = dc.log_priority

    def load_from_dict(self, dc):
        from utils import ip2bin
        self.ip_mode = int(dc['ip_mode'])
        self.ipaddr = ip2bin(dc['ipaddr'])
        self.netmask = ip2bin(dc['netmask'])
        self.gateway = ip2bin(dc['gateway'])
        self.mgmt_ipaddr = ip2bin(dc['mgmt_ipaddr'])
        self.mgmt_port = int(dc['mgmt_port'])
        self.syslog_ipaddr = ip2bin(dc['syslog_ipaddr'])
        self.syslog_port = int(dc['syslog_port'])
        self.syslog_priority = int(dc['syslog_priority'])
        self.log_priority = int(dc['log_priority'])

    def apply_to_dc(self, dc):
        from utils import bin2ip
        dc['ip_mode'] = self.ip_mode
        dc['ipaddr'] = bin2ip(self.ipaddr)
        dc['netmask'] = bin2ip(self.netmask)
        dc['gateway'] = bin2ip(self.gateway)
        dc['mgmt_ipaddr'] = bin2ip(self.mgmt_ipaddr)
        dc['mgmt_port'] = self.mgmt_port
        dc['syslog_ipaddr'] = bin2ip(self.syslog_ipaddr)
        dc['syslog_port'] = self.syslog_port
        dc['syslog_priority'] = self.syslog_priority
        dc['log_priority'] = self.log_priority
        return dc


#采样控制信息
class SamplingCtrl(dpkt.Packet):
    __hdr__ = (
        ('freq', 'B', 0xff),
        ('fft_size', 'B', 0xff)
    )

    def apply_to_dc(self, dc):
        dc['freq'] = self.freq
        dc['fft_size'] = self.fft_size
        return dc

#通道控制信息
class ChannelCtrl(dpkt.Packet):
    __hdr__ = (
        ('enable', 'B', 0xff),
        ('mu_factor', 'H', 0xffff),
        ('mode', 'B', 0xff),
        ('pre_process_mode', 'B', 0x01),
        ('photoelectron_value', 'L', 0xffffffff),
        ('win_size', 'B', 0xff)
    )

    def load_from_pa(self, pa):
        from app.settings import alg_win
        wins = []
        for f in pa.alg['fkeys']:
            wins.append(alg_win[f])
        win_data = ''
        for win in wins:
            win_data += self.WinSetting(**win).pack()
        self.enable = pa.enabled,
        self.mu_factor = sensitivitycompound(pa.digitalzoom),
        self.mode = pa.alg['mode'],
        self.win_size = len(wins),
        self.data = win_data

    def apply_to_pa(self, pa):
        pa['enable'] = bool(self.enable)
        pa['mu_factor'] = self.mu_factor
        pa['mode'] = self.mode
        pa['pre_process_mode'] = self.pre_process_mode
        pa['photoelectron_value'] = self.photoelectron_value
        pa['win_size'] = self.win_size
        win = []
        for n in xrange(self.win_size):
            one_win = {}
            one_win['begin'] = self.win[n].begin
            one_win['noise'] = self.win[n].noise
            one_win['end'] = self.win[n].end
            win.append(one_win)
        pa['win'] = win
        return pa

    def unpack(self, buf):
        dpkt.Packet.unpack(self, buf)
        self.win = []
        for n in xrange(self.win_size):
            self.win.append(self.WinSetting(self.data[n * 6:]))
        self.data = self.win

    def __len__(self):

        if isinstance(self.data, list):
            l = self.__hdr_len__
            for n in xrange(len(self.data)):
                l = l + len(self.data[n])
            return l
        else:
            return self.__hdr_len__ + len(self.data)

    def __repr__(self):
        l = ['%s=%r' % (k, getattr(self, k))
             for k in self.__hdr_defaults__
             if getattr(self, k) != self.__hdr_defaults__[k]]
        if self.data:
            if isinstance(self.data, list):
                ll = [repr(k) for k in self.data]
                l.append('data=[%s]' % ', '.join(ll))
            else:
                l.append('data=%r' % self.data)
        return '%s(%s)' % (self.__class__.__name__, ', '.join(l))

    def __str__(self):

        if isinstance(self.data, list):
            b = self.pack_hdr()
            for n in xrange(len(self.data)):
                b = b + str(self.data[n])
            return b
        else:
            return self.pack_hdr() + str(self.data)

    class WinSetting(dpkt.Packet):
        __hdr__ = (
            ('begin', 'H', 0xffff),
            ('end', 'H', 0xffff),
            ('noise', 'H', 0xffff)
        )

        def unpack(self, buf):
            dpkt.Packet.unpack(self, buf)
            self.data = None


#通道控制信息V1.0
class ChannelCtrl_v1(dpkt.Packet):
    __hdr__ = (
        ('enable', 'B', 0xff),
        ('mu_factor', 'B', 0xff),
        ('mode', 'B', 0xff),
        ('begin', 'H', 0xffff),
        ('end', 'H', 0xffff),
        ('noise', 'H', 0xffff)
    )


class PrepareSimplingData(dpkt.Packet):
    __hdr__ = (
        ('max', 'H', 0xff),
        ('min', 'H', 0xff),
        ('avg', 'H', 0xff),
        ('variance', 'H', 0xff),
        ('compression', 'H', 0xff),
        ('reserve6', 'H', 0xff),
        ('reserve7', 'H', 0xff),
        ('reserve8', 'H', 0xff)
    )

    def unpack(self, buf):
        dpkt.Packet.unpack(self, buf)
        self.freq = []
        for n in xrange(len(self.data) / 4):
            self.freq.append(struct.unpack_from(">L", self.data[n * 4:])[0])
        self.data = self.freq

    def __len__(self):

        if isinstance(self.data, list):
            l = self.__hdr_len__
            for n in xrange(len(self.data)):
                l = l + len(self.data[n])
            return l
        else:
            return self.__hdr_len__ + len(self.data)

    def __repr__(self):
        l = ['%s=%r' % (k, getattr(self, k))
             for k in self.__hdr_defaults__
             if getattr(self, k) != self.__hdr_defaults__[k]]
        if self.data:
            if isinstance(self.data, list):
                ll = [repr(k) for k in self.data]
                l.append('data=[%s]' % ', '.join(ll))
            else:
                l.append('data=%r' % self.data)
        return '%s(%s)' % (self.__class__.__name__, ', '.join(l))

    def __str__(self):

        if isinstance(self.data, list):
            b = self.pack_hdr()
            for n in xrange(len(self.data)):
                b = b + str(self.data[n])
            return b
        else:
            return self.pack_hdr() + str(self.data)


#开关控制
class SwitchCtrl(dpkt.Packet):
    __hdr__ = (
        ('relay', 'B', 0xff),
        ('led', 'B', 0xff),
        ('mixer', 'B', 0xff)
    )


class RawData(dpkt.Packet):
    __hdr__ = (
    )

bodies = {
    1: {
        GET_BASE_INFO_REQ: Empty,
        GET_BASE_INFO_RSP: BaseInfo_v1,
        GET_CHANNEL_CTRL_REQ: Empty,
        GET_CHANNEL_CTRL_RSP: ChannelCtrl_v1,
        SET_CHANNEL_CTRL_REQ: ChannelCtrl_v1,
        SET_CHANNEL_CTRL_RSP: Empty,
        SET_SWITCH_CTRL_REQ: SwitchCtrl,
        SET_SWITCH_CTRL_RSP: Empty,
        NOTIFY_PREPARE_SIMPLING_DATA: PrepareSimplingData,
        NOTIFY_SYS_FAIL: Empty,
        NOTIFY_CHANNEL_FAIL: Empty,
        NOTIFY_SYS_FAIL_RECOVERY: Empty,
        NOTIFY_CHANNEL_FAIL_RECOVERY: Empty
    },
    2: {
        GET_BASE_INFO_REQ: Empty,
        GET_BASE_INFO_RSP: BaseInfo,
        GET_COMM_INFO_REQ: Empty,
        GET_COMM_INFO_RSP: CommInfo,
        SET_COMM_INFO_REQ: CommInfo,
        SET_COMM_INFO_RSP: Empty,
        GET_SAMPLING_CTRL_REQ: Empty,
        GET_SAMPLING_CTRL_RSP: SamplingCtrl,
        SET_SAMPLING_CTRL_REQ: SamplingCtrl,
        SET_SAMPLING_CTRL_RSP: Empty,
        GET_CHANNEL_CTRL_REQ: Empty,
        GET_CHANNEL_CTRL_RSP: ChannelCtrl,
        SET_CHANNEL_CTRL_REQ: ChannelCtrl,
        SET_CHANNEL_CTRL_RSP: Empty,
        SET_SWITCH_CTRL_REQ: SwitchCtrl,
        SET_SWITCH_CTRL_RSP: Empty,
        SET_RESTORE_REQ: Empty,
        SET_RESTORE_RSP: Empty,
        SET_REBOOT_REQ: Empty,
        SET_REBOOT_RSP: Empty,
        SET_SAVE_CFG_REQ: Empty,
        SET_SAVE_CFG_RSP: Empty,
        SET_UPGRADE_REQ: Empty,
        SET_UPGRADE_RSP: Empty,
        NOTIFY_PREPARE_SIMPLING_DATA: PrepareSimplingData,
        NOTIFY_RAW_DATA: RawData,
        NOTIFY_SYS_FAIL: Empty,
        NOTIFY_CHANNEL_FAIL: Empty,
        NOTIFY_SYS_FAIL_RECOVERY: Empty,
        NOTIFY_CHANNEL_FAIL_RECOVERY: Empty,

        # for compatibility of v2
        SET_DEVICE_FUNCTION_RSP: Empty,
    },
    3: {
        GET_BASE_INFO_REQ: Empty,
        GET_BASE_INFO_RSP: BaseInfo,

        GET_COMM_INFO_REQ: Empty,
        GET_COMM_INFO_RSP: v22.CommInfo,

        SET_COMM_INFO_REQ: v22.CommInfo,
        SET_COMM_INFO_RSP: Empty,

        GET_SAMPLING_CTRL_REQ: Empty,
        GET_SAMPLING_CTRL_RSP: SamplingCtrl,

        SET_SAMPLING_CTRL_REQ: SamplingCtrl,
        SET_SAMPLING_CTRL_RSP: Empty,

        GET_CHANNEL_CTRL_REQ: Empty,
        GET_CHANNEL_CTRL_RSP: v22.ChannelCtrl,

        SET_CHANNEL_CTRL_REQ: v22.ChannelCtrl,
        SET_CHANNEL_CTRL_RSP: Empty,

        GET_DEVICE_FUNCTION_REQ: Empty,
        GET_DEVICE_FUNCTION_RSP: v22.DeviceFunction,

        SET_DEVICE_FUNCTION_REQ: v22.DeviceFunction,
        SET_DEVICE_FUNCTION_RSP: Empty,

        SET_SWITCH_CTRL_REQ: SwitchCtrl,
        SET_SWITCH_CTRL_RSP: Empty,

        SET_RESTORE_REQ: Empty,
        SET_RESTORE_RSP: Empty,

        SET_REBOOT_REQ: Empty,
        SET_REBOOT_RSP: Empty,

        SET_SAVE_CFG_REQ: Empty,
        SET_SAVE_CFG_RSP: Empty,

        SET_UPGRADE_REQ: Empty,
        SET_UPGRADE_RSP: Empty,

        NOTIFY_PREPARE_SIMPLING_DATA: PrepareSimplingData,
        NOTIFY_RAW_DATA: RawData,
        NOTIFY_SYS_FAIL: Empty,
        NOTIFY_CHANNEL_FAIL: Empty,
        NOTIFY_SYS_FAIL_RECOVERY: Empty,
        NOTIFY_CHANNEL_FAIL_RECOVERY: Empty
    }
}


def unpack(buf, ver=None):
    ver = ver or 2
    body = None
    vers = bodies.keys()
    if ver < min(vers) or ver > max(vers):
        raise ErrorUnknownType("unknown version %d" % ver)
    header = Header(buf[:Header.length])
    if header.cmd in bodies[ver]:
        if bodies[ver][header.cmd]:
            body = bodies[ver][header.cmd](buf[Header.length:])
        else:
            body = buf[Header.length:]
    else:
        raise ErrorUnknownType("unknown packet type 0x%x" % header.cmd)
    return (header, body)


def get_pair(cmd, ver=2):
    header = Header(cmd=cmd)
    try:
        body = bodies[ver][cmd]()
        return header, body
    except KeyError:
        logger.error('getting pkg body failed, cmd: %s, ver: %s', cmd, ver)


def combine(header, body):
    assert not header.data
    body_data = body.pack()
    header.length = len(body_data)
    header.data = body_data
    return header
