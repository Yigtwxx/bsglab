# Yildiz Cipher (Yıldız Şifreleme Aracı)

Bu proje, metin tabanlı şifreleme ve şifre çözme işlemlerini gerçekleştiren, Python ile yazılmış bir konsol uygulamasıdır. Ayrıca şifreleme algoritmasının ne kadar güvenilir olduğunu ölçmek için "Çığ Etkisi"ni (Avalanche Effect) test etme özelliğine sahiptir.

## Özellikler

- **Metin Şifreleme:** Girdiğiniz metni özel bir anahtar ile şifreler (Hexadecimal çıktı üretir).
- **Şifre Çözme:** Hex formatındaki şifreli metni orijinal haline döndürür.
- **Çığ Etkisi (Avalanche Effect) Testi:** Metindeki çok küçük (1 karakterlik veya 1 bitlik) değişimin, şifreli metnin ne kadarını değiştirdiğini oran olarak hesaplar.

## Dosya Yapısı

- `cipher.py`: Şifreleme algoritmasını içeren (YildizCipher) temel sınıftır.
- `main.py`: Kullanıcının işlem yapabilmesi için tasarlanmış ana menüyü içerir.
- `test_cipher.py`: Sistem fonksiyonlarının testlerini içerir.

## Kullanım

Projeyi çalıştırmak için terminal (veya komut satırı) üzerinden `main.py` dosyasını çalıştırın. Başlangıçta sizden bir şifreleme anahtarı (örn: `gizli123`) ayarlamanız istenecek:

```bash
python main.py
```

Uygulama açıldığında şu menüyle karşılaşacaksınız:
1. Metin Şifrele
2. Şifre Çöz
3. Çığ Etkisi Testi (Avalanche)
4. Çıkış

## Testleri Çalıştırma

Projeyle birlikte gelen birim testleri (unit tests) çalıştırmak için Python'ın yerleşik kütüphanesini kullanabilirsiniz:

```bash
python -m unittest test_cipher.py
```
