# Install requirements

>pip install -r requirements.txt

# How to use

1. Put a phone number in data.json. It must be a real phone number and include the country code (e.g. +1**********).
2. Go into utilities.py and change the value of test_flag to "False" in order to send messages to the real phone number. Leave it as true if you want to do some testing on a personal phone number beforehand.
3. Add messages that the app can randomly select from.

# How to add messages:

Add messages to the "messages" list in data.json.

>"messages":[<br>
>&nbsp;&nbsp;&nbsp;&nbsp;"message1",<br>
>&nbsp;&nbsp;&nbsp;&nbsp;"message2",<br>
>&nbsp;&nbsp;&nbsp;&nbsp;"message3"<br>
>]

(The messages are read using UTF-8 encoding, so make sure the characters in the messages list use UTF-8 encoding too, otherwise they won't be read properly.)