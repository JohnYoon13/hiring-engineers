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




