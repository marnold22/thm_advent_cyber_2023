# Day_13 [Intrusion-Detection] To the Pots, Through the Walls

+ Deployable Machine: Yes
+ SSH: Yes
  + UN: vantwinkle
  + PW: TwinkleStar

Description: The proposed merger and suspicious activities have kept all teams busy and engaged. So that the Best Festival Company's systems are safeguarded in the future against malicious attacks, McSkidy assigns The B Team, led by McHoneyBell, to research and investigate mitigation and proactive security. The team's efforts will be channelled into the company's defensive security process. You are part of the team – a security researcher tasked with gathering information on defence and mitigation efforts.

> IP: [10.10.213.85]

## LEARNING OBJECTIVES

1. Learn to understand incident analysis through the Diamond Model.
2. Identify defensive strategies that can be applied to the Diamond Model.
3. Learn to set up firewall rules and a honeypot as defensive strategies.

## OVERVIEW

1. Defensive Diamond Model
   1. **Threat hunting** is a proactive and iterative process, led by skilled security professionals, to actively search for signs of malicious activities or security weaknesses within the organisation's network and systems. Organisations can detect adversaries early in their attack lifecycle by conducting regular threat hunts. Threat hunters analyse behavioural patterns, identify advanced threats, and improve incident response. Developing predefined hunting playbooks and fostering collaboration among teams ensures a systematic and efficient approach to threat hunting.
   2. **Vulnerability management** is a structured process of identifying, assessing, prioritising, mitigating, and monitoring vulnerabilities in an organisation's systems and applications. Regular vulnerability scanning helps identify weaknesses that adversaries could exploit. Prioritising vulnerabilities based on their severity and potential impact, promptly patching or remediating vulnerabilities, and maintaining an up–to–date asset inventory is essential. Continuous monitoring, integration with threat intelligence feeds, and periodic penetration testing further strengthen the organisation's security posture. Meanwhile, reporting and accountability provide visibility into security efforts.

2. Firewall
   1. Stateless/packet-filtering: This firewall provides the most straightforward functionality by inspecting and filtering individual network packets based on a set of rules that would point to a source or destination IP address, ports and protocols. The firewall doesn’t consider any context of each connection when making decisions and effectively blocks denial–of–service attacks and port scans.
   2. Stateful inspection: This firewall is more sophisticated. It is used to track the state of network connections and use this information to make filtering decisions. For example, if a packet being channelled to the network is part of an established connection, the stateful firewall will let it pass through. However, the packet will be blocked if it is not part of an established connection.
   3. Proxy service: This firewall protects the network by filtering messages at the application layer, providing deep packet inspection and more granular control over traffic content. The firewall can block access to certain websites or block the transmission of specific types of files.
   4. Web application firewall (WAF): This firewall is designed to protect web applications. WAFs block common web attacks such as SQL injection, cross-site scripting, and denial-of-service attacks.
   5. Next-generation firewall: This firewall combines the functionalities of the stateless, stateful, and proxy firewalls with features such as intrusion detection and prevention and content filtering.

## STEPS

1. Deploy Machine
2. SSH into machine
   1. > ssh vantwinkle@10.10.213.85
      1. PW: TwinkleStar
3. CONFIG FIREWALL TO BLOCK TRAFFIC
   1. Check status
      1. > sudo ufw status
         1. "Inactive"
   2. Add Rules
      1. Allow outgoing
         1. > sudo ufw default allow outgoing
      2. Deny Incoming
         1. > sudo ufw default deny incoming
      3. Allow SSH
         1. sudo ufw allow 22/tcp
      4. Deny from IP_ADDRESS
         1. > sudo ufw deny from 192.168.100.25
      5. Deny Network Interface
         1. > sudo ufw deny in on eth0 from 192.168.100.26
   3. Enable our Rules
      1. > sudo ufw enable
   4. Check our rules
      1. > sudo ufw status verbose

         ```text
            To                         Action      From
            --                         ------      ----
            22/tcp                     ALLOW IN    Anywhere                  
            Anywhere                   DENY IN     192.168.100.25            
            Anywhere on eth0           DENY IN     192.168.100.26            
            22/tcp (v6)                ALLOW IN    Anywhere (v6) 
         ```
   
   4. Reset Values
      1. > sudo ufw reset
4. HONEYPOT
   1. TYPES:
      1. **Low–interaction** honeypots: These honeypots artfully mimic simple systems like web servers or databases. They gather intelligence on attacker behaviour and detect new attack techniques.
      2. **High–interaction** honeypots: These honeypots take deception to new heights, emulating complex systems like operating systems and networks. They collect meticulous details on attacker behaviour and study their techniques to exploit vulnerabilities.
   2. TOOL PenTBox
      1. Navigate to the tool
         1. > cd /pentbox/pentbox-1.8/
      2. Lets run the program
         1. > sudo ./pentbox.rb
            1. Option 2 -> Network Tools
            2. Option 3 -> Honeypot
            3. Option 2 -> Manual Config
               1. Port Open: -> 8080
               2. Insert False Message: -> Santa has gone for the Holidays. Tough luck.
         2. Navigate to website on port 8080
            1. INTRUSION DETECTED!
5. VAN-TWINKLE CHALLENGE
   1. Deploy Van Twinkle's firewall rules
      1. > sudo ./Van_Tinkle_riles.sh
   2. Examine Rules
      1. > sudo ufw status

         ```text
            To                         Action      From
            --                         ------      ----
            80/tcp                     ALLOW       Anywhere                  
            22/tcp                     ALLOW       Anywhere                  
            21/tcp                     DENY        Anywhere                  
            8088                       DENY        Anywhere                  
            8090/tcp                   DENY        Anywhere                  
            80/tcp (v6)                ALLOW       Anywhere (v6)             
            22/tcp (v6)                ALLOW       Anywhere (v6)             
            21/tcp (v6)                DENY        Anywhere (v6)             
            8088 (v6)                  DENY        Anywhere (v6)             
            8090/tcp (v6)              DENY        Anywhere (v6)
         ```

         1. In here we can see that Port 80 and Port 22 are allowed from anywhere, but Port 21, 8088, 8090 are all denied from anywhere
         2. So lets update these rules so we can potentially find the flag
   3. RULES
      1. Allow 8088
         1. > sudo ufw allow 8088
      2. Allow 8090
         1. > sudo ufw allow 8090/tcp
      3. Apply
         1. > sudo ufw enable
   4. Navigate to Website on port 8090
      1. Looking through the webpage we see `THM{P0T$_W@11S_4_S@N7@}`


## QUESTIONS

1. Which security model is being used to analyse the breach and defence strategies?
   1. `Diamond Model`
2. Which defence capability is used to actively search for signs of malicious activity?
   1. `Threat Hunting`
3. What are our main two infrastructure focuses? (Answer format: answer1 and answer2)
   1. `Firewall and Honeypot`
4. Which firewall command is used to block traffic?
   1. `deny`
5. There is a flag in one of the stories. Can you find it?
   1. `THM{P0T$_W@11S_4_S@N7@}`