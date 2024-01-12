#init a base image de Alpine, une petite distribution linux
FROM python:3-alpine3.19
#definir le répertoire de travail actuel
WORKDIR /
#copier le contenu du repertoire
ADD . /
#permet de run certianne command pour l'initioalisation du docker
RUN pip install -r requirements.txt
EXPOSE 3000
#definir les commandes au demarrage du docker
CMD python ./app.py