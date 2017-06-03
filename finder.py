# -*- coding: utf-8 -*-
import os

import sys
import xlrd

# excel files path
table = xlrd.open_workbook('/home/zhuangjy/Documents/work/computer.xlsx').sheets()[0]


def find(ip=None):
    num = table.nrows
    results = []
    print 'ip\tusername\tpassword\tport'
    for i in range(1, num):
        if ip is None or str(ip) in table.row_values(i)[0]:
            row = {'ip': str(table.row_values(i)[0]),
                   'name': str(table.row_values(i)[3]),
                   'pass': str(table.row_values(i)[4]),
                   'port': str(table.row_values(i)[6])}
            results.append(row)
    for row in results:
        if row is not None:
            print '{ip}\t{user}\t{password}\t{port}'.format(ip=row.get('ip'), user=row.get('name'),
                                                            password=row.get('pass'), port=row.get('port'))


def go(ip=None):
    print ip
    ip = str(ip)
    num = table.nrows
    results = []
    password, username, port = None, None, None
    for i in range(1, num):
        if ip is None or ip in str(table.row_values(i)[0]):
            results.append(table.row_values(i)[0])
            username = table.row_values(i)[3]
            password = str(table.row_values(i)[4])
            port = str(table.row_values(i)[6])
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
            print "sshpass -p {password} ssh -p {port} {user}@{ip}".format(port=port, password=password,
                                                                           user=username, ip=results[0])
            os.system("sshpass -p {password} ssh -p {port} {user}@{ip}"
                      .format(port=port, password=password, user=username, ip=results[0]))


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
            'find': lambda x: find(x)
        }[method](sys.argv[2])
