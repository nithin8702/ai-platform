## Deploy kubernetes clusters
    minikube start --cpus 8 --memory 12000 --disk-size=250g --kubernetes-version=v1.21.10

    https://eksctl.io/
    cd clusters
    eksctl create cluster -f eksworkshop.yaml
        CloudFormation
            -> VPC, Subnets, IternetGateway, IAM Roles
            -> EKS
    Attach alb policy to eksctl-eksworkshop-eksctl-nodegro-NodeInstanceRole-

## Validate clusters
    kubectl get nodes -o wide
    


## Install Kustomize
    sudo wget -O /usr/local/bin/kustomize https://github.com/kubernetes-sigs/kustomize/releases/download/v3.2.0/kustomize_3.2.0_linux_amd64
    sudo chmod +x /usr/local/bin/kustomize
    kustomize version

## Deploy kubeflow
    cd ../manifests
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
        <!-- kustomize build apps/pipeline/upstream/env/platform-agnostic-multi-user | kubectl apply -f - -->
        kustomize build apps/pipeline/upstream/env/aws | kubectl apply -f -

    KServe / KFServing
        kustomize build contrib/kserve/kserve | kubectl apply -f -
        kustomize build contrib/kserve/models-web-app/overlays/kubeflow | kubectl apply -f -

    Katib
        kustomize build apps/katib/upstream/installs/katib-with-kubeflow | kubectl apply -f -

        kustomize build apps/katib/upstream/installs/katib-external-db | kubectl apply -f -


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

    pip install passlib
    pip install bcrypt
    export HASH=$(python3 -c 'from passlib.hash import bcrypt; import getpass; print(bcrypt.using(rounds=12, ident="2y").hash(getpass.getpass()))')

    kubectl get cm dex -n auth -o yaml > dex-auth.yaml
    kubectl apply -f dex-auth.yaml
    kubectl rollout restart deployment dex -n auth

    kubectl get cm -n kubeflow
    kubectl get cm jupyter-web-app-config-9d479bc4bk -n kubeflow -o yaml > jupyter-web-app.yaml

    cd kf-profiles
    kubectl apply -f dev.yaml

    kubectl apply -f poddefault.yaml



## Ingress
    https://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html
        kubernetes.io/cluster/eksworkshop-eksctl shared
        kubernetes.io/role/elb 1
    Attach 2 roles eksctl-eksworkshop-eksctl-nodegro-NodeInstanceRole-
        roles/iam_alb_ingress_policy.json
        roles/iam_profile_controller_policy.json
    Change VPC Id in alb.yaml
    kubectl apply -f alb.yaml
    kubectl apply -f ingress.yaml
    kubectl get svc/istio-ingressgateway -n istio-system

    Check the logs
        kubectl -n kubeflow logs $(kubectl get pods -n kubeflow --selector=app.kubernetes.io/name=alb-ingress-controller --output=jsonpath={.items..metadata.name})

## Tear down kubeflow
    kubectl delete -f ingress.yaml
    kubectl delete -f alb.yaml

    cd manifests
    kubectl delete -k example

    Detach 2 roles in eksctl-eksworkshop-eksctl-nodegro-NodeInstanceRole-

    Delete tags in subnets which we added manually

## Tear down clusters
    eksctl delete cluster --region=us-east-1 --name=eksworkshop-eksctl



