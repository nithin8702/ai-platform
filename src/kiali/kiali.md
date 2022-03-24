helm fetch kiali/kiali-operator --untar

cd kiali-operator
kubectl create ns kiali-operator
helm --namespace kiali-operator install kiali-operator .

kubectl port-forward svc/kiali 20001:20001 -n istio-system


kubectl get secret -n istio-system $(kubectl get sa kiali-service-account -n istio-system -o "jsonpath={.secrets[0].name}") -o jsonpath={.data.token} | base64 -d


## Tear down Kiali
    kubectl delete kiali --all --all-namespaces
    helm uninstall --namespace kiali-operator kiali-operator
    kubectl delete crd kialis.kiali.io
    kubectl delete ns kiali-operator

## unable to delete the Kiali CR
    kubectl patch kiali kiali -n istio-system -p '{"metadata":{"finalizers": []}}' --type=merge