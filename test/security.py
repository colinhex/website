from website.utils import security
import unittest
import logging
import sys

# ---------- Logging Setup ----------

Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(
    stream=sys.stdout,
    filemode="w",
    format=Log_Format,
    level=logging.DEBUG
)

logger = logging.getLogger()


class Security(unittest.TestCase):

    def test_data_crypt(self):
        logger.info('Test Data Crypt')
        security.set_pref({'SECRET_KEY': '123password'})
        data = 'Zarathustra'
        logger.info('Original Data: ' + data)
        encrypted = security.encrypt_data(data)
        logger.info('Encrypted Data: ' + encrypted)
        decrypted = security.decrypt_data(encrypted)
        logger.info('Decrypted Data: ' + decrypted)
        self.assertEqual(data, decrypted)
