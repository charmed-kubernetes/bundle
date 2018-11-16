# Graylog and ElasticSearch log monitoring

Graylog provides a front-end interface for ElasticSearch can be used to search and view both container and node logs 
on all nodes within the Kubernetes cluster. This is effectively a modified ELK stack, where kibana is replaced 
by Graylog. 

## Scaling Elasticsearch

ElasticSearch is used to hold all the log data and server information logged by
Beats. You can add more Elasticsearch nodes by using the Juju command:

```
juju add-unit elasticsearch
```

## Configuring Graylog, ElasticSearch and Filebeat

After deployment, Graylog, ElasticSearch and Filebeat need some post-configuration to make them work. 
An example script for doing this can be found [here](https://github.com/CanonicalLtd/canonical-kubernetes-demos/blob/master/cdk-monitoring-and-logging/scripts/log-monitoring-config.sh#L49). 

## Accessing Graylog

You can retrieve the Graylog admin password using the following command:

```
juju run-action --wait graylog/0 show-admin-password
```

You can retrieve the graylog web interface URL by running the following command: 

```
proxy_public_ip=$(juju status apache2 --format yaml | grep public-address | sed -e 's/public-address://g' | sed -e 's/ //g')
echo "The Graylog UI is accessible at: http://$proxy_public_ip/. "
```
