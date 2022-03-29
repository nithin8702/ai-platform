Seldon
https://www.kubeflow.org/docs/external-add-ons/serving/seldon/


1.
Install Seldon
kustomize build seldon-core-operator/base | kubectl apply -n kubeflow -f -

2.
cat <<EOF | kubectl create -n seldon -f -
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: seldon-model
spec:
  name: test-deployment
  predictors:
  - componentSpecs:
    - spec:
        containers:
        - image: seldonio/mock_classifier_rest:1.3
          name: classifier
    graph:
      children: []
      endpoint:
        type: REST
      name: classifier
      type: MODEL
    name: example
    replicas: 1 
EOF


4.
kubectl get sdep seldon-model -n kubeflow-user-example-com -o jsonpath='{.status.state}\n'


5.
https://github.com/SeldonIO/seldon-core
http://3e100955-istiosystem-istio-2af2-1326224036.us-east-1.elb.amazonaws.com/seldon/kubeflow-user-example-com/seldon-model/api/v1.0/doc/

http://localhost:8080/seldon/kubeflow-user-example-com/seldon-model/api/v1.0/doc/

Copy the authservice_session token and authorize it in Swagger UI
In Request body,
{"data": {"ndarray":[[1.0, 2.0, 5.0]]}}
