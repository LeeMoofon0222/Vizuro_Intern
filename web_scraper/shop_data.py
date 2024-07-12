from bs4 import BeautifulSoup
import requests
import time
from urllib.parse import urlparse, parse_qs
import random


url = 'https://www.amazon.com/acer-Wireless-Non-Stop-Bluetooth5-3-Headphones/dp/B0CLYH2DRN/ref=sxin_16_sbv_search_btf?_encoding=UTF8&content-id=amzn1.sym.5cde1a09-4942-4242-87c5-e66d2d3b6a3c%3Aamzn1.sym.5cde1a09-4942-4242-87c5-e66d2d3b6a3c&cv_ct_cx=gaming%2Bheadsets&dib=eyJ2IjoiMSJ9.TeAUh4HrECihko2sKZE51A.xRjBuwPbdpYMBu2C2UUuuHjCaoLfZyIWg3SkYJrDOj4&dib_tag=se&keywords=gaming%2Bheadsets&pd_rd_i=B0CLYH2DRN&pd_rd_r=4661825c-41b4-4c76-9336-50c5cab08f62&pd_rd_w=nRXZa&pd_rd_wg=xcMyO&pf_rd_p=5cde1a09-4942-4242-87c5-e66d2d3b6a3c&pf_rd_r=V1EE101AZPK8M3J5934A&qid=1720420093&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sr=1-1-5190daf0-67e3-427c-bea6-c72c1df98776&th=1'

parsed_url = urlparse(url)
query_params = parse_qs(parsed_url.query)
productID = query_params.get('pd_rd_i', [None])[0]

reviewsUrl = [
              f'https://www.amazon.com/product-reviews/{productID}/ref=cm_cr_unknown?ie=UTF8&filterByStar=five_star&reviewerType=all_reviews&pageNumber=1#reviews-filter-bar',
              f'https://www.amazon.com/product-reviews/{productID}/ref=cm_cr_unknown?ie=UTF8&filterByStar=four_star&reviewerType=all_reviews&pageNumber=1#reviews-filter-bar',
              f'https://www.amazon.com/product-reviews/{productID}/ref=cm_cr_unknown?ie=UTF8&filterByStar=three_star&reviewerType=all_reviews&pageNumber=1#reviews-filter-bar',
              f'https://www.amazon.com/product-reviews/{productID}/ref=cm_cr_unknown?ie=UTF8&filterByStar=two_star&reviewerType=all_reviews&pageNumber=1#reviews-filter-bar',
              f'https://www.amazon.com/product-reviews/{productID}/ref=cm_cr_unknown?ie=UTF8&filterByStar=one_star&reviewerType=all_reviews&pageNumber=1#reviews-filter-bar'
              ]

custom_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept-Language': 'da, en-gb, en',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Referer': 'https://www.google.com/'
}


def get_amazon_reviews(urls):

    all_reviews = []

    for url in urls:
        reviews = []
        page = 1

        while len(reviews) < 10:
            current_url = url.replace('pageNumber=1', f'pageNumber={page}')
            response = requests.get(current_url, headers=custom_headers)

            soup = BeautifulSoup(response.content, 'html.parser')
            review_elements = soup.find_all('div', {'data-hook': 'review'})

            if not review_elements:
                break

            for review in review_elements:
                if len(reviews) >= 10:
                    break

                rating = review.find('i', {'data-hook': 'review-star-rating'})
                rating = rating.text.split()[0] if rating else 'N/A'

                title_element = review.find('a', {'data-hook': 'review-title'})
                if title_element:
                    full_title = title_element.text.strip()
                    title = ' '.join(full_title.split()[5:])
                else:
                    title = 'N/A'

                content = review.find('span', {'data-hook': 'review-body'})
                content = content.text.strip() if content else 'N/A'

                reviews.append({
                    'rating': rating,
                    'title': title,
                    'content': content
                })

            page += 1
            time.sleep(random.uniform(1, 3))  # 隨機延遲1到3秒

        all_reviews.append(reviews)

    return all_reviews



def parse_info(info_text):
    info_dict = {}
    lines = info_text.split('\n')
    for line in lines:
        parts = line.split(':')
        if len(parts) == 2:
            key = parts[0].strip()
            value = parts[1].strip()
            info_dict[key] = value
    return info_dict


response = requests.get(url, headers=custom_headers)
soup = BeautifulSoup(response.text, 'lxml')

title_element = soup.select_one('#productTitle')

title = title_element.text.strip()

# rating
rating_element = soup.select_one('#acrPopover')
rating_text = rating_element.attrs.get('title') if rating_element else 'Not found'
rating = rating_text.replace('out of 5 stars', '').strip() if rating_text else 'Not found'

# price
price_element = soup.select_one('span.a-offscreen')
price = price_element.text.strip() if price_element else 'Not found'

# img
image_element = soup.select_one('#landingImage')
image = image_element.attrs.get('src') if image_element else 'Not found'

# description
description_element = soup.select_one("#feature-bullets")
description = description_element.text.strip() if description_element else 'Not found'

# info
info_element = soup.find('table', {'id': 'productDetails_techSpec_section_1'}) or soup.find('table', {'id': 'productDetails_detailBullets_sections1'})
info = info_element.text.strip() if info_element else 'Not found'
info_dict = parse_info(info)

#reviews
result = get_amazon_reviews(reviewsUrl)



print(f"Name: {title}\n")
print(f"Rating: {rating} out of 5 stars\n")
print(f"Price: {price}\n")
print(f"Image: {image}\n")
print(f"Description: {description}\n")
print("Information: ", end='')
for key, value in info_dict.items():
    print(f"{key}: {value}")
print("\nReviews:")
star_words = ['5', '4', '3', '2', '1']
for i, reviews in enumerate(result):
    print(f"{star_words[i]} Star:")
    for j, review in enumerate(reviews, 1):
        print(f"{j}. Rating: {review['rating']}")
        print(f"Title: {review['title']}")
        print(f"Content: {review['content'][:500]}")