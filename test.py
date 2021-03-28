from notifypy import Notify

notification = Notify()
notification.title = "Cool Title"
notification.message = "Even cooler message."
notification.audio = "rsi_alerts\piece-of-cake-611.wav"
notification.send()