#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import socket
import datetime
import psutil
import json
import time


def bytes2human(n):
    symbols = ('K','M','G','T','P','E','Z','Y')
    prefix = {}
    for i,s in enumerate(symbols):
        prefix[s] = 1 << (i+1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' %(value,s)
    return '%sB' %n

def get_cpu_info():
    cpu_count = psutil.cpu_count()
    cpu_percent = psutil.cpu_percent(interval=1)
    return dict(cpu_count=cpu_count,cpu_percent=cpu_percent)

def get_memory_info():
    virtual_mem = psutil.virtual_memory()

    mem_total = bytes2human(virtual_mem.total)
    mem_percent = virtual_mem.percent
    # mem_free = bytes2human(virtual_mem.free + virtual_mem.buffers + virtual_mem.cached)
    mem_used = bytes2human(virtual_mem.total * virtual_mem.percent)

    return dict(mem_total=mem_total,mem_percent=mem_percent,
                # mem_free=mem_free,
                mem_used=mem_used)

def get_disk_info():
    disk_usage = psutil.disk_usage('/')

    disk_total = bytes2human(disk_usage.total)
    disk_percent = disk_usage.percent
    disk_free = bytes2human(disk_usage.free)
    disk_used = bytes2human(disk_usage.used)

    return dict(disk_total=disk_total,disk_percent=disk_percent,disk_free=disk_free,disk_used=disk_used)
def get_vod_info():
    vod_usage = psutil.disk_usage('d:/')

    vod_total = bytes2human(vod_usage.total)
    vod_percent = vod_usage.percent
    vod_free = bytes2human(vod_usage.free)
    vod_used = bytes2human(vod_usage.used)

    return dict(vod_total=vod_total,vod_percent=vod_percent,vod_free=vod_free,vod_used=vod_used)

def get_boot_info():
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')
    run_time = datetime.datetime.fromtimestamp(time.time()-psutil.boot_time()).strftime('%H:%M:%S')
    boot_usage = psutil.disk_usage('/boot')

    boot_total = bytes2human(boot_usage.total)
    boot_percent = boot_usage.percent
    boot_free = bytes2human(boot_usage.free)
    boot_used = bytes2human(boot_usage.used)
    return dict(run_time=run_time,boot_time=boot_time,boot_total=boot_total,boot_percent=boot_percent,boot_free=boot_free,boot_used=boot_used)

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    # if not ip:
    #     if_addrs = psutil.net_if_addrs()
    #     i = 0
    #     while 1:
    #         if_addrs_1 = if_addrs.items()[i][1][0]
    #         if if_addrs_1:
    #             if if_addrs_1.address == '127.0.0.1':
    #                 i += 1
    #             else:
    #                 ip = if_addrs_1
    #                 return ip
    #         else:
    #             return NULL

    return dict(ip=ip)

def get_net_io():
    net_io_counters = psutil.net_io_counters()
    # net_sent = bytes2human(net_io_counters.bytes_sent)
    net_sent = net_io_counters.bytes_sent
    # net_recv = bytes2human(net_io_counters.bytes_recv)
    net_recv = net_io_counters.bytes_recv
    net_packets_sent = net_io_counters.packets_sent
    net_packets_recv = net_io_counters.packets_recv
    net_errin = net_io_counters.errin
    net_errout = net_io_counters.errout
    net_dropin = net_io_counters.dropin
    net_dropout = net_io_counters.dropout
    now_time = datetime.datetime.now().strftime('%H:%M:%S')
    now_time_2 = datetime.datetime.now() + datetime.timedelta(seconds=3)
    now_time_3 = (datetime.datetime.now() + datetime.timedelta(seconds=3)).strftime('%H:%M:%S')

    return dict(net_sent=net_sent,net_recv=net_recv,net_packets_sent=net_packets_sent,net_packets_recv=net_packets_recv,net_errin=net_errin,
                net_errout=net_errout,net_dropin=net_dropin,net_dropout=net_dropout,now_time=now_time,now_time_3=now_time_3)



def collect_monitor_data():
    data = {}
    data.update(get_boot_info())
    data.update(get_cpu_info())
    data.update(get_memory_info())
    data.update(get_disk_info())
    data.update(get_host_ip())
    data.update(get_net_io())
    data.update(get_vod_info())
    # data = json.dumps(data)
    return data
