# Makefile for observable kubernetes

.PHONY: metadata
metadata:
	@echo "Updating extra-info metadata for bundle"
	@charm set cs:~containers/bundle/observable-kubernetes conjure:='{"friendly-name": "Observable Kubernetes", "version": 1}'

all: metadata
