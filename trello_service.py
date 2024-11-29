from datetime import datetime
import time
import sys

from trello_main import main

MOVE_HOUR = 4

if next(iter(sys.argv[1:])) == "--now":
    print("executing NOW", flush=True)
    main()
else:
    print("service started", flush=True)

while True:
    now = datetime.now()
    if now.hour == MOVE_HOUR and now.minute == 0:
        main()
        # Ensure "minute == 0" check to happen only once per day
        time.sleep(100)
    else:
        # Often enough for "minute == 0" check to happen
        time.sleep(10)
