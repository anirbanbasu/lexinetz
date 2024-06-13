# Containerisation using Docker
You can run the web app in a Docker container. To do so, you have to build its image (which we name as `lexinetz` although you can choose any other name) and run an instance (which we name as `lexinetz-container` but you can also pick a name of your choice) of that image, as follows.

```
docker build -f local.dockerfile -t lexinetz .
docker create -p 8765:8765/tcp --name lexinetz-container lexinetz
```
