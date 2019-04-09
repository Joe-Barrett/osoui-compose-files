# OSO-UI Compose Files :whale:
This repository hosts Docker Compose files which may be useful to the SKA OSO-UI
team during development. 

## Contributing
The files in this repository are made to be as environmentally independent as possible. **Please** ensure you do not check in any code which includes filepaths, this applies mostly to the `.env` file. Thanks :thumbsup:

## Usage
``` bash
# launch Tango and WebJive
make up

# optional: launch TMC devices
make tmc
# optional: launch TangoTest device
make start tangotest
# optional: launch Jive (Java version)
make start jive

# stop all containers
make down
```

After starting the WebJive containers and any required additional containers, navigate to 
`http://localhost:22484/testdb` to access WebJive. The following credentials can be used:

<dl>
  <dt>Username</dt>
  <dd>user1</dd>

  <dt>Password</dt>
  <dd>abc123</dd>
</dl>

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


