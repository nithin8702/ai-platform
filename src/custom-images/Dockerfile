FROM ubuntu:latest as base

RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y curl
RUN apt-get -y install vim
RUN apt-get -y install python3
RUN apt-get -y install python3-pip

RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin


RUN apt-get install git -y

WORKDIR /app
COPY . .


# ------------------------------------ Code Server ------------------------------------
FROM base AS codeserver
EXPOSE 8888
RUN curl -fsSL https://code-server.dev/install.sh | sh
WORKDIR /app
USER ${NB_UID}
RUN chmod u+x ./bootstrap_codeserver.sh
ENTRYPOINT ["/app/bootstrap_codeserver.sh"]

# ------------------------------------ Jupyter ------------------------------------
FROM base AS jupyter
RUN pip install jupyter -U && pip install jupyterlab
RUN jupyter notebook --generate-config
RUN echo "c.NotebookApp.terminado_settings = {\"shell_command\": ['/bin/bash']}" | tee -a /home/ray/.jupyter/jupyter_notebook_config.py
EXPOSE 8888
ENV NB_PREFIX /
WORKDIR /app
USER ${NB_UID}
RUN chmod u+x ./bootstrap_jupyter.sh
ENTRYPOINT ["/app/bootstrap_jupyter.sh"]