# Makefile for observable kubernetes

.PHONY: metadata
metadata:
	@echo "Updating extra-info metadata for bundle"
	@charm set cs:~containers/bundle/canonical-kubernetes conjure:='{"friendly-name": "Canonical Kubernetes", "version": 1}'

all: metadata
