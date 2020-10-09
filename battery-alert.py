# coding: utf-8
# @author octopoulo <polluxyz@gmail.com>
# @version 2020-10-08

"""
Battery alert
"""

from argparse import ArgumentParser
import os
from random import random, seed
from time import sleep, time

import psutil
from pygame import mixer


CUR_FOLDER = os.path.dirname(__file__)
SOUND_FOLDER = os.path.join(CUR_FOLDER, 'sound')


class BatteryAlert:
    def __init__(self, every: int, low: int, high: int):
        if every < 1:
            every = 1
        if high > 100:
            high = 100
        if low < 1:
            low = 1

        print(f'Battery alert: every={every} : low={low} : high={high}')
        self.every = every
        self.high = high
        self.low = low
        self.sounds = []
        self.sources = []

        self.scan_sounds()
        self.go()

    def alert(self, text: str, percent: int):
        """Sound alert
        """
        print(f"Battery too {text} at {percent}%, {'dis' if text == 'high' else ''}connect the cable!")
        index = int(random() * len(self.sounds))
        sound = self.sounds[index]
        if not sound:
            sound = mixer.Sound(os.path.join(SOUND_FOLDER, self.sources[index]))
            self.sounds[index] = sound

        sound.play()

    def go(self):
        """Infinite loop
        """
        seed(int(time()))
        mixer.init()

        while True:
            battery = psutil.sensors_battery()
            percent = battery.percent

            if battery.power_plugged:
                if percent > self.high:
                    self.alert('high', percent)
            elif percent < self.low:
                self.alert('low', percent)

            sleep(self.every)

    def scan_sounds(self):
        """Scan the sound folder
        """
        sources = os.listdir(SOUND_FOLDER)
        self.sources = [source for source in sources if source.endswith(('.ogg', '.wav'))]
        self.sounds = [None] * len(self.sources)
        print(f"{len(self.sources)} sounds scanned: {', '.join(self.sources)}")


def main():
    parser = ArgumentParser(description='Renter', prog='python __main__.py')
    add = parser.add_argument

    add('--every', nargs='?', default=60, type=int, help='check the battery every x seconds, default=60')
    add('--low', nargs='?', default=30, type=int, help='set the low threshold level, default=30')
    add('--high', nargs='?', default=80, type=int, help='set the high threshold level, default=75')
    args = parser.parse_args()

    battery_alert = BatteryAlert(args.every, args.low, args.high)


if __name__ == '__main__':
    main()
