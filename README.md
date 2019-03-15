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