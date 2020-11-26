# coding: utf-8
# @author octopoulo <polluxyz@gmail.com>
# @version 2020-11-25

"""
Battery alert
"""

from argparse import ArgumentParser
import os
from random import random, seed
from subprocess import CREATE_NEW_CONSOLE, Popen, run
from time import sleep, time

import psutil
from pygame import mixer


LOW = 1
HIGH = 2
SOUND_FOLDER = os.path.join(os.path.dirname(__file__), 'sound')


def default_int(value: int or str, default: int=None) -> int or None:
    """Convert a value to an int, on exception, return a default value
    """
    if isinstance(value, int):
        return value
    if value is None:
        return default

    try:
        value = int(float(value))
    except (TypeError, ValueError):
        value = default
    return value


class BatteryAlert:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

        self.devcon = kwargs.get('devcon')                                      # type: str
        self.every = max(default_int(kwargs.get('every'), 60), 1)               # type: int
        self.high = min(default_int(kwargs.get('high'), 75), 100)               # type: int
        self.low = max(default_int(kwargs.get('low'), 30), 1)                   # type: int
        self.no_sound = kwargs.get('no_sound')                                  # type: bool
        self.run_high = kwargs.get('run_high')                                  # type: int
        self.run_low = kwargs.get('run_low')                                    # type: int
        self.run_wakeup = kwargs.get('run_wakeup')                              # type: str

        print(f'Battery alert: devon={self.devcon} every={self.every} low={self.low} high={self.high}')
        self.sounds = []
        self.sources = []

        self.scan_sounds()
        self.go()

    def alert(self, which: str, percent: int):
        """Sound alert
        """
        text = 'high' if which == HIGH else 'low'
        print(f"Battery too {text} at {percent}%, {'dis' if which == HIGH else ''}connect the cable!")

        # 1) play a sound
        if not self.no_sound and self.sounds:
            index = int(random() * len(self.sounds))
            sound = self.sounds[index]
            if not sound:
                sound = mixer.Sound(os.path.join(SOUND_FOLDER, self.sources[index]))
                self.sounds[index] = sound
            sound.play()

        # 2) run custom commands
        params = None
        if which == HIGH:
            if self.run_high:
                params = self.run_high
            elif self.devcon:
                params = ['devcon', 'disable', self.devcon]
        elif which == LOW:
            if self.run_low:
                params = self.run_low
            elif self.devcon:
                params = ['devcon', 'enable', self.devcon]

        if params:
            result = run(params, capture_output=True, text=True)
            print(result.stdout)

    def go(self):
        """Infinite loop
        """
        check = 0
        start = time()
        seed(int(start))
        mixer.init()

        while True:
            # check battery %
            last = time()
            if last >= check + self.every:
                check = last
                battery = psutil.sensors_battery()
                percent = battery.percent

                if battery.power_plugged:
                    if percent > self.high:
                        self.alert(HIGH, percent)
                elif percent < self.low:
                    self.alert(LOW, percent)

            # sleep
            sleep((self.every + 1) // 2)

            # detect if computer woke up
            now = time()
            if now > last + self.every + 10:
                print('WOKE UP', now - start)
                if self.run_wakeup:
                    for command in self.run_wakeup.split('\\n'):
                        Popen(command, creationflags=CREATE_NEW_CONSOLE, shell=True)
                    exit()
                    break

    def scan_sounds(self):
        """Scan the sound folder
        """
        if self.no_sound:
            return
        if not os.path.isdir(SOUND_FOLDER):
            print(f'Note: {SOUND_FOLDER} does not exist.')
            return
        sources = os.listdir(SOUND_FOLDER)
        self.sources = [source for source in sources if source.endswith(('.ogg', '.wav'))]
        self.sounds = [None] * len(self.sources)
        text = '\n- '.join([''] + self.sources)
        print(f"{len(self.sources)} sounds scanned: {text}")


def main():
    parser = ArgumentParser(description='Battery Alert', prog='python battery-alert.py')

    group = parser.add_argument_group('main')
    add = group.add_argument
    add('--every', nargs='?', default=60, type=int, help='check the battery every x seconds, default=60')
    add('--high', nargs='?', default=75, type=int, help='set the high threshold level, default=75')
    add('--low', nargs='?', default=30, type=int, help='set the low threshold level, default=30')
    add('--no-sound', action='store_true', help='disable the sound, ex: to have custom commands do something better')
    add('--run-high', nargs='?', default=None, help='custom command to run when the battery level is too high')
    add('--run-low', nargs='?', default=None, help='custom command to run when the battery level is too low')
    add('--run-wakeup', nargs='?', default=None, help='command to run when waking up')

    group = parser.add_argument_group('devcon')
    add = group.add_argument
    add('--devcon', nargs='?', default=None, help='device id that devcon.exe will start/stop')
    add('--devcon-list', action='store_true', help='list usb hwids using devcon')
    add('--devcon-start', nargs='?', help='start a device with devcon.exe')
    add('--devcon-stop', nargs='?', help='stop a device with devcon.exe')

    args = parser.parse_args()
    args_dict = vars(args)
    args_set = set(item for item, value in args_dict.items() if value)

    # devcon testing
    if args_set & {'devcon_list', 'devcon_start', 'devcon_stop'}:
        if args.devcon_list:
            params = ['devcon', 'hwids', '=usb']
        elif args.devcon_start:
            params = ['devcon', 'enable', args.devcon_start]
        elif args.devcon_stop:
            params = ['devcon', 'disable', args.devcon_stop]

        result = run(params, capture_output=True, text=True)
        print(result.stdout)
    # run the program
    else:
        battery_alert = BatteryAlert(**args_dict)


if __name__ == '__main__':
    main()
