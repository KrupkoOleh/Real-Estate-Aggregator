import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from project.settings import env

BASE_DOMAIN = env.str('BASE_URL_LEMASSON_CONSEIL',
                      default='BASE_URL_LEMASSON_CONSEIL')


def get_html(url):
    """
    Fetches the HTML content from the specified URL.
    Args:
        url (str): The URL to fetch.
    Returns:
        str: The HTML content of the page if successful, None otherwise.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,'
                  'application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Ошибка: Сервер вернул статус "
                  f"{response.status_code} для {url}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка подключения: {e}")
        return None


def parse_product_links(html):
    """
    Parses the HTML of a listing page to extract links
    to individual product pages.
    Args:
        html (str): The HTML content of the listing page.
    Returns:
        list: A list of relative URLs (strings) to the product pages.
    """
    soup = BeautifulSoup(html, 'html.parser')
    items_wrapper = soup.find('div',
                              class_='property-listing-v2__items-wrapper')

    product_links = []
    if items_wrapper:
        elements = items_wrapper.select(
            'article.property-listing-v2__container.item'
        )

        if not elements:
            elements = items_wrapper.find_all('article')

        for element in elements:
            try:
                link_tag = element.find('a', class_='item__title')
                if link_tag and link_tag.get('href'):
                    product_links.append(link_tag.get('href'))
            except AttributeError:
                continue

    print(f"Найдено ссылок на странице: {len(product_links)}")
    return product_links


def save_image_urls(soup, listening_obj):
    """
    Finds images in the slider and saves their URLs to the Image model.
    Args:
        soup (BeautifulSoup): Parsed HTML of the product page.
        listening_obj (Listening): The Listening instance to attach images to.
    """
    from dashboard.models import Image

    slider_wrapper = soup.find('div',
                               class_='swiper-wrapper js-lightbox-swiper')
    if not slider_wrapper:
        return

    slides = slider_wrapper.find_all('div', class_='swiper-slide')

    processed_urls = set()

    for slide in slides:
        if 'swiper-slide-duplicate' in slide.get('class', []):
            continue

        link_tag = slide.find('a', attrs={'aria-label': 'zoom'})
        if not link_tag:
            continue

        img_url = link_tag.get('href')

        if not img_url or img_url in processed_urls:
            continue

        processed_urls.add(img_url)

        if img_url.startswith('//'):
            img_url = 'https:' + img_url
        elif img_url.startswith('/'):
            img_url = urljoin(BASE_DOMAIN, img_url)

        try:
            Image.objects.create(listening=listening_obj, image_url=img_url)

        except Exception:
            continue


def parse_product(html_code):
    """
    Parses the listing page, extracts product links, visits each product page,
    scrapes details (title, price), and saves the data to the database.
    Args:
        html_code (str): The HTML content of the listing page.
    Returns:
        bool: True if products were found and processed, False otherwise.
    """
    from dashboard.models import Listening

    links = parse_product_links(html_code)

    if not links:
        return False

    for link in links:
        try:
            if link.startswith('http'):
                full_link = link
            else:
                full_link = urljoin(BASE_DOMAIN, link)

            if Listening.objects.filter(link=full_link).exists():
                print(f"Пропуск (ссылка существует): {full_link}")
                continue

            response = get_html(full_link)
            if not response:
                continue

            soup = BeautifulSoup(response, 'html.parser')
            main_info_part = soup.find('div', class_='editorial__wrapper')
            if not main_info_part:
                print(f"Не найден контент на странице {full_link}")
                continue

            title_parts = main_info_part.find_all('span',
                                                  class_=['title__content-1',
                                                          'title__content-2'])

            title = " ".join([p.get_text(strip=True)
                              for p in title_parts]) or "No Title"
            price_tag = main_info_part.find('span', class_='details__price')
            price = price_tag.get_text(strip=True) if price_tag else "0"
            price_decimal = re.sub(r'[^\d]', '', price)
            if not price_decimal:
                price_decimal = 0

            description_tag = main_info_part.find("div",
                                                  class_="editorial__text")
            description = str(description_tag) if description_tag else ""

            obj, created = Listening.objects.get_or_create(
                link=full_link,
                defaults={
                    'title': title,
                    'price': price_decimal,
                    'description': description
                }
            )

            if created:
                print(f"Создано: {title}")
                save_image_urls(soup, obj)
            else:
                print(f"Уже существует: {title}")

        except AttributeError as e:
            print(f"Ошибка атрибута: {e}")
            continue

    return True


def run_scraper():
    """
    Main function to orchestrate the scraping process.
    Iterates through paginated pages, fetches HTML,
    and triggers product parsing
    until no more products are found.
    """
    page = 1

    while True:
        if page == 1:
            url = BASE_DOMAIN
        else:
            url = f'{BASE_DOMAIN}{page}'

        print(f"--- Парсинг страницы {page}: {url} ---")

        html_code = get_html(url)

        if not html_code:
            print("Не удалось получить HTML или конец страниц.")
            break

        has_products = parse_product(html_code)

        if not has_products:
            print("Товары не найдены, завершаем парсинг.")
            break

        page += 1
