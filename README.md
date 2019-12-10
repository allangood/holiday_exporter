# holiday_exporter
A simple python exporter that exports holidays to Prometheus to help with Alerting.
This exporter uses the awesome [python-holidays library](https://pypi.org/project/holidays/)

# The Problem
I want to fire some alerts on workdays only, but Prometheus/Alertmanager doesnt support it!
[You are not alone](https://github.com/prometheus/alertmanager/issues/876)

# Solution #1
Create a recording rule on Prometheus with all holidays.
This can be really complicated with non fixed holidays, like Easter.
[Implementation sugestion](https://gist.github.com/roidelapluie/8c67e9c8fb18b310a4a90cb92a23056b)

# Solution #2
Use this exporter and include it in your expression!

# How to run:
```
git clone https://github.com/allangood/holiday_exporter.git
cd holiday_exporter
vi includes/holiday_exporter.yaml
docker build -t holiday_exporter .
docker run -d -p 9110:9110 --name holiday holiday_exporter
```
Or you can specify your own configuration file:
Create your YAML file:
```
main:
 port: 9110

# Countries, states and provinces accordingly to https://pypi.org/project/holidays
holidays:
  - country: "CA"
    province: "ON"
  - country: "US"
    state: "CA"
```
Then use with your container:
```
docker run -d -p 9110:9110 -v my_config_file.yaml:/etc/holiday_exporter.yaml --restart unless-stopped --name holiday_exporter holiday_exporter
```

Then configure Prometheus to scrape your server:
```
- job_name: holiday_exporter
  scrape_interval: 10s
  scrape_timeout: 5s
  metrics_path: "/"
  static_configs:
  - targets:
    - <your_server_address>:9110
```

Metrics exposed:

|       Metric       |        Possible Values       |
|:------------------:|:----------------------------:|
|     is_holiday     | 1 =&gt; True / 0 =&gt; False |
| is_daylight_saving | 1 =&gt; True / 0 =&gt; False |

# Sample
```
# HELP is_holiday Boolean value if today is a statutory holiday
# TYPE is_holiday gauge
is_holiday{country="CA",province="ON",state="None"} 0.0
is_holiday{country="US",province="None",state="CA"} 0.0
# HELP is_daylightsavings Boolean value if today is local daylight saving time
# TYPE is_daylightsavings gauge
is_daylight_savings 0.0
```

# Alternatives
[This is another solution](https://github.com/OneMainF/time-range-exporter)

# Author:
 Allan Good
