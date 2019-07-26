# SKA Engineering UI Compose Utilities :whale:

[![Documentation Status](https://readthedocs.org/projects/ska-engineering-ui-compose-utils/badge/?version=latest)](https://developer.skatelescope.org/projects/ska-engineering-ui-compose-utils/en/latest/?badge=latest)

This repository hosts Docker Compose files which may be useful to developers working on the SKA Engineering UI tool. 
At the moment this is primarily the SKA-OSO-UI team. 

## Contributing
The files in this repository are made to be as environmentally independent as possible. **Please** ensure you do not check in any code which includes filepaths, this applies mostly to the `.env` file. Thanks :thumbsup:

## Usage
``` bash
# Create Tango DB and register all devices
make ds-config

# launch Tango and WebJive
make up

# optional: launch MVP devices
make mvp
# optional: launch TangoTest device
make start tangotest
# optional: launch Jive (Java version)
make start jive

# optional: launch OET
make oet
# optional: connect to OET. <ctrl><p> + <ctrl><q> to exit
docker attach oet

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

More complete usage can be found by building the docs.

## Docs
### Generate docs using Docker
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

Then open `docs/build/html/index.html` in your chosen browser.


# Online demo

http://integration.engageska-portugal.pt/testdb (log in with user1/abc123)
