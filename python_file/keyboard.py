#-*-coding: utf-8-*-
import RPi.GPIO as GPIO
import os
import sys
import random
from gtts import gTTS
from jamo import h2j, j2hcj
from unicode import join_jamos

__author__ = 'info-lab'

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings (False)

Row = [29, 31, 33, 35, 37]
Col = [12, 16, 18, 22, 24, 26, 32, 36, 38, 40]
sp = 3
bsp = 5
ok = 7
bnt = [11, 13, 15]

han1 = ['ㄱ','ㄴ','ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
han2 = ['ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅒ', 'ㅔ', 'ㅖ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅢ']
han3 = ['ㄲ','ㄸ','ㅃ', 'ㅆ', 'ㅉ', ' ']

Q = '사과 ', '하늘 ', '비행기 ', '우리나라 ', '안녕하세요 ', '만나서 반가워 '

text=[]

count = 0

jcnt = 0

for i in range(5):
        GPIO.setup(Row[i], GPIO.OUT)
for i in range(10):
        GPIO.setup(Col[i], GPIO.IN)

GPIO.setup(sp, GPIO.IN)
GPIO.setup(bsp, GPIO.IN)
GPIO.setup(ok, GPIO.IN)
GPIO.setup(bnt[0], GPIO.IN)
GPIO.setup(bnt[1], GPIO.IN)
GPIO.setup(bnt[2], GPIO.IN)

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
	global out1
	if(num>=1 and num<15):
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
	elif(num == 51 or num==52 or num==53):
		out1 = han3[5]
	elif(num == 54):
		print("mode1")
	elif(num == 55):
		print("mode2")
	elif(num == 56):
		print("mode3")
	else:
		out1 = 'error'

	print(out1)
	return out1

def mode1(a):
	if(count!=55 or count!=56):
		text=a
		merge_jamo=join_jamos(text)
		print(merge_jamo)

		tts = gTTS(merge_jamo, lang='ko', slow=False)
		tts.save('ex_ko.mp3')
		os.system("omxplayer ex_ko.mp3")
		if ((count >= 36 and count <= 49) or (out2 >= 36 and out2 <= 49 and count == 50)):
			tts = gTTS("받 침", lang='ko', slow=False)
			tts.save('ex_ko.mp3')
			os.system("omxplayer ex_ko.mp3")

def mode2(a):
	global jcnt
	text.append(a)
	if(count == 54):
		text.clear()
	elif (count == 52):
		del text[-1]
		del text[-1]
		if(jcnt>0):
			jcnt=jcnt-1
	elif (count==50):
		del text[-2]

	if ((count>= 1 and count<=14) or (count>=36 and count<=49)):
		jcnt=jcnt+1
	elif (count>=15 and count<=35):
		if (jcnt==3):
			if(text[-3]=='ㅅ' and text[-4]=='ㄱ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄳ')
			elif(text[-3]=='ㅈ' and text[-4]=='ㄴ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄵ')
			elif(text[-3]=='ㅎ' and text[-4]=='ㄴ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄶ')
			elif(text[-3]=='ㄱ' and text[-4]=='ㄹ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄺ')
			elif(text[-3]=='ㅁ' and text[-4]=='ㄹ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄻ')
			elif(text[-3]=='ㅂ' and text[-4]=='ㄹ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄼ')
			elif(text[-3]=='ㅅ' and text[-4]=='ㄹ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄽ')
			elif(text[-3]=='ㅌ' and text[-4]=='ㄹ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄾ')
			elif(text[-3]=='ㅍ' and text[-4]=='ㄹ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄿ')
			elif(text[-3]=='ㅎ' and text[-4]=='ㄹ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㅀ')
			elif(text[-3]=='ㅅ' and text[-4]=='ㅂ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㅄ')
		jcnt = 0

	merge_jamo=join_jamos(text)
	print(merge_jamo)
	if(count == 53):
		tts = gTTS(merge_jamo, lang='ko', slow=False)
		tts.save('ex_ko.mp3')
		os.system("omxplayer ex_ko.mp3")
		text.clear()
		jcnt = 0

def mode3(a):
	global jcnt, A

	text.append(a)
	if(count == 54):
		text.clear()
	elif (count == 52):
		del text[-1]
		del text[-1]
		if(jcnt>0):
			jcnt=jcnt-1
	elif (count==50):
		del text[-2]

	if ((count>= 1 and count<=14) or (count>=36 and count<=49)):
		jcnt=jcnt+1
	elif (count>=15 and count<=35):
		if (jcnt==3):
			if(text[-3]=='ㅅ' and text[-4]=='ㄱ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄳ')
			elif(text[-3]=='ㅈ' and text[-4]=='ㄴ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄵ')
			elif(text[-3]=='ㅎ' and text[-4]=='ㄴ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄶ')
			elif(text[-3]=='ㄱ' and text[-4]=='ㄹ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄺ')
			elif(text[-3]=='ㅁ' and text[-4]=='ㄹ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄻ')
			elif(text[-3]=='ㅂ' and text[-4]=='ㄹ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄼ')
			elif(text[-3]=='ㅅ' and text[-4]=='ㄹ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄽ')
			elif(text[-3]=='ㅌ' and text[-4]=='ㄹ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄾ')
			elif(text[-3]=='ㅍ' and text[-4]=='ㄹ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄿ')
			elif(text[-3]=='ㅎ' and text[-4]=='ㄹ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㅀ')
			elif(text[-3]=='ㅅ' and text[-4]=='ㅂ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㅄ')
		jcnt = 0

	merge_jamo=join_jamos(text)
	print(merge_jamo)
	if(count == 53):
		tts = gTTS(merge_jamo, lang='ko', slow=False)
		tts.save('ex_ko.mp3')
		os.system("omxplayer ex_ko.mp3")
		text.clear()
		jcnt = 0

		print('정답 비교'+A)

		if (A==merge_jamo):
			os.system("omxplayer o.mp3")
			#os.system("gtts-cli '정답입니다 ' -l ko --output ko_o.mp3")
			os.system("omxplayer ko_o.mp3")
		else:
			os.system("omxplayer x.mp3")
			#os.system("gtts-cli '오답입니다 ' -l ko --output ko_x.mp3")
			os.system("omxplayer ko_x.mp3")
		A = random.choice(Q)

		print('문제'+A)
		tts = gTTS('문제', lang='ko', slow=False)
		tts.save('ex_ko.mp3')
		os.system("omxplayer ex_ko.mp3")

		tts = gTTS(A, lang='ko', slow=False)
		tts.save('ex_ko.mp3')
		os.system("omxplayer ex_ko.mp3")


# main
while True :
	try:
		if(count==54):
			tts = gTTS("모드 일번 입니다.", lang='ko', slow=False)
			tts.save('ex_ko.mp3')
			os.system("omxplayer ex_ko.mp3")
			while True:
				out2 = count
				count=int(input())
				if(count == 55 or count == 56):
					break
				elif (str(type(count)) == "<class 'int'>"):
					mode1(hangul(count))

				else:
					print("error")
		elif(count==55):
			tts = gTTS("모드 이번 입니다.", lang='ko', slow=False)
			tts.save('ex_ko.mp3')
			os.system("omxplayer ex_ko.mp3")
			while True:
				count=int(input())
				if(count == 54 or count == 56):
					break
				elif (str(type(count)) == "<class 'int'>"):
					mode2(hangul(count))

				else:
					print("error")
		elif(count==56): # mode3
			tts = gTTS("모드 삼번 입니다. 문제", lang='ko', slow=False)
			tts.save('ex_ko.mp3')
			os.system("omxplayer ex_ko.mp3")

			A = random.choice(Q)

			print('_'+A+'_')

			tts = gTTS(A, lang='ko', slow=False)
			tts.save('ex_ko.mp3')
			os.system("omxplayer ex_ko.mp3")

			while True:
				count=int(input())
				if(count==54 or count==55):
					break
				elif (str(type(count)) == "<class 'int'>"):
					mode3(hangul(count))
				else:
					print("error")
		else:
			#count = KeyScan()
			#print(count)
			count = int(input())

	except KeyboardInterrupt:
		# Ctrl + C
		sys.exit()
	except:
		print('error')
		tts = gTTS("아무것도 입력되지 않았습니다.  모드를 다시 선택해주세요", lang='ko', slow=False)
		tts.save('ex_ko.mp3')
		os.system("omxplayer ex_ko.mp3")

		pass
