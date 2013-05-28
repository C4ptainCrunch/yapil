from threading import Thread, current_thread
from multiprocessing import Queue

class Pipe(object):
    def __init__(self, to_parent, from_parent,is_child):
        self.is_child = is_child
        self.to_parent = to_parent
        self.from_parent = from_parent

    @property
    def incomming(self):
        return self.from_parent if self.is_child else self.to_parent

    @property
    def out(self):
        return self.to_parent if self.is_child else self.from_parent



def go(fn, to_child=Queue(), from_child=Queue()):

    def _fn(*args, **kwargs):

        def threaded_fn(*args, **kwargs):
            pipe = Pipe(kwargs['from_child'], kwargs['to_child'],True)
            kwargs.pop('from_child')
            kwargs.pop('to_child')
            fn(pipe, *args, **kwargs)

        queues =  {'to_child' : to_child, 'from_child' : from_child}
        kwargs.update(queues)
        t = Thread(target=threaded_fn, args=args, kwargs=kwargs)
        t.start()
        return Pipe(kwargs['from_child'], kwargs['to_child'],False)

    return _fn