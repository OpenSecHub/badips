#!/bin/env python3
# coding:utf-8

import os
import re
import sys
import json
import logging
from datetime import datetime

import yaml  # pip3 install pyyaml
import urllib3

from modules.db import dbStore           # local module
from modules.summary import printSummary # local module




def readConfig():
    with open('conf/config.yml', encoding='utf-8', mode='r') as fp:
        content = fp.read()
        config = yaml.load(content, Loader=yaml.FullLoader)

    return config


def bodyProc(body, source):

    # remove comments(use regex)
    if 'comment' in source:
        comment = source['comment']
        if 'pattern_str' in comment:
            pattern = comment['pattern_str']
            if pattern:
                pattern = str(comment['pattern_str'])
                body = re.sub(pattern, '', body, flags=re.MULTILINE)

    # get target data(use regex)
    data_pattern = source['data']['pattern_str']
    data_index = source['data']['pattern_index']
    pattern = re.compile(data_pattern)

    lines = body.split('\n')
    count = 0
    ips = []
    for line in lines:
        line = line.strip()
        # skip empty line
        if line != '':
            m = pattern.search(line)
            if m:
                ip = m.group(data_index)
                ips.append(ip.strip())
                count = count + 1

    return count, ips

def httpRequest(http, source):

    url = source['url']
    referer = 'https://www.google.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': referer,
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Connection': 'close',
        'TE': 'Trailers'
    }
    result = {
        'name': source['name'],
        'enable': True,
        'status': 'OK',
        'message': 'success',
        'date': '-',
        'count': '-'
    }

    try:
        resp = http.request('GET', url, headers=headers, retries=1)
    except Exception as e:
        ex = sys.exc_info()
        result['status'] = 'NG'
        result['message'] = ex[1]
        print(e)
        return result

    # respone code
    if resp.status != 200:
        result['status'] = 'NG'
        result['message'] = 'website return code %d' % resp.status
        return result

    # read body, https://urllib3.readthedocs.io/en/latest/reference/urllib3.response.html
    resp.read(decode_content=True, cache_content=True)
    # byte to string
    body = resp.data.decode('utf-8','ignore')

    # get source update date
    if source['date']:
        if source['date']['location'] == 'HEADER':
            if 'field' in source['date']:
                field = source['date']['field']
                result['date'] = resp.headers[field]
        else: # BODY
            if 'pattern_str' in source['date']:
                pattern = source['date']['pattern_str']
                m = re.search(pattern, body, flags=0)
                index = 0
                if 'pattern_index' in source['date'] and m:
                    index = source['date']['pattern_index']
                    result['date'] = m.group(index)

    # analysis
    result['count'], result['ips'] = bodyProc(body, source)
    return result


def httpManager(proxy):

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    urllib3.disable_warnings(urllib3.exceptions.InsecurePlatformWarning)

    retries = urllib3.Retry(connect=3, read=5, redirect=3)
    logging.info('proxy policy: %s' % proxy['policy'])

    if proxy['policy'] == 'ALL':
        proxyMgr = urllib3.ProxyManager(proxy_url=proxy['url'], retries=retries)
        mgr = {'first': proxyMgr, 'second': None}
    elif  proxy['policy'] == 'NO':
        httpMgr = urllib3.PoolManager(retries=retries)
        mgr = {'first': httpMgr, 'second': None}
    else: # TRY
        proxyMgr = urllib3.ProxyManager(proxy_url=proxy['url'], retries=retries)
        httpMgr = urllib3.PoolManager(retries=retries)
        mgr = {'first': httpMgr, 'second': proxyMgr}

    return mgr


def cralwer(http, sources):

    results = []

    for source in sources:
        source = source['source']
        # the source is disable
        if source['status'] == 'DISABLE':
            result = {'name': source['name'], 'enable': False}
            logging.warning('source [%s] disabled' % source['name'])
            results.append(result)
            continue
        else:
            logging.info('start source [%s] ...' % source['name'])
            result = httpRequest(http['first'], source)
            if result['status'] != 'OK' and http['second']:
                logging.warning('restart via proxy source [%s] ...' % source['name'])
                result = httpRequest(http['second'], source)
            logging.info('end source [%s]' % (source['name']))
            results.append(result)

    return results


def logSetting():
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    LOG_FORMAT  = "[%(asctime)s][%(levelname)s] %(message)s"
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)


if __name__ == '__main__':
    logSetting()
    config = readConfig()
    http = httpManager(config['proxy'])

    # get IPs
    results = cralwer(http, config['sources'])

    # write IPs to datebase
    dbStore(results, config['database'])

    # print summary
    printSummary(results)
