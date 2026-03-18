# Yıldız Cipher - Custom Python Encryption Library

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6+-green.svg)
![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)
![Unit Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)
![Architecture](https://img.shields.io/badge/architecture-SPN-blueviolet.svg)
![Contributions](https://img.shields.io/badge/contributions-welcome-orange.svg)
[![GitHub stars](https://img.shields.io/github/stars/Yigtwxx/bsglab?style=social)](https://github.com/Yigtwxx/bsglab)
[![GitHub issues](https://img.shields.io/github/issues/Yigtwxx/bsglab)](https://github.com/Yigtwxx/bsglab/issues)

**Yıldız Cipher** is a custom-built, block-based symmetrical encryption algorithm and console application written entirely in Python. This educational project demonstrates the inner workings of modern cryptography architectures like Substitution-Permutation Networks (SPN).

🔐 **Key Features:**
- 128-bit block encryption with custom S-Box and P-Box
- ECB and CBC cipher modes
- Built-in Avalanche Effect testing
- Interactive CLI interface
- Educational codebase for learning cryptography

**Keywords:** Python encryption, custom cipher, SPN algorithm, block cipher, cryptography tutorial, Python security, encryption library

---

## 📖 Table of Contents

- [Quick Start](#-quick-start)
- [Core Features](#-core-features)
- [Installation](#-installation)
- [Usage Examples](#-usage-examples)
- [Project Architecture & File Structure](#-project-architecture--file-structure)
- [Algorithm Deep Dive (How it Works)](#-algorithm-deep-dive-how-it-works)
  - [1. Key Schedule](#1-key-schedule)
  - [2. The S-Box (Substitution)](#2-the-s-box-substitution)
  - [3. The P-Box (Permutation)](#3-the-p-box-permutation)
  - [4. The Mixing Layer (Diffusion)](#4-the-mixing-layer-diffusion)
  - [5. Padding & Cipher Mode](#5-padding--cipher-mode)
- [Running Unit Tests](#-running-unit-tests)
- [Contributing](#-contributing)
- [License](#-license)
- [Disclaimer](#-disclaimer)

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/Yigtwxx/bsglab.git
cd bsglab

# Run the application
python main.py
```

Enter your encryption key and start encrypting/decrypting text!

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

---

## 📦 Installation

### Requirements
- **Python 3.6+** (uses only standard library modules)
- No external dependencies required

### Setup Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Yigtwxx/bsglab.git
   cd bsglab
   ```

2. **Verify Python version:**
   ```bash
   python --version
   # Should show Python 3.6 or higher
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

### Alternative: Direct Download
Download the source files (`cipher.py`, `main.py`, `test_cipher.py`) and run `python main.py` in the same directory.

---

## 💻 Usage Examples

### Basic Encryption/Decryption
```bash
python main.py
```

```
=== Yildiz Şifreleme Aracı ===
Anahtar giriniz (örn: gizli123): mySecretKey

--- İŞLEM SEÇİN ---
1. Metin Şifrele (ECB)
2. Metin Şifrele (CBC)
3. Şifre Çöz
4. Çığ Etkisi Testi (Avalanche)
5. Çıkış

Seçiminiz (1/2/3/4/5): 1
Şifrelenecek metni girin: Hello World!
--> Şifreli Metin (Hex) [ECB]: a1b2c3d4e5f6789...
```

### Avalanche Effect Test
```
Seçiminiz (1/2/3/4/5): 4
Test edilecek metni girin: Hello World
--> Orijinal Şifre: a1b2c3d4e5f6789...
--> Değiştirilmiş Şifre: z9y8x7w6v54321...
--> Fark Yüzdesi: 68.75%
```

### Programmatic Usage
```python
from cipher import YildizCipher

# Initialize with key
cipher = YildizCipher("mySecretKey")

# Encrypt
plaintext = "Hello, World!"
encrypted = cipher.encrypt(plaintext, mode='ECB')
print(f"Encrypted: {encrypted}")

# Decrypt
decrypted = cipher.decrypt(encrypted, mode='ECB')
print(f"Decrypted: {decrypted}")
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

## ⚙️ Continuous Integration (GitHub Actions)

This repository is equipped with a **GitHub Actions setup (`ci.yml`)** to automate the validation process. Every time you push code or open a Pull Request to the `main` or `master` branches, GitHub's servers will automatically:
1. Spin up a fresh Ubuntu environment.
2. Install multiple versions of Python (`3.9`, `3.10`, `3.11`, `3.12`) to ensure broad compatibility.
3. Automatically execute all unit tests in `test_cipher.py`.
4. Only pass the build if your cryptographic logic remains intact.

*This pipeline purposely avoids strict style checkers (linters) and caching issues to guarantee a frictionless, functionality-first development experience.*

### 🏷️ Recommended Issue/PR Labels
To keep this project organized on GitHub, we recommend using the following labels for your Issues and Pull Requests:
- `bug` : For encryption logic failures or padding errors.
- `enhancement` : Proposing stronger hashing architectures or new cipher modes (e.g., CBC).
- `documentation` : Improving this README or internal docstrings.
- `good first issue` : Small improvements (e.g., UI tweaks in the console loop).
- `test` : Adding more rigorous Avalanche Effect or mathematical validation checks.

---

## 🤝 Contributing

Contributions are welcome and encouraged.

1. Read [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow.
2. Follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) during collaboration.
3. Use the provided issue and pull request templates in `.github/`.

If your change impacts encryption behavior, include test updates in `test_cipher.py`.

---

## 📄 License

**Educational Purposes Only.**  
While using robust mathematical principles like PKCS#7, MD5/SHA256 schedules, and SPN architectures, `Yıldız Cipher` uses ECB mode and math-based algebraic S-Boxes. It should **not** be used in production-grade software to encrypt deeply sensitive or financial data. For enterprise security, always rely on vetted standard libraries like AES-GCM (e.g., via the `cryptography` Python package).

---

## 📞 Contact & Support

- **GitHub Issues:** [Report bugs or request features](https://github.com/Yigtwxx/bsglab/issues)
- **Discussions:** [Join the conversation](https://github.com/Yigtwxx/bsglab/discussions)

**Star this repo** ⭐ if you find it useful for learning cryptography!

---

*Built with ❤️ for educational purposes. Learn, experiment, and contribute!*
