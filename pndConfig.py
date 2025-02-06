gc_name = "pndESP_DEV_Game"

class tasks:
    gc_tasks = "Game"
    ## gc_sensors = {0:{"name":"DS18X20_1", "type":"DS18X20","pin": 4, "ADC": False},
   ##               1:{"name":"DHT11_2", "type":"DHT11","pin": 27, "ADC": False},
   ##               2:{"name":"DHT11_3", "type":"DHT11","pin": 28, "ADC": False},
    ##              3:{"name":"Moisture_1", "type":"MOIST","pin": 0, "ADC": True},
   ##              4:{"name":"Moisture_2", "type":"MOIST","pin": 33, "ADC": True},
   ##               5:{"name":"Moisture_3", "type":"MOIST","pin": 35, "ADC": True}
    ##              }
    ##gc_display = { "sdaPin":6, "sclPin":7, "type": "SSD1306_I2C", "name": "myDisp", "widht":128, "height": 64}

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
    