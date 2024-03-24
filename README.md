# Real Estate Data Scraping Project

## Overview
This project is designed to scrape real estate listings from websites using the Scrapy framework and display the results through a web application. The data collected by the scraper is stored in a PostgreSQL database, and the web application provides a user-friendly interface to browse the data. This project is containerized using Docker to ensure easy deployment and consistency across different environments.

## Prerequisites:
Before you begin, ensure you have the following installed on your system:
- Python 3.8 or later
- Docker and Docker Compose
- Virtual Environment (venv) or python package manager

## Installation and Setup

### Setting Up the Environment
To implement the project from the beginning, run following commands
```bash
# Create virtual environment in order to run  scraping & ingestion scripts:
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt

# Running the Scraper: 
cd estate_scrape/ # It should be in place where you start you Scrapy project!
scrapy crawl sreality

# Initializing the Database and Web App with Docker
cd ../../
docker-compose up --build

# Ingesting Data into the Database
python python ingest_data.py
```

### Notes

- Scraping implemented via API due to the complex structure of the target site(s), API calls are made where possible to efficiently retrieve data in desired formats.
- 
- Scraped data is initially stored temporarily for quality assurance before being ingested into the PostgreSQL database, ensuring high data integrity
  





