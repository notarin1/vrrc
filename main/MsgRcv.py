from concurrent.futures import ProcessPoolExecutor

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.queues import Queue

queue = Queue(maxsize=10)


@gen.coroutine
def consumer():
    while True:
        input_dict = yield queue.get()
        try:
            with ProcessPoolExecutor(max_workers=4) as executor:
                future = executor.submit(expensive_function, input_dict)
        finally:
            queue.task_done()


@gen.coroutine
def producer(input_dict):
    yield queue.put(input_dict)


def expensive_function(input_dict):
    print("message: [%s]" % input_dict)
    # ここで受信したメッセージをwebsocketで返す

    write_to_clients


def start_consumer():
    IOLoop.current().spawn_callback(consumer)
