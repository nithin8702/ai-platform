## 1. Retrieve an authentication token and authenticate your Docker client to your registry.
    Use the AWS CL
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 307915334735.dkr.ecr.us-east-1.amazonaws.com

## 2. Build your Docker image using the following command.
    docker build -t test1 .

## 3. After the build completes, tag your image so you can push the image to this repository
    docker tag test1:latest 307915334735.dkr.ecr.us-east-1.amazonaws.com/test1:latest

## 4. Run the following command to push this image to your newly created AWS repository
    docker push 307915334735.dkr.ecr.us-east-1.amazonaws.com/test1:latest


## Trouble Shooting
    https://askubuntu.com/questions/1171460/how-to-fix-docker-error-response-from-daemon-cgroups-cannot-find-cgroup-moun
    sudo mkdir /sys/fs/cgroup/systemd
    sudo mount -t cgroup -o none,name=systemd cgroup /sys/fs/cgroup/systemd
