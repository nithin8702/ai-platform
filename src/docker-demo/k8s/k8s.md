## Configuring and enabling the registry-creds addon 
    minikube addons configure registry-creds
    minikube addons enable registry-creds
    minikube addons list
    Wait for 2 mins
    kubectl get secrets -> check for awscreds
    Play with manifests
        kubectl apply -f deployments.yaml
        kubectl apply -f services.yaml
    kubectl port-forward svc/mushroomclassifier-service 8080:80
