import requests
from bs4 import BeautifulSoup

articles_data = []  # 크롤링한 기사 데이터를 저장할 리스트

def crawl_article(article_url):
    try:
        response = requests.get(article_url)
        response.raise_for_status()  # 오류 발생 시 예외 처리
        soup = BeautifulSoup(response.text, 'html.parser')

        # 기사 제목
        title = soup.find('h1', class_='headline')
        title = title.get_text() if title else '제목 없음'

        # 기사 날짜
        date = soup.find('span', class_='txt-date')
        date = date.get_text() if date else '날짜 없음'

        # 기사 요약 (선택적)
        summary = soup.find('meta', {'name': 'description'})
        summary = summary.get('content') if summary else '요약 없음'

        # 기사 본문
        body = soup.find('div', class_='article-body')  # 여기서 클래스 수정
        if body:
            body = body.get_text(strip=True)
        else:
            body = '본문 내용 없음'
        #  저장 (본문을 리스트 형태로 저장)
        article_data = {
            'title': title,
            'date': date,
            'summary': summary,
            'body_chunks': body,  # 분리된 본문
            'url': article_url
        }
        articles_data.append(article_data)
        print(f"크롤링 완료: {len(body)}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {article_url}: {e}")

# -----------------------------
# 기사 크롤링 URL
# -----------------------------
base_url = "https://www.hankyung.com/economy/economic-policy?page="
marco_url="https://www.hankyung.com/economy/macro?page="
save_url=[base_url,marco_url]
for select_url in save_url:
  print(select_url)
  for page_num in range(1, 7):
      url = select_url + str(page_num)
      response = requests.get(url)
      soup = BeautifulSoup(response.text, 'html.parser')
      news_items = soup.find_all('div', class_='news-item')

      for item in news_items:
          link = item.find('a', href=True)
          if link:
              article_url = link['href']
              crawl_article(article_url)
