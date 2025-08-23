# --- Zola in Docker for GitHub Pages (docs/) ---
# Update if/when you bump Zola (no 'latest' tag available)
ZOLA_VERSION ?= v0.21.0
IMAGE        := ghcr.io/getzola/zola:$(ZOLA_VERSION)

# Paths
SITE_DIR     ?= $(CURDIR)
OUTPUT_DIR   ?= docs

# Common docker run prefix
DOCKER_RUN   := docker run --rm -u "$(shell id -u):$(shell id -g)" \
                 -v $(SITE_DIR):/app --workdir /app $(IMAGE)

.PHONY: pull init build serve clean

## Pull the pinned Zola image
pull:
	docker pull $(IMAGE)

## Initialize a new Zola site in the current directory
init: pull
	docker run --rm -it -u "$(id -u):$(id -g)" -v "$(pwd)":/app --workdir /app   ghcr.io/getzola/zola:v0.21.0 init . --force

## Build the site into ./docs (safe for GitHub Pages)
build: pull
	$(DOCKER_RUN) build --output-dir $(OUTPUT_DIR)

## Local preview at http://localhost:8080
serve: pull
	docker run --rm -u "$(shell id -u):$(shell id -g)" \
	  -v $(SITE_DIR):/app --workdir /app \
	  -p 8080:8080 -p 1024:1024 \
	  $(IMAGE) serve --interface 0.0.0.0 --port 8080 --base-url localhost

## Remove the generated output directory
clean:
	rm -rf $(OUTPUT_DIR)
