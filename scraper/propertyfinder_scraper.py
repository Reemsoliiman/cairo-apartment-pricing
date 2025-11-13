from playwright.sync_api import sync_playwright
import pandas as pd
import time
import random

def scrape_propertyfinder(max_pages=10):
    data = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = context.new_page()
        
        for page_num in range(1, max_pages + 1):
            url = f"https://www.propertyfinder.eg/en/search/c=1/l=5..8/t=2..4/bed=2..3?page={page_num}"
            page.goto(url, timeout=60000)
            page.wait_for_timeout(5000 + random.randint(1000, 3000))
            
            cards = page.query_selector_all('div[data-testid="property-card"]')
            for card in cards:
                try:
                    price = card.query_selector('span[data-testid="price"]')
                    area = card.query_selector('span[data-testid="size"]')
                    beds = card.query_selector('span[data-testid="beds"]')
                    location = card.query_selector('p[data-testid="locations"]')
                    compound = card.query_selector('span[data-testid="compound"]')
                    
                    data.append({
                        'price_egp': int(price.inner_text().replace('EGP', '').replace(',', '').strip()) if price else None,
                        'area_sqm': int(area.inner_text().split()[0]) if area else None,
                        'bedrooms': int(beds.inner_text()) if beds else None,
                        'district': location.inner_text().split(',')[-1].strip() if location else 'Unknown',
                        'compound_name': compound.inner_text().strip() if compound else '',
                        'listing_date': pd.Timestamp.now().strftime('%Y-%m-%d'),
                        'source': 'propertyfinder'
                    })
                except: continue
        browser.close()
    return pd.DataFrame(data)