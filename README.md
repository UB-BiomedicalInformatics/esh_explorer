# webprotege_configuration

Contains files for the osler.compbio.buffalo.edu webprotege install

get onto osler via ssh -L 8080:localhost:8080 osler.compbio.buffalo.edu

do:
docker compose up keycloak -d

Then go to:
http://localhost:8080

username: admin
password: entanglingVines

Create a realm with webprotoge.json

make sure the certs are coppied to ngnix and that nginx configuration docker-compose.yml and nginx/nginx.conf all match

do:

docker compose up


