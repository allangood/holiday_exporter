# holiday_exporter
A simple python exporter that exports holidays to Prometheus to help with Alerting.

# The Prooblem
I want to fire some alerts on workdays only, but Prometheus/Alertmanager doesnt support it!
[You are not alone](https://github.com/prometheus/alertmanager/issues/876)

# Solution #1
Create a recording rule on Prometheus with all holidays.
This can be really complicated with non fixed holidays, like Easter.
[Like this sugestion](https://gist.github.com/roidelapluie/8c67e9c8fb18b310a4a90cb92a23056b)

# Solution #2
Use this exporter and include it inside your expression!

# How to run:
```
git clone https://github.com/allangood/holiday_exporter.git
cd holiday_exporter
vi includes/holiday_exporter.yaml
docker build -t holiday_exporter .
docker run -d -p 9110:9110 --name holiday holiday_exporter
```
Or you can specify your own configuration file:
```
docker run -d -p 9110:9110 -v my_config_file.yaml:/etc/holiday_exporter.yaml --name holiday holiday_exporter
```

Then configure Prometheus to scrape your server:
```
- job_name: is_holiday
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


# Alternatives
[This is another solution](https://github.com/OneMainF/time-range-exporter)

# Author:
 Allan Good
