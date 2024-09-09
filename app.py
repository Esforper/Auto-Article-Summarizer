from flask import Flask, render_template, request, redirect, url_for
from Scraper import ScholarScraper
from ApiManager import GPTClient
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']  # Kullanıcının girdiği makale konusu
        apiManager = GPTClient()
        
        keyword_List = apiManager.Generate_keywords(query)
        #arama yapılacak kelimeleri listele
        keyword_List.insert(0,query)
        print (keyword_List)
        
        
        
        # Burada web scraping veya API sorgulama gibi işlemleri yapabilirsiniz.
        # Şimdilik basit bir çıktıyla kullanıcıya aranan konuyu göstereceğiz.
        scraper = ScholarScraper()
        scraper.search(query)
        # Sonuçları alıyoruz
        pdf_links, titles = scraper.get_results()
        scraper.close()        
        print(query)
        return render_template('results.html', titles=titles)

if __name__ == '__main__':
    app.run(debug=True)
