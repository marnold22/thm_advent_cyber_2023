# Day_08 [Disk-Forensics] Have a Holly, Jolly Byte!

+ Deployable Machine: Yes
+ RDP: Yes
  + UN: analyst
  + PW: AoC2023!

Description: The drama unfolds as the Best Festival Company and AntarctiCrafts merger wraps up! Tracy McGreedy, now a grumpy regional manager, secretly plans sabotage. His sidekick, Van Sprinkles, hesitantly kicks off a cyber attack – but guess what? Van Sprinkles is having second thoughts and helps McSkidy's team bust McGreedy's evil scheme!

> IP: [10.10.26.248]

## LEARNING OBJECTIVES

1. Use FTK Imager to track down and piece together McGreedy's deleted digital breadcrumbs, exposing his evil scheme. Learn how to perform the following with FTK Imager:
   1. Analyse digital artefacts and evidence.
   2. Recover deleted digital artefacts and evidence.
   3. Verify the integrity of a drive/image used as evidence.

## OVERVIEW

1. STORY
   1. Van Sprinkles, wrestling with his conscience, scatters USB drives loaded with malware. Little do the AntarctiCrafts employees know, a storm's brewing in their network. Van Jolly, shivering and clueless, finds a USB drive in the parking lot. Little does she know that plugging it in will unleash a digital disaster crafted by the vengeful McGreedy. But this is exactly what she does. Upon reaching her desk, she immediately plugs in the USB drive. Amidst the digital chaos of notifications and alerts from the cyber attack, McSkidy gets a cryptic email. It's Van Sprinkles, ridden with guilt, nudging her towards exposing McGreedy without blowing his own cover. McSkidy, with a USB in hand, reveals to Van Jolly the true nature of her innocent find – a tool for digital destruction! Shock and disbelief play across Van Jolly's face as McSkidy explains the gravity of the situation and the digital pandemonium unleashed upon their network by the insidious device. McSkidy, Forensic McBlue and the team, having confiscated the USB drive from Van Jolly, dive into a digital forensic adventure to unravel a web of deception hidden in the device. Every line of code has a story. McSkidy and the team piece it together, inching closer to the shadow in their network.
2. INVESTIGATING USB
   1. In our scenario, the write-protected USB drive that McSkidy confiscated will automatically be attached to the VM upon startup. The VM mounts an emulated USB flash drive, "\\PHYSICALDRIVE2 - Microsoft Virtual Disk [1GB SCSI]" in read-only mode to replicate the scenario where a physical drive, connected to a write blocker, is attached to an actual machine for forensic analysis.

## STEPS

1. Deploy Machine
2. RDP into machine
3. FTK-IMAGER
   1. > file -> add evidence item -> physical device -> "\\PHYSICALDRIVE2 - Microsoft Virtual Disk [1GB SCSI]"
   2. > file -> verify drive/image
      1. MD5 -> `b3066cdd1ebf79df4f8864ae14b545ce`
      2. SHA1 -> `39f2dea6ffb43bf80d80f19d122076b3682773c2`
   3. Explore Drive
      1. Open -> "DO_NOT_OPEN" folder
         1. In here we see:
            1. crypTOYminer_prototype.py
            2. JuicyTomaTOY.zip
            3. merger_contract.docx
            4. merger_sabotage_plan.pdf
            5. secretchat.txt
         2. All of these were deleted files so lets export them and take a look
      2. We also see several PNG files deleted
         1. wallpaper.png
         2. portrait.png
      3. > Rightclick -> export files -> desktop
4. EXPORTED FILES
   1. secretchat.txt

      ```text
         [23:45] Gr33dYsH4d0W: Hey, you there?
         [23:46] V4nd4LmUffL3r5: Yeah, what's up?
         [23:47] Gr33dYsH4d0W: Just finalizing the malware C2 setup. The server is good to go at mcgreedysecretc2.thm.
         [23:48] V4nd4LmUffL3r5: Good. How's the payload looking?
         [23:49] Gr33dYsH4d0W: It's hidden inside JuicyTomaTOY_final.zip. Should look innocent enough. I will share the password over a different chat.
         [23:49] Gr33dYsH4d0W: I will also send you additional details to use JuicyTomaTOYDownloader.exe with the necessary arguments in case you can plug the USB drive into a machine at the AntarctiCrafts office and do it yourself.
         [23:50] V4nd4LmUffL3r5: Cool. I'm still nervous about the drop. Dropping it in the parking lot feels risky.
         [23:51] Gr33dYsH4d0W: It's the best way. Our fellow frostlings are bound to find it and plug it in. Curiosity is a powerful thing.
         [23:52] V4nd4LmUffL3r5: Yeah, but what if I'm seen? I'm still shaking over this.
         [23:53] Gr33dYsH4d0W: Just act normal. No one suspects a thing. And if someone does catch on?
         [23:54] V4nd4LmUffL3r5: What then? We need a Plan B.
         [23:55] Gr33dYsH4d0W: If we get caught, we deny everything. I've wiped our digital footprints. Even with the USB, they have nothing on us.
         [23:56] V4nd4LmUffL3r5: What about the server?
         [23:57] Gr33dYsH4d0W: It's offshore, untraceable. As long as that USB isn't traced back to us, we're ghosts.
         [23:58] V4nd4LmUffL3r5: I'm not sure, man. This is getting too hot for me.
         [23:59] Gr33dYsH4d0W: Stay frosty. We're close to pulling this off. Just drop it tomorrow and we're golden.
         [00:00] V4nd4LmUffL3r5: Alright. I'll do it first thing.
         [00:01] Gr33dYsH4d0W: Good. Contact me once it's done. And remember, no names, no direct references. We’re just shadows.
         [00:02] V4nd4LmUffL3r5: Understood. Catch you later.
         [00:03] Gr33dYsH4d0W: Stay safe. Get ready to prepare and drop the USB drives then delete this chat.
      ```

      1. In here we see that the C2 server is `mcgreedysecretc2.thm`
   2. JuicyTomaTOY.zip
      1. Extract contents and we see `JuicyTomaTOY.exe`
   3. Portrait.png
      1. Don't see anything
   4. Wallpaper.png
      1. Don't see anything
5. FTK-IMAGER
   1. Going back to ftk-imager lets take a look at the PNG files dut directly through the HEX editor
   2. PORTRAIT.PNG
      1. > rightclick -> search -> "THM"
         1. FOUND: `THM{byt3-L3vel_@n4Lys15}`

## QUESTIONS

1. What is the malware C2 server?
   1. `mcgreedysecretc2.thm`
2. What is the file inside the deleted zip archive?
   1. `JuicyTomaTOY.exe`
3. What flag is hidden in one of the deleted PNG files?
   1. `THM{byt3-L3vel_@n4Lys15}`
4. What is the SHA1 hash of the physical drive and forensic image?
   1. `39f2dea6ffb43bf80d80f19d122076b3682773c2`
