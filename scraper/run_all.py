from propertyfinder_scraper import scrape_propertyfinder
# from cbe_rates import scrape_cbe_rates
import pandas as pd

if __name__ == "__main__":
    print("Scraping PropertyFinder...")
    pf = scrape_propertyfinder(max_pages=15)
    print(f"Got {len(pf)} listings")
    
    # print("Scraping CBE rates...")
    # rates = scrape_cbe_rates()
    
    pf.to_parquet('data/processed/scraped_latest.parquet', index=False)
    print("Scraping complete!")