#-*-coding: utf-8-*-
from gpiozero import Motor
import RPi.GPIO as GPIO
import os
import sys
import random
import time
from gtts import gTTS
from jamo import h2j, j2hcj
from unicode import join_jamos
import pymysql
import speech_recognition as sr
import cv2
import numpy as np
from PIL import Image
import socket
import threading
import math

__author__ = 'info-lab'

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings (False)

# board
#Row = [19,21,23,29,31,33,35,37]
#Col = [22, 24, 26, 32, 36, 38, 8]

# bcm
Row = [10,9,11,5,6,13,19,26]
#Col = [25,8,7,12,16,20,14]
Col = [25,8,7,12,16,20,14]

# bcm
motor_pin = [4,17,27,23]

han1 = ['ㄱ','ㄴ','ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
han2 = ['ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅒ', 'ㅔ', 'ㅖ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅢ']
han3 = ['ㄲ','ㄸ','ㅃ', 'ㅆ', 'ㅉ', ' ']
eng1=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

Q = 0

text=[]
merge_jamo = ""

login_state = "x"

count = 0
count1 = 0

sound = '' #한글 영어

jcnt = 0

menu = ""

conn=None
cur=None
sql=None

langarr =[]
steparr =[]
wordarr =[]
ansarr =[]

n = 0

user_name = []

activity = ""

conn=pymysql.connect(host='localhost', user='root', password='1234', db='mydb', charset='utf8')
cur=conn.cursor()


for i in range(8):
        GPIO.setup(Row[i], GPIO.OUT)
for i in range(7):
        GPIO.setup(Col[i], GPIO.IN)

for i in range(4):
	GPIO.setup(motor_pin[i], GPIO.OUT)

kor_motor = Motor(forward=4, backward=17)
eng_motor = Motor(forward=27, backward=23)

face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

IP = ''
PORT = 35000
SIZE = 1024
ADDR = (IP, PORT)
msg = ''
client_socket = ""

c_mode="한영"

appStudy = "x"
appsound = ""

def KeyScan():
	key_scan_line = [0,1,1,1,1,1,1,1]
	key_scan_loop = 0
	getPinData = [0,0,0,0,0,0,0]
	key_num = 0 # 실제 눌린 값

	#키 스캔 반복문
	for key_scan_loop in range(8):
        	# 키 매트릭스의 스캔 라인 설정 출력 값
        	# row
		GPIO.output(Row[0], key_scan_line[0])
		GPIO.output(Row[1], key_scan_line[1])
		GPIO.output(Row[2], key_scan_line[2])
		GPIO.output(Row[3], key_scan_line[3])
		GPIO.output(Row[4], key_scan_line[4])
		GPIO.output(Row[5], key_scan_line[5])
		GPIO.output(Row[6], key_scan_line[6])
		GPIO.output(Row[7], key_scan_line[7])
		time.sleep(0.000001)
		# 키 매트릭스의 열 값 취득
        	# col
		getPinData[0] = not GPIO.input(Col[0])
		getPinData[1] = not GPIO.input(Col[1])
		getPinData[2] = not GPIO.input(Col[2])
		getPinData[3] = not GPIO.input(Col[3])
		getPinData[4] = not GPIO.input(Col[4])
		getPinData[5] = not GPIO.input(Col[5])
		getPinData[6] = not GPIO.input(Col[6])

		if (getPinData[0]!=0 or getPinData[1]!=0 or getPinData[2]!=0 or getPinData[3]!=0 or getPinData[4]!=0 or getPinData[5]!=0 or getPinData[6]!=0):
			if (getPinData[0]==1 and getPinData[1]==0 and getPinData[2]==0 and getPinData[3]==0 and getPinData[4]==0 and getPinData[5]==0 and getPinData[6]==0):
				key_num = key_scan_loop*7 + 1
			elif (getPinData[0]==0 and getPinData[1]==1 and getPinData[2]==0 and getPinData[3]==0 and getPinData[4]==0 and getPinData[5]==0 and getPinData[6]==0):
				key_num = key_scan_loop*7 + 2
			elif (getPinData[0]==0 and getPinData[1]==0 and getPinData[2]==1 and getPinData[3]==0 and getPinData[4]==0 and getPinData[5]==0 and getPinData[6]==0):
				key_num = key_scan_loop*7 + 3
			elif (getPinData[0]==0 and getPinData[1]==0 and getPinData[2]==0 and getPinData[3]==1 and getPinData[4]==0 and getPinData[5]==0 and getPinData[6]==0):
				key_num = key_scan_loop*7 + 4
			elif (getPinData[0]==0 and getPinData[1]==0 and getPinData[2]==0 and getPinData[3]==0 and getPinData[4]==1 and getPinData[5]==0 and getPinData[6]==0):
				key_num = key_scan_loop*7 + 5
			elif (getPinData[0]==0 and getPinData[1]==0 and getPinData[2]==0 and getPinData[3]==0 and getPinData[4]==0 and getPinData[5]==1 and getPinData[6]==0):
				key_num = key_scan_loop*7 + 6
			elif (getPinData[0]==0 and getPinData[1]==0 and getPinData[2]==0 and getPinData[3]==0 and getPinData[4]==0 and getPinData[5]==0 and getPinData[6]==1):
				key_num = key_scan_loop*7 + 7
			print(key_num)
			return key_num

        	#key_scan_line 값을 순차적으로 1비트씩 총 7회 시프트함
		key_scan_line[7] = key_scan_line[6]
		key_scan_line[6] = key_scan_line[5]
		key_scan_line[5] = key_scan_line[4]
		key_scan_line[4] = key_scan_line[3]
		key_scan_line[3] = key_scan_line[2]
		key_scan_line[2] = key_scan_line[1]
		key_scan_line[1] = key_scan_line[0]

		if (key_scan_loop == 7):
			key_scan_line[0] = 0
		else:
			key_scan_line[0] = 1

def KeyScanEng():
	key_scan_line = [0,1,1,1,1,1,1,1]
	key_scan_loop = 0
	getPinData = [0,0,0,0]
	key_num = 0 # 실제 눌린 값

	#키 스캔 반복문
	for key_scan_loop in range(8):
        	# 키 매트릭스의 스캔 라인 설정 출력 값
        	# row
		GPIO.output(Row[0], key_scan_line[0])
		GPIO.output(Row[1], key_scan_line[1])
		GPIO.output(Row[2], key_scan_line[2])
		GPIO.output(Row[3], key_scan_line[3])
		GPIO.output(Row[4], key_scan_line[4])
		GPIO.output(Row[5], key_scan_line[5])
		GPIO.output(Row[6], key_scan_line[6])
		GPIO.output(Row[7], key_scan_line[7])
		time.sleep(0.000001)
		# 키 매트릭스의 열 값 취득
        	# col
		getPinData[0] = not GPIO.input(Col[0])
		getPinData[1] = not GPIO.input(Col[1])
		getPinData[2] = not GPIO.input(Col[2])
		getPinData[3] = not GPIO.input(Col[3])

		if (getPinData[0]!=0 or getPinData[1]!=0 or getPinData[2]!=0 or getPinData[3]!=0):
			key_num = key_scan_loop + getPinData[0] + getPinData[1]*9 + getPinData[2]*17 + getPinData[3]*25
			print(key_num)
			return key_num

        	#key_scan_line 값을 순차적으로 1비트씩 총 7회 시프트함
		key_scan_line[7] = key_scan_line[6]
		key_scan_line[6] = key_scan_line[5]
		key_scan_line[5] = key_scan_line[4]
		key_scan_line[4] = key_scan_line[3]
		key_scan_line[3] = key_scan_line[2]
		key_scan_line[2] = key_scan_line[1]
		key_scan_line[1] = key_scan_line[0]

		if (key_scan_loop == 7):
			key_scan_line[0] = 0
		else:
			key_scan_line[0] = 1

def percent():
	global n
	n=0
	kor1=eng1=0
	cur.execute('select ans from '+prtid+";")
	rows = cur.fetchall()
	ansarr.clear()

	for row in rows:
		ansarr.append(row[0])

	for i in ansarr:
		if(n<12 and ansarr[n]=='y'):
			kor1 = kor1+1
		elif(n>=12 and ansarr[n]=='y'):
			eng1 = eng1+1
		n=n+1
	return math.floor(kor1/12*100), math.floor(eng1/12*100)

def answer(str1):
	cur.execute("update "+prtid+" set ans = 'y' where word = '" + str1 +"';")
	conn.commit()

def gamedata():
	cur.execute('select ans, lastday, goal from '+prtid+";")
	rows = cur.fetchall()
	data = []

	for row in rows:
		data.append(row[0])
	last_day = rows[0][1]
	goal = rows[0][2] # 단위 : 10
	print('lastday = ',last_day,', goal = ',goal)

	if(data[0] != 'y' or data[1] != 'y' or data[2] != 'y' or data[3] != 'y'):
		gamescore = "단계 1,"
		gamescore += data[0]+','+data[1]+','+data[2]+','+data[3]+','
	elif(data[4] != 'y' or data[5] != 'y' or data[6] != 'y' or data[7] != 'y'):
		gamescore = "단계 2,"
		gamescore += data[4]+','+data[5]+','+data[6]+','+data[7]+','
	elif(data[8] != 'y' or data[9] != 'y' or data[10] != 'y' or data[11] != 'y'):
		gamescore = "단계 3,"
		gamescore += data[8]+','+data[9]+','+data[10]+','+data[11]+','

	if(data[12] != 'y' or data[13] != 'y' or data[14] != 'y' or data[15] != 'y'):
		gamescore += "단계 1,"
		gamescore += data[12]+','+data[13]+','+data[14]+','+data[15]
	elif(data[16] != 'y' or data[17] != 'y' or data[18] != 'y' or data[19] != 'y'):
		gamescore += "단계 2,"
		gamescore += data[16]+','+data[17]+','+data[18]+','+data[19]
	elif(data[20] != 'y' or data[21] != 'y' or data[22] != 'y' or data[23] != 'y'):
		gamescore += "단계 3,"
		gamescore += data[20]+','+data[21]+','+data[22]+','+data[23]
	elif(data[20] == 'y' and data[21] == 'y' and data[22] == 'y' and data[23] == 'y'):
		gamescore += "단계 3,"
		gamescore += data[20]+','+data[21]+','+data[22]+','+data[23]
	print('gamescore = ',gamescore)
	return last_day, goal, gamescore

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
			out1 = '_' # error
	elif(num==51 or num==52 or num==53):
		out1 = han3[5]
	elif(num == 54):
		print("mode1")
	elif(num == 55):
		print("mode2")
	elif(num == 56):
		print("mode3")
	else:
		pass
	print(out1)
	return out1

def voiceinput():
	# microphone에서 auido source를 생성합니다
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Say something!")
		audio = r.listen(source)
	str = r.recognize_google(audio, language='ko-KR')
	# 구글 웹 음성 API로 인식하기 (하루에 제한 50회)
	print("Google Speech Recognition thinks you said : " + str)
	return str

def mode1(a):
	global merge_jamo

	text.clear()

	text.append(a)
	merge_jamo=join_jamos(text)
	print(merge_jamo)
	if(count!=51 and count!=52 and text!='_'):
		tts = gTTS(merge_jamo, lang='ko', slow=False)
		tts.save('./music/ex_ko.mp3')
		os.system("mpg321 -g 100 ./music/ex_ko.mp3")
		if(appStudy=="o"):
			client_socket.sendall("현재학습확인,{},{}\r\n".format("한글,1",merge_jamo).encode())
			print("message back to client : 현재학습확인,{},{}".format("한글,1",merge_jamo))

		if ((count >= 36 and count <= 49) or ((out2 == 36 or out2 == 38 or out2 == 41 or out2 == 42 or out2 == 44) and count == 50)):
			os.system("mpg321 -g 100 ./music/bat_chim.mp3")

def mode2(a):
	global jcnt, jcnt2
	global merge_jamo

	text.append(a)
	if(count == 54):
		text.clear()
	elif (count == 52):
		del text[-1]
		del text[-1]
		if(jcnt>0):
			jcnt=jcnt-1
		elif(jcnt2>0):
			jcnt=jcnt2
			jcnt2=0
	elif (count==50):
		if(text[-2]=='ㄴ' or text[-2]=='ㄹ' or text[-2]=='ㅁ' or text[-2]=='ㅇ' or text[-2]=='ㅊ' or text[-2]=='ㅋ' or text[-2]=='ㅌ' or text[-2]=='ㅍ' or text[-2]=='ㅎ'):
			text.insert(-2,text[-2])
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
		jcnt2 = jcnt
		jcnt = 0

	merge_jamo=join_jamos(text)
	print(merge_jamo)

	if(appStudy=="o"):
		client_socket.sendall("현재학습확인,{},{}\r\n".format("한글,2",merge_jamo).encode())
		print("message back to client : 현재학습확인,{},{}".format("한글,2",merge_jamo))

	tts = gTTS(merge_jamo, lang='ko', slow=False)
	tts.save('./music/ex_ko.mp3')
	os.system("mpg321 -g 100 ./music/ex_ko.mp3")

	if(count == 53):
		text.clear()
		jcnt = 0

def mode3(a):
	global jcnt, A, jcnt2
	global merge_jamo

	text.append(a)
	if(count == 54):
		text.clear()
	elif (count == 52):
		del text[-1]
		del text[-1]
		if(jcnt>0):
			jcnt=jcnt-1
		elif(jcnt2>0):
			jcnt=jcnt2
			jcnt2=0
	elif (count==50):
		if(text[-2]=='ㄴ' or text[-2]=='ㄹ' or text[-2]=='ㅁ' or text[-2]=='ㅇ' or text[-2]=='ㅊ' or text[-2]=='ㅋ' or text[-2]=='ㅌ' or text[-2]=='ㅍ' or text[-2]=='ㅎ'):
			text.insert(-2,text[-2])
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
		jcnt2 = jcnt
		jcnt = 0

	merge_jamo=join_jamos(text)
	print(merge_jamo)

	if(appStudy=="o"):
		client_socket.sendall("현재학습확인,{},{}\r\n".format("한글,3",merge_jamo).encode())
		print("message back to client : 현재학습확인,{},{}".format("한글,3",merge_jamo))

	if(count == 53 and A!='end'):
		tts = gTTS(merge_jamo, lang='ko', slow=False)
		tts.save('./music/ex_ko.mp3')
		#os.system("omxplayer ./music/ex_ko.mp3")
		os.system("mpg321 -g 100 ./music/ex_ko.mp3")
		text.clear()
		jcnt = 0

		print('정답 비교'+A)

		if (A==merge_jamo):
			cur.execute("update "+prtid+" set ans = 'y' where word = '" + A + "';")
			conn.commit()
			#os.system("omxplayer ./music/ooo.mp3")
			os.system("mpg321 -g 100 ./music/ooo.mp3")
			#os.system("gtts-cli '정답입니다 ' -l ko --output ko_o.mp3")
		else:
			#os.system("omxplayer ./music/xxx.mp3")
			os.system("mpg321 -g 100 ./music/xxx.mp3")
			#os.system("gtts-cli '틀렸습니다. ' -l ko --output ko_x.mp3")

		kor1, eng1= percent()
		print("kor percent = ", kor1) # 0~100:1 step, 100~200:2 step, 200~300:3 step

		A = maria_set()
		if(A!='end'):
			print('문제'+A)
			#os.system("omxplayer ./music/question.mp3") # 문제
			os.system("mpg321 -g 100 ./music/question.mp3")
			tts = gTTS(A, lang='ko', slow=False)
			tts.save('./music/ex_ko.mp3')
			#os.system("omxplayer ./music/ex_ko.mp3")
			os.system("mpg321 -g 100 ./music/ex_ko.mp3")
		else:
			print('모드 3 종료')
			os.system("mpg321 -g 100 ./music/mode_sel.mp3")

def abc(num=0):
	global oute
	if(num>=1 and num<27):
        	oute = eng1[num-1]
	elif(num == 30):
		print("mode1")
	elif(num == 31):
		print("mode2")
	elif(num == 32):
		print("mode3")
	else:
		oute = ' '
	print(oute)
	return oute

def mode4(a): #알파벳 모드1
	global merge_jamo

	text=a
	merge_jamo=join_jamos(text)
	print(merge_jamo)

	if(appStudy=="o"):
		client_socket.sendall("현재학습확인,{},{}\r\n".format("영어,1",merge_jamo).encode())
		print("message back to client : 현재학습확인,{},{}".format("영어,1",merge_jamo))

	if(count1<27):
		tts = gTTS(merge_jamo, lang='en', slow=False)
		tts.save('./music/ex_en.mp3')
		#os.system("omxplayer ./music/ex_en.mp3")
		os.system("mpg321 -g 100 ./music/ex_en.mp3")

def mode5(a): #알파벳 모드2
	global merge_jamo

	text.append(a)
	if (count1 == 28):
		del text[-1]
		del text[-1]

	merge_jamo=join_jamos(text)
	print(merge_jamo)

	if(appStudy=="o"):
		client_socket.sendall("현재학습확인,{},{}\r\n".format("영어,2",merge_jamo).encode())
		print("message back to client : 현재학습확인,{},{}".format("영어,2",merge_jamo))

	tts = gTTS(merge_jamo, lang='en', slow=False)
	tts.save('./music/ex_en.mp3')
	os.system("mpg321 -g 100 ./music/ex_en.mp3")

	if(count1 == 29):
		text.clear()

def mode6(a): #알파벳 모드3
	global A
	global merge_jamo

	text.append(a)
	if (count1 == 28):
		del text[-1]
		del text[-1]

	merge_jamo=join_jamos(text)
	print(merge_jamo)

	if(appStudy=="o"):
		client_socket.sendall("현재학습확인,{},{}\r\n".format("영어,3",merge_jamo).encode())
		print("message back to client : 현재학습확인,{},{}".format("영어,3",merge_jamo))

	if(count1 == 29 and A!='end'):
		tts = gTTS(merge_jamo, lang='en', slow=False)
		tts.save('./music/ex_en.mp3')
		os.system("mpg321 -g 100 ./music/ex_en.mp3")

		text.clear()

		print('정답 비교'+A)
		if (A==merge_jamo):
			answer(merge_jamo)
			cur.execute("update "+prtid+" set ans = 'y' where word = '" + A + "';")
			conn.commit()
			#os.system("omxplayer ./music/ooo.mp3")
			os.system("mpg321 -g 100 ./music/ooo.mp3")
		else:
			#os.system("omxplayer ./music/xxx.mp3")
			os.system("mpg321 -g 100 ./music/xxx.mp3")

		kor1, eng1 = percent()
		print("eng percent = ", eng1) # 0~100:1 step, 100~200:2 step, 200~300:3 step

		A = maria_set()
		if(A!='end'):
			print('문제'+A)
			#os.system("omxplayer ./music/question.mp3") # 문제
			os.system("mpg321 -g 100 ./music/question.mp3")

			tts = gTTS(A, lang='en', slow=False)
			tts.save('./music/ex_en.mp3')
			#os.system("omxplayer ./music/ex_en.mp3")
			os.system("mpg321 -g 100 ./music/ex_en.mp3")
		else:
			print('모드 3 종료')
			os.system("mpg321 -g 100 ./music/mode_sel.mp3")

def maria_set():
	global Q, A
	Q += 1
	cur.execute('select step, word, ans from '+prtid+";")
	rows = cur.fetchall()
	ansarr.clear()

	for row in rows:
		steparr.append(row[0])
		wordarr.append(row[1])
		ansarr.append(row[2])

	if(sound == '한글'):
		print("Q=", Q)
		print('st, wo, ans = ', steparr[Q-1], wordarr[Q-1], ansarr[Q-1])

		if(Q==5 or Q==9 or Q==13):
			if(Q==5):
				if(ansarr[0]=='y' and ansarr[1]=='y' and ansarr[2]=='y' and ansarr[3]=='y'):
					return wordarr[Q-1]
				else:
					Q = 0
					return 'end'
			elif(n==9):
				if(ansarr[4]=='y' and ansarr[5]=='y' and ansarr[6]=='y' and ansarr[7]=='y'):
					return wordarr[Q-1]
				else:
					Q = 0
					return 'end'
			else:
				Q = 0
				return 'end'
		else:
			return wordarr[Q-1] # 단어 출력해줌

	if(sound == '영어'):
		print("Q=", Q)
		print('st, wo, ans = ', steparr[Q+11], wordarr[Q+11], ansarr[Q+11])

		if(Q==5 or Q==9 or Q==13):
			if(Q==5):
				if(ansarr[12]=='y' and ansarr[13]=='y' and ansarr[14]=='y' and ansarr[15]=='y'):
					return wordarr[Q+11]
				else:
					Q = 0
					return 'end'
			elif(n==9):
				if(ansarr[16]=='y' and ansarr[17]=='y' and ansarr[18]=='y' and ansarr[19]=='y'):
					return wordarr[Q+11]
				else:
					Q = 0
					return 'end'
			else:
				Q = 0
				return 'end'
		else:
			return wordarr[Q+11] # 단어 출력해줌

def han_mode():
	global count, A, text, c_mode, out2, merge_jamo, Q
	count = 0
	c_mode="한글"
	tts = gTTS("한글이 선택되었습니다.", lang='ko', slow=False)
	tts.save('./music/mode_kor.mp3')
	os.system("mpg321 -g 100 ./music/mode_kor.mp3")
	os.system("mpg321 -g 100 ./music/mode_sel.mp3")

	while True:
		if(count==54): # mode1
			print(time.strftime('%Y-%m-%d', time.localtime(time.time())))
			cur.execute("update "+prtid+" set lastday = "+str(time.strftime('%Y%m%d', time.localtime(time.time())))+" where id=1;")
			conn.commit()
			c_mode="한글,1"
			#os.system("omxplayer ./music/mode_1.mp3") # 모드 일번 입니다. 자음, 모음을 입력해주세요.
			os.system("mpg321 -g 100 ./music/mode_1.mp3")
			while True:
				out2 = count
				count = KeyScan() #count = int(input())
				time.sleep(0.5)
				if(count == 54 or count == 55 or count == 56):
					merge_jamo = ""
					text.clear()
					break
				elif((count == 53 and (not join_jamos(text).strip()))):
					#os.system("omxplayer ./music/mode_sel.mp3")
					os.system("mpg321 -g 100 ./music/mode_sel.mp3")
					text.clear()
					break
				elif(appsound=="영어"):
					break
				elif(str(type(count)) == "<class 'int'>"):
					mode1(hangul(count))
				else:
					pass
		elif(count==55): # mode2
			print(time.strftime('%Y-%m-%d', time.localtime(time.time())))
			cur.execute("update "+prtid+" set lastday = "+str(time.strftime('%Y%m%d', time.localtime(time.time())))+" where id=1;")
			conn.commit()
			c_mode="한글,2"
			#os.system("omxplayer ./music/mode_2.mp3") # 모드 이번 입니다. 단어 또는 문장을 입력해주세요.
			os.system("mpg321 -g 100 ./music/mode_2.mp3")
			while True:
				count = KeyScan() #count = int(input())
				time.sleep(0.5)
				if(count == 54 or count == 55 or count == 56):
					merge_jamo = ""
					text.clear()
					break
				elif((count == 53 and (not join_jamos(text).strip()))):
					#os.system("omxplayer ./music/mode_sel.mp3")
					os.system("mpg321 -g 100 ./music/mode_sel.mp3")
					break
				elif(appsound=="영어"):
					break
				elif (str(type(count)) == "<class 'int'>"):
					mode2(hangul(count))
				else:
					pass
		elif(count==56): # mode3
			print(time.strftime('%Y-%m-%d', time.localtime(time.time())))
			cur.execute("update "+prtid+" set lastday = "+str(time.strftime('%Y%m%d', time.localtime(time.time())))+" where id=1;")
			conn.commit()
			c_mode="한글,3"
			#os.system("omxplayer ./music/mode_3.mp3") # 모드 삼번 입니다. 문제
			os.system("mpg321 -g 100 ./music/mode_3.mp3")

			cur.execute("update "+prtid+" set ans='n' where lang='한글';")
			conn.commit()

			Q = 0
			A = maria_set()

			print('_'+A+'_')

			tts = gTTS(A, lang='ko', slow=False)
			tts.save('./music/ex_ko.mp3')
			#os.system("omxplayer ./music/ex_ko.mp3")
			os.system("mpg321 -g 100 ./music/ex_ko.mp3")

			while True:
				count = KeyScan() #count = int(input())
				time.sleep(0.5)
				if(count==54 or count==55 or count==56):
					Q = 0
					merge_jamo = ""
					text.clear()
					break
				elif(count == 53 and (not join_jamos(text).strip())):
					Q = 0
					os.system("mpg321 -g 100 ./music/mode_sel.mp3")
					break
				elif(appsound=="영어"):
					break
				elif (str(type(count)) == "<class 'int'>"):
					mode3(hangul(count))
				else:
					pass
		elif(appsound=="영어"):
			Q = 0
			text.clear()
			merge_jamo = ""
			break
		else:
			count = KeyScan() #count = int(input())
			print(count)
			merge_jamo = ""
			if(count == 53):
				break
			time.sleep(0.5)

def eng_mode():
	global count1, A, text, c_mode, merge_jamo, Q
	c_mode="영어"
	count1 = 0
	tts = gTTS("영어가 선택되었습니다.", lang='ko', slow=False)
	tts.save('./music/mode_eng.mp3')
	os.system("mpg321 -g 100 ./music/mode_eng.mp3")
	os.system("mpg321 -g 100 ./music/mode_sel.mp3")

	while True:
		if (count1 == 30):
			print(time.strftime('%Y-%m-%d', time.localtime(time.time())))
			cur.execute("update "+prtid+" set lastday = "+str(time.strftime('%Y%m%d', time.localtime(time.time())))+" where id=1;")
			conn.commit()
			c_mode="영어,1"
			#os.system("omxplayer ./music/mode_4.mp3") # 모드 일번 입니다. 알파벳을 입력해주세요.
			os.system("mpg321 -g 100 ./music/mode_4.mp3")
			while True:
				out2 = count1
				count1 = KeyScanEng() # count1 = int(input())
				time.sleep(0.5)
				if (count1 == 30 or count1 == 31 or count1 == 32):
					merge_jamo = ""
					break
				elif((count1 == 29 and (not join_jamos(text).strip()))):
					#os.system("omxplayer ./music/mode_sel.mp3")
					os.system("mpg321 -g 100 ./music/mode_sel.mp3")
					break
				elif(appsound=="한글"):
					break
				elif (str(type(count1)) == "<class 'int'>"):
					mode4(abc(count1))
				else:
					pass
		elif (count1 == 31):
			print(time.strftime('%Y-%m-%d', time.localtime(time.time())))
			cur.execute("update "+prtid+" set lastday = "+str(time.strftime('%Y%m%d', time.localtime(time.time())))+" where id=1;")
			conn.commit()
			c_mode="영어,2"
			#os.system("omxplayer ./music/mode_5.mp3") # 모드 이번 입니다. 단어 또는 문장을 입력해주세요.
			os.system("mpg321 -g 100 ./music/mode_5.mp3")
			while True:
				count1 = KeyScanEng() # count = int(input())
				time.sleep(0.5)
				if (count1 == 30 or count1 == 31 or count1 == 32):
					merge_jamo = ""
					text.clear()
					break
				elif((count1 == 29 and (not join_jamos(text).strip()))):
					#os.system("omxplayer ./music/mode_sel.mp3")
					os.system("mpg321 -g 100 ./music/mode_sel.mp3")
					break
				elif(appsound=="한글"):
					break
				elif (str(type(count1)) == "<class 'int'>"):
					mode5(abc(count1))
				else:
					pass
		elif (count1 == 32): # mode3
			print(time.strftime('%Y-%m-%d', time.localtime(time.time())))
			cur.execute("update "+prtid+" set lastday = "+str(time.strftime('%Y%m%d', time.localtime(time.time())))+" where id=1;")
			conn.commit()
			c_mode="영어,3"
			#os.system("omxplayer ./music/mode_6.mp3") # 모드 삼번 입니다. 문제
			os.system("mpg321 -g 100 ./music/mode_6.mp3")

			cur.execute("update "+prtid+" set ans='n' where lang='영어';")
			conn.commit()

			Q = 0
			A = maria_set()
			print('_'+A+'_')

			tts = gTTS(A, lang='en', slow=False)
			tts.save('./music/ex_en.mp3')
			#os.system("omxplayer ./music/ex_en.mp3")
			os.system("mpg321 -g 100 ./music/ex_en.mp3")

			while True:
				count1 = KeyScanEng() # count1 = int(input())
				time.sleep(0.5)
				if (count1 == 30 or count1 == 31 or count1 == 32):
					Q = 0
					merge_jamo = ""
					text.clear()
					break
				elif((count1 == 29 and (not join_jamos(text).strip()))):
					Q = 0
					os.system("mpg321 -g 100 ./music/mode_sel.mp3")
					break
				elif(appsound=="한글"):
					break
				elif (str(type(count1)) == "<class 'int'>"):
					mode6(abc(count1))
				else:
					pass
		elif(appsound=="한글"):
			Q = 0
			text.clear()
			merge_jamo = ""
			break
		else:
			count1 = KeyScanEng() # count1 = int(input())
			print(count1)
			merge_jamo = ""
			if(count1 == 29):
				break
			time.sleep(0.5)

def face_dataset():
	cam = cv2.VideoCapture(-1)
	cam.set(3, 640) # set video width
	cam.set(4, 480) # set video height

	face_id = 1
	while (os.path.exists("dataset/User." + str(face_id) + '.' + str(1) + ".jpg")):
		print(face_id)
		face_id += 1
	print(face_id)
	print("\n [INFO] Initializing face capture. Look the camera and wait ...")

	# Initialize individual sampling face count
	count = 0
	while(True):
		ret, img = cam.read()
		#img = cv2.flip(img, -1) # flip video image vertically
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = face_detector.detectMultiScale(gray, 1.3, 5)
		for (x,y,w,h) in faces:
			cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
			count += 1
			# Save the captured image into the datasets folder
			cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
			cv2.imshow('image', img)
		k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
		if k == 27:
			break
		elif count >= 60: # Take 60 face sample and stop video
			break

	# Do a bit of cleanup
	print("\n [INFO] Exiting Program and cleanup stuff")
	cam.release()
	cv2.destroyAllWindows()

# function to get the images and label data
def getImagesAndLabels(path):
	imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
	faceSamples=[]
	ids = []
	for imagePath in imagePaths:
		PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
		img_numpy = np.array(PIL_img,'uint8')
		id = int(os.path.split(imagePath)[-1].split(".")[1])
		faces = face_detector.detectMultiScale(img_numpy)
		for (x,y,w,h) in faces:
			faceSamples.append(img_numpy[y:y+h,x:x+w])
			ids.append(id)
	return faceSamples,ids


def face_training():
	# Path for face image database
	path = 'dataset'
	recognizer = cv2.face.LBPHFaceRecognizer_create()

	print("\n [INFO] Training faces. It will take a few seconds. Wait ...")
	faces,ids = getImagesAndLabels(path)
	recognizer.train(faces, np.array(ids))

	# Save the model into trainer/trainer.yml
	recognizer.write('trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi
	# Print the numer of faces trained and end program
	print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))


