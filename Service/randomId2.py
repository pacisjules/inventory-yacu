import random
import string
import datetime


myDateDay = datetime.datetime.now().weekday()
myHour = datetime.datetime.now().hour
myMin = datetime.datetime.now().min
mySec = datetime.datetime.now().second
dateRandom = random.choice(str(myDateDay))

f_char = random.choice(string.ascii_letters)
s_char = random.choice(string.ascii_letters)
t_char = random.choice(string.ascii_letters)
g_char = random.choice(string.ascii_letters)
after_char = random.choice(string.ascii_letters).upper()
name = (f_char+s_char+t_char+g_char).upper()

number1 = random.randint(1, 9)
snumber2 = random.randint(1, 9)
snumber3 = random.randint(1, myHour+1)


number = (str(number1)+str(snumber2)+str(snumber3))
numbe2 = (str(snumber3)+str(number1)+str(snumber2))
number3 = (str(snumber3)+str(snumber2)+str(number1))
number4 = (str(number3)+str(snumber2)+str(number1))
number5 = (str(number1)+str(snumber2)+str(number3))

if(len(number) == 4):
    number = number
elif(len(number) < 4):
    number = number+str(number1)
elif(len(number) > 4):
    number = number[:4]

id_all_random2 = (name+"-"+numbe2+"-"+after_char)

print(id_all_random2)
