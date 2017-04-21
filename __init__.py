# -*- coding: utf-8 -*-
import os

import xlrd
import sys
import fire


class Finder(object):
    table = xlrd.open_workbook('/home/zhuangjy/Documents/work/computer.xlsx').sheets()[0]

    @staticmethod
    def find(ip=None):
        num = Finder.table.nrows
        results = []
        print 'ip\tusername\tpassword\tport'
        for i in range(1, num):
            if ip is None or str(ip) in Finder.table.row_values(i)[0]:
                row = {'ip': str(Finder.table.row_values(i)[0]),
                       'name': str(Finder.table.row_values(i)[3]),
                       'pass': str(Finder.table.row_values(i)[4]),
                       'port': str(Finder.table.row_values(i)[6])}
                results.append(row)
        for row in results:
            if row is not None:
                print '{ip}\t{user}\t{password}\t{port}'.format(ip=row.get('ip'), user=row.get('name'),
                                                                password=row.get('pass'), port=row.get('port'))

    @staticmethod
    def go(ip=None):
        num = Finder.table.nrows
        results = []
        password, username = None, None
        for i in range(1, num):
            if ip is None or str(ip) in Finder.table.row_values(i)[0]:
                results.append(Finder.table.row_values(i)[0])
                username = Finder.table.row_values(i)[3]
                password = str(Finder.table.row_values(i)[4])
        else:
            if len(results) > 1:
                print 'too many ips,please refer a distinct ip.'
                for res in results:
                    print res
            elif len(results) == 0:
                print "can't find target."
            else:
                password = '%d' % float(password) if password.endswith('.0') else password
                print "sshpass -p {password} ssh {user}@{ip}".format(password=password, user=username, ip=results[0])
                os.system("sshpass -p {password} ssh {user}@{ip}"
                          .format(password=password, user=username, ip=results[0]))


if __name__ == '__main__':
    fire.Fire(Finder)
