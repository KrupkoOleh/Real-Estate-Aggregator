# Real Estate Aggregator

A modern **web application** for aggregating real estate listings from various sources. Built with **Django 6.0**, **Python 3.13**, and modern front-end technologies like **Bootstrap 5** and **HTMX**.

This application allows users to collect, view, and manage real estate listings from someone website in a single dashboard, with features like duplicate detection and direct parsing.

## Content

- [Functional](#functional)
- [Installation](#installation)
- [Stack of the technologies](#stack-of-the-technologies)
- [Demonstration](#demonstration)

## Functional

- **Dashboard**: View all aggregated listings in a convenient table format.
- **Parsing**: Automated collection of listings from external site (e.g., Lemasson Conseil).
- **Duplicate Detection**: Automatically checks for existing listings by link or title to avoid duplicates.
- **Management**: Add new listings manually, update or delete existing ones.
- **Interactive UI**: Modal windows for creating records and dynamic updates using HTMX without full page reloads.
- **Notifications**: User feedback via Django Messages (success/error alerts).

## Installation

> **Note:** Before running the project, make sure all line separators in scripts (like `entrypoint.sh`) are set to **LF**. Using CRLF may cause error as "exec ./entrypoint.sh: no such file or directory" in Docker.

1. **Clone the project:**
   ```bash
   git clone https://github.com/KrupkoOleh/Real-Estate-Aggregator.git
   ```

2. **Start Docker containers:**
   ```bash
   docker-compose up -d --build
   ```

4. **Open the website:**
   Go to [http://localhost:8000](http://localhost:8000)

## Stack of the technologies

1. **Programming Language**: Python (v 3.13)
2. **Web Framework**: Django (v 6.0)
3. **Architecture**: Monolithic application with HTMX for dynamic interactions
4. **Database**: MySQL (v 8.0)
5. **Front-end**: Bootstrap 5, HTMX, Hyperscript
6. **Parsing**: BeautifulSoup4, Requests
7. **Containers and Environment**: Docker + Docker Compose

## Demonstration

![image of the db](https://i.postimg.cc/8z3PdTBt/image.png)
![image of the db](https://i.postimg.cc/NFggGFBv/image.png)
![image of the db](https://i.postimg.cc/WzXsdV1w/image.png)
![image of the db](https://i.postimg.cc/5NFLMDTc/image.png)
![image of the db](https://i.postimg.cc/tg9xWJTH/image.png)
