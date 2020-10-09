Battery Alert
=============

Summary
-------
Utility to let you know when a battery level is too low or too high on your laptop,
in order to save its battery lifespan.

I wrote this script for myself and found it very useful on my Surface Pro 7.
A new battery is not so expensive, but it's tricky to replace it on that laptop, and that's also extra waste/pollution.

Obviously, companies like Microsoft don't want us to easily replace the battery,
nor do they want us to extend the battery lifespan, because we would buy fewer devices.
Look at `planned obsolescence`: https://en.wikipedia.org/wiki/Planned_obsolescence


The problem
-----------
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

Solutions
---------
There are 3 ways to deal with this, that I found:
1) a sound alert, the advantage is that you're still in control, for example in some cases you may not want to stop
charging the laptop, if you're doing something important like playing some game. The problem is that if you're not there
to hear the sound, then the laptop will go all the way to 100% which will hurt the battery lifespan.

2) enable/disable charging. Not all manufacturers let you do this without some hacking, so it might not be safe,
but if you have a computer that gives you the tool to do this, then this is ideal of course, but then maybe they already
give the option to limit the battery, in which case my script is useless :)

3) enable/disable USB charging, for laptops being charged via USB. I haven't found a way to do this though,
as the laptop can still be charged even when turned off, but maybe the Operating System can control this sometimes.

The script has some kind of support for all 3 points.


Sound alert
-----------
So, the first solution is to detects if the battery is too low/high, and then emits a random alert sound.
The sounds are located in the `sound` folder, and can be replaced with anything, as long as they're `.ogg` or `.wav`.

Because the sound is played every 60 seconds (by default), I'm not forgetting anymore.


Custom command
--------------
If you have another program or script that can stop your laptop from charging, either by deactiving an USB port
or by directly stopping the battery, you can specify this with:
- --run-low : this is where you want to start charging
- --run-high : this is where you want to stop charging


USB powered laptop
------------------
Some laptops can be powered via USB, but normally a disabled USB port will still provide power delivery,
so this solution might not work at all and is experimental.
The program supports devcon.exe via `--devcon`, this will enable/disable the USB port when the battery level exceeds
the threshold. This is for Windows only.

https://docs.microsoft.com/en-us/windows-hardware/drivers/devtest/devcon


Install
-------
```
pip install -r requirements.txt
```

This installs `psutil` and `pygame`.


Examples
--------
1)
```
python battery-alert.py --every 60 --low 25 --high 75
```

This checks the battery level every 60 seconds, and raises an alarm if it goes below 25% or above 75%.

2)
```
python .\battery-alert.py --high 60 --run-high 'git status'
```

This runs `git status` when the battery goes above 60%, useless but you get the point!
You could have it launch firefox for example.


Sounds taken from
-----------------
https://freesound.org/people/plasterbrain/sounds/242856/
https://freesound.org/people/tim.kahn/sounds/83339/
https://freesound.org/people/VABsounds/sounds/394697/
https://freesound.org/people/Wagna/sounds/325987/
