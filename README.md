# RotorHazard-plugins


1) Put `rh_led_handler_circles` and `rh_led_handler_clock` to `src/server/plugins`

2) Add new parameter to `LED` section in `config.json`:
 
   - `"CLOCK_COLOR": "blue"` (red/yellow/green/blue/white)

3) Set parameters in `LED` section :

   - `"LED_ROWS": 4` or `"LED_ROWS": 8`
 
   - `"INVERTED_PANEL_ROWS": true` if characters are broken

   - `"PANEL_ROTATE": 1` if text is upside-down

4) Select LED Events:

   - Race Staging - Staging Circles
   
   - Race Stop - Circles

   - Race Start - GO!

   - Server Startup - Real Time Clock

   - Idle (Ready, Racing, Stopped)  - Real Time Clock
