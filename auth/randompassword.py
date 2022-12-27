import random
import string
import uuid

f_char=random.choice(string.ascii_letters)
s_char=random.choice(string.ascii_letters)
t_char=random.choice(string.ascii_letters)
g_char=random.choice(string.ascii_letters)
name=(f_char+s_char+t_char+g_char).upper()

number1=random.randint(1,9)
number2=random.randint(1,9)
number3=random.randint(1,9)

number=(str(number1)+str(number2)+str(number3))
all_random=(name+number)


#Random Key
random_key=str(uuid.uuid4())+str(uuid.uuid1())+all_random