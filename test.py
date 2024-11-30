import time
from datetime import datetime, timedelta

if __name__ == '__main__':
    deadline = datetime.now() + timedelta(seconds=5)
    while(datetime.now() < deadline):
        time.sleep(1)
        print(deadline)
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))