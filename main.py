import datetime
import os
import sqlite3
import subprocess
import time

from bs4 import BeautifulSoup
import requests
import playsound as playsound
import speech_recognition as sr
from gtts import gTTS
import webbrowser

rec = sr.Recognizer()


class Sesli_asistan():
    def __init__(self):
        self.rec = sr.Recognizer()
        self.name = ""
        self.city = ""
        self.firstDate()
        """while True:
            voice=self.record()
            if voice!="":
                self.wakeUp(voice.lower())"""

    """def wakeUp(self,voice):
        if "hey" in voice or "asistan" in voice:
            self.speak("sizi dinliyorum.")
            self.firstDate()"""

    def speak(self, speech):
        tts = gTTS(text=speech, lang="tr")
        file = "answer.mp3"
        tts.save(file)
        playsound.playsound(file)
        os.remove(file)

    def record(self):
        print("Seni dinliyorum...")
        with sr.Microphone() as mic:
            audio = rec.listen(mic, phrase_time_limit=5)
            self.voice = ""
            print("burada")
            try:
                self.voice = rec.recognize_google(audio, language="tr-TR")
            except sr.UnknownValueError:
                self.speak("Ne dediğini anlayamadım.")
            except sr.RequestError:
                self.speak("Sistemle ilgili bir hata oluştu.")
                self.exitTheProgram()
            return self.voice

    def firstDate(self):
        con = sqlite3.connect('C:\\Users\\enesg\\OneDrive\\Masaüstü\\test.sqlite')
        cursor = con.cursor()
        cursor.execute(" CREATE TABLE IF NOT EXISTS USER(Name varchar(20),Surname varchar(20))")
        con.commit()

        cursor.execute("SELECT * FROM USER")
        self.name = cursor.fetchall()
        if len(self.name) == 0:
            self.speak("Merhaba. Ben senin yeni sesli asistanınım. Adın nedir?")
            self.name = self.record()
            self.name_list = self.name.split(" ")

            cursor.execute("INSERT INTO USER VALUES(?,?)", (self.name_list[0], self.name_list[1]))
            con.commit()

            cursor.execute("SELECT * FROM USER")
            self.name = cursor.fetchall()
            self.welcome()
        else:
            self.welcome()

    def welcome(self):
        self.hour = datetime.datetime.now().hour
        if (self.hour > 7 and self.hour < 12):
            self.speak("Günaydın", self.name[0], [0])
        elif (self.hour >= 12 and self.hour < 18):
            self.speak("Tünaydın " + self.name[0][0])
        elif (self.hour >= 18 and self.hour < 22):
            self.speak("İyi Akşamlar " + self.name[0][0])
        else:
            self.speak("İyi Geceler " + self.name[0][0])
        self.doWhatTold()

    def doWhatTold(self):
        self.speak("Sana nasıl yardımcı olabilirim")
        voice = self.record()
        voice = voice.lower()
        if "hava durumu" in voice:

            self.speak("hangi şehrin hava durumunu istiyorsunuz?")
            self.city = self.record()
            self.city = self.city.lower()
            self.city = self.city.replace("ı", "i")
            url = "https://www.hurriyet.com.tr/hava-durumu/" + self.city + "/"
            request = requests.get(url)
            dataThatCame = request.content
            soup = BeautifulSoup(dataThatCame, "html.parser")
            status = (soup.find_all("p", {"class": "weather-detail-condition-text"}))
            temperature = (soup.find_all("p", {"class": "weather-detail-hightemp"}))
            statusOfCity = []
            temperatureOfCity = []
            for i in status:
                i = i.text
                statusOfCity.append(i)
            for i in temperature:
                i = i.text
                temperatureOfCity.append(i)

            weather = "Bugün" + self.city + "için hava sıcaklığı" + temperatureOfCity[0] + " ve " + statusOfCity[0]
            self.speak(weather)
            time.sleep(5)
            self.reListen()
        elif "kimsin" in voice or "adın ne" in voice:
            self.speak("Benim adım Siri ve senin sesli asistanınım.")
            time.sleep(5)
            self.reListen()
        elif "nasılsın" in voice or "nasıl gidiyor" in voice:
            self.speak("Sana yardımcı oldukça daha iyi oluyorum")
            time.sleep(5)
            self.reListen()
        elif "saat kaç" in voice:  # tamamlandi
            saat = "Saat şu anda " + str(datetime.datetime.now().hour) + " " + str(datetime.datetime.now().minute)
            self.speak(saat)
            time.sleep(5)
            self.reListen()

        elif "hesap makinesi" in voice or "hesapla" in voice:
            os.startfile("calc.exe")
            time.sleep(5)
            self.reListen()
        elif "kimdir" in voice or "kim" in voice:
            voice = voice.split()
            who = ""
            for i in range(len(voice) - 1):
                who += voice[i] + " "
            who = who.strip()
            who = who.replace(" ", "_")
            webbrowser.open("https://tr.wikipedia.org/wiki/" + who)
            time.sleep(5)
            self.reListen()

        elif "nedir" in voice or "nasıldır" in voice:

            # https://www.google.com/search?q=programlama+dili+nedir&
            self.voice = self.voice.replace(" ", "+")
            self.voice = self.voice.lower()
            webbrowser.open("https://www.google.com/search?q={}&".format(self.voice))
            time.sleep(5)
            self.reListen()

        elif "youtube" in voice:
            self.speak("YouTube açılıyor")
            webbrowser.open("https://www.youtube.com/")
            time.sleep(5)
            self.reListen()

        elif "netflix" in voice:
            self.speak("Netflix açılıyor")
            webbrowser.open("https://www.netflix.com/tr/")
            time.sleep(5)
            self.reListen()

        elif "kamera" in voice:
            subprocess.run('start microsoft.windows.camera:', shell=True)
            time.sleep(5)
            self.reListen()
        elif "film" in voice:
            self.speak("Hangi tür filmi izlemek istersin?")
            voice = self.record()
            voice = voice.replace(" ", "-")
            voice = voice.lower()
            webbrowser.open("https://hdfilmizle.pro/filmizle/{}/".format(voice))
            self.speak("{} türü için bulduğum filmler".format(voice))
            time.sleep(5)
            self.reListen()

        elif "not et" in voice or "not tut" in voice:
            self.speak("not defterinin adı ne olsun")
            nameOfTheTxt=self.record()+".txt"
            self.speak("Not etmek istediklerini söyleyebilirsin.")
            text=self.record()
            file=open(nameOfTheTxt,"w",encoding="utf-8")
            file.writelines(text)
            file.close()
            time.sleep(5)
            self.reListen()

        """elif "uykuda bekle" in voice or "uyu" in voice:
            self.speak("isteğin üzerine uykuya geçiyorum.")
            self.speak("istediğin zaman ismimi söyleyerek beni uyandırabilirsin.")
            with sr.Microphone as mic:
                audio = rec.listen(mic, phrase_time_limit=15)
                self.voice = ""
                try:
                    self.voice = rec.recognize_google(audio, language="tr-TR")
                except sr.UnknownValueError:
                    self.speak("Ne dediğini anlayamadım.")
                except sr.RequestError:
                    self.speak("Sistemle ilgili bir hata oluştu.")
                    self.exitTheProgram()

                if "siri" in voice:
                    self.reListen()"""








    def reListen(self):
        self.speak("Başka bir isteğin var mı ?")
        voice = self.record()
        voice = voice.lower()
        if "hayır" in voice or "teşekkür ederim" in voice or "yok" in voice:
            self.exitTheProgram()
        else:
            self.doWhatTold()

    def exitTheProgram(self):
        quit()


Sesli_asistan()