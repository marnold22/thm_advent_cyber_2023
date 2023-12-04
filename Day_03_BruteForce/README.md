# Day_03 [Brute-Forcing] Hydra is Coming to Town

+ Deployable Machine: Yes
+ Website: Yes

Description: Everyone was shocked to discover that several critical systems were locked. But the chaos didn’t end there: the doors to the IT rooms and related network infrastructure were also locked! Adding to the mayhem, during the lockdown, the doors closed suddenly on Detective Frost-eau. As he tried to escape, his snow arm got caught, and he ended up losing it! He’s now determined to catch the perpetrator, no matter the cost. It seems that whoever did this had one goal: to disrupt business operations and stop gifts from being delivered on time. Now, the team must resort to backup tapes to recover the systems. To their surprise, they find out they can’t unlock the IT room door! The password to access the control systems has been changed. The only solution is to hack back in to retrieve the backup tapes.

> IP: [10.10.212.2]

## LEARNING OBJECTIVES

1. How many different PIN codes do we have?
2. How many different passwords can we generate?
3. How long does it take to find the password by brute force?

## OVERVIEW

1. How Long Does It Take To Brute Force the Password
   1. 14 million is a huge number, but we can use a computer system to try out all the possible password combinations, i.e., brute force the password. If trying a password takes 0.001 seconds due to system throttling (i.e., we can only try 1,000 passwords per second), finding the password will only take up to four hours.
   2. If you are curious about the maths, 624×0.001 = 14, 776 seconds is the number of seconds necessary to try out all the passwords. We can find the number of hours needed to try out all the passwords by dividing by 3,600 (1 hour = 3,600 seconds): 14,776/3,600 = 4.1 hours.
   3. In reality, the password can be closer to the beginning of the list or closer to the end. Therefore, on average, we can expect to find the password in around two hours, i.e., 4.1/2 = 2.05 hours. Hence, a four-character password is generally considered insecure.
   4. We should note that in this hypothetical example, we are assuming that we can try 1,000 passwords every second. Few systems would let us go this fast. After a few incorrect attempts, most would lock us out or impose frustratingly long waiting periods. On the other hand, with the password hash, we can try passwords offline. In this case, we would only be limited by how fast our computer is.
   5. We can make passwords more secure by increasing the password complexity. This can be achieved by specifying a minimum password length and character variety. For example, the character variety might require at least one uppercase letter, one lowercase letter, one digit, and one symbol.

## STEPS

1. Deploy Machine
2. Navigate to wesbite "http://10.10.212.2:8000"
   1. On this page we see a keypad that has "0-9" and "a-f" as possible inputs
   2. Inputing values we see that we can only use 3 characters/digits
   3. Redirects to a "Access denied" if incorrect
3. CRUNCH
   1. Generate list of passcodes given the parameters
      1. 16 characters (0-9, a-f)
      2. Min of 3 characters/digits
      3. Max of 3 characters/digits
   2. > crunch 3 3 0123456789ABCDEF -o codes.txt
4. HYDRA
   1. Inspect source code to find fields submitted by the FORM
      1. POST -> request type to login.php
      2. pin -> input field
      3. Access denied -> error message
   2. Craft command
      1. > hydra -l '' -P codes.txt -f -v 10.10.212.2 http-post-form "/login.php:pin=^PASS^:Access denied" -s 8000
         1. RESPONSE: `[8000][http-post-form] host: 10.10.212.2   password: 6F5`
         2. Success, our password is `6F5`
5. ENTER
   1. Input the passcode
   2. We are redirected to control.php which looks to have 4 options
      1. Adjust AC Temp
      2. Test Backup Power
      3. Unlock Door
      4. Reset Pin
   3. We want to unlock the door
      1. FLAG: `THM{pin-code-brute-force}`
   

## QUESTIONS

1. Using crunch and hydra, find the PIN code to access the control system and unlock the door. What is the flag?
   1. `THM{pin-code-brute-force}`
