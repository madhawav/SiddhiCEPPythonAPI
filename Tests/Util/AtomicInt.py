from multiprocessing import Lock


class AtomicInt:
    '''
    An atomic integer class. All operations are thread safe.
    '''

    def __init__(self, value=0):
        self.value = value
        self.lock = Lock()

    def set(self, value):
        with self.lock:
            self.value = value

    def addAndGet(self, value):
        with self.lock:
            self.value += value
            return self.value

    def get(self):
        with self.lock:
            return self.value
