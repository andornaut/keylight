MIN_BRIGHTNESS = 0
MAX_BRIGHTNESS = 100

MIN_COLOR = 2900
# Although the API accepts values up to 7000, 6987 is the maximum that was observed to work.
MAX_COLOR = 7000

DEFAULT_PORT = 9123

# Seconds to wait for Zeroconf discovery to find a Key Light.
DISCOVERY_TIMEOUT = 1

# Seconds to wait on a single HTTP request to the Key Light. A light that has
# been idle takes several seconds to answer its first request, so this is set
# well above the sub-second time a woken light takes.
REQUEST_TIMEOUT = 15
