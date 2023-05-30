import sensor, image, time, math
from pyb import UART,LED
uart = UART(3,115200)
uart.init(115200, bits=8, parity=None, stop=1)
def sending_data(x,y,z):
	global uart;
	data = bytearray([0x2C,0x12,x,y,z,0x5B])
	uart.write(data);
GRAYSCALE_THRESHOLD = [(0, 60)]
ROIS = [(0, 80, 160, 20, 0.7)]
sensor.reset()
LED(1).on()
LED(2).on()
LED(3).on()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
clock = time.clock()
while(True):
	clock.tick()
	img = sensor.snapshot()
	centroid_sum = 0
	for r in ROIS:
		blobs = img.find_blobs(GRAYSCALE_THRESHOLD, roi=ROIS[0:4], merge=True)
		sb=len(blobs)
		if blobs:
			for largest_blob in blobs:
				img.draw_rectangle(largest_blob.rect())
				img.draw_cross(largest_blob.cx(), largest_blob.cy())
				sending_data(largest_blob.cx(),sb,1)
