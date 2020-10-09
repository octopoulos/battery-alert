Battery Alert
=============

Problem
-------
I wrote this script for myself, then realized it could be useful to other people as well.

Batteries in laptops can have a short lifespan, especially:
- if the battery level reaches 0% or 100%
- if they're charged too quickly (fast charging)
- if the temperature is too high

Some battery saving is achieved if the charge-discharge amplitude is minimized, so if the level stays close to 50%:
- 50-50 : ideal
- 40-60 : great
- 30-70 : very good
- 20-80 : good
- 10-90 : bad

So, until now, I've been trying to constantly watch the battery status, and of course, most of the time I fail
to notice that it's too low or too high!

Solution
--------
Unfortunately, it's not possible to stop the battery from charging the laptop, at least not for all laptops.
So, this program detects if the battery is too low/high, then emits a random sound.
The sounds are located in the `sound` folder, and can be replaced with anything, as long as they're `.ogg` or `.wav`.

Because the sound is played every 60 seconds (by default), I'm not forgetting anymore.

Sounds taken from:
https://freesound.org/people/plasterbrain/sounds/242856/
https://freesound.org/people/tim.kahn/sounds/83339/
https://freesound.org/people/VABsounds/sounds/394697/
https://freesound.org/people/Wagna/sounds/325987/

Install
-------
```
pip install -r requirements.txt
```

This installs `psutil` and `pygame`.


Run
---

```
python battery-alert.py --every 60 --low 25 --high 75
```

This checks the battery level every 60 seconds, and raises an alarm if it goes below 25% or above 75%.
