# FairDyne-Bot

This is a proof-of-concept bot for Unfair Undyne, a browser-based adaptation of the "Undyne" boss fight from the game Undertale

This project is intended for educational purposes only. Please respect the game's terms of service and use this bot responsibly.

## Features
- Real-time screen capture and processing using `mss` and `OpenCV`
- Two input methods
    - OS-level keyboard events using the `keyboard` library
    - WebSocket communication using `flask-socketio` for direct interaction with the game's source code
- Stable & resilient
    - Proven to run for 2+ hours without damage under test conditions*
    - Handles multiple arrows and fast movements effectively**

\* Testing was conducted on the `FIGHT THE TRUE HERO` difficulty setting. Red soul damage was disabled for the duration of the test.\
** The bot only misses red arrows (not implemented) and isolate cases (e.g. arrows that get close with few frames to spare).

## Input method comparison
| Method        | OS-level Keyboard Events | WebSocket Communication |
|---------------|--------------------------|-------------------------|
| **Setup Complexity** | Low                      | Medium (requires WebSocket setup)                 |
| **Responsiveness**   | Medium (depends on system): 10-50ms | Near instantaneous |
| **Stability**        | Medium (keystrokes may be sent to other applications) | High (only game visibility is required) |


## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/Powercube7/fairdyne-bot.git
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Choose your input method:
    - **OS-level Keyboard Events**:
      - Run the bot using:
         ```bash
         python keyboard_bot.py
         ```
    - **WebSocket Communication**:
      - Inject the `inject_listener.js` script into the game page using a browser extension like Tampermonkey or directly in the browser console by using the developer tools.
      - In a separate terminal, start a WebSocket server:
         ```bash
         python server.py
         ```
      - Run the bot using:
         ```bash
         python websocket_bot.py
         ```
4. (Optional) Adjust the screen capture area in the bot scripts by modifying the `monitor` variable.

### Credits
- UNDERTALE © 2015 Toby Fox
- [Fairdyne](https://github.com/joezeng/fairdyne) v0.99 by Joe Zeng
- Bot developed by Powercube

### Future Improvements
- Velocity-based arrow prediction instead of reaction-based movement + red arrow implementation
- Train a machine learning agent for red soul attack avoidance
- Cleaner code structure and configuration system