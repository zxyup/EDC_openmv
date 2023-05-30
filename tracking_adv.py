import sensor, image, time, math
from pyb import UART,LED
uart = UART(3,115200)
uart.init(115200, bits=8, parity=None, stop=1)
def sending_data(x,y,z):
	global uart;
	data = bytearray([0x2C,0x12,x,y,z,0x5B])
	uart.write(data);
GRAYSCALE_THRESHOLD = [(0, 60)]
ROIS = [(0, 80, 160, 20),(0, 10, 160, 20)]
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
clock = time.clock()
LED(1).on()
LED(2).on()
LED(3).on()
while(True):
	clock.tick()
	img = sensor.snapshot()
	a=80
	b=80
	blobs1 = img.find_blobs(GRAYSCALE_THRESHOLD, roi=ROIS[0], merge=True)
	if(blobs1):
		lb1 = blobs1[0]
		a=lb1.cx()
	blobs2 = img.find_blobs(GRAYSCALE_THRESHOLD, roi=ROIS[1], merge=True)
	if(blobs1 and blobs2):
		lb2 = blobs2[0]
		a=lb1.cx()
		dx=0.8*a+0.2*b
	else:
		dx=a
	dx=int(dx)
	print(dx)
	sending_data(dx,1,1)
