# Containerisation using Docker
You can run the web app ~~or, the REST API~~ in a Docker container. To do so, you have to build its image (which we name as `lexinetz` although you can choose any other name) and run an instance (which we name as `lexinetz-container` but you can also pick a name of your choice) of that image, as follows.

```
docker build -f local.dockerfile -t lexinetz .
docker create -p 8765:8765/tcp --name lexinetz-container lexinetz
```

<!-- If you want to change the settings of the app itself inside the container, login to the container as `root`. You can do this by running `docker exec -it tldrlc-container bash`. Once, you have the shell access in the container, edit the file `/app/.env` using the `nano` editor that is installed for convenience. For example, you can change the default behaviour of the containerised app to use your preferred remote graph, index and document storage. Then, restart the _same_ container, by running `docker container restart tldrlc-container`. Remember that these changes _will not_ propagate to any new container that you spin out of the image. -->
