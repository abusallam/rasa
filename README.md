# Welcome :D

Rasa X deployment in Docker Swarm Cluster + Traefik Load Balancer

Before we start with the deployment of the service it is important to check out the deployment.env file and set up 
the enviroment variables we desire. It is IMPORTANT to change the default tokens, you can use command `openssl rand -base64 32` to create new secrets.

## Traefik Deployment

create the htpasswd file with the admin user to access the dashboard

`htpasswd -c ./htpasswd admin`

and start the stack

`docker stack deploy -c traefik.yml traefik`

Just wait few seconds for Traefik service to go up and setup letsencrypt automatically and you should be able to access the dashboard.

## Rasa X stack deployment

`docker stack deploy -c rasa-x.yml rasax`

#### Rasa X credentials setup

In order to access Rasa X, we need to set up our password. By default the community version create the user `me` and we need to create a password for it.


It is important to be in the docker swarm node where the container is running. 
`docker stack ps rasax`

Then we need to know the Rasa X container ID. 
`docker ps | grep rasa-x`

Access the container
`docker exec -it CONTAINER-ID bash`

Once inside of the container we just need to update/create the password
`python ./scripts/manage_users.py create --update me YOU_PASSWORD admin`

after that you will be able to access Rasa X dashboard using your new password.

#### Rasa X file permissions

Rasa X does not run the container as privileged user, instead of that they run as user 1001. *Really good security practice*
Because of that it is necessary to change file/folder ownership in our volume storage.
In our example docker compose `rasa-x.yml` we are using the path `/data/rasa-test/app/` as our volume storage.

We just need to run the command in our docker swarm node
`chown -R 1001:root /data/rasa-test/app/`