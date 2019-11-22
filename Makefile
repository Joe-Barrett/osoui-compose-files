# Set dir of Makefile to a variable to use later
MAKEPATH := $(abspath $(lastword $(MAKEFILE_LIST)))
BASEDIR := $(notdir $(patsubst %/,%,$(dir $(MAKEPATH))))

COMPOSE_FILES := $(filter-out ds-config.yml,$(wildcard *.yml))
COMPOSE_FILE_ARGS := $(foreach yml,$(COMPOSE_FILES),-f $(yml))

ATTACH_COMPOSE_FILE_ARGS := $(foreach yml,$(filter-out tango.yml,$(COMPOSE_FILES)),-f $(yml))

# If the first make argument is "start" or "stop"...
ifeq (start,$(firstword $(MAKECMDGOALS)))
  SERVICE_TARGET = true
else ifeq (stop,$(firstword $(MAKECMDGOALS)))
  SERVICE_TARGET = true
else ifeq (attach,$(firstword $(MAKECMDGOALS)))
  SERVICE_TARGET = true
ifndef NETWORK_MODE
$(error NETWORK_MODE must specify the network to attach to, e.g., make NETWORK_MODE=tangonet-powersupply ...)
endif
ifndef TANGO_HOST
$(error TANGO_HOST must specify the Tango database device, e.g., make TANGO_HOST=powersupply-databaseds:100000 ...)
endif
endif
ifdef SERVICE_TARGET
  # .. then use the rest as arguments for the make target
  SERVICE := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(SERVICE):;@:)
endif

#
# Never use the network=host mode when running CI jobs, and add extra
# distinguishing identifiers to the network name and container names to
# prevent collisions with jobs from the same project running at the same
# time.
#
ifneq ($(CI_JOB_ID),)
NETWORK_MODE := tangonet-$(CI_JOB_ID)
CONTAINER_NAME_PREFIX := $(CI_JOB_ID)-
else
CONTAINER_NAME_PREFIX :=
endif

ifeq ($(OS),Windows_NT)
	$(error Sorry, Windows is not supported yet)
else
	UNAME_S := $(shell uname -s)
	ifeq ($(UNAME_S),Linux)
		DISPLAY ?= :0.0
		# host mode is disabled for now as WebJive deps require routing via Traefik
		NETWORK_MODE ?= tangonet
		XAUTHORITY_MOUNT := /tmp/.X11-unix:/tmp/.X11-unix
		XAUTHORITY ?= /hosthome/.Xauthority
		# /bin/sh (=dash) does not evaluate 'docker network' conditionals correctly
		SHELL := /bin/bash
	endif
	ifeq ($(UNAME_S),Darwin)
		IF_INTERFACE := $(shell netstat -nr | awk '{ if ($$1 ~/default/) { print $$6} }')
		DISPLAY := $(shell ifconfig $(IF_INTERFACE) | awk '{ if ($$1 ~/inet$$/) { print $$2} }'):0
		# network_mode = host doesn't work on MacOS, so fix to the internal network
		NETWORK_MODE ?= tangonet
		XAUTHORITY_MOUNT := $(HOME)/.Xauthority:/hosthome/.Xauthority:ro
		XAUTHORITY := /hosthome/.Xauthority
	endif
endif

WEBJIVE_COMPOSE_FILES = tangogql.yml webjive.yml traefik.yml
WEBJIVE_COMPOSE_FILE_ARGS := $(foreach yml,$(WEBJIVE_COMPOSE_FILES),-f $(yml))

#
# When running in network=host mode, point devices at a port on the host
# machine rather than at the container.
#
ifeq ($(NETWORK_MODE),host)
	TANGO_HOST := $(shell hostname):10000
	MYSQL_HOST := $(shell hostname):3306
else
	TANGO_HOST := $(CONTAINER_NAME_PREFIX)databaseds:10000
	MYSQL_HOST := $(CONTAINER_NAME_PREFIX)tangodb:3306
endif

# image tag to use for TMC containers
TMC_VERSION := 0.1.3


DOCKER_COMPOSE_ARGS := DISPLAY=$(DISPLAY) XAUTHORITY=$(XAUTHORITY) TANGO_HOST=$(TANGO_HOST) \
		NETWORK_MODE=$(NETWORK_MODE) XAUTHORITY_MOUNT=$(XAUTHORITY_MOUNT) MYSQL_HOST=$(MYSQL_HOST) \
		CONTAINER_NAME_PREFIX=$(CONTAINER_NAME_PREFIX) COMPOSE_IGNORE_ORPHANS=true TMC_VERSION=$(TMC_VERSION)

.PHONY: up down minimal start stop status clean pull help
.DEFAULT_GOAL := help

pull: ## pull the images from the Docker hub
	$(DOCKER_COMPOSE_ARGS) docker-compose $(COMPOSE_FILE_ARGS) pull

up: webjive  ## start Tango and WebJive, preparing all other services
	$(DOCKER_COMPOSE_ARGS) docker-compose $(COMPOSE_FILE_ARGS) up --no-start

debug:  ## start and debug all devices
	$(DOCKER_COMPOSE_ARGS) docker-compose $(COMPOSE_FILE_ARGS) up

down:  ## stop all services and tear down the system
	$(DOCKER_COMPOSE_ARGS) docker-compose $(COMPOSE_FILE_ARGS) -f ds-config.yml down
ifneq ($(NETWORK_MODE),host)
	docker network inspect $(NETWORK_MODE) &> /dev/null && ([ $$? -eq 0 ] && docker network rm $(NETWORK_MODE)) || true
