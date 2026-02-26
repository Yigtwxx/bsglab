import unittest
from cipher import YildizCipher

class TestYildizCipher(unittest.TestCase):
    def setUp(self):
        self.key = "TestKey123"
        self.cipher = YildizCipher(self.key)

    def test_encrypt_decrypt_simple(self):
        original = "Hello World"
        encrypted = self.cipher.encrypt(original)
        decrypted = self.cipher.decrypt(encrypted)
        self.assertEqual(original, decrypted)

    def test_encrypt_decrypt_long(self):
        original = "This is a longer sentence that spans multiple blocks to test ECB mode and padding."
        encrypted = self.cipher.encrypt(original)
        decrypted = self.cipher.decrypt(encrypted)
        self.assertEqual(original, decrypted)

    def test_encrypt_decrypt_empty(self):
        original = ""
        encrypted = self.cipher.encrypt(original)
        decrypted = self.cipher.decrypt(encrypted)
        self.assertEqual(original, decrypted)

    def test_avalanche_effect_concept(self):
        # Changing 1 char in plaintext should change many in ciphertext
        t1 = "Hello World"
        t2 = "Hello world" # lowercase w
        c1 = self.cipher.encrypt(t1)
        c2 = self.cipher.encrypt(t2)
        self.assertNotEqual(c1, c2)
        
        # Check how many hex chars differ (simple heuristic)
        diff = sum(1 for a, b in zip(c1, c2) if a != b)
        print(f"Avalanche Diff: {diff}/{len(c1)} chars changed")
        self.assertTrue(diff > 5) # Expect reasonable difference

if __name__ == '__main__':
    unittest.main()
