"""Yandex Translate Api Python Pyqt5
demirtaserdem@gmail.com
https://github.com/demirtaserdem/yandex-translate-api-python-pyqt5
"""

import requests
import os
import sys

from PyQt5.QtWidgets import QWidget,QApplication,QLineEdit,QPushButton
from PyQt5.QtWidgets import QMainWindow,QLabel,QVBoxLayout,QHBoxLayout
from PyQt5.QtWidgets import QTextBrowser,QMessageBox
from PyQt5.QtGui import QIcon

#Qwidget Class2ı
class Yta(QWidget):
    def __init__(self):
        super().__init__()
        #Program başlamadan önce son arananları temizliyor.
        self.clean_Last_Searched()
        self.init_ui()

    def init_ui(self):
        #Tasarım kısmı
        self.input_word_tag = QLabel("Kelimeyi Giriniz: ")
        self.input_word = QLineEdit()
        self.translate_button = QPushButton("Çevir")
        self.output_word_tag = QLabel("Çeviri: ")
        self.output_word = QLineEdit()
        #Çıkış kelimenin Sadece Okunur Şekilde Gözükmesi İçin
        self.output_word.setReadOnly(True)
        
        self.last_searched_area_tag = QLabel("Son Arananlar: ")
        self.last_searched_area = QTextBrowser()
        self.last_search_show_btn = QPushButton("Son Arananları Göster")
        self.last_search_clean_btn = QPushButton("Son Arananları Temizle")

        self.v_box = QVBoxLayout()
        self.v_box.addWidget(self.input_word_tag)
        self.v_box.addWidget(self.input_word)
        self.v_box.addWidget(self.output_word_tag)
        self.v_box.addWidget(self.output_word)

        #Çevir ve Geçmiş Aramaları göster butonunun yanyana durması için
        self.h_box_button = QHBoxLayout()
        self.h_box_button.addWidget(self.last_search_show_btn)
        self.h_box_button.addWidget(self.translate_button)
        self.v_box.addLayout(self.h_box_button)
        
        self.v_box.addWidget(self.last_searched_area_tag)
        self.v_box.addWidget(self.last_searched_area)
        self.v_box.addWidget(self.last_search_clean_btn)
        self.v_box.addStretch()

        self.h_box = QHBoxLayout()
        self.h_box.addStretch()
        self.h_box.addLayout(self.v_box)
        self.h_box.addStretch()

        self.setLayout(self.h_box)
        #Tasarım kısmı sonu

        #Butonlara Fonksiyonların Bağlanması
        #Kelimeyi girip entera basılırsa
        self.input_word.returnPressed.connect(self.translate_input)		
        #Butonlara tıklandığında
        self.translate_button.clicked.connect(self.translate_input)
        self.last_search_show_btn.clicked.connect(self.printLastSearch)
        self.last_search_clean_btn.clicked.connect(
            self.clean_Last_Searched_with_sure)

    def translate_input(self):
        """Çevir butonu fonksiyonu
        """ 
        #Kelimenin boş karakterli olup olmadığını kontrol.
        if self.input_word.text().strip():
            self.create_url()
            self.translateFunc()
            self.writeLastSearch()

    def create_url(self):
        #Yandex Apide Çeviri Url İsteğni oluşturmak için kısımlara ayrıldı.
        #"https://tech.yandex.com/translate/doc/dg/reference/
        # translate-docpage/JSON"
        #temel alınarak oluşturulmuştur.
        #Url'nin ilk değişmeeyen kısmı
        base_url ="https://translate.yandex.net/api/v1.5/tr.json/translate"
        # Api key yandex translate tarafından alınacak.
        # "https://translate.yandex.com/developers/keys"
        key = ("?key=trnsl.1.1.20190121T100542Z.4befbb4bba198843."
            +"b6081dd6370342a5c61258dbb83fb7b9a58dd523")
        #arama yapacağımız kelime - metindir. ilk url oluşturulurken 
        #"Merhaba" yazılmıştır, text = Str() oluşturulabilir.
        self.text = self.input_word.text().strip()
        #url'nin devamı kullanılan bir sabit
        base_text = "&text="
        #Çevirilmesi istenen dil değişkeni
        lang = "en" 
        #tr- kısmı çevrinmesi istenen dilin otomatik algılamasını kapatıp
        #türkçeden çeviri yapılmasını sağlıyor. örn. "&lang=tr-eng" ya da
        # otomatik: "&lang=eng" olarak yazılabilir.
        base_lang = "&lang=tr-"
        #oluşan temel url
        self.translate_url = (base_url + key+base_lang + lang + base_text
            + self.text)  

    def translateFunc(self):
        """Oluşturulan url'ye istek gönderir, alır, json objesine çevirir
        json objesinin içinden ilgili kısmı dataya yazar. Çevriyi Str 
        olarak döndürür.
        """
        data_get = requests.get(self.translate_url)
        data_json = data_get.json()
        self.data = data_json["text"][0]
        self.input_word.setText("")
        
    def writeLastSearch(self):
        """Çevrilen ve çeviri kelimeyi str olarak alır,
        last_searchs.txt dosyasına yazar konsola yazabiliyorsa yazar, 
        utf-8 hatasından - çince vs hata olursa hata mesajı verir.
        """
        with open("last_searchs.txt","a",encoding = "utf-8") as file:
            file.write(self.text +" --->>> "+ self.data + "\n")
        try:
            self.output_word.setReadOnly(False)
            self.output_word.setText(self.text + " --->>> " + self.data)
            self.output_word.setReadOnly(True)
        except:
            print("""Konsola yazdırırken hata oluştu... txt dosyasını 
                kontrol edebilirsiniz. \n""")

    def printLastSearch(self):
        """Son Arananların listesini
        last_searchs.txt den alır. yazdırır
        """
        #last_searchs.txt olmamısın durumu için hata denetimi.
        try:
            #Dosyanın Boş Olup olmadığı kontol edilmiştir
            if os.stat("last_searchs.txt").st_size == 0:
                self.last_searched_area.setText("Son Aranan Kelime" 
                    +"Bulunmamaktadır.")
            else:
                with open("last_searchs.txt","r",encoding = "utf-8") as file:
                    self.last_searched_area.setText(file.read())
        except:
            pass
            
    def clean_Last_Searched_sure(self):
        """Mesaj penceresi ile emin misinin sorusu sorar.
        duruma göre true veya false olarak dönüş yaptırır.
        """
        qm = QMessageBox()
        ret = qm.question(self,'Emin Misiniz?',"Son Arananları " 
            +"Silmek İstediğinizden Emin misiniz?",qm.Yes | qm.No)
        if ret == qm.Yes:
            return True
        else:
            return False
    
    def clean_Last_Searched(self):
        """last_searchs.txt dosyasının temizlenmesini ve oluşmasını
        sağlar
        """
        open("last_searchs.txt","w",encoding = "utf-8").close()
        self.printLastSearch()
    
    def clean_Last_Searched_with_sure(self):
        """Emin misin messageboxla birlikte son arananlar temizleme 
        işlemi
        """
        if self.clean_Last_Searched_sure():
            self.clean_Last_Searched()

class Menu(QMainWindow):
    """Daha sonra geliştirilebilmesi için QMainwindow nesnesi
    içine QWidget eklenmiştir 
    """
    def __init__(self):
        super().__init__()
        self.yta = Yta()
        self.setCentralWidget(self.yta)
        self.create()

    def create(self):
        """Pencereyi oluşturur konumunu ayarlar title ve iconu ayarlar.
        """
        self.setGeometry(300,200,350,300)
        self.setWindowTitle("Yandex Translate Api")
        self.setWindowIcon(QIcon(self.resource_path('icon1.ico')))
        self.show()

    def resource_path(self,relative_path):
        """ Get absolute path to resource, works for dev and for 
        PyInstaller 
        """
        #Pyinstaller sys modülünde geçici olarak _meipass özelliği 
        #oluşturuyor.Oluşmamışsa 
        # os.path.dirname(os.path.abspath(__file__)) çağrılıyor.
        base_path = getattr(sys, '_MEIPASS', 
            os.path.dirname(os.path.abspath(__file__)))

        return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = Menu()
    sys.exit(app.exec_())

