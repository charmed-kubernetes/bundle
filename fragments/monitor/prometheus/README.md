# Prometheus & Grafana Performance Monitoring

Grafana provides a customisable graphical interface for viewing performance metrics for Kubernetes. 
It can provide both node metrics and container metrics, along with capacity planning information and much more. 

## Configuring Grafana and Prometheus

In order to use Grafana and Prometheus, the Prometheus Scraper must be run. 
An example script for doing this can be found [here](https://github.com/CanonicalLtd/canonical-kubernetes-demos/blob/master/cdk-monitoring-and-logging/scripts/log-monitoring-config.sh). 

## Accessing Grafana

The admin password for Grafana can be obtained using the command: 

```
juju run-action --wait grafana/0 get-admin-password
```

The public port and IP for grafana can be found using the commands:

```
grafana_public_ip=$(juju status  grafana --format yaml | grep public-address | sed -e 's/public-address://g' | sed -e 's/ //g')
grafana_port=$(juju config grafana port | sed -e 's/"//g')
echo "The Grafana UI is available at: http://$grafana_public_ip:$grafana_port."
```
