# kubectl
    https://kubernetes.io/docs/tasks/tools/


## Enable minikube
    https://minikube.sigs.k8s.io/docs/start/
    minikube start



## Configuring and enabling the registry-creds addon 
    minikube addons configure registry-creds
    minikube addons enable registry-creds
    minikube addons list
    Wait for 2 mins
    kubectl get secrets -> check for awscreds
    Play with manifests
        kubectl apply -f deployments.yaml
        kubectl apply -f services.yaml
    kubectl port-forward svc/mushroomclassifier-service 8080:9000

## TroubleShooting
    kubectl -n default get pods/mushroomclassifier-deployment-6476896d8-jvln2
    kubectl -n default get pods/mushroomclassifier-deployment-6476896d8-jvln2 -o wide
    kubectl -n default describe pods/mushroomclassifier-deployment-6476896d8-jvln2
    kubectl -n default get pods/mushroomclassifier-deployment-6476896d8-jvln2 -o wide
    kubectl -n default describe pods/mushroomclassifier-deployment-6476896d8-jvln2
    kubectl -n default get pods
    kubectl -n default get deployments

