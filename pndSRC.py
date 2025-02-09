import network
import pndConfig as cfg
import time
import ntptime
import machine
import socket
import gc
import sys
import ujson
import json
from machine import Pin, I2C, ADC

class storage():
    def __init__(self):
        self.file = "data.pnd"
        self.str = ""
        self.obj = {}
    
    def read(self):
        r = open(self.file)
        self.obj = json.loads(r.read())
        return self.obj
        
    def write(self, obj):
        self.str = json.dumps(obj, separators=None)
        f = open(self.file, "w" )
        f.write(self.str)
        f.close()
        
    def cx(self, cx):
        mystr = json.dumps(cx, separators=None)
        f = open("cx.pnd", "w" )
        f.write(mystr)
        f.close()

class dtime():
    def __init__(self):
        year, mon, day, h, m, s, nope, nope2 = time.localtime()
        h = h + 2
        year = year - 2000
        if(h == 24 ):
            h = 0
        elif(h == 25):
            h = 1 
        self.date = str(day) + "." + str(mon) + "." + str(year)
        if(m < 10):
            sM = "0" + str(m)
        else:
            sM = str(m)
        if(s < 10):
            sS = "0" + str(s)
        else:
            sS = str(s)
        if(h < 10):
            sH = "0" + str(h)
        else:
            sH = str(h)
        self.time = sH + ":" + sM+ ":" + sS

class wifi():
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.lastTry = 0
        self.e = "wifi struggles"
        
    def connect(self):
        conntimeout = 0
        wlan = self.wlan
        wlan.active(False)
        wlan.active(True)
        wlan.connect(cfg.wifi.gc_ssid, cfg.wifi.gc_secret)
        print('connecting to: ' + cfg.wifi.gc_ssid)
        while not wlan.isconnected():
            print('connecting...')
            time.sleep(1)
            conntimeout = conntimeout + 1
            if(conntimeout > 20): break
        if(not wlan.isconnected()): ecx.handle(ecx(),self,self.e)
        
        print(wlan.ifconfig())
        print('connected!')

    def disconnect(self):
        wlan = self.wlan
        wlan.disconnect()
        wlan.active(False)
        print('disconnected!')
        
    def reconnect(self):
        wlan = self.wlan
        wlan.disconnect()
        wlan.active(False)
        print('disconnected!')
        wlan.active(False)
        del wlan
        time.sleep(1)
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        conntimeout = 1
        self.wlan.connect(cfg.wifi.gc_ssid, cfg.wifi.gc_secret)
        print('connecting to: ' + cfg.wifi.gc_ssid)
        while not self.wlan.isconnected():
            print('connecting...')
            time.sleep(1)
            conntimeout = conntimeout + 1
            self.lastTry = 1
            if(conntimeout > 20): break
            
        if(not self.wlan.isconnected()): ecx.handle(ecx(),self, self.e)
            
    def getMac(self):
        import ubinascii
        mac = ubinascii.hexlify(self.wlan.config('mac'),':').decode()
        return mac
        
    def status(self):
        wlan = self.wlan
        status = wlan.status()
        if(status == 3):
            ip, netmask, gateway, dns = wlan.ifconfig()
            status =  "\r\nWLan connected to: " + cfg.wifi.gc_ssid
            status += "\r\nWLan IP: " + ip
            status += "\r\nWLan NetMask: " + netmask
            status += "\r\nWLan Gateway: " + gateway
            status += "\r\nWLan DNS: " + dns
            return status
        else:
            return "\r\nnot connected"
    
    def getIp(self):
        wlan = self.wlan
        ip, netmask, gateway, dns = wlan.ifconfig()
        return ip
        
