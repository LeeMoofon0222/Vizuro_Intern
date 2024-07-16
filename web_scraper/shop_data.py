from bs4 import BeautifulSoup
import requests
import time
from urllib.parse import urlparse, parse_qs
import random
from openai import OpenAI
import os
from dotenv import load_dotenv



def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
    )
    return response.choices[0].message.content

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


load_dotenv()
client = OpenAI(
  api_key=os.getenv('OPENAI_API_KEY'),
)
url = 'https://www.amazon.com/15-ProMax-Smartphone-Unlocked-Titanium/dp/B0D8RTFQYC/ref=sr_1_1_sspa?crid=3V9KY9NC5MV1Y&dib=eyJ2IjoiMSJ9.mR8oGuhsfH89CRAntrdspl2mOUTcZys3zCJNaMnrIWMECkNwcx4dA0mRCF8gi75OtsxjfPnH3siSn-z-i6uIpKRboRAuT-DGn_Iy4aT6POuyblQRGzP_oZ3HWxaXPOS9UW7rqXJQnKo4NiHjcXpSI_l-M3B-68lAGYWuGOBRfizMdnmBRtSMj_9KM1h6b-hKKxmobEgQe4SHD9fi452ZxkjmF4kn3CQ9pQDrLUW18Cw.zX1e2kBLWLDmD0jqqTyMmop4vXI9i5D5v37PwwdS-Ng&dib_tag=se&keywords=phone&qid=1721118237&sprefix=phone%2Caps%2C294&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1'
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
info_element = soup.find('table', {'id': 'productDetails_techSpec_section_1'}) or soup.find('table', {'id': 'productDetails_detailBullets_sections1'}) or soup.select_one("#prodDetails")
info = info_element.text.strip() if info_element else 'Not found'
info_dict = parse_info(info)

#reviews
result = get_amazon_reviews(reviewsUrl)

text = f"Name: {title}\nRating: {rating} out of 5 stars\nPrice: {price}\nImage: {image}\nDescription: {description}\nInformation: "
for key, value in info_dict.items():
    text += f"{key}: {value}\n"
text += "Reviews:\n"
star_words = ['5', '4', '3', '2', '1']
for i, reviews in enumerate(result):
    text += f"{star_words[i]} Star:\n"
    for j, review in enumerate(reviews, 1):
        text += f"{j}. Rating: {review['rating']}\nTitle: {review['title']}\nContent: {review['content'][:500]}\n"

# prompt = "Please analysis the product, includes its advantages, disadvantages and make a conclution\n" + text

# print(get_completion(prompt).strip())

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