from concurrent.futures import ProcessPoolExecutor

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.queues import Queue

event_queue = Queue(maxsize=10)


@gen.coroutine
def consumer():
    while True:
        input_dict = yield event_queue.get()
        try:
            with ProcessPoolExecutor(max_workers=4) as executor:
                future = executor.submit(expensive_function, input_dict)
        finally:
            event_queue.task_done()


@gen.coroutine
def producer(input_dict):
    yield event_queue.put(input_dict)


def expensive_function(input_dict):
    print("message: [%s]" % input_dict)


def start_consumer():
    IOLoop.current().spawn_callback(consumer)
