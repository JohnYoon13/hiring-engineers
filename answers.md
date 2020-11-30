# Assignment overview:
1. [Collecting metrics](#collecting-metrics)
2. [Visualizing data](#visualizing-data)
3. [Final question](#final-question)


# Collecting metrics

## Add tags in the Agent config file, and show us a screenshot of your host and its tags on the Host Map page in Datadog.
I implemented the following configurations in the **datadog.yaml** file (located in the directory, **/etc/datadog-agent**):
```yaml
tags:
  - environment:staging
  - name:real_madrid_fc
```
The following screenshot shows the corresponding results on the [Host Map](https://app.datadoghq.com/infrastructure/map?host=3376094498&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host):

![0tags](https://user-images.githubusercontent.com/35269716/100461321-a5cf8380-3096-11eb-9c6c-3cc74a873e91.png)

## Install a database on your machine (MongoDB, MySQL, or PostgreSQL), then install the respective Datadog integration for that database.
I implemented the following configurations in the **conf.yaml** file (located in the directory, **/etc/datadog-agent/conf.d/mysql.d**):
```yaml
init_config:
instances:
  - server: 127.0.0.1
    user: datadog
    pass: "tw"
    port: 3306
    options:
      replication: false
      galera_cluster: true
      extra_status_metrics: true
      extra_innodb_metrics: true
      extra_performance_metrics: true
      schema_size_metrics: false
      disable_innodb_metrics: false
``` 
The following screenshot shows the corresponding results on the ["MySQL - Overview" dashboard](https://app.datadoghq.com/dash/integration/12/mysql---overview):

![1mysql](https://user-images.githubusercontent.com/35269716/100461612-06f75700-3097-11eb-9439-443d2f6c3706.png)

## Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
I implemented the following python script in the **custom_my_metric.py** file (and placed it in the directory, **/etc/datadog-agent/checks.d**):
```python
import random
# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from new versions of the Agent...
    from datadog_checks.base import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version < 6.6.0
    from checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

class RandNumCheck(AgentCheck):
    def check(self, instance):
        self.gauge('random.zero.to.thousand', random.randint(0, 1000))
```

I implemented the following configurations in the **custom_my_metric.yaml** file (and placed it in the directory, **/etc/datadog-agent/conf.d**):
```yaml
init_config:
instances: [{}]
```
The following screenshot shows the corresponding results on the ["Custom Agent Check" dashboard](https://app.datadoghq.com/dashboard/8s7-dnz-iug?from_ts=1606406735824&live=true&to_ts=1606410335824):

![2check](https://user-images.githubusercontent.com/35269716/100461716-2c846080-3097-11eb-92b8-e4c26f832f99.png)

The following screenshot shows the corresponding results on a more detailed view of the ["Custom Agent Check" dashboard](https://app.datadoghq.com/dashboard/8s7-dnz-iug?from_ts=1606406735824&fullscreen_end_ts=1606413632270&fullscreen_paused=false&fullscreen_section=overview&fullscreen_start_ts=1606410032270&fullscreen_widget=7875338312458988&live=true&to_ts=1606410335824):

![3fullscreen](https://user-images.githubusercontent.com/35269716/100461758-373ef580-3097-11eb-8c8b-f04ecea31705.png)

## Change your check's collection interval so that it only submits the metric once every 45 seconds.
## Bonus Question: Can you change the collection interval without modifying the Python check file you created?
I updated the **custom_my_metric.yaml** file with the following:
```yaml
init_config:
instances:
  - min_collection_interval: 45
```

# Visualizing data:
## Utilize the Datadog API to create a Dashboard that contains:
* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.

I implemented and used the following python script in the **api_dashboards.py** file:
```python
from datadog import initialize, api

options = {
    'api_key': 'ba3b35b93da6244f4ae958f7ac5d7c1f',
    'app_key': '3fc17dab284e9136e4bcbcf1fcd31c797f50b3d6'
}

initialize(**options)

title = 'API Visualizations'
widgets = [

{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'random.zero.to.thousand{*}'}
        ],
        'title': 'Custom Metric'
    }
},

{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': "anomalies(mysql.performance.user_time{*}, 'basic', 2)"}
        ],
        'title': 'Anomalies function with database'
    }
}]

layout_type = 'ordered'
description = 'api visualizations'
is_read_only = True
notify_list = ['johnyoon13@gmail.com']
template_variables = [{
    'name': 'host1',
    'prefix': 'host',
    'default': 'my-host'
}]

saved_views = [{
    'name': 'Saved views for hostname 2',
    'template_variables': [{'name': 'host', 'value': '<HOSTNAME_2>'}]}
]

api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables,
                     template_variable_presets=saved_views)
```

The following screenshot shows the corresponding results on the ["API Visualizations" dashboard](https://app.datadoghq.com/dashboard/mzp-tt5-43z/api-visualizations?from_ts=1606425283791&live=true&to_ts=1606428883791):

![4api](https://user-images.githubusercontent.com/35269716/100461831-50e03d00-3097-11eb-8b6f-f89a3da69da4.png)

# Access the Dashboard from your Dashboard List in the UI:
## Set the Dashboards's timeframe to the past 5 minutes.
The following screenshot shows the process for setting the dashboard's timeframe to the past 5 minutes:

![5minutes](https://user-images.githubusercontent.com/35269716/100461890-66edfd80-3097-11eb-8147-857053c3e4f3.png)

## Take a snapshot of this graph and use the @ notation to send it to yourself.
The following screenshot shows the process for sending a snapshot to myself using the @ notation:

![6send](https://user-images.githubusercontent.com/35269716/100461919-73725600-3097-11eb-8cda-3db22c98b57b.png)

## Bonus Question: What is the Anomaly graph displaying?
The Datadog documentation states that the anomaly graph displays ["when a metric is behaving differently than it has in the past."](https://docs.datadoghq.com/monitors/monitor_types/anomaly/) A gray anomaly band highlights the deviation boundaries. Similarly, the graph uses a color system where orange indicates unusual values and blue indicates normal values. In this particular instance, the anomaly graph shows the **mysql.performance.user_time** metric using the "basic" algorithm. This algorithm works best with [metrics with no repeating seasonal pattern.](https://docs.datadoghq.com/monitors/monitor_types/anomaly/#anomaly-detection-algorithms) 

_________
# Final question
# Datadogpy: the Datadog Python Library
Datadogpy is a collection of tools that provides a layer of abstraction on top of:

* [Datadog's HTTP REST API](https://docs.datadoghq.com/api/v1/) 
* [Datadog's DogStatsD (Datadog Agent's metrics aggregation server)](https://docs.datadoghq.com/developers/dogstatsd/?tab=hostagent)

This abstraction provides an efficient and user-friendly interface for developers who plan on using Python to interact with Datadog. 

If you have experience with [Python](https://www.python.org/about/gettingstarted/), [Datadog](https://docs.datadoghq.com/), and [APIs](https://www.redhat.com/en/topics/api/what-are-application-programming-interfaces), the following information can help you install the **datadogpy** library. This guide will also demonstrate how to to set up and use the **datadogpy** library to access the Datadog API. Then you will see how to configure and apply the **datadogpy** library to use DogStatsD.

## Guide overview

1. [Installation](#installation)
2. [Datadog API: Configuration](#datadog-api-configuration)
3. [Datadog API: Usage](#datadog-api-usage)
4. [DogStatsD: Configuration](#dogstatsd-configuration)
5. [DogStatsD: Usage](#dogstatsd-usage)
6. [Best practices and next steps](#best-practices-and-next-steps)
7. [Acknowledgment](#acknowledgment)


## Installation
Prequisites for this library include: 
* [a Datadog account](https://www.datadoghq.com/free-datadog-trial/)
* [access to a Datadog project](https://docs.datadoghq.com/getting_started/)
* [Python](https://www.python.org/downloads/)
* [Python's package installer, pip](https://pypi.org/project/pip/)

In order to install the **datadogpy** library, run the following:

```
pip install datadog
```

Alternatively, you can also install the library directly from the source. First clone the repository:
```
git clone https://github.com/DataDog/datadogpy.git
```

Then enter the library's directory and run the following command:
```
python setup.py install
```

## Datadog API: Configuration

1. Create a new Python file. Then gain access to the necessary features with the following line:
```python
from datadog import initialize, api
```

2. Go to your Datadog account's settings page to get a [Datadog API key and application key](https://docs.datadoghq.com/account_management/api-app-keys/) through the following URL:
```
https://app.datadoghq.com/account/settings#api
```

3. Generate both keys through the settings page, which should look like the image below:

![7keys](https://user-images.githubusercontent.com/35269716/100520085-011e7600-316a-11eb-91ec-7e7739b94b2a.png)

4. Implement the following **options** configurations into your Python file:
```python
# insert your newly generated keys into their appropriate spots
options = {
    'api_key': '<YOUR_API_KEY>',
    'app_key': '<YOUR_APP_KEY>'
}
```

5. Finally, in order to run the initialize method, include the following line:
```python
initialize(**options)
```
The code so far should look like the following:
```python
from datadog import initialize, api

options = {
    'api_key': '<YOUR_API_KEY>',
    'app_key': '<YOUR_APP_KEY>'
}

initialize(**options)
``` 

## Datadog API: Usage
The **datadogpy** library can access the Datadog API for a wide range of Datadog products, from logs to dashboards to monitors. This guide will focus on how to delete a monitor. 

This stage will build on the configurations set up in the previous section.

1. Select the monitor you want to delete from the full list of your monitors found in the following URL:
```
https://app.datadoghq.com/monitors/manage
```

2. Open the detailed page of the monitor you want to delete. Save the monitor's identification number found under the **Properties** tab:

![8monitor](https://user-images.githubusercontent.com/35269716/100521105-a12ace00-316f-11eb-8ed7-0ea19dd30774.png)

3. Pass the monitor's identification number as the parameter for the following delete function:
```python
api.Monitor.delete(<MONITOR_ID>)
```

If other resources reference the monitor, then you might need to force delete the monitor. To do this, pass another parameter, **force**, with its value set to **True**:
```python
api.Monitor.delete(<MONITOR_ID>, force=True)
```

4. Run your Python script. Then confirm that it successfully deleted the monitor by once again reviewing the full list of your monitors:
```
https://app.datadoghq.com/monitors/manage
```

The following code shows all the components combined:
```python
from datadog import initialize, api

options = {
    'api_key': '<YOUR_API_KEY>',
    'app_key': '<YOUR_APP_KEY>'
}

initialize(**options)

# Delete a monitor
api.Monitor.delete(<MONITOR_ID>)

# Force delete a monitor to override warnings
# api.Monitor.delete(<MONITOR_ID>, force=True)
```

## DogStatsD: Configuration
1. Open your **datadog.yaml** file. Find the **DogStatsD Configuration** section. Uncomment the line with **"use_dogstatsd: true"** and the line with ""**dogstatsd_port: 8125"** so that the lines match the following:
```yaml
#############################
## DogStatsD Configuration ##
#############################

## @param use_dogstatsd - boolean - optional - default: true
## Set this option to false to disable the Agent DogStatsD server.
#
use_dogstatsd: true

## @param dogstatsd_port - integer - optional - default: 8125
## Override the Agent DogStatsD port.
## Note: Make sure your client is sending to the same UDP port.
#
dogstatsd_port: 8125
```

2. Create a new Python file. Then gain access to the necessary features with the following line:
```python
from datadog import initialize, statsd
```

3. Implement the following **options** configurations into your Python file:
```python
# DogStatsD listens to UDP port 8125 on default
options = {
    'statsd_host':'127.0.0.1',
    'statsd_port':8125
}
```

However, if you prefer to use [UDS](https://docs.datadoghq.com/developers/dogstatsd/unix_socket?tab=host), then use the following **options** configurations:
```python
options = {
    'statsd_socket_path' : PATH_TO_SOCKET
}
```

4. Finally, in order to run the initialize method, include the following line:
```python
initialize(**options)
```

The code so far should look like the following:
```python
from datadog import initialize, statsd

options = {
    'statsd_host':'127.0.0.1',
    'statsd_port':8125
}

# alternative option for UDS
# options = {
#     'statsd_socket_path' : PATH_TO_SOCKET
# }

initialize(**options)
``` 

## DogStatsD: Usage
The Datadog documentation states that ["DogStatsD](https://docs.datadoghq.com/developers/dogstatsd/?tab=hostagent) accepts custom metrics, events, and service checks over UDP and periodically aggregates and forwards them to Datadog." In order to demonstrate features from **datadogpy** and DogStatsD, this guide will show how to send [**COUNT** metrics](https://docs.datadoghq.com/developers/metrics/types/?tab=count#definition) to Datadog.

This stage will build on top of the configurations set up in the previous section.

1. Include the time library:
```python
import time
```

2. Select which **COUNT** methods you plan to use in your project using the following [table](https://docs.datadoghq.com/developers/metrics/dogstatsd_metrics_submission/#count):

![9table](https://user-images.githubusercontent.com/35269716/100524541-0938de80-3187-11eb-8ef1-38890dcefec0.png)

3. This guide will use both the **increment** method and the **decrement** method:
```python
while(1):
  statsd.increment('example_metric.increment', tags=["environment:dev"])
  statsd.decrement('example_metric.decrement', tags=["environment:dev"])
  time.sleep(10)
```
The parameters used in both methods can be further explored in the table below:
![10param](https://user-images.githubusercontent.com/35269716/100524598-73518380-3187-11eb-86b4-bf97a06f642d.png)

4. Run your Python script. Then verify your results by setting up a [dashboard.](https://docs.datadoghq.com/getting_started/dashboards/) The final product should look like the following:

![11results](https://user-images.githubusercontent.com/35269716/100524654-fb378d80-3187-11eb-8b99-24da48911d79.png)

The following code shows all the components combined:
```python
from datadog import initialize, statsd
import time

options = {
    'statsd_host':'127.0.0.1',
    'statsd_port':8125
}

initialize(**options)

while(1):
  statsd.increment('example_metric.increment', tags=["environment:dev"])
  statsd.decrement('example_metric.decrement', tags=["environment:dev"])
  time.sleep(10)
```


## Best practices and next steps
To explore best practices for tools covered in this guide, you can review the following:

* [API keys](https://docs.datadoghq.com/account_management/api-app-keys/#transferring-apiapplication-keys)
* [Monitors](https://www.datadoghq.com/blog/tagging-best-practices-monitors/)
* [Tagging](https://www.datadoghq.com/blog/tagging-best-practices/)

## Acknowledgment
Thank you to the **datadogpy** community. In particular, kudos to the following developers who provided enormous contributions: [yannmh](https://github.com/yannmh) (Yann), [zippolyte](https://github.com/zippolyte) (Hippolyte HENRY), and [nmuesch](https://github.com/nmuesch) (Nicholas Muesch).





