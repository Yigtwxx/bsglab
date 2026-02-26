from cipher import YildizCipher

def main():
    print("=== Yildiz Şifreleme Aracı ===")
    
    # 1. Anahtar Al
    anahtar = input("Anahtar giriniz (örn: gizli123): ")
    if not anahtar:
        anahtar = "gizli123"
        print(f"Varsayılan anahtar kullanılıyor: {anahtar}")
        
    cipher = YildizCipher(anahtar)
    
    while True:
        print("\n--- İŞLEM SEÇİN ---")
        print("1. Metin Şifrele")
        print("2. Şifre Çöz")
        print("3. Çığ Etkisi Testi (Avalanche)")
        print("4. Çıkış")
        
        secim = input("Seçiminiz (1/2/3/4): ").strip()
        
        if secim == '1':
            metin = input("\nŞifrelenecek metni girin: ")
            if metin:
                sifreli = cipher.encrypt(metin)
                print(f"--> Şifreli Metin (Hex): {sifreli}")
            
        elif secim == '2':
            sifreli_hex = input("\nÇözülecek şifreyi (Hex) girin: ")
            if sifreli_hex:
                try:
                    cozulen = cipher.decrypt(sifreli_hex)
                    print(f"--> Çözülen Metin: {cozulen}")
                except Exception as e:
                    print(f"HATA: Şifre çözülemedi! ({e})")
                
        elif secim == '3':
            metin = input("\nTest edilecek metni girin: ")
            if metin:
                # 1. Original Encryption
                c1 = cipher.encrypt(metin)
                
                # 2. Modify one character (flip last char bit) or just change last char
                # Simple approach: change last char to something else
                if len(metin) > 0:
                    last_char_code = ord(metin[-1])
                    new_char = chr(last_char_code ^ 1) # Flip 1 bit
                    metin2 = metin[:-1] + new_char
                else:
                    metin2 = "a" # Handle empty case

                c2 = cipher.encrypt(metin2)
                
                print(f"\n1. Metin: {metin}")
                print(f"2. Metin: {metin2} (1 bit/karakter değişti)")
                print(f"--> Çıktı 1: {c1}")
                print(f"--> Çıktı 2: {c2}")
                
                # Calculate difference
                diff_count = sum(1 for a, b in zip(c1, c2) if a != b)
                total_len = len(c1)
                ratio = (diff_count / total_len) * 100
                
                print(f"\nFarklı Karakter Sayısı: {diff_count} / {total_len}")
                print(f"Değişim Oranı (Avalanche): %{ratio:.2f}")
                if ratio > 40:
                    print("SONUÇ: Çığ etkisi BAŞARILI (Yüksek değişim).")
                else:
                    print("SONUÇ: Çığ etkisi ZAYIF.")

        elif secim == '4':
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim, tekrar deneyin.")

if __name__ == "__main__":
    main()
