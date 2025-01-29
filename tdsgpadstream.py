from tango.server import Device, attribute, command
import threading
import time
import tango
import numpy as np
import socket
 
class Gamepad(Device):
    ## tango attributes
    polling_period = 100
    bt01 = attribute(label="D_Up", dtype='int', access=tango.READ, rel_change=1, polling_period=polling_period)
    bt02 = attribute(label="D_Down", dtype='int', access=tango.READ, rel_change=1, polling_period=polling_period)
    bt03 = attribute(label="D_Left", dtype='int', access=tango.READ, rel_change=1, polling_period=polling_period)
    bt04 = attribute(label="D_Right", dtype='int', access=tango.READ, rel_change=1, polling_period=polling_period)
    bt05 = attribute(label="Start", dtype='int', access=tango.READ, rel_change=1, polling_period=polling_period)
    bt06 = attribute(label="Back", dtype='int', access=tango.READ, rel_change=1, polling_period=polling_period)
    bt07 = attribute(label="LA", dtype='int', access=tango.READ, rel_change=1, polling_period=polling_period)
    bt08 = attribute(label="RA", dtype='int', access=tango.READ, rel_change=1, polling_period=polling_period)
    bt09 = attribute(label="L_Button", dtype='int', access=tango.READ, rel_change=1, polling_period=polling_period)
    bt10 = attribute(label="R_Button", dtype='int', access=tango.READ, rel_change=1, polling_period=polling_period)
    bt11 = attribute(label="B_11", dtype='int', access=tango.READ, rel_change=1, polling_period=polling_period)
    bt12 = attribute(label="B_12", dtype='int', access=tango.READ, rel_change=1, polling_period=polling_period)
    bt13 = attribute(label="A", dtype='int', access=tango.READ, rel_change=1, polling_period=polling_period)
    bt14 = attribute(label="B", dtype='int', access=tango.READ, rel_change=1, polling_period=polling_period)
    bt15 = attribute(label="X", dtype='int', access=tango.READ, rel_change=1, polling_period=polling_period)
    bt16 = attribute(label="Y", dtype='int', access=tango.READ, rel_change=1, polling_period=polling_period)

    vr01 = attribute(dtype='float', access=tango.READ, rel_change=1, polling_period=polling_period)
    vr02 = attribute(dtype='float', access=tango.READ, rel_change=1, polling_period=polling_period)
    vr03 = attribute(dtype='float', access=tango.READ, rel_change=1, polling_period=polling_period)
    vr04 = attribute(dtype='float', access=tango.READ, rel_change=1, polling_period=polling_period)
    vr05 = attribute(dtype='float', access=tango.READ, rel_change=1, polling_period=polling_period)
    vr06 = attribute(dtype='float', access=tango.READ, rel_change=1, polling_period=polling_period)

    ## init variables
    statusbit = 0
    _bt01 = 0
    _bt02 = 0
    _bt03 = 0
    _bt04 = 0
    _bt05 = 0
    _bt06 = 0
    _bt07 = 0
    _bt08 = 0
    _bt09 = 0
    _bt10 = 0
    _bt11 = 0
    _bt12 = 0
    _bt13 = 0
    _bt14 = 0
    _bt15 = 0
    _bt16 = 0

    _vr01 = 0.0
    _vr02 = 0.0
    _vr03 = 0.0
    _vr04 = 0.0
    _vr05 = 0.0
    _vr06 = 0.0

    ## udp variables
    udpport = 10123
    buffer_size = 128
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", udpport))

    ## tango attribute read functions
    def read_bt01(self): return self._bt01
    def read_bt02(self): return self._bt02
    def read_bt03(self): return self._bt03
    def read_bt04(self): return self._bt04
    def read_bt05(self): return self._bt05
    def read_bt06(self): return self._bt06
    def read_bt07(self): return self._bt07
    def read_bt08(self): return self._bt08
    def read_bt09(self): return self._bt09
    def read_bt10(self): return self._bt10
    def read_bt11(self): return self._bt11
    def read_bt12(self): return self._bt12
    def read_bt13(self): return self._bt13
    def read_bt14(self): return self._bt14
    def read_bt15(self): return self._bt15
    def read_bt16(self): return self._bt16

    def read_vr01(self): return self._vr01
    def read_vr02(self): return self._vr02
    def read_vr03(self): return self._vr03
    def read_vr04(self): return self._vr04
    def read_vr05(self): return self._vr05
    def read_vr06(self): return self._vr06
    
    def init_device(self):
        super().init_device()
        self.set_state(tango.DevState.ON)
        self.t = threading.Thread(target=self.update_loop)
        self.t.start()
 
    def update_loop(self):
        print("Thread loop starting in 2 seconds...")
        time.sleep(2)
        #t0 = time.time()
        while True:
            try:
                data, addr = self.sock.recvfrom(self.buffer_size)
                #t1 = time.time()
                #print("Loop time: {:.3f} ms".format((t1-t0)*1000))
                #t0 = t1
                #print(f"Received message: {data.decode()} from {addr}")
                msg = data.decode().strip().split(',')
                self.statusbit = int(msg[0])
                a = int(msg[1])
                self._bt01 = (a>>0 & 0x01)
                self._bt02 = (a>>1 & 0x01)
                self._bt03 = (a>>2 & 0x01)
                self._bt04 = (a>>3 & 0x01)
                self._bt05 = (a>>4 & 0x01)
                self._bt06 = (a>>5 & 0x01)
                self._bt07 = (a>>6 & 0x01)
                self._bt08 = (a>>7 & 0x01)
                self._bt09 = (a>>8 & 0x01)
                self._bt10 = (a>>9 & 0x01)
                self._bt11 = (a>>10 & 0x01)
                self._bt12 = (a>>11 & 0x01)
                self._bt13 = (a>>12 & 0x01)
                self._bt14 = (a>>13 & 0x01)
                self._bt15 = (a>>14 & 0x01)
                self._bt16 = (a>>15 & 0x01)
                self._vr01 = float(msg[2])
                self._vr02 = float(msg[3])
                self._vr03 = float(msg[4])
                self._vr04 = float(msg[5])
                self._vr05 = float(msg[6])
                self._vr06 = float(msg[7])
                if self.statusbit==0:
                    self.set_state(tango.DevState.STANDBY)
                else:
                    self.set_state(tango.DevState.ON)
            except Exception as e:
                print(f"Error: {e}")
                self.set_state(tango.DevState.FAULT)
                time.sleep(5) 
 
if __name__ == "__main__":
    Gamepad.run_server()
