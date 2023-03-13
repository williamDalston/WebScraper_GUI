import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import threading

SAVE_DIR = '/Users/alston/Desktop/scripts/'

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Web Scraper')
        self.geometry('400x150')

        ttk.Label(self, text='Enter a URL to scrape:').pack(side=tk.TOP, padx=5, pady=5)
        self.url_entry = ttk.Entry(self, width=50)
        self.url_entry.pack(side=tk.TOP, padx=5, pady=5)

        self.run_button = ttk.Button(self, text='Run', command=self.run_web_scraper)
        self.run_button.pack(side=tk.TOP, padx=5, pady=5)

        self.progress_bar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.progress_bar.pack(side=tk.TOP, padx=5, pady=5)

        self.output_label = ttk.Label(self, text='')
        self.output_label.pack(side=tk.TOP, padx=5, pady=5)

    def run_web_scraper(self):
        self.run_button.config(state=tk.DISABLED)
        self.output_label.config(text='')

        url = self.url_entry.get()

        t = threading.Thread(target=self.run_web_scraper_thread, args=(url,))
        t.start()

    def run_web_scraper_thread(self, url):
        filename = os.path.basename(url)
        save_path = os.path.join(SAVE_DIR, f'{filename}.txt')

        scraped_links = set()

        def scrape_links(url):
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                text = soup.get_text()

                with open(save_path, 'a') as f:
                    f.write(text)

                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href is not None and href.endswith('.htm'):
                        full_href = urljoin(url, href)
                        if full_href.count('/') == url.count('/'):
                            if full_href not in scraped_links:
                                scraped_links.add(full_href)
                                scrape_links(full_href)

                                self.progress_bar.step(1)
                                self.progress_bar.update_idletasks()

            else:
                print(f'Response status code {response.status_code} for URL: {url}')

        scrape_links(url)
        messagebox.showinfo('Web Scraper', 'Web scraping is complete.')
        self.run_button.config(state=tk.NORMAL)

if __name__ == '__main__':
    App().mainloop()
