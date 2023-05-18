# !/usr/bin/env python
# coding=utf-8
#
# Generate a list of dnsmasq rules with ipset for gfwlist
#
# Copyright (C) 2014 http://www.shuyz.com
# Ref https://code.google.com/p/autoproxy-gfwlist/wiki/Rules
# https://gist.github.com/lanceliao/85cd3fcf1303dba2498c

import urllib3
import re
import os
import datetime
import base64
import shutil

mydnsip = '127.0.0.1'
mydnsport = '5153'

# the url of gfwlist
baseurl = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'
# match comments/title/whitelist/ip address
comment_pattern = '^\!|\[|^@@|^\d+\.\d+\.\d+\.\d+'
domain_pattern = '([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*'
# do not write to router internal flash directly

fs = open("./gfwlist.conf", "w")
fs.write('# gfw list ipset rules for dnsmasq\n')
fs.write('# updated on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
fs.write('#\n')

http = urllib3.PoolManager()

print('fetching list...')
content = http.request("GET", baseurl).data
content = base64.b64decode(content).decode("utf-8")

# write the decoded content to file then read line by line
tfs = open("./gfwlist.txt", 'w')
tfs.write(content)
tfs.close()
tfs = open("./gfwlist.txt", 'r')

print('page content fetched, analysis...')

# remember all blocked domains, in case of duplicate records
domainlist = []

for line in tfs.readlines():
    if re.findall(comment_pattern, line):
        print('this is a comment line: ' + line)
    # fs.write('#' + line)
    else:
        domain = re.findall(domain_pattern, line)
        if domain:
            try:
                found = domainlist.index(domain[0])
                print(domain[0] + ' exists.')
            except ValueError:
                print('saving ' + domain[0])
                domainlist.append(domain[0])
                fs.write('server=/.%s/%s#%s\n' % (domain[0], mydnsip, mydnsport))
                # fs.write('ipset=/.%s/gfwlist\n' % domain[0])
        else:
            print('no valid domain in this line: ' + line)

tfs.close()
fs.close()
