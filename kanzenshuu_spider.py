import scrapy
import json
from urllib.parse import urljoin
import logging


class KanzenshuuSpider(scrapy.Spider):
    name = 'kanzenshuu_manga'
    allowed_domains = ['kanzenshuu.com']
    
    # Custom settings for the spider
    custom_settings = {
        'DOWNLOAD_DELAY': 1,  # Be respectful - 1 second delay between requests
        'RANDOMIZE_DOWNLOAD_DELAY': 0.5,  # Randomize delay (0.5 to 1.5 seconds)
        'CONCURRENT_REQUESTS': 1,  # Process one request at a time
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'FEED_EXPORT_ENCODING': 'utf-8',  # Ensure UTF-8 encoding
        'FEED_EXPORT_FIELDS': ['chapter_id', 'url', 'chapter_date', 'wj_toriyama_text', 'wj_toriyama_html', 'links_in_div', 'status']
    }

    logger = logging.getLogger()

    def start_requests(self):
        """Generate URLs for all chapters from chp-001 to chp-591"""
        base_url = 'https://www.kanzenshuu.com/manga/db/'

        for chapter_num in range(1, 592):  # 1 to 591 inclusive
            chapter_id = f"chp-{chapter_num:03d}"  # Format as chp-001, chp-002, etc.
            url = urljoin(base_url, chapter_id)
            
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={'chapter_id': chapter_id}
            )
    
    def parse(self, response):
        """Parse each chapter page and extract the wj_toriyama div"""
        chapter_id = response.meta['chapter_id']
        
        # Check if the page loaded successfully
        if response.status != 200:
            self.logger.warning(f"Failed to load {response.url} - Status: {response.status}")
            return
        
        # Extract the div with class "wj_toriyama"
        wj_toriyama_divs = response.css('div.wj_toriyama')
        wj_chapter_date = response.css(".odd *::text").getall()
        self.logger.info(f"Chapter date: {wj_chapter_date}")
        
        if wj_toriyama_divs:
            for div in wj_toriyama_divs:
                # Extract all text content from the div
                text_content = div.css('::text').getall()
                text_content = [text.strip() for text in text_content if text.strip()]
                
                # Extract all HTML content from the div
                html_content = div.get()
                
                # Extract any links within the div
                links = div.css('a::attr(href)').getall()

                # Extract chapter date and Shonen Jump issue
                chapter_date = "".join(wj_chapter_date).replace('\n', '').replace('Premiered:', '')

                yield {
                    'chapter_id': chapter_id,
                    'url': response.url,
                    'chapter_date': chapter_date,
                    'wj_toriyama_text': ' '.join(text_content),
                    'wj_toriyama_html': html_content,
                    'links_in_div': links,
                    'status': 'found'
                }
        else:
            # Log when no wj_toriyama div is found
            self.logger.info(f"No wj_toriyama div found in {chapter_id}")
            yield {
                'chapter_id': chapter_id,
                'url': response.url,
                'wj_toriyama_text': None,
                'wj_toriyama_html': None,
                'links_in_div': [],
                'status': 'not_found'
            }


# Additional utility script to run the spider
if __name__ == '__main__':
    """
    To run this spider with proper Japanese character support:
    
    For JSON with readable Japanese characters:
    scrapy runspider kanzenshuu_spider.py -o results.json -s FEED_EXPORT_ENCODING=utf-8
    
    For CSV (often better for Japanese text):
    scrapy runspider kanzenshuu_spider.py -o results.csv
    
    For JSON Lines format (recommended for large datasets):
    scrapy runspider kanzenshuu_spider.py -o results.jsonl
    """
    print("To run this spider with proper Japanese character support:")
    print("1. Install scrapy: pip install scrapy")
    print("2. For JSON: scrapy runspider kanzenshuu_spider.py -o results.json")
    print("3. For CSV: scrapy runspider kanzenshuu_spider.py -o results.csv")  
    print("4. For JSONL: scrapy runspider kanzenshuu_spider.py -o results.jsonl")
    print("5. Results will preserve Japanese characters correctly")

