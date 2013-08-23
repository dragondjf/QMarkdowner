# -*- coding: utf-8 -*-
# settings in here can be modified by user after deployment
default_ifname = 'eth0'
default_vlan_ifname = 'eth0'
update_task_max = 5  # max number of running firmware update tasks
enable_wave_display = True
FFT_SIZE = 1024

log = {
    'log_max_bytes': 5 * 1024 * 1024,  # 5M
    'backup_count': 10,
    'log_path': {
        # logger of running server; DONOT change the name 'logger'
        'logger': 'log/files/server.log',
        # logger of user behavior
        'user_logger': 'log/files/user.log'
    }
}

#算法缺省参数设置
pa_alg = {
    'ifpms': {
        #斜率校正判定
        'fiberbreak_k': [{
            'break_time': 2,  # 短纤响应时间
            'fiber_break': 200  # 斜率校正断纤，特征值data9超过此值表示断纤
        }],
        #平均校正判定
        'fiberbreak_davg': [{
            'break_time': 2,  # 短纤响应时间
            'fiber_break': 60,  # 一个点的断纤平均值davg门限
        }],
        #标准周界
        'ifpms_normal': [{
            'sensitivity': 80,  # 对应的f值进行比较的灵敏度门限
            'responsetime': 3,  # 响应时间
            'ratio': 2  # 响应时间内超过灵敏度的百分比门限
        }],
        #自适应周界
        'ifpms_adaptation': [{
            'sensitivity': 80,  # 对应的f值进行比较的灵敏度门限
            'responsetime': 3,  # 响应时间
            'ratio': 2  # 响应时间内超过灵敏度的百分比门限
        }],
        #均方周界
        'ifpms_meansquare': [{
            'sensitivity': 80,  # 对应的f值进行比较的灵敏度门限
            'responsetime': 3,  # 响应时间
            'ratio': 2  # 响应时间内超过灵敏度的百分比门限
        }]
    },
    'gsd': {
        #斜率校正判定
        'fiberbreak_k': [{
            'break_time': 2,  # 短纤响应时间
            'fiber_break': 200  # 斜率校正断纤，特征值data9超过此值表示断纤
        }],
        #平均校正判定
        'fiberbreak_davg': [{
            'break_time': 2,  # 短纤响应时间
            'fiber_break': 60,  # 一个点的断纤平均值davg门限
        }],
        #标准地波
        'gsd_normal': [{
            'responsetime_s': 6,    # 短时间范围：单位为秒，乘以单位点数则为瞬间点数
            'responsetime_l': 300,    # 长时间范围：单位为秒，乘以单位点数则为瞬间点数
            'sensitivity': 40,  # 相对特征值data0进行比较的
            'ratio': 80   # 长时间统计的预警率百分比门限
        }],
        'gsd_adaptation': [{
            'responsetime_s': 6,    # 短时间范围：单位为秒，乘以单位点数则为瞬间点数
            'responsetime_l': 300,    # 长时间范围：单位为秒，乘以单位点数则为瞬间点数
            'sensitivity': 40,  # 相对特征值data0进行比较的
            'ratio': 80   # 长时间统计的预警率百分比门限
        }],
        #爆破算法
        'gsd_blast': [{
            'responsetime': 1,  # 爆破响应时间
            'absolutef': 5000,  # 爆破绝对能量值门限
            'relatef': 40,  # 爆破相对值门限
            'blast_num': 2  # 爆破多点复核个数
        }]
    }
}


default_alg = {
    'ifpms': {
        'defence_start': 0,
        'defence_end': 0,
        'mode': 2,
        'fiber_workmode': 'fiberbreak_k',
        'fiberbreak_k': pa_alg['ifpms']['fiberbreak_k'],
        'fiberbreak_davg': pa_alg['ifpms']['fiberbreak_davg'],

        'alarm_workmode': 'ifpms_adaptation',
        'ifpms_normal': pa_alg['ifpms']['ifpms_normal'],
        'ifpms_adaptation': pa_alg['ifpms']['ifpms_adaptation'],
        'ifpms_meansquare': pa_alg['ifpms']['ifpms_meansquare'],
        'defence_start': 0,
        'defence_end': 0,
        'fkeys': ['f0']
    },
    'gsd': {
        'defence_start': 0,
        'defence_end': 0,
        'mode': 2,
        'fiber_workmode': 'fiberbreak_k',
        'fiberbreak_k': pa_alg['gsd']['fiberbreak_k'],
        'fiberbreak_davg': pa_alg['gsd']['fiberbreak_davg'],

        'alarm_workmode': 'gsd_adaptation',
        'gsd_normal': pa_alg['gsd']['gsd_normal'],
        'gsd_adaptation': pa_alg['gsd']['gsd_adaptation'],
        'gsd_blast': pa_alg['gsd']['gsd_blast'],

        'fkeys': ['f1']
    }
}


#预处理窗口
alg_win = {
    'f0': {'begin': 2, 'end': 30, 'noise': 15, 'magic': 1},
    'f1': {'begin': 2, 'end': 30, 'noise': 0, 'magic': 1},
    'f2': {'begin': 30, 'end': 510, 'noise': 0, 'magic': 1},
    'f3': {'begin': 2, 'end': 50, 'noise': 0, 'magic': 1},
    'f4': {'begin': 2, 'end': 60, 'noise': 0, 'magic': 1},
    'f5': {'begin': 2, 'end': 70, 'noise': 0, 'magic': 1},
    'f6': {'begin': 2, 'end': 80, 'noise': 0, 'magic': 1},
    'f7': {'begin': 2, 'end': 90, 'noise': 0, 'magic': 1}
}

DSIZE = 4096  # 数据缓冲区大小

fiberbreak_history = 1500

magic = 20


#均方周界算法中开启度范围
mean_min = 1000  # 默认开启度最小值
mean_max = 3000  # 默认开启度最大值
mean_magic = 4  # 进行均方运算的开启度比例限定因子
mean_range_magic = 10  # 进行均方运算的开启度范围限定因子
mean_points = 10  # 特征运算所用的点数

# zzh add
tcp_server = {
    'port': 6002,
    'timeout': 5,  # second
    'get_socket_fd': 3
}

udp_client = {
    'server_port': 6004,
    'timeout': 2  # seconds
}

wav_path = 'static/wavs/'

wav_days = 10  # 音频保留天数

default_tpl = {
    'webservice': {
        'enabled': False,
        'urls': None
    },
    'video': {
        'enabled': False,
        'url': None
    },
    'sound': {
        'enabled': True,
        'name': "alarm.wav"
    },
    'relay': {
        'enabled': True,
        'relay_duration': 3
    },
    'led': True,
    'cellphones': {
        'enabled': False,
        'number': None
    },
    'warning_mode': ["warning", 'blast']
}

sms_set_template = {
    "dev_id": "/dev/ttyUSB0",
    "baud_rate": 9600
}

web_server_port = 9000

# zzh add over
