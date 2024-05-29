# DLData

The main goal of this project is to learn data engineering. This project deploys a kubernetes cluster in which the project should run. I will update this readme when there is more functionality.

## Initial setup

To run this, we already need a kubernetes cluster with a docker registry, certificates and a Crunchy PGO running. We also need the tools installed to run skaffold.

## Deploy

First make sure to build all the containers using

```sh
skaffold build -d <your.repository>
```

To start the application, simply deploy using

```sh
skaffold run -d <your.repository>
```
