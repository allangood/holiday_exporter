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

Here is a quick how to use this exporter:

Create an alert rule in Prometheus:
```
- alert: Is_Holiday
  expr: is_holiday > 0
  labels:
    severity: warning
```

And create an inhibit_rules in Alertmanager:
```
- source_match:
    alertname: Is_Holiday
  target_match:
    severity: warning
  equal:
  - severity
```

With this configuration, any alert with a label "severity = warning" will be inhibited by the holiday exporter.
You can go beyond and put some work hours as well:
```
- alert: Is_Work_Hours
  expr:
    is_holiday > 0
    or
    hour() - (scalar(is_daylight_saving_time) + 6) < 8
    or
    day_of_week() == 0
    or
    day_of_week() == 6
  labels:
    severity: warning
```
In this rule, my timezone is -6 and it will be triggered if is a holiday, or current hour is > 17 and < 8, or day of week is Saturday or Sunday.
When this alert fires, it will inhibit any rule with a label "severity = warning".

# How to run:
```
git clone https://github.com/allangood/holiday_exporter.git
cd holiday_exporter
vi includes/holiday_exporter.yaml
docker build -t holiday_exporter .
docker run -d -p 9137:9137 --name holiday holiday_exporter
```
Or you can specify your own configuration file:
Create your YAML file:
```
main:
 port: 9137

# Countries, states and provinces accordingly to https://pypi.org/project/holidays
holidays:
  - country: "CA"
    province: "ON"
  - country: "US"
    state: "CA"
```
Run the holiday_exporter container:
```
docker run -d -p 9137:9137 -v my_config_file.yaml:/etc/holiday_exporter.yaml --restart unless-stopped --name holiday_exporter allangood/holiday_exporter
```

Version 1.1 and later of this exporter supports custom holidays.
You just have to add a section like this to your configuration file:
```
custom_holidays:
  # Dates must be in ISO format: YYYY-MM-DD
  # Use temaplte {YYYY} for year and {MM} for month
  - date: "{YYYY}-01-01"
    description: "Some event that happens every year"
  - date: "{YYYY}-{MM}-01"
    description: "Some event that repeats every month at specific day"
  - date: "2019-12-17"
    description: "Some day this year only"
```

Then configure Prometheus to scrape your server:
```
- job_name: holiday_exporter
  scrape_interval: 10s
  scrape_timeout: 5s
  metrics_path: "/"
  static_configs:
  - targets:
    - <your_server_address>:9137
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
is_holiday{country="Custom",province="Custom",state="Custom"} 1.0
# HELP is_daylightsavings Boolean value if today is local daylight saving time
# TYPE is_daylightsavings gauge
is_daylight_savings 0.0
```

# Alternatives
[This is another solution](https://github.com/OneMainF/time-range-exporter)

# Author:
 Allan Good
