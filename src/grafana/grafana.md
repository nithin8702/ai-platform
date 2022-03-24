https://www.eksworkshop.com/intermediate/240_monitoring/deploy-grafana/
https://awskrug.github.io/eks-workshop/monitoring/deploy-grafana/



helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

helm install my-release grafana/grafana


kubectl port-forward service/grafana 3000:3000


helm delete my-release




NOTES:
1. Get your 'admin' user password by running:

   kubectl get secret --namespace default my-release-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

2. The Grafana server can be accessed via port 80 on the following DNS name from within your cluster:

   my-release-grafana.default.svc.cluster.local

   Get the Grafana URL to visit by running these commands in the same shell:

     export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=my-release" -o jsonpath="{.items[0].metadata.name}")
     kubectl --namespace default port-forward $POD_NAME 3000

3. Login with the password from step 1 and the username: admin
#################################################################################
######   WARNING: Persistence is disabled!!! You will lose your data when   #####
######            the Grafana pod is terminated.                            #####
#################################################################################
