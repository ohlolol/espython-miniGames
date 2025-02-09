import pndSRC as mypnd
import pndConfig as cfg
import ntptime
import ujson
import time
import machine
import array
import gc



class rt():
    
    wifi = mypnd.wifi
    Psystem = mypnd.Psystem
    lastTry = 0
    cycle = 0
    looping = 0
    
    def run(self):
        self.cycle = 1
        while True:
            try:
               ## main loop
                gc.collect()
                machine.idle()
                self.mq = mqService()
                self.mq.logConf()
                if hasattr(cfg.tasks, "gc_sensors"):
                    self.mq.logSensors(self.Sensors)
                self.mq.close()
                del self.mq
                print(self.Psystem.status())
                year, mon, day, h, m, s, nope, nope2 = time.localtime()
                if((m % 55) == 0):
                    self.wifi.reconnect()
                self.cycle = self.cycle + 1
                if(self.cycle > 10000): self.cycle = 1
                machine.idle()
                time.sleep(self.looping)
            except OSError as e:
                mypnd.ecx.handle(self,e)

    def backgroundTask(self):

        lhttp = mypnd.webserver()
        print('starting Webserver...')
        
        ## method with main loop goes here
        lhttp.showStatusPage()

    def init(self, lastTry):
        try:
            self.Psystem.setCallback(self)
            i = 0
            self.lastTry = lastTry
            self.wifi.connect()
            ntptime.host = cfg.defaults.gc_ntp_host
            try:
                ntptime.settime()
            except:
                pass
            if hasattr(cfg.tasks, "gc_sensors"):
                self.Sensors = {}
                for sens in cfg.tasks.gc_sensors:
                    if cfg.tasks.gc_sensors[sens]['ADC']:
                        self.Sensors[i] = mypnd.adcsens(cfg.tasks.gc_sensors[sens]['name'],cfg.tasks.gc_sensors[sens]['pin'])
                    else:
                        self.Sensors[i] = mypnd.sens(cfg.tasks.gc_sensors[sens]['name'],cfg.tasks.gc_sensors[sens]['type'],cfg.tasks.gc_sensors[sens]['pin'])
                    i += 1                 
            self.looping = cfg.defaults.gc_looping
        except OSError as e:
            mypnd.ecx.handle(self,e)
        
        
class pndCBObejct():
    me = object()
    caller = object()
    
    def __init__(self, caller):
        self.me = self
        self.caller = caller
        
    def getMe(self):
        return self.me
    
    def getCaller(self):
        return self.caller
    