class system():
    def __init__(self):
        self.timeInit = time.time()
        self.obj = None
    
    def setCallback(self, obj):
        self.cb = obj
        
    def status(self):
        cpufq = machine.freq() / 1000000
        memfree = gc.mem_free() / 1024
        memusage = gc.mem_alloc() / 1024
        mem = memfree + memusage
        if(self.cb.cfg.defaults.gc_battery):
            loop = self.cb.looping / 1000
            loop = loop / 60
            uptimeS = 01
            self.cb.data["uptimeM"] = self.cb.cycle * loop
            self.cb.data["uptimeH"] = self.cb.data["uptimeM"] / 60
            self.cb.data["uptimeD"] = self.cb.data["uptimeH"] / 24
        
        else:
            uptimeS = self.cb.cycle * self.cb.looping
            self.cb.data["uptimeM"] = uptimeS / 60
            self.cb.data["uptimeH"] = self.cb.data["uptimeM"] / 60
            self.cb.data["uptimeD"] = self.cb.data["uptimeH"] / 24
        print("tiefer")
        system = "System:\nDevice: "+ cfg.gc_name + "\nSystem: " + sys.platform + "\nFirmware: " + sys.version 
        system += "\n\nRessources:\nCPU Speed: " + "{:.0f}".format(cpufq) + "MHz"
        system += "\nMEM All: " + "{:.2f}".format(mem) + "Kb"
        system += "\nMEM Free: " + "{:.2f}".format(memfree) + "Kb"
        system += "\nMEM Used: " + "{:.2f}".format(memusage) + "Kb"
        system += "\nSYS Uptime: "+ str(self.cb.data["uptimeD"] ) + ":" + str(self.cb.data["uptimeH"] ) + ":" + str(self.cb.data["uptimeM"] ) + ":" + str(uptimeS)
        system += "\nSYS MQTT Message Count: " + "{:.0f}".format(self.cb.cycle) + "Messages"
        return system

    def statusJSON(self):

        cpufq = machine.freq() / 1000000
        memfree = gc.mem_free() / 1024
        memusage = gc.mem_alloc() / 1024
        mem = memfree + memusage
        if(self.cb.cfg.defaults.gc_battery):
            loop = self.cb.looping / 1000
            loop = loop / 60
            uptimeS = 01
            self.cb.data["uptimeM"] = self.cb.cycle * loop
            self.cb.data["uptimeH"] = self.cb.data["uptimeM"] / 60
            self.cb.data["uptimeD"] = self.cb.data["uptimeH"] / 24
        
        else:
            uptimeS = self.cb.cycle * self.cb.looping
            self.cb.data["uptimeM"] = uptimeS / 60
            self.cb.data["uptimeH"] = self.cb.data["uptimeM"] / 60
            self.cb.data["uptimeD"] = self.cb.data["uptimeH"] / 24
            
        jsSys = ujson.dumps({ "ip": self.cb.wifi.getIp(), "name": cfg.gc_name, "mqtt_msg_count": self.cb.cycle, "uptime_min" : self.cb.data["uptimeM"], "uptime_days" : "{:.2f}".format(self.cb.data["uptimeD"]),
                              "uptime_hr" : "{:.2f}".format(self.cb.data["uptimeH"]), "memory" : "{:.2f}".format(mem), "mem_free" : "{:.2f}".format(memfree), "mem_usage" : "{:.2f}".format(memusage) })
        return jsSys
    
    def getUptimeM(self):
        timeDiff = time.time()-self.timeInit  
        (minutes, seconds) = divmod(timeDiff, 60)  
        (hours, minutes) = divmod(minutes, 60)  
        (days,hours) = divmod(hours, 24)
        return minutes
    
class ecx():
    def handle(self,obj, e):
        try:
            if(hasattr(obj, 'lastTry')):
                if(obj.lastTry == 1):
                    print("FATAL ERROR - Restart device. Error: " + str(e))
                    time.sleep(5) 
                    machine.reset()
                        
            print("FATAL ERROR - Trying recovery from: " + str(e))
            time.sleep(2)
            del obj
            import pnd as recoverPND
            fresh_runtime = recoverPND.rt()
            fresh_runtime.init(1)
            time.sleep(1)
            fresh_runtime.run()
        except:
            import pnd as lastPND
            last_runtime = lastPND.rt()
            last_runtime.init(1)
            time.sleep(1)
            last_runtime.run()
    
class webserver():
    sockl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockl.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def showStatusPage(self):
        s = self.sockl
        s.bind(('', 80))
        s.listen(5)
        print('WebServices up and running! Waiting for connections...')
        while True:
            try:
                conn, addr = s.accept()
                print('Got a connection from %s' % str(addr))
                request = conn.recv(1024)
                request = str(request)
                self.handler(request, conn)
                gc.collect()
            except Exception as e:
                pass
            
    def handler(self, request, conn):
        #print('Request = %s' % request)
        json = request.find('/?json=')
        if(json == 6):
            self.JSONHandler(request, conn)
            exit()
        
        
        get = request.find('/?get=system')
        restart = request.find('/?fun=reset')
        print(get)
        response = ""
        if(get == 6):
            s = Psystem.status()
            final = s.replace("\n", "<br>")
            response += '<html><head><title>Pundo Web Server</title></head><body><h1>Pundo Web Server</h1><p><strong>' + final + '</strong></p></body></html>'
            print("bin 2")
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
            conn.close()
            
        elif(restart == 6):
            print('time to restart')
            response += '<html><head><title>Pundo Web Server</title></head><body><h1>Pundo Web Server</h1><p><strong>Rebooting</strong></p></body></html>'
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
            conn.close()
            time.sleep(3)
            machine.reset()
        
        else:
            response += '<html><head><title>Pundo Web Server</title></head><body><h1>Pundo Web Server</h1><p><strong>Wrong Command</strong></p></body></html>'
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
            conn.close()
        
            
    def JSONHandler(self, request, conn):
        pass
    
    
class pndIFBase:
    def pndObj(self, id:str) -> Object:
        """Test pls hang on"""
        pass
    def pndTest(self) ->str:
        return "Still in development please hang on"
    
class httpRQ(pndIFBase):
    def pndObj(self):
        return self
    
    def post(self, url, data):
        post_data = data ##ujson.dumps(data)
        request_url = url
        res = requests.post(request_url, headers = {'content-type': 'application/json'}, data = post_data)
        return res.text
    
class pndIFGame:
    Game = object()
    def gameRuntime(self) -> Object:
        """Must return an object wtih an run method"""
        pass
    
    def setUp(self) ->str:
        self.Game = self.gameRuntime()
        self.Game.setup()
        return "setup Done"
    def run(self) ->str:
        self.Game.run()
        return "Game started"
    def stop(self) ->str:
        self.Game.stop()
        return "Game Stopped"

