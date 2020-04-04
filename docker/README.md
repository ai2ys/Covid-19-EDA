# Build the docker image
Run the `build.sh` shell script from the terminal.

```bash
$ ./docker/build.sh
``` 

# Run the docker container
Run the docker container by executing the `start.sh` shell script from the terminal.
```bash
$ ./docker/start.sh
```

# Make shell scripts executable for current user
`chmod u+x <shell script name>`


# Misc
```bash
$ docker start covid19_eda
$ docker exec -it covid19_eda bash
<username>@<container_id>:/workspace$ jupyter notebook list
``` 

Stop / remove all of Docker containers:
```bash
$ docker stop $(docker ps -a -q)
$ docker rm $(docker ps -a -q)
```