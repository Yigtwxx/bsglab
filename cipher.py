import hashlib

__version__ = "1.0.0"

class YildizCipher:
    def __init__(self, key_text):
        """
        Initialize the cipher with a key string.
        The key will be hashed to ensure it is 128 bits (16 bytes).
        """
        # Ensure key is 16 bytes
        self.key = hashlib.md5(key_text.encode('utf-8')).digest()
        self.block_size = 16
        self.rounds = 10
        self.round_keys = self._generate_round_keys()

    def _generate_round_keys(self):
        """
        Simple key expansion.
        Generates 'rounds + 1' subkeys, each 16 bytes long.
        """
        keys = []
        # Initial key
        current_key = self.key
        keys.append(current_key)
        
        for i in range(self.rounds):
            # Derive next key deterministically using SHA-256 for good mixing
            # In a real scenario, a specialized schedule is faster, but this is secure and easy.
            next_key_digest = hashlib.sha256(current_key + bytes([i])).digest()
            current_key = next_key_digest[:16] # Take first 16 bytes
            keys.append(current_key)
            
        return keys

    def _substitute(self, block):
        """
        Substitution Layer (S-Box equivalent).
        Mathematical S-Box: S(x) = (x * 3 + 7) % 256
        """
        return bytes([(b * 3 + 7) % 256 for b in block])

    def _inv_substitute(self, block):
        """
        Inverse Substitution Layer.
        Inverse of S(x): x = ((y - 7) * 171) % 256
        See math: 3*171 = 513 = 2*256 + 1 == 1 (mod 256)
        """
        return bytes([((b - 7) * 171) % 256 for b in block])

    def _permute(self, block):
        """
        Permutation Layer (P-Box equivalent).
        We treat the 16 bytes as a 4x4 matrix and shift rows.
        Row 0: Shift 0
        Row 1: Shift 1 left
        Row 2: Shift 2 left
        Row 3: Shift 3 left
        """
        # Convert to list for mutable operations
        b = list(block)
        new_block = [0] * 16
        
        # Matrix form indices:
        # 0  1  2  3
        # 4  5  6  7
        # 8  9  10 11
        # 12 13 14 15
        
        # Row 0 (No shift)
        new_block[0:4] = b[0:4]
        
        # Row 1 (Shift left by 1) -> 4 5 6 7 becomes 5 6 7 4
        new_block[4:8] = b[5:8] + b[4:5]
        
        # Row 2 (Shift left by 2) -> 8 9 10 11 becomes 10 11 8 9
        new_block[8:12] = b[10:12] + b[8:10]
        
        # Row 3 (Shift left by 3) -> 12 13 14 15 becomes 15 12 13 14
        new_block[12:16] = b[15:16] + b[12:15]
        
        return bytes(new_block)

    def _inv_permute(self, block):
        """
        Inverse Permutation Layer.
        Shift rows right instead of left.
        """
        b = list(block)
        new_block = [0] * 16
        
        # Row 0 (No shift)
        new_block[0:4] = b[0:4]
        
        # Row 1 (Shift right by 1) -> 5 6 7 4 becomes 4 5 6 7
        new_block[4:8] = b[7:8] + b[4:7]
        
        # Row 2 (Shift right by 2)
        new_block[8:12] = b[10:12] + b[8:10] # shifting by 2 is symmetric for len 4
        
        # Row 3 (Shift right by 3) -> 15 12 13 14 becomes 12 13 14 15
        new_block[12:16] = b[13:16] + b[12:13]
        
        return bytes(new_block)

    def _xor_bytes(self, a, b):
        return bytes([x ^ y for x, y in zip(a, b)])

    def _pad(self, plaintext):
        """
        PKCS7 Padding to make plaintext multiple of 16 bytes.
        """
        padding_len = self.block_size - (len(plaintext) % self.block_size)
        padding = bytes([padding_len] * padding_len)
        return plaintext + padding

    def _unpad(self, plaintext):
        """
        Remove PKCS7 Padding.
        """
        padding_len = plaintext[-1]
        # Validity check
        if padding_len == 0 or padding_len > self.block_size:
             # In a real app, raise error, but here we might just return safely
             raise ValueError("Invalid padding")
        
        # Verify all padding bytes
        for i in range(1, padding_len + 1):
             if plaintext[-i] != padding_len:
                 raise ValueError("Invalid padding")
                 
        return plaintext[:-padding_len]

    def _mix(self, block):
        """
        Mixing Layer to provide diffusion.
        We use addition modulo 256 to combine bytes with their neighbors.
        Forward: s[i] = (s[i] + s[(i+1)%16]) % 256
        Must be done carefully to be reversible.
        We will use a temporary copy for the source to avoid dependency loop issues in simple implementation,
        BUT to get propagation we want dependencies.
        
        Let's do a simple reversible chain:
        s[0] += s[1]
        s[1] += s[2]
        ...
        s[15] += s[0] (uses new s[0])
        """
        b = list(block)
        # Mix forward
        for i in range(15):
             b[i] = (b[i] + b[i+1]) % 256
        # Last one wraps around to the *new* b[0] for extra mixing
        b[15] = (b[15] + b[0]) % 256
        return bytes(b)

    def _inv_mix(self, block):
        """
        Inverse Mixing Layer.
        Reverse the operations in opposite order.
        """
        b = list(block)
        # Undo last step first
        b[15] = (b[15] - b[0]) % 256
        # Undo others
        for i in range(14, -1, -1):
             b[i] = (b[i] - b[i+1]) % 256
        return bytes(b)

    def encrypt_block(self, block):
        state = block
        
        # Initial Round Key Addition
        state = self._xor_bytes(state, self.round_keys[0])
        
        # Main Rounds
        for i in range(1, self.rounds + 1):
            state = self._substitute(state)
            state = self._permute(state)
            state = self._mix(state) # Added Mixing
            state = self._xor_bytes(state, self.round_keys[i])
            
        return state

    def decrypt_block(self, block):
        state = block
        
        # Undo rounds in reverse
        for i in range(self.rounds, 0, -1):
            state = self._xor_bytes(state, self.round_keys[i])
            state = self._inv_mix(state) # Undo Mixing
            state = self._inv_permute(state)
            state = self._inv_substitute(state)
            
        # Undo Initial Round Key
        state = self._xor_bytes(state, self.round_keys[0])
        
        return state

    def encrypt(self, plaintext_str, mode='ECB'):
        if isinstance(plaintext_str, str):
            plaintext_bytes = plaintext_str.encode('utf-8')
        else:
            plaintext_bytes = plaintext_str
            
        padded_text = self._pad(plaintext_bytes)
        encrypted_bytes = b""

        if mode == 'CBC':
            # Generate random IV
            import os
            iv = os.urandom(self.block_size)
            encrypted_bytes += iv
            previous_block = iv

            for i in range(0, len(padded_text), self.block_size):
                block = padded_text[i : i + self.block_size]
                xor_block = self._xor_bytes(block, previous_block)
                encrypted_block = self.encrypt_block(xor_block)
                encrypted_bytes += encrypted_block
                previous_block = encrypted_block

        else: # ECB Mode
            for i in range(0, len(padded_text), self.block_size):
                block = padded_text[i : i + self.block_size]
                encrypted_block = self.encrypt_block(block)
                encrypted_bytes += encrypted_block
            
        return encrypted_bytes.hex()

    def decrypt(self, ciphertext_hex, mode='ECB'):
        ciphertext_bytes = bytes.fromhex(ciphertext_hex)
        decrypted_padded = b""
        
        if mode == 'CBC':
            iv = ciphertext_bytes[:self.block_size]
            actual_ciphertext = ciphertext_bytes[self.block_size:]
            previous_block = iv

            for i in range(0, len(actual_ciphertext), self.block_size):
                block = actual_ciphertext[i : i + self.block_size]
                decrypted_block_raw = self.decrypt_block(block)
                decrypted_block = self._xor_bytes(decrypted_block_raw, previous_block)
                decrypted_padded += decrypted_block
                previous_block = block
        else:
            for i in range(0, len(ciphertext_bytes), self.block_size):
                block = ciphertext_bytes[i : i + self.block_size]
                decrypted_block = self.decrypt_block(block)
                decrypted_padded += decrypted_block
            
        try:
            decrypted_bytes = self._unpad(decrypted_padded)
            return decrypted_bytes.decode('utf-8')
        except Exception as e:
            return f"[Error: Decryption Failed or Invalid Padding: {e}]"
