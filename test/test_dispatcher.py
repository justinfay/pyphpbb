import unittest
from unittest import mock

from pyphpbb import Dispatcher, DispatcherEmpty


class DummyTime:

    def __init__(self):
        self._time = -1

    def __call__(self):
        self._time += 1
        return self._time


class TestDispatcher(unittest.TestCase):

    def setUp(self):
        self.dispatcher = Dispatcher()

    def test_put(self):
        self.dispatcher.put('http://foo.com', 1)
        self.assertEqual(
            self.dispatcher._queue,
            [('http://foo.com', 1)])
        self.dispatcher.put('http://bar.com', 2)
        self.assertEqual(
            self.dispatcher._queue,
            [('http://foo.com', 1), ('http://bar.com', 2)])

    def test_get_empty(self):
        dispatcher = Dispatcher()
        with self.assertRaises(DispatcherEmpty):
            dispatcher.get()

    def test_get_order(self):
        self.test_put()
        self.assertEqual(
            self.dispatcher.get(),
            ('http://foo.com', 1))
        self.assertEqual(
            self.dispatcher.get(),
            ('http://bar.com', 2))

    @mock.patch('time.time', DummyTime())
    @mock.patch('time.sleep', mock.Mock())
    def test_is_limited(self):
        self.dispatcher.rate_limit = 1
        self.dispatcher.put('http://foo.com', 1)
        self.dispatcher.put('http://bar.com', 1)
        self.dispatcher.get()
        self.assertTrue(self.dispatcher._is_limited('http://foo.com'))
        self.assertFalse(self.dispatcher._is_limited('http://bar.com'))

    @mock.patch('time.time', DummyTime())
    @mock.patch('time.sleep', mock.Mock())
    def test_get_limited(self):
        self.dispatcher.rate_limit = 2
        self.dispatcher.put('http://foo.com', 1)
        self.dispatcher.put('http://foo.com', 1)
        self.dispatcher.put('http://bar.com', 2)
        self.assertEqual(
            self.dispatcher.get(),
            ('http://foo.com', 1))
        self.assertEqual(
            self.dispatcher.get(),
            ('http://bar.com', 2))
        self.assertEqual(
            self.dispatcher.get(),
            ('http://foo.com', 1))


if __name__ == "__main__":
    unittest.main()
