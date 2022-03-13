### Files
    train_dataset.csv --> Its for Model Building
    test_dataset.csv --> Its for ModelTesting
    train.py --> Model Training
    predict.py --> ML Inference Web App
    

### Steps
    1. Run train.py  file for Model building and to save the model in pickle format
            In Terminal --> python3 train.py
            It will generate 2 output files (svc_model.pkl and lr_model.pkl)
    2. Run the following in jupter terminal or in command prompt
            streamlit run predict.py


### Troubleshooting
    # Steps - execute the following to containerize the model
# If you are getting permission error while executing docker, just add sudo
# example - sudo docker build -t mushroomclassifier:latest .

# 1. To build the docker image
# docker build -t mushroomclassifier:latest .
    # If you getting this error -> cgroup mountpoint does not exist: unknown
        sudo mkdir /sys/fs/cgroup/systemd
        sudo mount -t cgroup -o none,name=systemd cgroup /sys/fs/cgroup/systemd


# 2. To list docker images
# docker images

# 3. To run the prediction app from docker image
# sudo docker run -p 8501:8501 mushroomclassifier:latest

# TroubleShooting docker images
    # to list the container
    # docker container ls

    # stop the existing mushroom classifier container
    # docker stop 63379580f4c7
    # docker rm -f 63379580f4c7


    # To debug the docker image - optional
    # docker run -it mushroomclassifier bash

    # To delete all containers including its volumes and images
    # docker system prune -a
    # docker rm -vf $(docker ps -a -q)
    # docker rmi -f $(docker images -a -q)


## Deploy into ECR
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 807582834527.dkr.ecr.us-east-1.amazonaws.com
    docker build -t mushroomclassifier .
    docker tag mushroomclassifier:latest 807582834527.dkr.ecr.us-east-1.amazonaws.com/mushroomclassifier:latest
    docker push 807582834527.dkr.ecr.us-east-1.amazonaws.com/mushroomclassifier:latest
    

## Configuring and enabling the registry-creds addon 
    minikube addons configure registry-creds
    minikube addons enable registry-creds
    minikube addons list
    Wait for 2 mins
    Play with manifests
        kubectl apply -f deployments.yaml
        kubectl apply -f services.yaml
    kubectl port-forward svc/mushroomclassifier-service 8080:80
