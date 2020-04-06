# Build the docker image
Run the `build.sh` shell script from the terminal.

```bash
$ ./docker/build.sh
``` 

# Run the docker container
Run the docker container by executing the `initial_start.sh` shell script from the terminal. This will mount the project directory into the container.
```bash
$ ./docker/initial_start.sh
```
Later on it is possible to run the container with thei `start.sh` script. This will open a bash. Afterwards the running notebook can be accessed using:
 ```bash
 jupyter notebook list
 ```

# Misc
## Make shell scripts executable for current user
`chmod u+x <shell script name>`

## Stop / remove all of Docker containers
```bash
$ docker stop $(docker ps -a -q)
$ docker rm $(docker ps -a -q)
```