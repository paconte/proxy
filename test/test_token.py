import unittest
import proxy.jwttoken as token
from proxy.settings import JWT_ALGO, JWT_KEY
from jwt.exceptions import InvalidAlgorithmError
from jwt.exceptions import InvalidSignatureError


KEY_1, KEY_2 = "secret", "public"
ALG_1, ALG_2 = "HS256", "HS512"


class TestToken(unittest.TestCase):

    def test_encode_decode_positive(self):
        payload = {"sub": "1234567890", "name": "John Doe", "iat": 1516239022}
        encoded = token.encode(payload, algo=ALG_1, key=KEY_1)
        decoded = token.decode(encoded, algo=ALG_1, key=KEY_1)
        self.assertEqual(payload, decoded)
        encoded = token.encode(payload, algo=ALG_1, key=KEY_2)
        decoded = token.decode(encoded, algo=ALG_1, key=KEY_2)
        self.assertEqual(payload, decoded)
        encoded = token.encode(payload, algo=ALG_2, key=KEY_1)
        decoded = token.decode(encoded, algo=ALG_2, key=KEY_1)
        self.assertEqual(payload, decoded)
        encoded = token.encode(payload, algo=ALG_2, key=KEY_2)
        decoded = token.decode(encoded, algo=ALG_2, key=KEY_2)
        self.assertEqual(payload, decoded)

    def test_encode_decode_negative(self):
        payload = {"sub": "1234567890", "name": "John Doe", "iat": 1516239022}
        encoded = token.encode(payload, algo=ALG_1, key=KEY_1)
        with self.assertRaises(InvalidSignatureError):
            token.decode(encoded, algo=ALG_1, key=KEY_2)
        with self.assertRaises(InvalidAlgorithmError):
            token.decode(encoded, algo=ALG_2, key=KEY_1)

    def test_default_payload(self):
        payload = token.get_default_payload()
        encoded = token.encode(payload, algo=JWT_ALGO, key=JWT_KEY)
        decoded = token.decode(encoded, algo=JWT_ALGO, key=JWT_KEY)
        self.assertEqual(payload, decoded)


if __name__ == "__main__":
    unittest.main()
