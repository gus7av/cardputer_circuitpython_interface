import sdcardio
import storage
import board
import sys

sd = sdcardio.SDCard(board.SD_SPI(), board.SD_CS)
vfs = storage.VfsFat(sd)
storage.mount(vfs, "/sd")
sd_lib_path = "/sd/lib"
sys.path.append(sd_lib_path)
