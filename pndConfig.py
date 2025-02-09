gc_name = "pndESP_DEV_Game"

class tasks:
    gc_tasks = "Game"
    gc_touch = {"spi": 2, "sck": 25, "mosi": 32, "miso": 39, "baud": 10000000, "cs": 33, "intPin": 36}
    gc_display = {"spi":1, "sck":14, "mosi":13, "baud":10000000, "dc":2, "cs":15, "rst":15, "width":320, "height":240, "bgr":False, "gamma":True, "rotation":270, "backlight":21}
    gc_games = {0:{"name":"4-Gewinnt", "source":"4winner", "plugins":{}},
                1:{"name":"Nummer-Raten", "source":"guess_number", "plugins":{}}}
    
class defaults:
    gc_battery = True
    gc_adc_min = 1024
    gc_adc_max = 4096
    gc_ntp_host = "time.pundoria.de"
    gc_looping = 1

class wifi:
    gc_ssid = "Schnell2.4"
    gc_secret = "llenhcS1!"
    
class mqtt:
    gc_host = "mq.pundoria.de"
    gc_port = 1883
    gc_topic_config ="pndpg/"+ gc_name +"/config"
    gc_topic_sensor ="pndpg/"+ gc_name +"/sensors"
    gc_user = "pndiot"
    gc_secret = "illi123"
    