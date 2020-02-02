# PetFinder Scrapy Crawler

This repository implements a spider for collecting [PetFinder](https://www.petfinder.com) breeds sections.

This source code will be used as base for an medium article about web crawling using Scrapy framework.

## Installation
```bash
pip install -r requirements.txt
```

## Running petfinder spider
```bash
scrapy crawl pet_finder -o pet_finder.json
```

If you want to filter a specific logging level you can pass the flag -L LOG_LEVEL

```bash
scrapy crawl pet_finder -o pet_finder.json -L INFO
```