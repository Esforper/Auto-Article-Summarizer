from openai import OpenAI
import os

class GPTClient:
    def __init__(self, model="gpt-4o-mini"):
        self.model = model

    def generate_text(self, prompt,system_prompt):
        
        api_key = os.getenv("OPENAI_API_KEY")
        
        client = OpenAI(api_key = api_key)
        
        try:
            messages = []
            
            # Eğer sistem mesajı varsa ekliyoruz
            
            messages.append({"role": "system", "content": system_prompt})
            # Kullanıcıdan gelen prompt'u ekliyoruz
            messages.append({"role": "user", "content": prompt})
            
            response = client.chat.completions.create(
                model = self.model,
                messages = messages
            )
            
            print ("Generate text test " + response.choices[0].message.content)  
             
            return response.choices[0].message.content
            
        
        except Exception as e:
            print(f"Hata: {e}")
            return None
    


    def Generate_keywords(self,first_prompt):
        system_prompt = """Görevin sana verilen makale konusu ile ilgili google scholarda arama yapmak istesem hangi anahtar kelimeleri kullanmam gerekiyor
        bana bu kelimelerin bir listesini çıkar, her kelimeden sonra / koy, herhangi bir açıklama metni veya markdown bir metin yazma sadece bana kelime listesi çıkar.
        bu kelimeler için sırayla makale araştıracağım için olabildiğince konu ile alakalı kelimeler üret. her kelime için ayrı ayrı makale araştıracağım.
        örneğin sana sanal odyometre dersem anahtar kelime olarak şunları ver:
        odyometre / odyometri / sanal gerçeklik / sanal odyometre
        gibi, sana daha uzun metin verilirse de böyle böl
        """
         # API'den anahtar kelimeleri içeren yanıtı alıyoruz
        result_text = self.generate_text(first_prompt, system_prompt)
        print(result_text)
        
        # Yanıtı kontrol ediyoruz
        if result_text is None:
            print("Hata: GPT API'den bir yanıt alınamadı.")
            return []  # Boş liste döndürüyoruz        
        
        
        # Anahtar kelimeleri / karakterine göre ayırıyoruz
        keywords = [keyword.strip() for keyword in result_text.split("/") if keyword.strip()]
        
        # Anahtar kelimeler listesini döndürüyoruz
        return keywords
        