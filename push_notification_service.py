from pushbullet import Pushbullet
import os

API_KEY = os.environ.get('PUSH_BULLET_API_KEY')
pb = Pushbullet(API_KEY)


def send_notification_to_mobile(title, text):
    pb.push_note(title, text)

