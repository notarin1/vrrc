from tornado.queues import Queue

event_queue = Queue(maxsize=10)


def enqueue_event(event):
    event_queue.put(event)


def queue_routine(function):
    while True:
        if not event_queue.empty():
            function(event_queue.get().result())
