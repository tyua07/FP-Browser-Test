from Crypto.Cipher import AES
import base64


class AESLibrary(object):
    def __init__(self):
        self.key = b"bSmT4152SKC1XBhjpxZ446c1L0e5IGEf"
        self.iv = b"PoYF83GyaZryX9rT"

    @staticmethod
    def to_string(encrypt_data):
        """
        格式化成 base64 字符串
        """
        return base64.b64encode(encrypt_data).decode("utf8")

    def encrypt(self, context):
        """
        加密
        """
        bs = AES.block_size
        pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
        encryption_suite = AES.new(self.key, AES.MODE_CBC, self.iv)
        return encryption_suite.encrypt(bytes(pad(context), 'utf-8'))

    def decrypt(self, cipher_text):
        """
        解密
        """
        decryption_suite = AES.new(self.key, AES.MODE_CBC, self.iv)
        return decryption_suite.decrypt(bytes(cipher_text, 'utf-8')).decode()
