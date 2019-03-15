from io import StringIO
import unittest

from pyphpbb import util


class TestUtil(unittest.TestCase):

    def test_invalid_fqdn(self):
        with self.assertRaises(ValueError):
            util.fqdn('')

    def test_fqdn(self):
        self.assertEqual(
            'foo.com',
            util.fqdn('http://foo.com/fwewf/wefwe'))

        self.assertEqual(
            'foo.com',
            util.fqdn('https://foo.com/fwewf/wefwe'))

        self.assertEqual(
            'foo.com',
            util.fqdn('ftp://foo.com?fpp=bar'))

    def test_write_csv(self):
        fh = StringIO()
        util.write_csv(fh, [range(3) for _ in range(3)])
        fh.seek(0)
        self.assertEqual(
            fh.read(),
            "0,1,2\r\n0,1,2\r\n0,1,2\r\n")


if __name__ == "__main__":
    unittest.main()
