# 2023-24 Worlds

This is our team's source for the 2023 VEX Robotics World Championship. Hopefully you can learn something (or criticize!).

I'm thinking about trying to get a MATLAB educational license and using that next year, or at least switching to PROS instead of my home-built solution (it works well, but still, _Python_).

By the way, a lot of the older commits attributed to @rh0820 were actually authored by @zabackary; I just was lazy and didn't touch the git config. In addition, I don't think @plumking actually touched the project (he was doing scouting/booth planning) so those commits are likely @Spacyhula's. Most of the final code was written by @zabackary, but the drive team, @Spacyhula, and @rh0820 were essential for making this happen by setting up the field, etc., and @Spacyhula and @rh0820 helped think up a lot of the ideas that went into the final product.

## Setup

1. Install vexmason if you don't have it already.
2. Create the local configuration at [`.vscode/vexmason-local-config.json`](./.vscode/vexmason-local-config.json). Use the following as a template:
```json
{
    "config_version": "1.1",
    "defines_overrides": {
        "__USE_REAL_BOT__": true,
        "__AUTONOMOUS_ROUTE__": "Offense 1",
        "__COMPETITION_MODE__": true
    }
}
```
3. Install the dependencies with `pip install -r requirements.txt`
4. (optional) Ignore errors in [`compiled.py`](./build/compiled.py) as they don't matter by adding the following to [`.vscode/settings.json`](./.vscode/settings.json) inside of the JSON object:
```json
"python.analysis.ignore": [
    "build/compiled.py"
]
```
5. (optional) Upload the contents of [`resources/sdcard`](./resources/sdcard/) to the root directory of an SD card and put it in the V5 brain to show the logo image.

If you run into any problems while compiling (i.e., an error popup saying VEX Error in the bottom right of your screen), make sure to check [`build/vexmason.log`](./build/vexmason.log) to see if there's any useful logs. If the error is a line 1 syntax error, chances are the upload failed (maybe you interrupted it?), so simply re-upload it. If the error is a syntax error for something that works on your development machine, keep in mind that V5 Python is built on MicroPython and only supports syntax up until around Python 3.5 (i.e. no `match` or positional-only arguments among other things).
