kubectl get crd


---------------Pytorch Job------------------
kubectl apply -f pytorchjob.yaml

kubectl get pods -l job-name=pytorch-simple


PODNAME=$(kubectl get pods -l job-name=pytorch-simple,replica-type=master,replica-index=0 -o name -n kubeflow)

kubectl logs -f ${PODNAME} -n kubeflow



---------------Tensorflow Job------------------
kubectl apply -f tfjob.yaml
kubectl get tfjob tfjob-simple


---------------MPI Job-------------------------
PODNAME=$(kubectl get pods -l mpi_job_name=tensorflow-benchmarks,mpi_role_type=launcher -o name)
kubectl logs -f ${PODNAME}




----Experiments-------------
kubectl get experiments -n kubeflow-user-example-com
