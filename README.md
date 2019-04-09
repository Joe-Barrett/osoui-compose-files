# SKA Engineering UI Compose Utilities :whale:
This repository hosts Docker Compose files which may be useful to developers working on the SKA Engineering UI tool. 
At the moment this is primarily the SKA-OSO-UI team. 

## Contributing
The files in this repository are made to be as environmentally independent as possible. **Please** ensure you do not check in any code which includes filepaths, this applies mostly to the `.env` file. Thanks :thumbsup:

## Usage
``` bash
docker-compose -f <service stack>.yml up -d
```

### Stacks
This table describes which services come with which service stack.

| File                   |   Tango Database   |      TangoGQL      |    Test Device     |       Webjive       |
| ---------------------- | :----------------: | :----------------: | :----------------: | :-----------------: |
| tangogql               | :heavy_check_mark: | :heavy_check_mark: |        :x:         |         :x:         |
| tangogql.testdevice    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |         :x:         |
| webjive                | :heavy_check_mark: | :heavy_check_mark: |        :x:         | :heavy_check_mark:  |
| webjive.dev            | :heavy_check_mark: | :heavy_check_mark: |        :x:         | :heavy_check_mark:* |
| webjive.dev.testdevice | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark:* |
\* Dev mode uses `npm start` rather than serving the app using nginx.  
### Integration image
The team provide a reference release of the current webjive system in the form of a set of docker images stored on the SKA docker hub

These represent a relatively stable, but not necessarily functionally complete version of the webjive and TangoGQL components.

|Component            |Image name                 |
| --------------------| :-----------------------: |
|Authentication server|webjive-develop_auth       |
|TangoGQL             |webjive-develop_tangogql   |
|Dashboard repository |webjive-develop_dashboards | 
|Webjive              |webjive-develop_webjive    |

A local docker environment of these components correctly configured together with the necessary supporting images (such as the system images for tangodb and tangocs) can be built locally by running the docker compose file:

``` bash
 docker-compose -f webjive.tangogql.integration.yml up -d
```
Then open `http://localhost:22484/testdb` in your chosen browser.



More complete usage can be found by building the docs.

## Docs
### Using Docker
Ensure Docker is running and run the following command in the repository's root
directory
``` bash
docker run --rm -d -v $(pwd):/tmp -w /tmp/docs netresearch/sphinx-buildbox sh -c "make html"
```

### Using Make
This method requires Python, Make, Sphinx, and other dependencies to be installed on your system

Navigate to the docs directory
``` bash
cd docs
```
Run the make command, recommended is HTML
``` bash
make html
```

Then open `docs/build/index.html` in your chosen browser.