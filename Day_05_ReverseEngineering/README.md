# Day_05 [Reverse-Enineering] A Christmas DOScovery: Tapes of Yule-tide Past

+ Deployable Machine: Yes
+ RDP: Yes
  + UN: Administrator
  + PW: Passw0rd!

Description: The backup tapes have finally been recovered after the team successfully hacked the server room door. However, as fate would have it, the internal tool for recovering the backups can't seem to read them. While poring through the tool's documentation, you discover that an old version of this tool can troubleshoot problems with the backup. But the problem is, that version only runs on DOS (Disk Operating System)! Thankfully, tucked away in the back of the IT room, covered in cobwebs, sits an old yellowing computer complete with a CRT monitor and a keyboard. With a jab of the power button, the machine beeps to life, and you are greeted with the DOS prompt. Restoring Backups in DOS. Frost-eau, who is with you in the room, hears the beep and heads straight over to the machine. The snowman positions himself in front of it giddily. "I haven't used these things in a looong time," he says, grinning. He hovers his hands on the keyboard, ready to type, but hesitates. He lifts his newly installed mechanical arm, looks at the fat and stubby metallic fingers, and sighs. "You take the helm," he says, looking at you, smiling but looking embarrassed. "I'll guide you." You insert a copy of the backup tapes into the machine and start exploring.

> IP: [10.10.111.96]

## LEARNING OBJECTIVES

1. Experience how to navigate an unfamiliar legacy system.
2. Learn about DOS and its connection to its contemporary, the Windows Command Prompt.
3. Discover the significance of file signatures and magic bytes in data recovery and file system analysis.

## OVERVIEW

1. The Disk Operating System was a dominant operating system during the early days of personal computing. Microsoft tweaked a DOS variant and rebranded it as MS-DOS, which later served as the groundwork for their graphical extension, the initial version of Windows OS. The fundamentals of file management, directory structures, and command syntax in DOS have stood the test of time and can be found in the command prompt and PowerShell of modern-day Windows systems.
2. While the likelihood of needing to work with DOS in the real world is low, exploring this unfamiliar system can still be a valuable learning opportunity.

## STEPS

1. Deploy Machine
2. Remote into RDP session
3. Boot Dos-Box-X
   1. We are met with what looks to be an old school dos system lets explore
4. DOS-BOX
   1. > ls
      1. DEV, GAMES, NOTES, TC, TOOLS, ac2023.bak, plan.txt
      2. Lets take a look at the plan.txt file
   2. > dir
      1. ac2023.bak - 12,407 bytes
   3. > type plan.txt

      ```text
         Usage:
         ------
         1. Launch the program
         2. Follow onscreen prompts to either backup or restore data
         3. Specify the source destination paths as prompted
         4. Review the operation summary and ensure your data is securely handled

         Acknowledgements:
         -----------------
         Big thanks to Prof. Cliffski McBlue and my caffeine-fueled comrades
         during the university days. The journey from concept to code was a
         roller-coaster of debugging and a-ha moments. Now, the BackupMaster
         3000 is ready to serve and protect the whimsical data of AntartiCrafts!

         Troubleshooting:
         ----------------
         If you encounter any issues during the backup or restore processes,
         ensure to check the first few bytes of the file in question. The
         first bytes of the file signature should be "41 43". If these bytes
         do not match, it's likely that the file is not compatible or may be
         corrupted.

         Backup, Restore, and Conquer!
      ```

      1. So in the troubleshooting section it looks like we need to make sure the file signiture is correct
      2. Lets check the bytes of the "Magic Bytes" string of the ac2023.bak
   4. > EDIT ac2023.bak
      1. The first 2 bytes are "XX" and for a microsoft / DOS file we need "MZ"
      2. We need to convert our "41 43" from hex into text
      3. CYBERCHEF
         1. FROM HEX: "41 43" = "AC"
         2. We need to change the first two characters from XX to AC
   5. > EDIT ac2023.bak
      1. Change first 2 characters to "AC"
      2. > ALT F -> S (To save)
   6. BUMASTER.EXE
      1. Now we can run the BUMASTER.EXE executable on C:\AC2023.BAK
      2. > BUMASTER.EXE C:\AC2023.BAK
         1. RESPONSE:

            ```text
               Backup successully restored.
               Congratulations
               THM{0LD_5CH00l_C00L_d00D}
            ```

## QUESTIONS

1. How large (in bytes) is the AC2023.BAK file?
   1. `12,704`
2. What is the name of the backup program?
   1. `BackupMaster3000`
3. What should the correct bytes be in the backup's file signature to restore the backup properly?
   1. `41 43`
4. What is the flag after restoring the backup successfully?
   1. `THM{0LD_5CH00l_C00L_d00D}`
