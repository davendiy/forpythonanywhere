#!/usr/bin/env python3
# -*-encoding: utf-8-*-

from threading import RLock


class ThreadedDict:
    """
    Dictionary wrapper class for safe usage from different threads
    """
    def __init__(self):
        self.data = {}

        # lock object to avoid simultaneous modifying from different threads
        self.lock = RLock()

    def _wrap(self, f):
        """
        Decorator for non-magic methods of dict
        """

        def new_f(*args, **kwargs):

            # if was acquired by a different thread
            # the new one will wait here until it is released
            with self.lock:
                res = f(*args, **kwargs)
                return res

        return new_f

    def __getitem__(self, item):
        with self.lock:
            return self.data.__getitem__(item)

    def __setitem__(self, key, value):
        with self.lock:
            self.data.__setitem__(key, value)

    def __delitem__(self, key):
        with self.lock:
            self.data.__delitem__(key)

    def __contains__(self, item):
        with self.lock:
            return self.data.__contains__(item)

    def __getattr__(self, name):
        """
        Wrapper for non-magic methods calls (magic methods are not called
        via any handler, so they have to be redefined explicitly)

        :param name: param name
        :return:
        """
        cur = self.data.__getattribute__(name)
        return self._wrap(cur)


if __name__ == '__main__':
    import threading
    import time


    test1 = {2: 3,
             4: 3,
             5: 2,
             3: 2}

    test2 = {3: 3,
             4: 5,
             2: 4,
             5: 2}

    def test_func1():
        for _ in range(100):
            test1[test1[2]] = test2[test1[5]]

    def test_func2():
        for _ in range(100):
            test1[test2[4]] = test2[test1[5]]

    tmp = threading.Thread(target=test_func1, daemon=True)
    tmp2 = threading.Thread(target=test_func2, daemon=True)

    tmp.start()
    tmp2.start()

    time.sleep(4)

    tmp.join()
    tmp2.join()
    print(test1, test2)
