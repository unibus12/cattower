#-*-coding: utf-8-*-
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings (False)
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
	# Init_data, PORTC의 상위 니블의 출력 값
	key_scan_line = [1,1,1,0]
	#키 스캔 라인 변경을 위한 반복문 인자, 키 매트릭스 열의 입력 값
	key_scan_loop = 0
	getPinData = [0,0,0,0]
	key_num = 0 # 실제 눌린 키 매트릭스 값

	#키 스캔 반복문
	for key_scan_loop in range(4):
        	# 키 매트릭스의 스캔 라인 설정 출력 값
        	# row
		GPIO.output(Row1, key_scan_line[0])
 	     	GPIO.output(Row2, key_scan_line[1])
      		GPIO.output(Row3, key_scan_line[2])
      		GPIO.output(Row4, key_scan_line[3])
		time.sleep(0.000001)

        	# 키 매트릭스의 열 값 취득
        	# C 포트의 하위 니블 값, 74LS14 사용으로 입력 신호가 반전되어 들어옴 // col
        	getPinData[0] = GPIO.input(Col1)
		getPinData[1] = GPIO.input(Col2)
		getPinData[2] = GPIO.input(Col3)
		getPinData[3] = GPIO.input(Col4)

        	if (getPinData[0]!=0 or getPinData[1]!=0 or getPinData[2]!=0 or getPinData[3]!=0):
  			if (getPinData[0]==1 and getPinData[1]==0 and getPinData[2]==0 and getPinData[3]==0):
				# C 포트의 하위 니블의 반전된 값
                		# 1110이 맞으면 현재 count 값에 4를 곱한 후
                        	#1을 더하고 key_num 변수에 저장
                    		key_num = key_scan_loop*4 + 1

			elif (getPinData[0]==0 and getPinData[1]==1 and getPinData[2]==0 and getPinData[3]==0):
                        	# C 포트의 하위 니블의 반전된 값
                        	# 1101이 맞으면 현재 count 값에 4를 곱한 후
                        	#2을 더하고 key_num 변수에 저장
                        	key_num = key_scan_loop*4 + 2

			elif (getPinData[0]==0 and getPinData[1]==0 and getPinData[2]==1 and getPinData[3]==0):
                        	# 1011이 맞으면 현재 count 값에 4를 곱한 후
                        	#3을 더하고 key_num 변수에 저장
                        	key_num = key_scan_loop*4 + 3

                	elif (getPinData[0]==0 and getPinData[1]==0 and getPinData[2]==0 and getPinData[3]==1):
                        	# 0111이 맞으면 현재 count 값에 4를 곱한 후
                        	#4을 더하고 key_num 변수에 저장
                        	key_num = key_scan_loop*4 + 4
			#print(key_num)
			return key_num
        	#key_scan_line 값을 순차적으로 1비트씩 총 3회 시프트함
        	key_scan_line[0] = key_scan_line[1]
		key_scan_line[1] = key_scan_line[2]
      		key_scan_line[2] = key_scan_line[3]
      		if (key_scan_loop == 3):
         		key_scan_line[3] = 0
      		else:
         		key_scan_line[3] = 1

count = 0
# 여기부터 main
while True :
	count = KeyScan()
	print(count)
	time.sleep(1)