endif

minimal: ## start the base Tango system
ifneq ($(NETWORK_MODE),host)
	docker network inspect $(NETWORK_MODE) &> /dev/null || ([ $$? -ne 0 ] && docker network create $(NETWORK_MODE))
endif
	$(DOCKER_COMPOSE_ARGS) docker-compose -f tango.yml up -d

webjive: minimal ## start WebJive
	$(DOCKER_COMPOSE_ARGS) docker-compose -f tango.yml $(WEBJIVE_COMPOSE_FILE_ARGS) up -d

oet: minimal  ## start the OET
	$(DOCKER_COMPOSE_ARGS) docker-compose -f tango.yml -f oet.yml up -d

start: up ## start a service (usage: make start <servicename>)
	$(DOCKER_COMPOSE_ARGS) docker-compose $(COMPOSE_FILE_ARGS) start $(SERVICE)

export_dashboards: webjive  ## export WebJive dashboards
	docker exec -i mongodb mongodump --archive > data/mongo/dashboards.dump

import_dashboards: webjive ## import WebJive dashboards
	docker exec -i mongodb mongorestore --archive < data/mongo/dashboards.dump

add_dashboard: webjive ## add a dashboard to WebJive (include path to dashboard dump in DASHBOARD_PATH variable)
	docker exec -i mongodb mongorestore --archive < $(DASHBOARD_PATH)

delete_dashboard: webjive ## delete a dashboard from WebJive (include dashboard name in DASHBOARD_NAME variable)
	docker exec -i mongodb mongo dashboards --eval "db.dashboards.remove({'name': '$(DASHBOARD_NAME)'})"

ds-config: minimal
	$(DOCKER_COMPOSE_ARGS) docker-compose -f ds-config.yml -f tango.yml up -d
	@echo Waiting for Tango DB to be populated
	@docker wait tmc-dsconfig > /dev/null
	@docker wait sdp-dsconfig > /dev/null
	@docker wait csp-dsconfig > /dev/null
	@echo Complete
	@$(MAKE) down

mvp: up ## start MVP devices
	$(DOCKER_COMPOSE_ARGS) docker-compose $(COMPOSE_FILE_ARGS) start \
		oet \
		sdpmaster \
		sdpsubarray \
		cspmaster \
		cspsubarray \
		cbfmaster \
		cbfsubarray01 \
		vcc001 \
		vcc002 \
		vcc003 \
		vcc004 \
		fsp01 \
		tmclogger \
		dishmaster1  \
		dishmaster2 \
		dishmaster3 \
		dishmaster4 \
		dishleafnode1 \
		dishleafnode2 \
		dishleafnode3 \
		dishleafnode4 \
		cspsubarrayleafnode \
		cspmasterleafnode \
		sdpsubarrayleafnode \
		sdpmasterleafnode \
		subarraynode1 \
		subarraynode2 \
		centralnode \
		rsyslog-tmcprototype \
		tm-alarmhandler

test-cli: mvp ## test the OET command line interface via scripting
	docker cp $(CURDIR)/test-harness $(CONTAINER_NAME_PREFIX)oet:/app
	docker exec -it $(CONTAINER_NAME_PREFIX)oet /bin/bash -c /app/test-harness/run_test.sh | tee test-harness/report.txt
	@$(MAKE) down

ds-test-config: minimal
	$(DOCKER_COMPOSE_ARGS) docker-compose -f ds-config.yml -f tango.yml up -d
	@echo Waiting for Tango DB to be populated
	@docker wait test-dsconfig > /dev/null
	@$(MAKE) down

test-webjive: check-user-and-password webjive ## run webjive end-to-end tests
	$(DOCKER_COMPOSE_ARGS) docker-compose $(COMPOSE_FILE_ARGS) up -d webjivetestdevice
	$(DOCKER_COMPOSE_ARGS) docker-compose $(COMPOSE_FILE_ARGS) up -d webjive-e2e-test
	docker cp $(CURDIR)/webjive-test-harness $(CONTAINER_NAME_PREFIX)webjive-e2e-test:/test
	@$(MAKE) add_dashboard DASHBOARD_PATH=webjive-test-harness/PollingTestDashboard.dump
	docker exec -it $(CONTAINER_NAME_PREFIX)webjive-e2e-test python3 test/webjive_e2e_test.py $(WEBJIVE_USERNAME) $(WEBJIVE_PASSWORD) "http://localhost:22484/testdb/devices"  | tee webjive-test-harness/report.txt
	@$(MAKE) delete_dashboard DASHBOARD_NAME=PollingTestDashboard
	@$(MAKE) down

check-user-and-password:
ifndef WEBJIVE_USERNAME
	$(error WEBJIVE_USERNAME is not set. Usage: test-webjive WEBJIVE_USERNAME=username WEBJIVE_PASSWORD=password)
endif
ifndef WEBJIVE_PASSWORD
	$(error WEBJIVE_PASSWORD is not set. Usage: test-webjive WEBJIVE_USERNAME=username WEBJIVE_PASSWORD=password)
endif

stop:  ## stop a service (usage: make stop <servicename>)
	$(DOCKER_COMPOSE_ARGS) docker-compose $(COMPOSE_FILE_ARGS) stop $(SERVICE)

status:  ## show the container status
	$(DOCKER_COMPOSE_ARGS) docker-compose $(COMPOSE_FILE_ARGS) ps

clean: down  ## clear all TANGO database entries
	docker volume rm $(BASEDIR)_tangodb
	docker volume rm $(BASEDIR)_tangogql-logs

help:   ## show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'