from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

class ScholarScraper:
    def __init__(self):
        # Microsoft Edge seçeneklerini ayarlıyoruz
        self.edge_options = Options()
        self.edge_options.add_argument("--headless")  # Headless mod
        self.edge_options.add_argument("--no-sandbox")
        self.edge_options.add_argument("--disable-dev-shm-usage")

        # Edge WebDriver yolunu belirtiyoruz
        self.driver_service = Service('C:/DRIVERS/msedgedriver.exe')  # msedgedriver yolunu belirtin

        # Edge WebDriver'ı başlatıyoruz
        self.driver = webdriver.Edge(service=self.driver_service, options=self.edge_options)

    def search(self, query):
        # Google Scholar ana sayfasını açıyoruz
        self.driver.get("https://scholar.google.com")

        # Arama kutusunu buluyoruz ve arama terimini giriyoruz
        search_box = self.driver.find_element("name", "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)  # Enter tuşuna basılıyor

        # Sayfanın yüklenmesi için bekleme
        time.sleep(3)

    def get_results(self):
        # Sayfanın HTML kaynağını alıyoruz
        page_source = self.driver.page_source

        # BeautifulSoup ile HTML'yi parse ediyoruz
        soup = BeautifulSoup(page_source, 'html.parser')

        # Belirli bir ID'ye sahip elementi buluyoruz
        gs_res_ccl_mid = soup.find(id="gs_res_ccl_mid")

        # PDF linklerini ve başlıkları toplamak için listeler
        pdf_links = []
        titles = []

        if gs_res_ccl_mid:
            # Tüm makale div'lerini buluyoruz
            for item in gs_res_ccl_mid.find_all("div", class_="gs_r gs_or gs_scl"):
                # PDF bağlantılarını topluyoruz
                pdf_link = item.find("a", href=True, text="[PDF]")
                if pdf_link:
                    pdf_url = pdf_link['href']
                    pdf_text = pdf_link.text
                    pdf_links.append((pdf_text, pdf_url))

                # Başlıkları topluyoruz
                title_link = item.find("h3", class_="gs_rt").find("a", href=True)
                if title_link:
                    title_text = title_link.text
                    title_url = title_link['href']
                    titles.append((title_text, title_url))

        return pdf_links, titles
    
    def close(self):
        # WebDriver'ı kapatıyoruz
        self.driver.quit()
