import pywhatkit
import utilities
import datetime
import time
import math

# Global variables
run_flag = True

def schedule_msg(number,msg,year,month,day,hour,minute):
    scheduled_dt = datetime.datetime(year,month,day,hour,minute)
    current_dt = datetime.datetime.now()
    seconds_to_wait = (scheduled_dt - current_dt).total_seconds() # Number of seconds to wait until sending the message
    if seconds_to_wait > 0:
        print(f"Opening WhatsApp in {math.floor(seconds_to_wait)} seconds...")
        utilities.long_sleep(seconds_to_wait)
        pywhatkit.sendwhatmsg_instantly(number,msg,wait_time=30,tab_close=True)
    else:
        print("The scheduled time has already passed!")
    
def main():
    utilities.initialize_msg_array()
    receiving_number = utilities.get_phone_number()
    if receiving_number == "Invalid":
        print("Phone number is invalid!")
        return
    
    # Ask user for first time to schedule, then for the interval
    dt_to_schedule = utilities.ask_user_for_datetime()
    dt_interval = utilities.ask_user_for_interval()
    
    while run_flag:
        msg = utilities.get_random_msg()
        print(f"\nNext message scheduled for {dt_to_schedule.year}/{dt_to_schedule.month:02}/{dt_to_schedule.day:02} at {dt_to_schedule.hour:02}:{dt_to_schedule.minute:02}")
        print(f"Sending message to {utilities.format_phone_number(receiving_number)}")
        print(f"Message to be sent: \n\n{msg}\n")
        schedule_msg(receiving_number, msg, dt_to_schedule.year, dt_to_schedule.month, dt_to_schedule.day, dt_to_schedule.hour, dt_to_schedule.minute)
        print("Sleeping for 10 seconds to prepare for next transmission...")
        print("----------------------------------------------------------------------------------------")
        time.sleep(10)
        # Add interval to dt_to_schedule
        dt_to_schedule = dt_to_schedule + datetime.timedelta(minutes=dt_interval)

if __name__ == "__main__":
    main()