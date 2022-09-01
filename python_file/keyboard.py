#-*-coding: utf-8-*-
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings (False)

Row = [29, 31, 33, 35, 37]
Col = [12, 16, 18, 22, 24, 26, 32, 36, 38, 40]

han1 = ['ㄱ','ㄴ','ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
han2 = ['ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅒ', 'ㅔ', 'ㅖ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅢ']
han3 = ['ㄲ','ㄸ','ㅃ', 'ㅆ', 'ㅉ']

count = 0
for i in range(5):
        GPIO.setup(Row[i], GPIO.OUT)
for i in range(10):
        GPIO.setup(Col[i], GPIO.IN)

def KeyScan():
	# 상위 니블을 스위칭하면서 출력
	# Init_data, PORTC의 상위 니블의 출력 값
	key_scan_line = [1,1,1,1,0]
	#키 스캔 라인 변경을 위한 반복문 인자, 키 매트릭스 열의 입력 값
	key_scan_loop = 0
	getPinData = [0,0,0,0,0,0,0,0,0,0]
	key_num = 0 # 실제 눌린 키 매트릭스 값

	#키 스캔 반복문
	for key_scan_loop in range(5):
        	# 키 매트릭스의 스캔 라인 설정 출력 값
        	# row
		GPIO.output(Row[0], key_scan_line[0])
		GPIO.output(Row[1], key_scan_line[1])
		GPIO.output(Row[2], key_scan_line[2])
		GPIO.output(Row[3], key_scan_line[3])
		GPIO.output(Row[4], key_scan_line[4])
		time.sleep(0.000001)
		# 키 매트릭스의 열 값 취득
        	# C 포트의 하위 니블 값, 74LS14 사용으로 입력 신호가 반전되어 들어옴 // col
		getPinData[0] = GPIO.input(Col[0])
		getPinData[1] = GPIO.input(Col[1])
		getPinData[2] = GPIO.input(Col[2])
		getPinData[3] = GPIO.input(Col[3])
		getPinData[4] = GPIO.input(Col[4])
		getPinData[5] = GPIO.input(Col[5])
		getPinData[6] = GPIO.input(Col[6])
		getPinData[7] = GPIO.input(Col[7])
		getPinData[8] = GPIO.input(Col[8])
		getPinData[9] = GPIO.input(Col[9])

		if (getPinData[0]!=0 or getPinData[1]!=0 or getPinData[2]!=0 or getPinData[3]!=0 or getPinData[4]!=0 or getPinData[5]!=0 or getPinData[6]!=0 or getPinData[7]!=0 or getPinData[8]!=0 or getPinData[9]!=0):
			if (getPinData[0]==1 and getPinData[1]==0 and getPinData[2]==0 and getPinData[3]==0 and getPinData[4]==0 and getPinData[5]==0 and getPinData[6]==0 and getPinData[7]==0 and getPinData[8]==0 and getPinData[9]==0):
				key_num = key_scan_loop*9 + 1
                                # 입력의 반전된 값
                        	# 현재 count 값에 9를 곱한 후
                        	# 숫자를 더하고 key_num 변수에 저장
			elif (getPinData[0]==0 and getPinData[1]==1 and getPinData[2]==0 and getPinData[3]==0 and getPinData[4]==0 and getPinData[5]==0 and getPinData[6]==0 and getPinData[7]==0 and getPinData[8]==0 and getPinData[9]==0):
				key_num = key_scan_loop*9 + 2
			elif (getPinData[0]==0 and getPinData[1]==0 and getPinData[2]==1 and getPinData[3]==0 and getPinData[4]==0 and getPinData[5]==0 and getPinData[6]==0 and getPinData[7]==0 and getPinData[8]==0 and getPinData[9]==0):
				key_num = key_scan_loop*9 + 3
			elif (getPinData[0]==0 and getPinData[1]==0 and getPinData[2]==0 and getPinData[3]==1 and getPinData[4]==0 and getPinData[5]==0 and getPinData[6]==0 and getPinData[7]==0 and getPinData[8]==0 and getPinData[9]==0):
				key_num = key_scan_loop*9 + 4
			elif (getPinData[0]==0 and getPinData[1]==0 and getPinData[2]==0 and getPinData[3]==0 and getPinData[4]==1 and getPinData[5]==0 and getPinData[6]==0 and getPinData[7]==0 and getPinData[8]==0 and getPinData[9]==0):
				key_num = key_scan_loop*9 + 5
			elif (getPinData[0]==0 and getPinData[1]==0 and getPinData[2]==0 and getPinData[3]==0 and getPinData[4]==0 and getPinData[5]==1 and getPinData[6]==0 and getPinData[7]==0 and getPinData[8]==0 and getPinData[9]==0):
				key_num = key_scan_loop*9 + 6
			elif (getPinData[0]==0 and getPinData[1]==0 and getPinData[2]==0 and getPinData[3]==0 and getPinData[4]==0 and getPinData[5]==0 and getPinData[6]==1 and getPinData[7]==0 and getPinData[8]==0 and getPinData[9]==0):
				key_num = key_scan_loop*9 + 7
			elif (getPinData[0]==0 and getPinData[1]==0 and getPinData[2]==0 and getPinData[3]==0 and getPinData[4]==0 and getPinData[5]==0 and getPinData[6]==0 and getPinData[7]==1 and getPinData[8]==0 and getPinData[9]==0):
				key_num = key_scan_loop*9 + 8
			elif (getPinData[0]==0 and getPinData[1]==0 and getPinData[2]==0 and getPinData[3]==0 and getPinData[4]==0 and getPinData[5]==0 and getPinData[6]==0 and getPinData[7]==0 and getPinData[8]==1 and getPinData[9]==0):
				key_num = key_scan_loop*9 + 9
			elif (getPinData[0]==0 and getPinData[1]==0 and getPinData[2]==0 and getPinData[3]==0 and getPinData[4]==0 and getPinData[5]==0 and getPinData[6]==0 and getPinData[7]==0 and getPinData[8]==0 and getPinData[9]==1):
				key_num = key_scan_loop*9 + 10
			#print(key_num)
			return key_num
        	#key_scan_line 값을 순차적으로 1비트씩 총 3회 시프트함
		key_scan_line[0] = key_scan_line[1]
		key_scan_line[1] = key_scan_line[2]
		key_scan_line[2] = key_scan_line[3]
		key_scan_line[3] = key_scan_line[4]

		if (key_scan_loop == 4):
			key_scan_line[4] = 0
		else:
			key_scan_line[4] = 1

def hangul(num=0):
	if(num==0):
		out1 = 'None'
	elif(num>=1 and num<15):
                out1 = han1[num-1]
	elif(num>=15 and num<36):
		out1 = han2[num-15]
	elif(num>=36 and num<50):
		out1 = han1[num-36]
	elif(num==50):
		if (out1 == 'ㄱ'):
			out1 = han3[0]
		elif (out1 == 'ㄷ'):
			out1 = han3[1]
		elif (out1 == 'ㅂ'):
			out1 = han3[2]
		elif (out1 == 'ㅅ'):
			out1 = han3[3]
		elif (out1 == 'ㅈ'):
			out1 = han3[4]
		else:
			out1 = 'error'
	else:
		out1 = 'error'

	print(out1)

# 여기부터 main
while True :
	count = KeyScan()
	print(count)
	if (str(type(count)) == "<class 'int'>"):
		hangul(count)
	time.sleep(1)
