#!/usr/bin/make
#
# plone-path is added when "vhost_path: mount/site" is defined in puppet
plone=$(shell grep plone-path port.cfg|cut -c 14-)
hostname=$(shell hostname)
instance1_port=$(shell grep instance1-http port.cfg|cut -c 18-)
disable=1
copydata=1
instance=instance-debug
profile=collective.messagesviewlet:base

all: run

.PHONY: bootstrap
bootstrap:
	virtualenv-2.7 .
	./bin/python bootstrap-buildout.py

.PHONY: setup
setup:
	virtualenv-2.7 .
	./bin/pip install --upgrade pip
	./bin/pip install -r requirements.txt

.PHONY: buildout
buildout:
	if ! test -f bin/buildout;then make setup;fi
	bin/buildout -v

.PHONY: run
run:
	if ! test -f bin/instance1;then make buildout;fi
	bin/instance1 fg

.PHONY: cleanall
cleanall:
	rm -fr lib bin/buildout develop-eggs downloads eggs parts .installed.cfg