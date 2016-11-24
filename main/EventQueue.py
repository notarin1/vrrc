from tornado.queues import Queue

event_queue = Queue(maxsize=10)


# queueにデータを入れる
def enqueue_event(event):
    event_queue.put(event)


# 100msec周期で呼ばれて、queueにデータがあればwebsocketで値を返す
def queue_routine(function):
    while True:
        if not event_queue.empty():
            result = event_queue.get().result()
            if result is not str:
                result = str(result)
            function(result)
