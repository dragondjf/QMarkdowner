# -*- coding: UTF8 -*-
import dpkt
import datetime
from utils import sensitivitycompound


#通信控制信息
class CommInfo(dpkt.Packet):
    __hdr__ = (
        ('ip_mode', 'B', 0),
        ('ipaddr', '4s', '\xff' * 4),
        ('netmask', '4s', '\xff' * 4),
        ('gateway', '4s', '\xff' * 4),
        ('mgmt_ipaddr', '4s', '\xff' * 4),
        ('mgmt_port', 'H', 0xffff),
        ('syslog_ipaddr', '4s', '\xff' * 4),
        ('syslog_port', 'H', 6004),
        ('syslog_priority', 'B', 0),
        ('log_priority', 'B', 0),

        ('mgmt_mode', 'B', 0),  # 0: 采集器模式(通信模式5) 1: 独立模式(通信模式6)
        ('password', '3s', '\xff' * 3),
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

        self.mgmt_mode = dc.mgr_mode
        self.password = str(dc.password)

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
        self.mgmt_mode = int(dc['mgmt_mode'])

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

        dc['mgmt_mode'] = self.mgmt_mode
        # dc['password'] = ''.join(map(chr, self.password))
        return dc

# class Window(dpkt.Packet):
#     __hdr__ = (
#         ('begin', 'H', 0),
#         ('end', 'H', 0),
#         ('noise', 'H', 0)
#     )


#通道控制信息
class ChannelCtrl(dpkt.Packet):
    __hdr__ = (
        ('enable', 'B', 0xff),
        ('mu_factor', 'H', 0xffff),
        ('mode', 'B', 0xff),
        ('pre_process_mode', 'B', 0xff),
        ('photoelectron_value', 'L', 0xffffffff),
        ('win_size', 'B', 8),
        # ('windows', '%ss' % 3 * 8, Window().pack() * 8),
        # damn it!
        ('begin1', 'H', 0),
        ('end1', 'H', 0),
        ('noise1', 'H', 0),
        ('begin2', 'H', 0),
        ('end2', 'H', 0),
        ('noise2', 'H', 0),
        ('begin3', 'H', 0),
        ('end3', 'H', 0),
        ('noise3', 'H', 0),
        ('begin4', 'H', 0),
        ('end4', 'H', 0),
        ('noise4', 'H', 0),
        ('begin5', 'H', 0),
        ('end5', 'H', 0),
        ('noise5', 'H', 0),
        ('begin6', 'H', 0),
        ('end6', 'H', 0),
        ('noise6', 'H', 0),
        ('begin7', 'H', 0),
        ('end7', 'H', 0),
        ('noise7', 'H', 0),
        ('begin8', 'H', 0),
        ('end8', 'H', 0),
        ('noise8', 'H', 0),
        ('defence_start', 'B', 0xff),  # 0-23
        ('defence_end', 'B', 0xff),  # 0-23
        ('work_mode', 'B', 0xff),  # 标准周界和自适应周界
        ('sensitivity', 'H', 0xff),  # 灵敏度
        ('response_time', 'B', 0xff),  # 响应时间
        ('noise_immunity', 'B', 0xff)  # 抗干扰度
    )

    def set_windows(self, windows):
        for i, w in enumerate(windows):
            setattr(self, 'begin%s' % i + 1, w.begin)
            setattr(self, 'end%s' % i + 1, w.end)
            setattr(self, 'noise%s' % i + 1, w.noise)
        self.win_size = len(windows)

    def get_windows(self):
        windows = []
        for i in xrange(1, self.win_size + 1):
            windows.append({
                'begin': getattr(self, 'begin%s' % i),
                'end': getattr(self, 'end%s' % i),
                'noise': getattr(self, 'noise%s' % i)
            })
        return windows

    def load_from_pa(self, pa):
        self.enable = pa.enabled
        self.mu_factor = sensitivitycompound(pa.digitalzoom)
        self.mode = pa.alg['mode']
        # pre_process_mode = 1
        # photoelectron_valuee = 1
        from app.settings import alg_win
        windows = []
        for f in pa.alg['fkeys']:
            windows.append(alg_win[f])

        self.win_size = 4

        self.defence_start = pa.alg['defence_start']
        self.defence_end = pa.alg['defence_end']
        work_mode = 1

        if pa.alg['alarm_workmode'] == u'ifpms_adaptation':
            work_mode = 0
        elif pa.alg['alarm_workmode'] == u'ifpms_normal':
            work_mode = 1
        elif pa.alg['alarm_workmode'] == u'ifpms_dector':
            work_mode = 2
        elif pa.alg['alarm_workmode'] == u'ifpms_meansquare':
            work_mode = 3

        # 下位机标准周界对应第一个窗口，自适应对应第二个窗口
        if work_mode == 0 or work_mode == 2:
            setattr(self, 'begin2', windows[0]['begin'])
            setattr(self, 'end2', windows[0]['end'])
            setattr(self, 'noise2', windows[0]['noise'])
        if work_mode == 1:
            setattr(self, 'begin1', windows[0]['begin'])
            setattr(self, 'end1', windows[0]['end'])
            setattr(self, 'noise1', windows[0]['noise'])
        if work_mode == 3:  # 下位机低频窗口noise由0变成5，高频窗口noise由0变成1，高频窗口
            setattr(self, 'begin3', windows[0]['begin'])
            setattr(self, 'end3', windows[0]['end'])
            setattr(self, 'noise3', windows[0]['noise'] + 5)
            setattr(self, 'begin4', windows[1]['begin'])
            setattr(self, 'end4', windows[1]['end'])
            setattr(self, 'noise4', windows[1]['noise'] + 1)

        self.work_mode = work_mode
        self.sensitivity = pa.alg[pa.alg['alarm_workmode']][0]['sensitivity']
        self.response_time = pa.alg[pa.alg['alarm_workmode']][0]['responsetime']
        self.noise_immunity = pa.alg[pa.alg['alarm_workmode']][0]['ratio']

    # def apply_to_pa(self, pa):
    #     pa.alg['enabled'] = bool(self.enable)
    #     pa.digitalzoom = self.mu_factor
    #     pa.alg['mode'] = self.mode
    #     pa.alg['defence_start'] = self.defence_start
    #     pa.alg['defence_end'] = self.defence_end
    #     work_mode = "ifpms_adaptation"
    #     if self.work_mode == 1:
    #         work_mode = "ifpms_adaptation"
    #     elif self.work_mode == 0:
    #         work_mode = "ifpms_normal"
    #     elif self.work_mode == 3:
    #         work_mode = "ifpms_adaptation"
    #     elif self.work_mode == 2:
    #         work_mode = "ifpms_meansquare"

    #     pa['alg']['work_mode'] = work_mode
    #     pa.alg[pa.alg['alarm_workmode']][0]['sensitivity'] = self.sensitivity
    #     pa.alg[pa.alg['alarm_workmode']][0]['responsetime'] = self.response_time
    #     pa.alg[pa.alg['alarm_workmode']][0]['ratio'] = self.noise_immunity
    #     return pa

# class Phone(dpkt.Packet):
#     __hdr__ = (
#         ('mode', 'B', 0),  # 1:管理员(收发) 0:操作员(收)
#         ('number', '11s', '\xff' * 11),
#     )


#设备功能控制
class DeviceFunction(dpkt.Packet):
    __hdr__ = (
        ('year', 'H', 0),  # 2012-2049
        ('month', 'B', 0),  # 1-12
        ('day', 'B', 0),  # 1-31
        ('hour', 'B', 0),  # 0-23
        ('minute', 'B', 0),  # 0-59
        ('second', 'B', 0),  # 0-59
        ('relay_duration', 'H', 2),  # 继电器输出持续时间(second) 0-3600
        ('activated_phone_count', 'B', 8),  # 有效的手机号码个数 0-8
        # 八个手机号码位
        # ('cellphones', '%ss' % (1 + 11) * 8, 0),
        # damn it!
        ('phone_mode1', 'B', 0),
        ('phone1', '11s', '/xff' * 11),
        ('phone_mode2', 'B', 0),
        ('phone2', '11s', '/xff' * 11),
        ('phone_mode3', 'B', 0),
        ('phone3', '11s', '/xff' * 11),
        ('phone_mode4', 'B', 0),
        ('phone4', '11s', '/xff' * 11),
        ('phone_mode5', 'B', 0),
        ('phone5', '11s', '/xff' * 11),
        ('phone_mode6', 'B', 0),
        ('phone6', '11s', '/xff' * 11),
        ('phone_mode7', 'B', 0),
        ('phone7', '11s', '/xff' * 11),
        ('phone_mode8', 'B', 0),
        ('phone8', '11s', '/xff' * 11),
        # 中文名称unicode编码字符串长度, 最大值MAX=16(中文字数) * 4=64
        ('pa_name_len1', 'B', 0),
        # 中文转unicode编码字符串 4个字符/一个汉字
        ('pa_name1', '65s', '/xff' * 64),
        ('pa_name_len2', 'B', 0),
        ('pa_name2', '65s', '/xff' * 64),
        ('pa_name_len3', 'B', 0),
        ('pa_name3', '65s', '/xff' * 64),
        ('pa_name_len4', 'B', 0),
        ('pa_name4', '65s', '/xff' * 64),
    )

    def get_pa_name(self, ch):
        name = u''
        for i in range(getattr(self, 'pa_name_len%s' % ch) / 4):
            four_bytes = getattr(self, 'pa_name%s' % ch)[0 + i * 4:4 * (i + 1)]
            name += unichr(int(four_bytes, 16))
        return name

    def set_pa_name(self, name, ch):
        uni_len = len(name)
        assert uni_len * 4 < 64
        name = unicode(name)
        pa_name = ''.join(['%04x' % ord(uc) for uc in name])
        setattr(self, 'pa_name%s' % ch, pa_name)
        setattr(self, 'pa_name_len%s' % ch, uni_len * 4)

    def set_cellphones(self, phones):
        for i, p in enumerate(phones):
            setattr(self, 'phone_mode%s' % (i + 1), p['mode'])
            setattr(self, 'phone%s' % (i + 1), str(p['number']))
        self.activated_phone_count = len(phones)

    def get_cellphones(self):
        phones = []
        for i in range(1, self.activated_phone_count):
            phones.append({
                'mode': getattr(self, 'phone_mode%s' % i),
                'number': getattr(self, 'phone%s' % i)
            })
        return phones

    def pack_hdr(self):
        if not self.year:
            d = datetime.datetime.now()
            for k in ('year', 'month', 'day', 'hour', 'minute', 'second'):
                setattr(self, k, getattr(d, k))
        return super(DeviceFunction, self).pack_hdr()

    def load_from_dc(self, dc):
        self.relay_duration = dc['relay_duration']
        self.set_cellphones(dc.cellphones)
        for pa in dc['pa']:
            self.set_pa_name(pa['name'], pa['no'])
        return dc

    def apply_to_dc(self, dc):
        dc['relay_duration'] = self.relay_duration
        dc['cellphones'] = self.get_cellphones()
        for pa in dc['pa']:
            pa['name'] = self.get_pa_name(pa['no'])
            pa.save()
        return dc