## RDS and S3
    https://github.com/awslabs/kubeflow-manifests/tree/v1.3-branch/distributions/aws/examples/rds-s3

    export S3_BUCKET=kf-pipelines-demo
    export CLUSTER_REGION=us-east-1
    aws s3 mb s3://$S3_BUCKET --region $CLUSTER_REGION
    wget https://cloudformation-kubeflow.s3-us-west-2.amazonaws.com/rds.yaml


    export AWS_CLUSTER_NAME=eksworkshop-eksctl
    export CLUSTER_NAME=eksworkshop-eksctl
    export CLUSTER_REGION=us-east-1

    # Retrieve your VpcId.
    aws ec2 describe-vpcs \
        --output json \
        --filters Name=tag:alpha.eksctl.io/cluster-name,Values=$AWS_CLUSTER_NAME \
        | jq -r '.Vpcs[].VpcId'

    # Retrieve the list of SubnetIds for your cluster's Private subnets. Select at least 2.
    aws ec2 describe-subnets \
        --output json \
        --filters Name=tag:alpha.eksctl.io/cluster-name,Values=$AWS_CLUSTER_NAME Name=tag:aws:cloudformation:logical-id,Values=SubnetPrivate* \
        | jq -r '.Subnets[].SubnetId'

    # Retrieve the SecurityGroupId for your nodes.
    # Note: This assumes that your nodes share the same SecurityGroup
    INSTANCE_IDS=$(aws ec2 describe-instances --query 'Reservations[*].Instances[*].InstanceId' --filters "Name=tag-key,Values=eks:cluster-name" "Name=tag-value,Values=$AWS_CLUSTER_NAME" --output text)
    for i in "${INSTANCE_IDS[@]}"
    do
    echo "SecurityGroup for EC2 instance $i ..."
    aws ec2 describe-instances --output json --instance-ids $i | jq -r '.Reservations[].Instances[].SecurityGroups[].GroupId'
    done  


    aws secretsmanager create-secret --name rds-secret --secret-string '{"username":"admin","password":"Kubefl0w","database":"kubeflow","host":"km15dmykah4awpr.crcltrql51qh.us-east-1.rds.amazonaws.com","port":"3306"}' --region $CLUSTER_REGION


    aws secretsmanager create-secret --name s3-secret --secret-string '{"accesskey":"AKIA3YB5QD5PV3E3UAW5","secretkey":"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"}' --region $CLUSTER_REGION




    kustomize build distributions/aws/aws-secrets-manager/base > aws-secrets-manager.yaml
    kustomize build apps/pipeline/upstream/env/aws > aws-pipelines.yaml
    kustomize build apps/katib/upstream/installs/katib-external-db-with-kubeflow > aws-katib.yaml


    kubectl run -it --rm --image=mysql:5.7 --restart=Never mysql-client -- mysql -h km15dmykah4awpr.crcltrql51qh.us-east-1.rds.amazonaws.com -u admin -pKubefl0w

    working
    exec katib-mysql-6dcb447c6f-8jpkb
    mysql -h km15dmykah4awpr.crcltrql51qh.us-east-1.rds.amazonaws.com -u admin -pKubefl0w

    aws secretsmanager get-secret-value \
    --region $CLUSTER_REGION \
    --secret-id rds-secret \
    --query 'SecretString' \
    --output text

    aws secretsmanager delete-secret \
    --secret-id rds-secret \
    --force-delete-without-recovery

    aws secretsmanager delete-secret \
    --secret-id s3-secret \
    --force-delete-without-recovery






kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/secrets-store-csi-driver/v1.0.0/deploy/rbac-secretproviderclass.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/secrets-store-csi-driver/v1.0.0/deploy/csidriver.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/secrets-store-csi-driver/v1.0.0/deploy/secrets-store.csi.x-k8s.io_secretproviderclasses.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/secrets-store-csi-driver/v1.0.0/deploy/secrets-store.csi.x-k8s.io_secretproviderclasspodstatuses.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/secrets-store-csi-driver/v1.0.0/deploy/secrets-store-csi-driver.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/secrets-store-csi-driver/v1.0.0/deploy/rbac-secretprovidersyncing.yaml

kubectl apply -f https://raw.githubusercontent.com/aws/secrets-store-csi-driver-provider-aws/main/deployment/aws-provider-installer.yaml





kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/secrets-store-csi-driver/v1.0.0/deploy/rbac-secretproviderclass.yaml
kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/secrets-store-csi-driver/v1.0.0/deploy/csidriver.yaml
kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/secrets-store-csi-driver/v1.0.0/deploy/secrets-store.csi.x-k8s.io_secretproviderclasses.yaml
kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/secrets-store-csi-driver/v1.0.0/deploy/secrets-store.csi.x-k8s.io_secretproviderclasspodstatuses.yaml
kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/secrets-store-csi-driver/v1.0.0/deploy/secrets-store-csi-driver.yaml
kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/secrets-store-csi-driver/v1.0.0/deploy/rbac-secretprovidersyncing.yaml
kubectl delete -f https://raw.githubusercontent.com/aws/secrets-store-csi-driver-provider-aws/main/deployment/aws-provider-installer.yaml



