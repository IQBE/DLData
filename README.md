# DLData

The main goal of this project is to learn data engineering. This project deploys a kubernetes cluster in which the project should run. I will update this readme when there is more functionality.

## Initial setup

To run this, we already need a kubernetes cluster with a docker registry, certificates and a Crunchy PGO running. We also need the tools installed to run skaffold.
Optionally you can also set up an orchestrator like Airflow or Mage

## Deploy

To build and start the application, simply deploy using

```sh
skaffold run -d <your.repository>
```

## Devolopment
To develop on this project, open it using VS Code, and make sure to have the Devcontainer plugin installed. VS Code should automatically prompt you to open the project inside its devcontainer. If not, open the VS Code Command Palette using `Ctrl+Shift+P` and run _Dev Containers: Open in Container..._. This starts up a devcontainer with a database, all environment variables in place and everything set up to start. After this you can can take a look at the `invoke --list` command to see what you can do to initiate and migrate the db, or run the api.
