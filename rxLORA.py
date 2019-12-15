from time import sleep
from SX127x.LoRa import *
from SX127x.board_config import BOARD

BOARD.setup()
lora = LoRa()

def RX():
    BOARD.led_on()
    print("\nDados recebidos")
    lora.clear_irq_flags(RxDone=1)
    payload = lora.read_payload(nocheck=True)
    print(bytes(payload).decode("utf-8",'ignore'))
    lora.set_mode(MODE.SLEEP)
    lora.reset_ptr_rx()
    BOARD.led_off()
    lora.set_mode(MODE.RXCONT)
RX()
