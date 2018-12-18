# OSO-UI Compose Files :whale:
This repository hosts Docker Compose files which may be useful to the SKA OSO-UI
team during development. 

## Contributing
The files in this repository are made to be as environmentally independent as possible. **Please** ensure you do not check in any code which includes filepaths, this applies mostly to the `.env` file. Thanks :thumbsup:

## Usage
``` bash
docker-compose -f <service stack>.yml up -d
```

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
Run the make command, reccomended is HTML
``` bash
make html
```

Then open `docs/build/index.html` in your chosen browser.