def face_recognition():
	global percent
	recognizer = cv2.face.LBPHFaceRecognizer_create()
	recognizer.read('trainer/trainer.yml')
	cascadePath = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
	faceCascade = cv2.CascadeClassifier(cascadePath);
	font = cv2.FONT_HERSHEY_SIMPLEX

	#iniciate id counter
	id = 0

	# names related to ids: example ==> loze: id=1,  etc
	# 이런식으로 사용자의 이름을 사용자 수만큼 추가해준다.
	#names = ['None', 'kim', 'lee', 'jang']
	face_id = 1
	names = ['None']
	while (os.path.exists("dataset/User." + str(face_id) + '.' + str(1) + ".jpg")):
		print(face_id)
		names.append("User" + str(face_id))
		face_id += 1
	print(names)

	# Initialize and start realtime video capture
	cam = cv2.VideoCapture(-1)
	if(cam.isOpened() == False):
		print("캠 안열림!")
	else:
		print("캠 열림!")

	cam.set(3, 640) # set video widht
	cam.set(4, 480) # set video height

	# Define min window size to be recognized as a face
	minW = 0.1*cam.get(3)
	minH = 0.1*cam.get(4)
	percent = []

	for count_p in range(10):
		ret, im = cam.read()
		print("im = ", im)
		gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

		faces = faceCascade.detectMultiScale(
			gray,
			scaleFactor = 1.2,
			minNeighbors = 5,
			minSize = (int(minW), int(minH)),
			)

		for(x,y,w,h) in faces:
			cv2.rectangle(im, (x,y), (x+w,y+h), (0,255,0), 2)
			id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
			# Check if confidence is less them 100 ==> "0" is perfect match
			if (confidence < 100):
				id = names[id]
				percent.append(round(100 - confidence))
				confidence = "  {0}%".format(round(100 - confidence))
				print("confidence = " + str(confidence))
			else:
				id = "unknown"
				confidence = "  {0}%".format(round(100 - confidence))
				print("confidence = " + str(confidence))

			print("촬영 횟수 = "+str(count_p+1))

			cv2.putText(im, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
			cv2.putText(im, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
		cv2.imshow('camera',im)

		k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
		if k == 27:
			break

	percent_arr = np.array(percent)
	Mean = round(np.mean(percent_arr))
	print("mean = " + str(Mean))
	if(Mean > 40):
		pass
	else:
		id = "unknown"

	# Do a bit of cleanup
	print("\n [INFO] Exiting Program and cleanup stuff")
	cam.release()
	cv2.destroyAllWindows()
	print("user id = " + id)

	return id

def menu_one():
	os.system("mpg321 -g 100 ./music/signup.mp3") #회원가입을 시작합니다.
	os.system("mpg321 -g 100 ./music/step1.mp3") # 보드 앞에 정면을 보고 앉아주세요.
	os.system("mpg321 -g 100 ./music/step2.mp3") #얼굴을 등록하는 중입니다.
	face_dataset()
	os.system("mpg321 -g 100 ./music/step3.mp3") #얼굴 등록이 완료되었습니다.

def menu_two():
	global prtid
	os.system("mpg321 -g 100 ./music/face_recog.mp3") # 얼굴 인식을 시작합니다.
	print("얼굴 인식 시작")
	prtid = face_recognition()

def server():
	global msg, prtid, count, appsound, count1, c_mode, menu, login_state, activity
	global appStudy, merge_jamo
	global client_socket

	print("server start")

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.bind(ADDR)  # 주소 바인딩
		server_socket.listen()  # 클라이언트의 요청을 받을 준비
		client_socket, client_addr = server_socket.accept()  # 수신대기, 접속한 클라이언트 정보 (소켓, 주소) 반환
		print("connected")
		activity = "로그인"

	print("thread start")

	while (True):
		msg = client_socket.recv(1024).decode()
		if (msg!=""):
			print("[{}] massage : {}".format(client_addr, msg))
			if(msg=="회원가입"):
				activity = "회원가입"
				menu = "일"
			if(msg=="로그인"):
				activity = "로그인"
				menu = "이"
			if(msg=="메뉴"):
				activity = "메뉴"
				appStudy = "x"
			if(msg=="한글"):
				activity = "한글"
				appsound="한글"
			if(msg=="영어"):
				activity = "영어"
				appsound="영어"
			if(msg=="한글,1"):
				activity = "한글"
				appsound="한글"
				count=54
			if(msg=="한글,2"):
				activity = "한글"
				appsound="한글"
				count=55
			if(msg=="한글,3"):
				activity = "한글"
				appsound="한글"
				count=56
			if(msg=="영어,1"):
				activity = "영어"
				appsound="영어"
				count1=30
			if(msg=="영어,2"):
				activity = "영어"
				appsound="영어"
				count1=31
			if(msg=="영어,3"):
				activity = "영어"
				appsound="영어"
				count1=32
			if(msg=="현재학습확인"):
				activity = "현재학습확인"
				appStudy = "o"
				if(merge_jamo):
					print("study = ",merge_jamo)
					client_socket.sendall("현재학습확인,{},{}\r\n".format(c_mode,merge_jamo).encode())
					print("message back to client : 현재학습확인,{},{}".format(c_mode,merge_jamo))
				else:
					print("!study = ",c_mode)
					client_socket.sendall("현재학습확인,{}\r\n".format(c_mode).encode())
					print("message back to client : 현재학습확인,{}".format(c_mode))
			if(msg[:2]=="정보"):
				activity = "정보"
				msg1, msg2 = percent()
				client_socket.sendall("정보,{},{}\r\n".format(msg1,msg2).encode())
				print("message back to client : 정보,{},{}".format(msg1,msg2))
			if(msg[:2]=="진도"):
				activity = "진도"
				last_day, goal, gamescore = gamedata()
				if(msg=="진도"):
					client_socket.sendall("진도,{},{},{}\r\n".format(last_day,goal,gamescore).encode())
					print("message back to client : 진도,{},{},{}".format(last_day,goal,gamescore))
				else:
					goal = msg[3:]
					cur.execute("update "+prtid+" set goal = "+goal+" where id=1;")
					conn.commit()
					print("goal : {}".format(goal))
	client_socket.close()  # 클라이언트 소켓 종료

t=threading.Thread(target=server)
t.start()

# main
while True:
	try:
		if(login_state == "x"):
			if(menu == "일"):
				if(msg == "얼굴등록" or msg == "얼굴등록 board"):
					menu_one()
					while(msg=="얼굴등록"):
						pass
					if(msg=="회원가입,success" or msg == "얼굴등록 board"):
						#tts = gTTS("회원가입이 완료되었습니다.", lang='ko', slow=False)
						#tts.save('./music/signup_success.mp3')
						os.system("mpg321 -g 100 ./music/signup_success.mp3")

						# database 생성
						face_id = 1
						while (os.path.exists("dataset/User." + str(face_id) + '.' + str(1) + ".jpg")):
							print(face_id)
							face_id += 1

						cur.execute("create table User" + str(face_id-1) + " (select * from user01);")
						conn.commit()

						# 새 훈련 데이터 생성
						face_training()

					elif(msg=="회원가입,cancel"):
						#tts = gTTS("회원가입이 취소되었습니다.", lang='ko', slow=False)
						#tts.save('./music/signup_fail.mp3')
						os.system("mpg321 -g 100 ./music/signup_fail.mp3")

						# 사진 삭제
						face_id = 1
						while (os.path.exists("dataset/User." + str(face_id) + '.' + str(1) + ".jpg")):
							print(face_id)
							face_id += 1
						os.system("rm dataset/User."+ str(face_id-1) + '.*')
					msg = ""
					menu = ""
				else:
					pass
			elif(menu == "이"):
				menu_two()
				print("prtid = " + prtid)

				if(prtid != "unknown"):
					os.system("mpg321 -g 100 ./music/login_success.mp3") # 로그인 성공했습니다.
					login_state = "o"
					print("activity = "+ activity)
					if(activity == "로그인"):
						client_socket.sendall("로그인,success\r\n".encode())
					print("face login [{}] success".format(prtid))
				else:
					os.system("mpg321 -g 100 ./music/login_fail.mp3") # 로그인 실패했습니다.
					login_state = "x"
					if(activity == "로그인"):
						client_socket.sendall("로그인,fail\r\n".encode())
						client_socket.sendall("로그인,facelog_fail\r\n".encode())
					print("face login fail")
				menu = ""
			else:
				tts = gTTS("회원가입을 하시려면 일 , 로그인을 하시려면 이 를 말해주세요.", lang='ko', slow=False)
				tts.save('./music/menu_sel.mp3')
				os.system("mpg321 -g 100 ./music/menu_sel.mp3") # 회원가입을 하시려면 일 , 로그인을 하시려면 이 를 말해주세요.
				if(menu != "일" and menu != "이"):
					menu = voiceinput()
					if(menu=="일"):
						msg = "얼굴등록 board"

		elif(login_state == "o"):
			if(sound == '한글'):
				print("한글 모터 앞, 영어 모터 뒤")
				kor_motor.forward()
				eng_motor.backward()

				han_mode()
				sound = ""
			elif(sound == '영어'): #카운트 바꾸기
				print("한글 모터 뒤, 영어 모터 앞")
				kor_motor.backward()
				eng_motor.forward()

				eng_mode()
				sound = ""
			else:
				# 언어 선택
				#os.system("mpg321 -g 100 ./music/lan.mp3") # 언어를 선택하세요. 한글, 영어
				print('언어 선택')
				#appsound = "영어"
				if(appsound=="한글"):
					sound = "한글"
					c_mode = "한글"
				elif(appsound=="영어"):
					sound = "영어"
					c_mode = "영어"
				elif(appsound!="한글" and appsound!="영어"):
					os.system("mpg321 -g 100 ./music/lan.mp3") # 언어를 선택하세요. 한글, 영어
					sound = voiceinput()
					print(sound)
					c_mode = ""
					count = None
					count1 = None

	except KeyboardInterrupt:
		# Ctrl + C
		GPIO.cleanup()
		sys.exit()
	except sr.UnknownValueError:
		print("Google Speech Recognition could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))
	#except:
	#	print("문제가 많다")
	#	pass
