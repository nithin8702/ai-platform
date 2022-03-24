
# add prometheus Helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

# add grafana Helm repo
helm repo add grafana https://grafana.github.io/helm-charts



helm install prometheus prometheus-community/prometheus \
    --namespace prometheus \
    --set alertmanager.persistentVolume.storageClass="gp2" \
    --set server.persistentVolume.storageClass="gp2"


kubectl get all -n prometheus


kubectl port-forward -n prometheus deploy/prometheus-server 8080:9090

helm uninstall prometheus --namespace prometheus
kubectl delete ns prometheus


<!-- # add prometheus Helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

# add grafana Helm repo
helm repo add grafana https://grafana.github.io/helm-charts


curl -o prometheus-values.yaml https://raw.githubusercontent.com/helm/charts/master/stable/prometheus/values.yaml


Open the prometheus-values.yaml you downloaded by double clicking on the file name on the left panel. You need to make three edits to this file.

Search for storageClass in the prometheus-values.yaml, uncomment and change the value to “prometheus”. You will do this twice, under both server & alertmanager manifests

The third edit you will do is to expose Prometheus server as a NodePort. Because Prometheus is exposed as ClusterIP by default, the web UI cannot be reached outside of Kubernetes. By exposing the service as NodePort, we will be able to reach Prometheus web UI from the worker node IP address. Search for type: ClusterIP and add nodePort: 30900 and change the type to NodePort as indicated below.


## List of IP addresses at which the Prometheus server service is available
## Ref: https://kubernetes.io/docs/user-guide/services/#external-ips
##
externalIPs: []

loadBalancerIP: ""
loadBalancerSourceRanges: []
servicePort: 80
nodePort: 30900
type: NodePort -->