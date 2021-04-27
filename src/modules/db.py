import json
import redis
import logging

import modules.ipchk as ipchk # local module

def dbRedis(results, config, reader):
    try:
        dbred = redis.Redis(host=config['host'], port=config['port'], password=config['passwd'],db=config['db'], decode_responses=True)
    except Exception as e:
        print(e)
        return False

    for result in results:
        if result['enable'] and result['status'] == 'OK':
            for ip in result['ips']:
                location =ipchk.geoip2Search(reader, ip)
                json_str = json.dumps({'name': result['name'], 'date': result['date'], 'location': location})
                dbred.set(ip, json_str)

    dbred.close()
    return True



def dbStore(results, config):
    logging.info('[START] write to database ...')
    reader = ipchk.geoip2Load()

    if config['type'] == 'redis':
        res = dbRedis(results, config, reader)
    else:
        logging.warning('Sorry %s is not implemented yet.' % config['type'])

    ipchk.geoip2Close(reader)

    logging.info('[END] write to database')
