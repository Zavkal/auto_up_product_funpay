import time
import config #noqa
from adapters.adapter_base import SeleniumConfirmation

if __name__ == '__main__':
    while True:
        base_adapter = SeleniumConfirmation()
        base_adapter.login_up_products()
        time.sleep(14400)