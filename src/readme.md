## Deploy kubernetes clusters
    cd clusters
    eksctl create cluster -f eksworkshop.yaml
    Attach alb policy to eksctl-eksworkshop-eksctl-nodegro-NodeInstanceRole-

## Validate clusters
    kubectl get nodes -o wide
    


## Install Kustomize
    sudo wget -O /usr/local/bin/kustomize https://github.com/kubernetes-sigs/kustomize/releases/download/v3.2.0/kustomize_3.2.0_linux_amd64
    sudo chmod +x /usr/local/bin/kustomize
    kustomize version

## Deploy kubeflow
    cd manifests
    while ! kustomize build example | kubectl apply -f -; do echo "Retrying to apply resources"; sleep 10; done

    cert-manager
        kustomize build common/cert-manager/cert-manager/base | kubectl apply -f -
        kustomize build common/cert-manager/kubeflow-issuer/base | kubectl apply -f -

    Istio
        kustomize build common/istio-1-11/istio-crds/base | kubectl apply -f -
        kustomize build common/istio-1-11/istio-namespace/base | kubectl apply -f -
        kustomize build common/istio-1-11/istio-install/base | kubectl apply -f -

    Dex
        kustomize build common/dex/overlays/istio | kubectl apply -f -

    OIDC AuthService
        kustomize build common/oidc-authservice/base | kubectl apply -f -

    Knative
        kustomize build common/knative/knative-serving/overlays/gateways | kubectl apply -f -
        kustomize build common/istio-1-11/cluster-local-gateway/base | kubectl apply -f -

        kustomize build common/knative/knative-eventing/base | kubectl apply -f -

    Kubeflow Namespace
        kustomize build common/kubeflow-namespace/base | kubectl apply -f -

    Kubeflow Roles
        kustomize build common/kubeflow-roles/base | kubectl apply -f -

    Kubeflow Istio Resources
        kustomize build common/istio-1-11/kubeflow-istio-resources/base | kubectl apply -f -

    Kubeflow Pipelines
        kustomize build apps/pipeline/upstream/env/platform-agnostic-multi-user | kubectl apply -f -

    KServe / KFServing
        kustomize build contrib/kserve/kserve | kubectl apply -f -
        kustomize build contrib/kserve/models-web-app/overlays/kubeflow | kubectl apply -f -

    Katib
        kustomize build apps/katib/upstream/installs/katib-with-kubeflow | kubectl apply -f -

    Central Dashboard
        kustomize build apps/centraldashboard/upstream/overlays/kserve | kubectl apply -f -

    Admission Webhook
        kustomize build apps/admission-webhook/upstream/overlays/cert-manager | kubectl apply -f -

    Notebooks
        kustomize build apps/jupyter/notebook-controller/upstream/overlays/kubeflow | kubectl apply -f -
        kustomize build apps/jupyter/jupyter-web-app/upstream/overlays/istio | kubectl apply -f -

    Profiles + KFAM
        kustomize build apps/profiles/upstream/overlays/kubeflow | kubectl apply -f -

    Volumes Web App
        kustomize build apps/volumes-web-app/upstream/overlays/istio | kubectl apply -f -

    Tensorboard
        kustomize build apps/tensorboard/tensorboards-web-app/upstream/overlays/istio | kubectl apply -f -
        kustomize build apps/tensorboard/tensorboard-controller/upstream/overlays/kubeflow | kubectl apply -f -

    Training Operator
        kustomize build apps/training-operator/upstream/overlays/kubeflow | kubectl apply -f -

    User Namespace
        kustomize build common/user-namespace/base | kubectl apply -f -

## Validate kubeflow resources
    kubectl get pods -n cert-manager
    kubectl get pods -n istio-system
    kubectl get pods -n auth
    kubectl get pods -n knative-eventing
    kubectl get pods -n knative-serving
    kubectl get pods -n kubeflow
    kubectl get pods -n kubeflow-user-example-com

## Kubeflow UI
    kubectl port-forward svc/istio-ingressgateway -n istio-system 8080:80

## Ingress
    https://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html
        kubernetes.io/cluster/eksworkshop-eksctl shared
        kubernetes.io/role/elb 1
    Attach 2 roles eksctl-eksworkshop-eksctl-nodegro-NodeInstanceRole-
        roles/iam_alb_ingress_policy.json
        roles/iam_profile_controller_policy.json
    kubectl apply -f alb.yaml
    kubectl apply -f ingress.yaml
    kubectl get svc/istio-ingressgateway -n istio-system

    Check the logs
        kubectl -n kubeflow logs $(kubectl get pods -n kubeflow --selector=app.kubernetes.io/name=alb-ingress-controller --output=jsonpath={.items..metadata.name})

## Tear down kubeflow
    kubectl delete -f ingress.yaml
    kubectl delete -f alb.yaml
    Detach 2 roles in eksctl-eksworkshop-eksctl-nodegro-NodeInstanceRole-

    cd manifests
    kubectl delete -k example

## Tear down clusters
    eksctl delete cluster --name eksworkshop-eksctl
