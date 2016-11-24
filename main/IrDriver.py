# 通知コールバックをnotify_callbackに設定する
# 何か
import main.RepeatedTimer


class IrDriver:
    ir_value = 0

    def __init__(self, notify_callback, threshold):
        self.threshold = threshold
        self.notify_callback = notify_callback
        self.rt = main.RepeatedTimer.RepeatedTimer(0.2, self.check_ir, "IR")

    def start(self):
        self.rt.start()

    def stop(self):
        self.rt.stop()

    def check_ir(self, message):
        # 0.2sec周期で呼び出される
        # IR値を読み出して、前回値がthreshold を超えた or thresholdを下回った場合に通知する
        self.notify_callback(message)
