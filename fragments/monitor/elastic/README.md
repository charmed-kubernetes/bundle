# Elastic Monitoring

## Scaling Elasticsearch

ElasticSearch is used to hold all the log data and server information logged by
Beats. You can add more Elasticsearch nodes by using the Juju command:

```
juju add-unit elasticsearch
```

## Accessing Kibana

The Kibana web interface can display real time graphs and charts related to the
cluster. The Beats charms are sending metrics to Elasticsearch; Kibana displays
this data through various dashboards.

First, ensure the `beats` dashboards are available:

* `juju run-action --wait kibana/0 load-dashboard dashboard=beats`

Now, find the public address of the `kibana` charm:

* `juju status kibana`

The remaining steps take place in the Kibana web interface. Note that Kibana is
configured to listen on port `8080` in this bundle:

* Access Kibana by browser: http://KIBANA_IP_ADDRESS:8080/
* Select a default index pattern (e.g. `topbeat-*`)
  * Click the star button to make this the default index
* Select "Dashboard" from the left menu
* Select "Topbeat / Dashboard" from the left menu

![Setup Kibana](http://i.imgur.com/tgYFSjM.gif)
