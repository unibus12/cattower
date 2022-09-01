#-*-coding: utf-8-*-
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
Row1 = 31
Row2 = 33
Row3 = 35
Row4 = 37
Col1 = 32
Col2 = 36
Col3 = 38
Col4 = 40

GPIO.setup(Row1, GPIO.OUT)
GPIO.setup(Row2, GPIO.OUT)
GPIO.setup(Row3, GPIO.OUT)
GPIO.setup(Row4, GPIO.OUT)
GPIO.setup(Col1, GPIO.IN)
GPIO.setup(Col2, GPIO.IN)
GPIO.setup(Col3, GPIO.IN)
GPIO.setup(Col4, GPIO.IN)

def KeyScan():
	# 상위 니블을 스위칭하면서 출력
	#Init_data, PORTC의 상위 니블의 출력 값
	key_scan_line = [1,1,1,0]

	#키 스캔 라인 변경을 위한 반복문 인자, 키 매트릭스 열의 입력 값
	key_scan_loop = 0
	getPinData = 0
	key_num = 0 # 실제 눌린 키 매트릭스 값

	#키 스캔 반복문
	for key_scan_loop in range(4):
        	# 키 매트릭스의 스캔 라인 설정을 위한 PORTC 출력 값
        	# 4->5->6->7 순서대로 활성화 // row
		GPIO.output(31, key_scan_line[0])
		GPIO.output(33, key_scan_line[1])
		GPIO.output(35, key_scan_line[2])
		GPIO.output(37, key_scan_line[3])
		time.sleep(0.000001)

        	#key_scan_line 값을 순차적으로 1비트씩 총 3회 시프트함
        	# 0end = 0xEF, 1end = 0xDE, 2end = 0xBC, 3end = 0x78;
        	# 스캔 라인의 선택적 출력 값은 상위 니블만 해당하므로 하위 니블은 무시함
        	key_scan_line[0] = key_scan_line[1]
		key_scan_line[1] = key_scan_line[2]
		key_scan_line[2] = key_scan_line[3]
		if (key_scan_loop == 3):
			key_scan_line[3] = 0
		else:
			key_scan_line[3] = 1
		print(key_scan_line)

while True :
     	KeyScan()
