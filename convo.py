import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import matplotlib.pyplot as plt
import time

def benimKonvolusyon(x, y):
    x = np.array(x, dtype=np.float64)
    y = np.array(y, dtype=np.float64)
    
    xUzunluk = len(x)
    yUzunluk = len(y)
    
    sonuc = np.zeros(yUzunluk + xUzunluk - 1, dtype=np.float64)
    
    for i in range(xUzunluk):
        for j in range(yUzunluk):
            sonuc[i + j] += x[i] * y[j]   
    return sonuc


x = []
y = []
xUzunluk = int(input("x dizisinin uzunlugunu giriniz: "))
xBaslangic = int(input("x dizisinin koordinat duzleminde basladigi noktayi giriniz (Orn: -2): "))
for i in range(xUzunluk):
    print(f"x[{i}] ({xBaslangic + i} noktasindaki deger): ", end="")
    temp = float(input())
    x.append(temp)
yUzunluk = int(input("y dizisinin uzunlugunu giriniz: "))
yBaslangic = int(input("y dizisinin koordinat duzleminde basladigi noktayi giriniz (Orn: -2): "))
for i in range(yUzunluk):
    print(f"y[{i}] ({yBaslangic + i} noktasindaki deger): ", end="")
    temp = float(input())
    y.append(temp)

sonuc = benimKonvolusyon(x, y)

xKonumlar = list(range(xBaslangic, xBaslangic + xUzunluk))
print(xKonumlar)
xSifirIndeksi = -xBaslangic if -xBaslangic in xKonumlar else None
yKonumlar = list(range(yBaslangic, yBaslangic + yUzunluk))
print(yKonumlar)
ySifirIndeksi = -yBaslangic if -yBaslangic in yKonumlar else None
sonucKonumlar = list(range(xBaslangic + yBaslangic, xBaslangic + yBaslangic + len(sonuc)))
sonucSifirIndeksi = -(xBaslangic + yBaslangic) if -(xBaslangic + yBaslangic) in sonucKonumlar else None

print("X:", x)
print("X'te 0'in bulundugu index:", xSifirIndeksi)
print("Y:", y)
print("Y'de 0'in bulundugu index:", ySifirIndeksi)
print("Benim Fonskiyonumun Konvolusyon Sonucu:", sonuc)
print("Benim Fonksiyonumun Sonucunda 0'in bulundugu index:", sonucSifirIndeksi)
hazirFonksiyonSonuc = np.convolve(x, y)
print("Np.Convolve Sonucu:", hazirFonksiyonSonuc)

plt.figure(figsize=(10, 8))  

plt.subplot(2, 2, 1)  
plt.stem(xKonumlar, x, 'b')
plt.xlabel("Time")  
plt.ylabel("Amplitude")
plt.title("x[n] Fonksiyonu")

plt.subplot(2, 2, 2)  
plt.stem(yKonumlar, y, 'r')
plt.xlabel("Time")  
plt.ylabel("Amplitude")
plt.title("y[n] Fonksiyonu")

plt.subplot(2, 2, 3)  
plt.stem(sonucKonumlar, sonuc, 'c')
plt.xlabel("Time")  
plt.ylabel("Amplitude")
plt.title("Benim Konvolusyon Fonksiyonum")

plt.subplot(2, 2, 4)  
plt.stem(sonucKonumlar, hazirFonksiyonSonuc, 'k')
plt.xlabel("Time")  
plt.ylabel("Amplitude")
plt.title("Hazir Konvolusyon Fonksiyonu")

plt.tight_layout() 
plt.show()

fs = 10000
sd.default.samplerate = fs
kayitSureleri = [5, 10]  
mDegerleri = [3, 4, 5]    

for kayit_suresi in kayitSureleri:
    print(f"{kayit_suresi} Saniyelik ses kaydi basladi.\n")
    try:
        ses_kaydi = sd.rec(int(kayit_suresi * fs), samplerate=fs, channels=1)
        sd.wait()
        print("Bitti")
        write(f'input{kayit_suresi}.wav', fs, ses_kaydi) 
        kayit_sonucu = np.array(ses_kaydi).flatten()
    except Exception as e:
        print(f"Kaydederken hata olustu: {e}")

    for m in mDegerleri:
        print(f"\nM = {m} için islemler basladi\n")
        A = 0.5
        
        h = np.zeros(m * 400 + 1, dtype=np.float64)
        
        h[0] = 1
        for i in range(m):
            h[(i + 1) * 400] = A * (i + 1)

        print("\nHazır Fonksiyon\n")
        start_time_hazir = time.time()
        convolved = np.convolve(kayit_sonucu, h)
        end_time_hazir = time.time()
        print(f"Hazir fonksiyonun calisma suresi: {end_time_hazir - start_time_hazir} saniye")
        print("Ses oynatiliyor.")
        sd.play(convolved, blocking=True)
        print("Oynatma bitti.")
        write(f'output{kayit_suresi}_hazir_m{m}.wav', fs, convolved) 
        
        print("\nBenim Fonksiyonum\n")
        start_time_benim = time.time()
        konvolusyon_sonucu = benimKonvolusyon(kayit_sonucu, h)
        end_time_benim = time.time()
        print(f"Benim fonksiyonumun calisma suresi: {end_time_benim - start_time_benim} saniye")
        konvolusyon_sonucu = konvolusyon_sonucu.astype(np.float32)
        print("Ses oynatiliyor.")
        sd.play(konvolusyon_sonucu, blocking=True)
        print("Oynatma bitti.")
        write(f'output{kayit_suresi}_benim_m{m}.wav', fs, konvolusyon_sonucu)

print("Program sonlaniyor...")