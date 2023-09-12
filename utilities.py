import random
import datetime
import json
import math
import time
import phonenumbers

# Will send messages to test phone number when set to True
# Change to "False" to send messages to the real phone number
test_flag = True

# Don't touch anything down from here :)
msg_array = []

def is_test():
    return test_flag

def get_messages():
    with open("data.json","r",encoding="utf-8") as data_file:
        data = json.load(data_file)
        return data["messages"]
    
def initialize_msg_array():
    for message in get_messages():
        msg_array.append(message)

def get_random_msg():
    # Shuffle the list so it sends in a random order.
    random.shuffle(msg_array)

    # Grab the message from the end of the array.
    try:
        msg = msg_array[len(msg_array)-1]
    # Exception happens if the list is empty.
    except: 
        msg = "Sorry I'm out of custom messages! Tell Jordan to make a longer list next time!"
    
    # Custom addition to the first message that sends.
    if len(msg_array) == 12:
        msg += '\n\nYeah, I finally got around to finishing this bot lol. I hope you enjoy the silly messages you\'ll be getting throughout today! Happy Birthday! - Jordan'

    # Pop it from the msg_array to prevent repeat sends.
    try:
        msg_array.pop()
    except:
        print("No msg to pop!")

    return msg + '\n\t\t\t\t\t- Jordan\'s Bot'
    
def sanitize_list(list):
    l = list
    # Iterates through list for these reasons:
    # 1. Gets rid of the extra \n characters in each string.
    # 2. TODO: Removes comments from the list so they cannot be chosen or displayed.
    # 3. Removes empty items like ''.
    for i in range(0,len(l)): # 1
        l[i] = remove_slash_n(l[i])
    pop_empty_list_items(l) # 3
    return l

def remove_slash_n(txt):
    txt = txt
    if txt.endswith('\n'):
        txt = txt[:-1]
    if txt.startswith('\n'):
        txt = txt[1:]
    return txt

def pop_empty_list_items(list):
    l = list
    popped = True # If an item was popped last time, try again until there are no more items to pop.
    while (popped):
        popped = False # Reset 'popped' flag. If no item is popped in the for loop below, then the while loop will stop.
        for i in range(0,len(l)):
            if l[i] == '':
                l.pop(i)
                popped = True
                break
            
def calculate_next_time():
    currenttime = datetime.datetime.now()
    minute = 47 # Always schedule the minute to be 47.
    even_hour = currenttime.hour % 2 == 0 # True if the current hour is an even number.
    before_minute = currenttime.minute < minute # True if the current minute is before the specified minute.
    # Makes sure the scheduled hour is always the next even hour.
    if not even_hour:
        hour = currenttime.hour + 1
    elif before_minute:
        
        hour = currenttime.hour
    elif (not before_minute):
        hour = currenttime.hour + 2

    # Fix formatting errors. (i.e. hour cannot be 24 and minute cannot be 60)  
    if (minute == 60):
        minute = 0
        hour = hour + 1
    if (hour == 24):
        hour = 0
    if (hour == 25):
        hour = 1  
    return [hour, minute]

def calculate_next_test_time():
    currenttime = datetime.datetime.now()
    minute = currenttime.minute + 2
    hour = currenttime.hour

    # Fix formatting errors. (i.e. hour cannot be 24 and minute cannot be 60)  
    if (minute >= 60):
        minute = minute - 60
        hour = hour + 1
    if (hour >= 24):
        hour = hour - 24 
    return [hour, minute]

def validate_phone_number(phone_number):
    try:
        parsed_phone_number = phonenumbers.parse(phone_number)
    except phonenumbers.NumberParseException:
        return False
    else:
        return (phonenumbers.is_possible_number(parsed_phone_number) and phonenumbers.is_valid_number(parsed_phone_number))

def format_phone_number(phone_number):
    if validate_phone_number(phone_number):
        return phonenumbers.format_number(phonenumbers.parse(phone_number), phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    else:
        return phone_number

def get_test_phone_number():
    with open("data.json","r",encoding="utf-8") as data_file:
        data = json.load(data_file)
        phone_number = data["phone_numbers"]["test_number"]
        if validate_phone_number(phone_number):
            return phone_number
        else:
            return "Invalid"
    
def get_real_phone_number():
    with open("data.json","r",encoding="utf-8") as data_file:
        data = json.load(data_file)
        phone_number = data["phone_numbers"]["real_number"]
        if validate_phone_number(phone_number):
            return phone_number
        else:
            return "Invalid"
    
def get_phone_number():
    if (is_test()):
        return get_test_phone_number()
    else:
        return get_real_phone_number()
    
def ask_user_for_datetime():
    # Ask user for first time to schedule, then for the interval    
    datetime_str = input("Enter a date and time (YYYY/MM/DD HH:MM):\n").strip()
    dt_format = "%Y/%m/%d %H:%M"
    try:  
        datetime_obj = datetime.datetime.strptime(datetime_str, dt_format)
        formatted_datetime_str = datetime.datetime.strftime(datetime_obj, dt_format)
    except ValueError:
        print(f"{datetime_str} is invalid! Please try again.")
        ask_user_for_datetime()
    else:
        #print(f"{formatted_datetime_str} is valid!")
        return datetime_obj
    
def ask_user_for_interval():
    # Ask user for interval to send messages in
    interval = input("\nHow often should messages be sent? (in minutes)\n").strip()
    try:
        x = int(interval)
        if x < 1:
            raise ValueError
    except (TypeError, ValueError):
        print("Invalid input! Please enter a positive whole number.")
        return ask_user_for_interval()
    else:
        return x
    
def long_sleep(n):
    seconds_in_month = 2592000
    months_to_sleep = math.floor(n / seconds_in_month)
    remainder = n % seconds_in_month
    # time.sleep() has a max sleep time
    # I artificially extend that by sleeping 1 month at a time, and then sleeping the remaining seconds
    for i in range(months_to_sleep):
        time.sleep(seconds_in_month)
    
    time.sleep(remainder)