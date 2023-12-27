# Day_24 [Mobile-Analysis] You Are on the Naughty List, McGreedy

+ Deployable Machine: Yes
+ RDP: Yes
  + UN: administrator
  + PW: jNgQTDN7

Description: Detective Frost-eau continues to piece the evidence together, and Tracy McGreedy is now a suspect. What’s more, the detective believes that McGreedy communicated with an accomplice. Smartphones are now an indispensable part of our lives for most of us. We use them to communicate with friends, family members, and colleagues, browse the Internet, shop online, perform e-banking transactions, and many other things. Among other reasons, it’s because smartphones are so intertwined in our activities that they can help exonerate or convict someone of a crime. Frost-eau suggests that Tracy’s company-owned phone be seized so that Forensic McBlue can analyse it in his lab to collect digital evidence. Because it’s company-owned, no complicated legal procedures are required.

> IP: [10.10.31.52]

## LEARNING OBJECTIVES

1. Procedures for collecting digital evidence
2. The challenges with modern smartphones
3. Using Autopsy Digital Forensics with an actual Android image

## OVERVIEW

1. Acquiring Digital Forensics Image
   1. There are four main types of forensic image acquisition:
      1. Static acquisition: A bit-by-bit image of the disk is created while the device is turned off.
      2. Live acquisition: A bit-by-bit image of the disk is created while the device is turned on.
      3. Logical acquisition: A select list of files is copied from the seized device.
      4. Sparse acquisition: Select fragments of unallocated data are copied. The unallocated areas of the disk might contain deleted data; however, this approach is limited compared to static and live acquisition because it doesn’t cover the whole disk.

## CREATE AUTOPSY FILE (PRACTICAL)

1. MAIN TOOLS FOR ANDROID PHONES
   1. Android Debug Bridge (adb)
   2. Autopsy Digital Forensics
2. CREATE A BACKUP
   1. > adb backup -all -f android_backup.ab
3. WITH ROOT ACCESS
   1. > adb shell
   2. > mount | grep data
   3. > adb pull /dev/block/dm-0 Android-McGreedy.img

## STEPS

1. Deploy Machine
2. RDP into machine
3. PRACTICAL CASE
   1. We are going to use the McGreed.aut file in Tracy -> Documents folder
4. AUTOPSY
   1. Launch Autopsy
      1. New Case
      2. Tracy McGreedy - Android
      3. Case Number: 101
   2. Add Data Source
      1. Generate new hostname based on data source name
      2. Disk Image or VM File
         1. Now provide the Disk IMG
            1. PATH -> /Downloads/Android-McGreedy.img
      3. Select Modules
         1. Definitely need the two ANDROID ANALYZER modules
5. McGreedy.aut
   1. Now that we have the image loaded, lets strar exploring
   2. EXPLORE
      1. View Files -> File Types -> By Extension -> Images
         1. BOARD2.JPG -> `THM{DIGITAL_FORENSICS}`
      2. Data Artifacts -> Contacts
         1. Name -> `Detective Carrot-Nose`
      3. Data Artefacts -> Messages
         1. Outgoing Message -> 2023-10-28 17:42:05 GMT -> `chee7AQu`

## QUESTIONS

1. One of the photos contains a flag. What is it?
   1. `THM{DIGITAL_FORENSICS}`
2. What name does Tracy use to save Detective Frost-eau’s phone number?
   1. `Detective Carrot-Nose`
3. One SMS exchanged with Van Sprinkles contains a password. What is it?
   1. `chee7AQu`
