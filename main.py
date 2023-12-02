import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request

app = Flask(__name__)


def scrape_and_summarize(url):
  try:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string if soup.title else "No Title Found"
    article = soup.find('article') or soup.find('div',
                                                class_='article-content')
    summary = article.get_text(
        separator='\n').strip() if article else "No Content Found"
    return title, summary
  except Exception as e:
    return "Error", f"Failed to scrape {url}: {str(e)}"


@app.route('/scrape', methods=['POST'])
def scrape_url():
  url = request.json.get('url') if request.json else None
  if url:
    title, summary = scrape_and_summarize(url)
    markdown_summary = f"# {title}\n\n## Summary\n{summary}\n"
    return jsonify({'markdown_summary': markdown_summary})
  return jsonify({'error': 'Invalid request. URL not provided.'}), 400


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
