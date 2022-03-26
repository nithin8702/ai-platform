eksctl utils associate-iam-oidc-provider \
    --cluster eksworkshop-eksctl \
    --approve

ACCOUNT_ID=807582834527

aws iam create-policy   \
  --policy-name k8s-asg-policy \
  --policy-document file://cluster-autoscaler-policy.json

eksctl create iamserviceaccount \
    --name cluster-autoscaler \
    --namespace kube-system \
    --cluster eksworkshop-eksctl \
    --attach-policy-arn "arn:aws:iam::${ACCOUNT_ID}:policy/k8s-asg-policy" \
    --approve \
    --override-existing-serviceaccounts

kubectl -n kube-system describe sa cluster-autoscaler

kubectl apply -f cluster-autoscaler-autodiscover.yaml

kubectl -n kube-system logs -f deployment/cluster-autoscaler

kubectl apply -f nvidia-device-plugin.yaml

kubectl -n kube-system get daemonsets




-----Delete
kubectl delete -f nvidia-device-plugin.yaml
kubectl delete -f cluster-autoscaler-autodiscover.yaml
eksctl delete iamserviceaccount cluster-autoscaler --namespace kube-system --cluster eksworkshop-eksctl