import requests
from bs4 import BeautifulSoup
import openai

def fetch_webpage_text(url):
    response = requests.get(url)
    response.raise_for_status()  # 確保請求成功
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text()


# 測試程式碼
url = "https://www.amazon.com/acer-Wireless-Non-Stop-Bluetooth5-3-Headphones/dp/B0CLYH2DRN/ref=sxin_16_sbv_search_btf?_encoding=UTF8&content-id=amzn1.sym.5cde1a09-4942-4242-87c5-e66d2d3b6a3c%3Aamzn1.sym.5cde1a09-4942-4242-87c5-e66d2d3b6a3c&cv_ct_cx=gaming%2Bheadsets&dib=eyJ2IjoiMSJ9.TeAUh4HrECihko2sKZE51A.xRjBuwPbdpYMBu2C2UUuuHjCaoLfZyIWg3SkYJrDOj4&dib_tag=se&keywords=gaming%2Bheadsets&pd_rd_i=B0CLYH2DRN&pd_rd_r=4661825c-41b4-4c76-9336-50c5cab08f62&pd_rd_w=nRXZa&pd_rd_wg=xcMyO&pf_rd_p=5cde1a09-4942-4242-87c5-e66d2d3b6a3c&pf_rd_r=V1EE101AZPK8M3J5934A&qid=1720420093&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sr=1-1-5190daf0-67e3-427c-bea6-c72c1df98776&th=1"
webpage_text = fetch_webpage_text(url)
print(webpage_text)
