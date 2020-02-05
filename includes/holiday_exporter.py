#!/usr/bin/python3

import sys
import yaml
import time
import holidays
from pathlib import Path
from datetime import date, datetime
from prometheus_client import Gauge, start_http_server


'''
Example of the configuration file:
---
main:
 port: 9110

holidays:
  - country: CA
    province: ON
  - country: US
    state: CA
'''

if __name__ == '__main__':

    if len(sys.argv) < 2:
        file_path = Path('/etc/holiday_exporter.yaml')
    else:
        file_path = Path(sys.argv[1])

    if not file_path.exists():
        print('Configuration file "{}" does not exists.'.format(str(file_path)))
        sys.exit(1)
    with file_path.open('r') as stream:
        config = yaml.load(stream, Loader=yaml.SafeLoader)

    g_is_holiday = Gauge('is_holiday', 'Boolean value if today is a statutory holiday', ['country', 'state', 'province'])
    g_is_dst = Gauge('is_daylight_saving_time', 'Boolean value if today is local daylight saving time' )

    try:
        start_http_server(port=config['main']['port'], addr='0.0.0.0')
    except OSError as e:
        print('Error starting server: %s' %e)
        sys.exit(200)

    while True:
        now = datetime.now()
        g_is_dst.set(int(time.localtime().tm_isdst))

        if 'custom_holidays' in config:
            is_holiday = 0
            for custom_holiday in config['custom_holidays']:
                isodate = custom_holiday['date'].upper().format(YYYY=now.year, MM='%02d'%now.month)
                if date.fromisoformat(isodate) == date.today():
                    is_holiday = 1
                    break
            g_is_holiday.labels(country = 'Custom', state = 'Custom', province = 'Custom').set(is_holiday)
        for c in config['holidays']:
            country = c['country']
            prov = str(c['province']) if 'province' in c.keys() else None
            state = str(c['state']) if 'state' in c.keys() else None
            current_holidays = holidays.CountryHoliday(country, prov=prov, state=state)
            is_holiday = int(now in current_holidays)
            g_is_holiday.labels(country = country, state = state, province = prov).set(is_holiday)
        # If hour is less than 22, then sleep for 1 hour
        if now.hour < 22:
            time.sleep(60 * 60)
        # If hour is less than 23, then sleep for 30 minutes
        elif now.hour < 23:
            time.sleep(60 * 30)
        # If time less than 23:40, the sleep for 5 minutes
        elif now.minute < 40:
            time.sleep(60 * 5)
        # If time less than 23:50, the sleep for 1 minute
        elif now.minute < 50:
            time.sleep(60 * 1)
        else:
            # If time more than 23:50, the sleep for 1 second
            time.sleep(1)
