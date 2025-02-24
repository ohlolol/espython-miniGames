gc_name = "pndESP_DEV_Game"

class tasks:
    gc_tasks = "MiniGameSystem"
    gc_touch = {"spi": 2, "sck": 25, "mosi": 32, "miso": 39, "baud": 1000000, "cs": 33, "intPin": 36}
    ## new CYD the roation is 0 on the old one we need rotation 270
    gc_display = {"spi":1, "sck":14, "mosi":13, "baud":10000000, "dc":2, "cs":15, "rst":15, "width":320, "height":240, "bgr":False, "gamma":True, "rotation":0, "backlight":21}
    
    gc_games = {0:{"name":"4-Gewinnt", "source":"4winner", "plugins":{}},
                1:{"name":"Nummer-Raten", "source":"guess_number", "plugins":{}},
                2:{"name":"snake", "source":"snake", "plugins":{}}
                }
    
class defaults:
    gc_bTask   = False
    gc_wifi	   = False
    gc_battery = False
    gc_adc_min = 1024
    gc_adc_max = 4096
    gc_ntp_host = "time.pundoria.de"
    gc_looping = 1

class wifi:
    gc_ssid = ""
    gc_secret = ""
    
    