# -*- coding: utf-8 -*-
import os

import sys
import xlrd

# excel files path
hosts = xlrd.open_workbook('/home/zhuangjy/Documents/work/computer.xlsx').sheets()[0]
mysqls = xlrd.open_workbook('/home/zhuangjy/Documents/work/computer.xlsx').sheets()[1]


def find(ip=None):
    num = hosts.nrows
    results = []
    print 'ip\tusername\tpassword\tport'
    for i in range(1, num):
        if ip is None or str(ip) in hosts.row_values(i)[0]:
            row = {'ip': str(hosts.row_values(i)[0]),
                   'name': str(hosts.row_values(i)[3]),
                   'pass': str(hosts.row_values(i)[4]),
                   'port': str(hosts.row_values(i)[6])}
            results.append(row)
    for row in results:
        if row is not None:
            print '{ip}\t{user}\t{password}\t{port}'.format(ip=row.get('ip'), user=row.get('name'),
                                                            password=row.get('pass'), port=row.get('port'))


def go(ip=None):
    num = hosts.nrows
    results = []
    password, username, port = None, None, None
    for i in range(1, num):
        if ip is None or ip in str(hosts.row_values(i)[0]):
            results.append(hosts.row_values(i)[0])
            username = hosts.row_values(i)[3]
            password = str(hosts.row_values(i)[4])
            port = str(hosts.row_values(i)[6])
    else:
        if len(results) > 1:
            print 'too many ips,please refer a distinct ip.'
            for res in results:
                print res
        elif len(results) == 0:
            print "can't find target."
        else:
            password = '%d' % float(password) if password.endswith('.0') else password
            port = '%d' % float(port) if port.endswith('.0') else port
            cmd = "sshpass -p {password} ssh -p {port} {user}@{ip}".format(port=port, password=password,
                                                                           user=username, ip=results[0])
            print cmd
            os.system(cmd)


def mysql(ip=None):
    num = mysqls.nrows
    results = []
    password, username, port = None, None, None
    for i in range(1, num):
        if ip is None or ip in str(mysqls.row_values(i)[0]):
            results.append(mysqls.row_values(i)[0])
            username = mysqls.row_values(i)[3]
            password = str(mysqls.row_values(i)[4])
            port = str(mysqls.row_values(i)[6])
    else:
        if len(results) > 1:
            print 'too many ips,please refer a distinct ip.'
            for res in results:
                print res
        elif len(results) == 0:
            print "can't find target."
        else:
            password = '%d' % float(password) if password.endswith('.0') else password
            port = '%d' % float(port) if port.endswith('.0') else port
            cmd = "mycli -h {ip} -P {port} -u {user} -p {password}".format(port=port, password=password, user=username,
                                                                           ip=results[0])
            print cmd
            os.system(cmd)


if __name__ == '__main__':
    argv_len = len(sys.argv) - 1
    if argv_len < 1 or argv_len > 2:
        print 'invalid argv!'
    elif argv_len == 1:
        go(sys.argv[1])
    else:
        method = sys.argv[1]
        result = {
            'go': lambda x: go(x),
            'find': lambda x: find(x),
            'mysql': lambda x: mysql(x)
        }[method](sys.argv[2])
