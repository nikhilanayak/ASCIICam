# ASCIICam - Display Your Camera In Your Terminal Using Python
ASCIICam uses OpenCV and curses to display pixels from your camera in your terminal using ASCII text.



## Running
To run (`python3`):
* Clone this repo (Download zip or using `git` CLI)
* Run: `pip install -r requirements.txt` to install the required packages
* Run: `python main.py` (or `python3` on some systems)


## Options
To find the help menu, run `python main.py --help`
* --width x (int) - sets the width of the output screen to x chars
* --height y (int) - sets the height of the output screen to y chars
* --usecolor b (bool) - if enabled, uses grayscale to create a "heatmap" with terminal colors. Otherwise, displays in grayscale
* --showfps b (bool) - if disabled, hides FPS from top left of screen. Otherwise, shows FPS




# TODO
* Multithreading. On my computer, the processing, streaming, etc. runs at ~30 fps. Some optimization is possible but multithreading (or numpy vectorization) will cause significant improvements