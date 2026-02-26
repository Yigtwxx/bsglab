# Yildiz Cipher (Yıldız Encryption Tool)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.x-green.svg)
![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)
![Unit Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)
![Architecture](https://img.shields.io/badge/architecture-SPN-blueviolet.svg)
![Contributions](https://img.shields.io/badge/contributions-welcome-orange.svg)

**Yildiz Cipher** is a custom-built, block-based symmetrical encryption algorithm and console application written entirely in Python. Designed as an educational project, it provides practical insights into how modern cryptography architectures—like Substitution-Permutation Networks (SPN)—operate under the hood.

This tool not only facilitates text encryption and decryption using a user-supplied key but also features a built-in **Avalanche Effect Testing Suite** to measure the algorithm's robustness against minor plaintext modifications.

---

## 📖 Table of Contents

- [Core Features](#-core-features)
- [Project Architecture & File Structure](#-project-architecture--file-structure)
- [Algorithm Deep Dive (How it Works)](#-algorithm-deep-dive-how-it-works)
  - [1. Key Schedule](#1-key-schedule)
  - [2. The S-Box (Substitution)](#2-the-s-box-substitution)
  - [3. The P-Box (Permutation)](#3-the-p-box-permutation)
  - [4. The Mixing Layer (Diffusion)](#4-the-mixing-layer-diffusion)
  - [5. Padding & Cipher Mode](#5-padding--cipher-mode)
- [Installation Requirements](#-installation-requirements)
- [Usage Guide](#-usage-guide)
- [Running Unit Tests](#-running-unit-tests)
- [Disclaimer](#-disclaimer)

---

## ✨ Core Features

1. **Deterministic Text Encryption:** Utilizes a custom 128-bit block size algorithm to secure plaintext strings, converting them into Hexadecimal format for secure transmission and storage.
2. **Text Decryption:** Allows users to input exact Hexadecimal ciphertexts alongside their secret keys to recover the original plaintext smoothly.
3. **Avalanche Effect Testing:** A powerful internal validator that demonstrates the butterfly effect in cryptography. It modifies exactly 1 bit (or 1 character) of the plaintext and outputs the statistical percentage difference between the two resulting ciphertexts, indicating algorithm strength.
4. **Interactive CLI:** An easy-to-use, menu-driven command-line interface.

---

## 📂 Project Architecture & File Structure

The workspace is kept minimal, modular, and highly readable:

```text
bsglab/
├── cipher.py         # The core engine: defines the YildizCipher class and all cryptographic math.
├── main.py           # The frontend: CLI loops, user input handling, and the Avalanche test logic.
├── test_cipher.py    # The validator: Local unit tests ensuring the cipher doesn't break.
├── .gitignore        # Git configuration to ignore __pycache__ and environments.
└── README.md         # The documentation you are reading right now.
```

---

## 🧠 Algorithm Deep Dive (How it Works)

The algorithm is structured similarly to AES (Advanced Encryption Standard), utilizing a multi-round **Substitution-Permutation Network (SPN)**. It operates on **16-byte (128-bit) blocks** and goes through **4 distinct computational rounds**.

### 1. Key Schedule
When you provide a string key (e.g., `"secret123"`), the `YildizCipher` normalizes it by hashing it via **MD5** to ensure it is exactly 16 bytes. To generate subkeys for the 4 rounds, the engine uses deterministic **SHA-256 chaining**, mixing the current key with the round index to ensure each round utilizes a drastically different piece of cryptographic material.

### 2. The S-Box (Substitution Layer)
Unlike AES which uses a fixed look-up table, `YildizCipher` uses a mathematically contiguous S-box. 
For every byte $x$:
- **Forward:** $S(x) = (x \times 3 + 7) \pmod{256}$
- **Inverse (Decryption):** $S^{-1}(y) = ((y - 7) \times 171) \pmod{256}$
*(Note: 171 is the modular multiplicative inverse of 3 modulo 256).*

### 3. The P-Box (Permutation Layer)
This layer scatters the data. Treating the 16-byte block as a $4 \times 4$ matrix, the cipher mimics the AES `ShiftRows` operation:
- **Row 0:** No shift
- **Row 1:** Shift left by 1
- **Row 2:** Shift left by 2
- **Row 3:** Shift left by 3

### 4. The Mixing Layer (Diffusion)
To ensure a high Avalanche Effect, the bytes are mathematically bound to their neighbors. Using modulo 256 addition, the algorithm chains the bytes functionally: each byte $i$ becomes $(byte[i] + byte[i+1]) \pmod{256}$, ensuring that a change in one byte ripples across the entire block seamlessly.

### 5. Padding & Cipher Mode
- **Padding:** Implements standard **PKCS#7**. If an input is 4 bytes, it adds 12 bytes, each with a mathematical value of `12`.
- **Mode of Operation:** It currently relies on **ECB (Electronic Codebook)** mode, processing each 16-byte chunk independently.

---

## 🚀 Installation Requirements

This project relies purely on standard Python libraries (`hashlib`, `unittest`). **No third-party packages or `pip` installations are required.**

1. Ensure you have **Python 3.x** installed on your system.
2. Clone the repository or download the source files.
3. Open your terminal/command prompt and navigate to the project directory:
   ```bash
   cd path/to/bsglab
   ```

---

## 💻 Usage Guide

Start the application by executing the `main.py` entry point:

```bash
python main.py
```

### 1. Setting the Key
On launch, the CLI asks for an encryption key.
```text
=== Yildiz Şifreleme Aracı ===
Anahtar giriniz (örn: gizli123): myAwesomeKey
```
*(If left blank, it defaults securely to `gizli123`)*

### 2. Main Menu Actions
You will be prompted with an interactive menu containing 4 selections:

#### Option 1: Encrypt Text
Allows you to write standard text and receive the **Hexadecimal** ciphertext.
```text
Şifrelenecek metni girin: Hello, GitHub!
--> Şifreli Metin (Hex): 8a4b2c9e7f...
```

#### Option 2: Decrypt Text
Paste the previously outputted Hexadecimal text to retrieve your plaintext, provided your initial key matches!

#### Option 3: Avalanche Effect Test
Input a string. The program will:
1. Encrypt your normal string.
2. Flip the last bit/character of your string and encrypt the new version.
3. Compare the two ciphertexts side-by-side.
4. Output the **Percentage of Difference (# of different Hex characters)**. If it's over 40-50%, the algorithm proves its diffusion strength!

---

## 🛠 Running Unit Tests

To ensure the codebase is structurally sound (especially if you modify the cryptography math in `cipher.py`), run the native Python `unittest` suite:

```bash
python -m unittest test_cipher.py
```

**What the tests check:**
- Standard Plaintext Encryption to Decryption parity.
- Complex/Long Sentence padding validation.
- Empty string edge cases.
- Avalanche Effect baseline thresholds (ensuring a 1-character change alters >5 hexadecimal characters).

---

## ⚠️ Disclaimer

**Educational Purposes Only.**  
While using robust mathematical principles like PKCS#7, MD5/SHA256 schedules, and SPN architectures, `YildizCipher` uses ECB mode and math-based algebraic S-Boxes. It should **not** be used in production-grade software to encrypt deeply sensitive or financial data. For enterprise security, always rely on vetted standard libraries like AES-GCM (e.g., via the `cryptography` Python package).
