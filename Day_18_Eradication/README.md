# Day_18 [Eradication] A Gift That Keeps on Giving

+ Deployable Machine: Yes

Description: McGreedy is very greedy and doesn't let go of any chance to earn some extra elf bucks. During the investigation of an insider threat, the Blue Team found a production server that was using unexpectedly high resources. It might be a cryptominer. They narrowed it down to a single unapproved suspicious process. It has to be eliminated to ensure that company resources are not misused. For this, they must find all the nooks and crannies where the process might have embedded itself and remove it

> IP: [10.10.46.228]

## LEARNING OBJECTIVES

1. Identify the CPU and memory usage of processes in Linux.
2. Kill unwanted processes in Linux.
3. Find ways a process can persist beyond termination.
4. Remove persistent processes permanently.

## OVERVIEW

## STEPS

1. Deploy Machine
2. Open Split Pane
3. IDENTIFY THE PROCESS
   1. > top

      ```text
         PID USER      PR   NI   VIRT    RES    SHR S  %CPU  %MEM   TIME    COMMAND
         630 root      20   0    2488   1524   1432 R 100.0   0.0   4:28.78 a
         920 ubuntu    20   0  370556 149032  63120 R   1.7   3.7   0:06.78 Xtigervnc
         1812 root     20   0  123216  27344   7768 S   0.7   0.7   0:00.99 python3
         708 root      20   0 1315024  18076  10380 S   0.3   0.4   0:00.73 amazon-ssm-agen
         1824 ubuntu   20   0  398900  49332  38284 S   0.3   1.2   0:01.27 mate-terminal
      ```

      1. In here we can see that there is a processID = 630, with command "a" that is using almost 100% of CPU
4. KILLING THE CULPRIT
   1. Making note of the PID from the previous step lets kill that process
      1. > sudo kill 630
   2. Now lets go back and check to see if it worked
      1. > top

         ```text
            1982 root      20   0    2488   1432   1344 R 100.0   0.0   0:43.34 a
             920 ubuntu    20   0  374976 153492  63124 S   5.3   3.8   0:09.94 Xtigervnc
            1812 root      20   0  123496  27608   7768 S   3.3   0.7   0:01.94 python3
            1824 ubuntu    20   0  398900  49572  38292 S   1.3   1.2   0:01.65 mate-terminal
         ```

         1. uh-oh, we can see that the command is still being ran, but it has a different ProcessID now
5. CHECKING CRON-TAB
   1. > crontab -l

      ```text
         # Edit this file to introduce tasks to be run by cron.
         # 
         # Each task to run has to be defined through a single line
         # indicating with different fields when the task will be run
         # and what command to run for the task
         # 
         # To define the time you can provide concrete values for
         # minute (m), hour (h), day of month (dom), month (mon),
         # and day of week (dow) or use '*' in these fields (for 'any').
         # 
         # Notice that tasks will be started based on the cron's system
         # daemon's notion of time and timezones.
         # 
         # Output of the crontab jobs (including errors) is sent through
         # email to the user the crontab file belongs to (unless redirected).
         # 
         # For example, you can run a backup of all your user accounts
         # at 5 a.m every week with:
         # 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
         # 
         # For more information see the manual pages of crontab(5) and cron(8)
         # 
         # m h  dom mon dow   command
         @reboot sudo runuser -l ubuntu -c 'vncserver :1 -depth 24 -geometry 1900x1200'
         @reboot sudo python3 -m websockify 80 localhost:5901 -D
      ```

      1. Nothing in here stands out, so lets try switching users and see if root is running something
   2. > sudo su
   3. > crontab -l

      ```text
         # Edit this file to introduce tasks to be run by cron.
         # 
         # Each task to run has to be defined through a single line
         # indicating with different fields when the task will be run
         # and what command to run for the task
         # 
         # To define the time you can provide concrete values for
         # minute (m), hour (h), day of month (dom), month (mon),
         # and day of week (dow) or use '*' in these fields (for 'any').
         # 
         # Notice that tasks will be started based on the cron's system
         # daemon's notion of time and timezones.
         # 
         # Output of the crontab jobs (including errors) is sent through
         # email to the user the crontab file belongs to (unless redirected).
         # 
         # For example, you can run a backup of all your user accounts
         # at 5 a.m every week with:
         # 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
         # 
         # For more information see the manual pages of crontab(5) and cron(8)
         # 
         # m h  dom mon dow   command
      ```

      1. ... still nothing!
6. CHEKING FOR RUNNING SERVICES
   1. Lets list all services and specifically all that are "enabled"
      1. > systemctl list-unit-files | grep enabled

         ```text
            proc-sys-fs-binfmt_misc.automount              static          enabled      
            -.mount                                        generated       enabled      
            dev-hugepages.mount                            static          enabled      
            dev-mqueue.mount                               static          enabled      
            proc-sys-fs-binfmt_misc.mount                  disabled        enabled      
            snap-amazon\x2dssm\x2dagent-5163.mount         enabled         enabled      
            snap-amazon\x2dssm\x2dagent-7628.mount         enabled         enabled      
            snap-core-16202.mount                          enabled         enabled      
            snap-core18-2790.mount                         enabled         enabled      
            snap-core18-2796.mount                         enabled         enabled      
            snap-core20-1361.mount                         enabled         enabled      
            snap-core20-2015.mount                         enabled         enabled      
            snap-lxd-22526.mount                           enabled         enabled      
            snap-lxd-24061.mount                           enabled         enabled      
            sys-fs-fuse-connections.mount                  static          enabled      
            sys-kernel-config.mount                        static          enabled      
            sys-kernel-debug.mount                         static          enabled      
            sys-kernel-tracing.mount                       static          enabled      
            acpid.path                                     enabled         enabled      
            apport-autoreport.path                         enabled         enabled      
            cups.path                                      enabled         enabled      
            systemd-ask-password-console.path              static          enabled      
            systemd-ask-password-plymouth.path             static          enabled      
            systemd-ask-password-wall.path                 static          enabled      
            session-1.scope                                transient       enabled      
            session-c1.scope                               transient       enabled      
            a-unkillable.service                           enabled         enabled      
            accounts-daemon.service                        enabled         enabled      
            acpid.service                                  disabled        enabled      
            alsa-restore.service                           static          enabled      
            alsa-state.service                             static          enabled      
            alsa-utils.service                             masked          enabled      
            anacron.service                                enabled         enabled      
            apparmor.service                               enabled         enabled      
            apport-autoreport.service                      static          enabled      
            apport-forward@.service                        static          enabled      
            apport.service                                 generated       enabled      
            apt-daily-upgrade.service                      static          enabled      
            apt-daily.service                              static          enabled      
            atd.service                                    enabled         enabled      
            autovt@.service                                enabled         enabled      
            avahi-daemon.service                           enabled         enabled      
            blk-availability.service                       enabled         enabled      
            blueman-mechanism.service                      enabled         enabled      
            bluetooth.service                              enabled         enabled      
            bolt.service                                   static          enabled      
            brltty-udev.service                            static          enabled      
            brltty.service                                 disabled        enabled      
            clean-mount-point@.service                     static          enabled      
            cloud-config.service                           enabled         enabled      
            cloud-final.service                            enabled         enabled      
            cloud-init-local.service                       enabled         enabled      
            cloud-init.service                             enabled         enabled      
            colord.service                                 static          enabled      
            configure-printer@.service                     static          enabled      
            console-setup.service                          enabled         enabled      
            container-getty@.service                       static          enabled      
            cron.service                                   enabled         enabled      
            cryptdisks-early.service                       masked          enabled      
            cryptdisks.service                             masked          enabled      
            cups-browsed.service                           enabled         enabled      
            cups.service                                   enabled         enabled      
            dbus-fi.w1.wpa_supplicant1.service             enabled         enabled      
            dbus-org.bluez.service                         enabled         enabled      
            dbus-org.freedesktop.Avahi.service             enabled         enabled      
            dbus-org.freedesktop.hostname1.service         static          enabled      
            dbus-org.freedesktop.locale1.service           static          enabled      
            dbus-org.freedesktop.login1.service            static          enabled      
            dbus-org.freedesktop.ModemManager1.service     enabled         enabled      
            dbus-org.freedesktop.nm-dispatcher.service     enabled         enabled      
            dbus-org.freedesktop.resolve1.service          enabled         enabled      
            dbus-org.freedesktop.timedate1.service         static          enabled      
            dbus-org.freedesktop.timesync1.service         enabled         enabled      
            dbus.service                                   static          enabled      
            display-manager.service                        indirect        enabled      
            dm-event.service                               static          enabled      
            dmesg.service                                  enabled         enabled      
            e2scrub@.service                               static          enabled      
            e2scrub_all.service                            static          enabled      
            e2scrub_fail@.service                          static          enabled      
            e2scrub_reap.service                           enabled         enabled      
            ec2-instance-connect.service                   enabled         enabled      
            emergency.service                              static          enabled      
            finalrd.service                                enabled         enabled      
            fprintd.service                                static          enabled      
            friendly-recovery.service                      static          enabled      
            fstrim.service                                 static          enabled      
            fwupd-offline-update.service                   static          enabled      
            fwupd.service                                  static          enabled      
            gdm.service                                    static          enabled      
            gdm3.service                                   static          enabled      
            geoclue.service                                static          enabled      
            getty-static.service                           static          enabled      
            getty@.service                                 enabled         enabled      
            gpu-manager.service                            enabled         enabled      
            grub-common.service                            generated       enabled      
            grub-initrd-fallback.service                   enabled         enabled      
            hddtemp.service                                generated       enabled      
            hibagent.service                               generated       enabled      
            hibinit-agent.service                          enabled         enabled      
            hwclock.service                                masked          enabled      
            ifup@.service                                  static          enabled      
            ifupdown-pre.service                           static          enabled      
            ifupdown-wait-online.service                   disabled        enabled      
            iio-sensor-proxy.service                       static          enabled      
            initrd-cleanup.service                         static          enabled      
            initrd-parse-etc.service                       static          enabled      
            initrd-switch-root.service                     static          enabled      
            initrd-udevadm-cleanup-db.service              static          enabled      
            ippusbxd@.service                              static          enabled      
            irqbalance.service                             enabled         enabled      
            iscsi.service                                  enabled         enabled      
            iscsid.service                                 disabled        enabled      
            kerneloops.service                             enabled         enabled      
            keyboard-setup.service                         enabled         enabled      
            kmod-static-nodes.service                      static          enabled      
            kmod.service                                   static          enabled      
            lightdm.service                                indirect        enabled      
            logrotate.service                              static          enabled      
            lvm2-lvmpolld.service                          static          enabled      
            lvm2-monitor.service                           enabled         enabled      
            lvm2-pvscan@.service                           static          enabled      
            lvm2.service                                   masked          enabled      
            lxd-agent-9p.service                           enabled         enabled      
            lxd-agent.service                              enabled         enabled      
            man-db.service                                 static          enabled      
            mdadm-grow-continue@.service                   static          enabled      
            mdadm-last-resort@.service                     static          enabled      
            mdcheck_continue.service                       static          enabled      
            mdcheck_start.service                          static          enabled      
            mdmon@.service                                 static          enabled      
            mdmonitor-oneshot.service                      static          enabled      
            mdmonitor.service                              static          enabled      
            ModemManager.service                           enabled         enabled      
            modprobe@.service                              static          enabled      
            motd-news.service                              static          enabled      
            multipath-tools-boot.service                   masked          enabled      
            multipath-tools.service                        enabled         enabled      
            multipathd.service                             enabled         enabled      
            netplan-ovs-cleanup.service                    enabled-runtime enabled      
            network-manager.service                        enabled         enabled      
            networkd-dispatcher.service                    enabled         enabled      
            networking.service                             enabled         enabled      
            NetworkManager-dispatcher.service              enabled         enabled      
            NetworkManager-wait-online.service             enabled         enabled      
            NetworkManager.service                         enabled         enabled      
            ondemand.service                               enabled         enabled      
            open-iscsi.service                             enabled         enabled      
            open-vm-tools.service                          enabled         enabled      
            openvpn-client@.service                        disabled        enabled      
            openvpn-server@.service                        disabled        enabled      
            openvpn.service                                enabled         enabled      
            openvpn@.service                               disabled        enabled      
            packagekit-offline-update.service              static          enabled      
            packagekit.service                             static          enabled      
            plymouth-halt.service                          static          enabled      
            plymouth-kexec.service                         static          enabled      
            plymouth-log.service                           static          enabled      
            plymouth-poweroff.service                      static          enabled      
            plymouth-quit-wait.service                     static          enabled      
            plymouth-quit.service                          static          enabled      
            plymouth-read-write.service                    static          enabled      
            plymouth-reboot.service                        static          enabled      
            plymouth-start.service                         static          enabled      
            plymouth-switch-root.service                   static          enabled      
            plymouth.service                               static          enabled      
            polkit.service                                 static          enabled      
            pollinate.service                              enabled         enabled      
            pppd-dns.service                               enabled         enabled      
            procps.service                                 static          enabled      
            pulseaudio-enable-autospawn.service            masked          enabled      
            quotaon.service                                static          enabled      
            rc-local.service                               static          enabled      
            rc.service                                     masked          enabled      
            rcS.service                                    masked          enabled      
            rescue.service                                 static          enabled      
            rsync.service                                  enabled         enabled      
            rsyslog.service                                enabled         enabled      
            rtkit-daemon.service                           disabled        enabled      
            saned.service                                  masked          enabled      
            saned@.service                                 indirect        enabled      
            screen-cleanup.service                         masked          enabled      
            secureboot-db.service                          enabled         enabled      
            serial-getty@.service                          indirect        enabled      
            setvtrgb.service                               enabled         enabled      
            snap.amazon-ssm-agent.amazon-ssm-agent.service enabled         enabled      
            snap.lxd.activate.service                      enabled         enabled      
            snap.lxd.daemon.service                        static          enabled      
            snapd.apparmor.service                         enabled         enabled      
            snapd.autoimport.service                       enabled         enabled      
            snapd.core-fixup.service                       enabled         enabled      
            snapd.failure.service                          static          enabled      
            snapd.recovery-chooser-trigger.service         enabled         enabled      
            snapd.seeded.service                           enabled         enabled      
            snapd.service                                  enabled         enabled      
            snapd.snap-repair.service                      static          enabled      
            snapd.system-shutdown.service                  enabled         enabled      
            speech-dispatcher.service                      disabled        enabled      
            speech-dispatcherd.service                     disabled        enabled      
            spice-vdagent.service                          indirect        enabled      
            spice-vdagentd.service                         indirect        enabled      
            ssh.service                                    enabled         enabled      
            ssh@.service                                   static          enabled      
            sshd.service                                   enabled         enabled      
            sudo.service                                   masked          enabled      
            switcheroo-control.service                     enabled         enabled      
            syslog.service                                 enabled         enabled      
            system-update-cleanup.service                  static          enabled      
            systemd-ask-password-console.service           static          enabled      
            systemd-ask-password-plymouth.service          static          enabled      
            systemd-ask-password-wall.service              static          enabled      
            systemd-backlight@.service                     static          enabled      
            systemd-binfmt.service                         static          enabled      
            systemd-bless-boot.service                     static          enabled      
            systemd-boot-check-no-failures.service         disabled        enabled      
            systemd-boot-system-token.service              static          enabled      
            systemd-exit.service                           static          enabled      
            systemd-fsck-root.service                      static          enabled      
            systemd-fsck@.service                          static          enabled      
            systemd-fsckd.service                          static          enabled      
            systemd-halt.service                           static          enabled      
            systemd-hibernate-resume@.service              static          enabled      
            systemd-hibernate.service                      static          enabled      
            systemd-hostnamed.service                      static          enabled      
            systemd-hwdb-update.service                    static          enabled      
            systemd-hybrid-sleep.service                   static          enabled      
            systemd-initctl.service                        static          enabled      
            systemd-journal-flush.service                  static          enabled      
            systemd-journald.service                       static          enabled      
            systemd-journald@.service                      static          enabled      
            systemd-kexec.service                          static          enabled      
            systemd-localed.service                        static          enabled      
            systemd-logind.service                         static          enabled      
            systemd-machine-id-commit.service              static          enabled      
            systemd-modules-load.service                   static          enabled      
            systemd-network-generator.service              disabled        enabled      
            systemd-networkd-wait-online.service           enabled         enabled      
            systemd-networkd.service                       enabled         enabled      
            systemd-poweroff.service                       static          enabled      
            systemd-pstore.service                         enabled         enabled      
            systemd-quotacheck.service                     static          enabled      
            systemd-random-seed.service                    static          enabled      
            systemd-reboot.service                         static          enabled      
            systemd-remount-fs.service                     enabled-runtime enabled      
            systemd-resolved.service                       enabled         enabled      
            systemd-rfkill.service                         static          enabled      
            systemd-suspend-then-hibernate.service         static          enabled      
            systemd-suspend.service                        static          enabled      
            systemd-sysctl.service                         static          enabled      
            systemd-sysusers.service                       static          enabled      
            systemd-time-wait-sync.service                 disabled        enabled      
            systemd-timedated.service                      static          enabled      
            systemd-timesyncd.service                      enabled         enabled      
            systemd-tmpfiles-clean.service                 static          enabled      
            systemd-tmpfiles-setup-dev.service             static          enabled      
            systemd-tmpfiles-setup.service                 static          enabled      
            systemd-udev-settle.service                    static          enabled      
            systemd-udev-trigger.service                   static          enabled      
            systemd-udevd.service                          static          enabled      
            systemd-update-utmp-runlevel.service           static          enabled      
            systemd-update-utmp.service                    static          enabled      
            systemd-user-sessions.service                  static          enabled      
            systemd-volatile-root.service                  static          enabled      
            udev.service                                   static          enabled      
            udisks2.service                                enabled         enabled      
            ufw.service                                    enabled         enabled      
            unattended-upgrades.service                    enabled         enabled      
            upower.service                                 disabled        enabled      
            usb_modeswitch@.service                        static          enabled      
            usbmuxd.service                                static          enabled      
            user-runtime-dir@.service                      static          enabled      
            user@.service                                  static          enabled      
            uuidd.service                                  indirect        enabled      
            vgauth.service                                 enabled         enabled      
            vmtoolsd.service                               enabled         enabled      
            wacom-inputattach@.service                     static          enabled      
            whoopsie.service                               enabled         enabled      
            wpa_supplicant-nl80211@.service                disabled        enabled      
            wpa_supplicant-wired@.service                  disabled        enabled      
            wpa_supplicant.service                         enabled         enabled      
            wpa_supplicant@.service                        disabled        enabled      
            x11-common.service                             masked          enabled      
            xfs_scrub@.service                             static          enabled      
            xfs_scrub_all.service                          static          enabled      
            xfs_scrub_fail@.service                        static          enabled      
            machine.slice                                  static          enabled      
            system-systemd\x2dcryptsetup.slice             static          enabled      
            user.slice                                     static          enabled      
            acpid.socket                                   enabled         enabled      
            apport-forward.socket                          enabled         enabled      
            avahi-daemon.socket                            enabled         enabled      
            cups.socket                                    enabled         enabled      
            dbus.socket                                    static          enabled      
            dm-event.socket                                enabled         enabled      
            iscsid.socket                                  enabled         enabled      
            lvm2-lvmpolld.socket                           enabled         enabled      
            multipathd.socket                              enabled         enabled      
            saned.socket                                   disabled        enabled      
            snap.lxd.daemon.unix.socket                    enabled         enabled      
            snapd.socket                                   enabled         enabled      
            spice-vdagentd.socket                          static          enabled      
            ssh.socket                                     disabled        enabled      
            systemd-fsckd.socket                           static          enabled      
            systemd-initctl.socket                         static          enabled      
            systemd-journald-audit.socket                  static          enabled      
            systemd-journald-dev-log.socket                static          enabled      
            systemd-journald-varlink@.socket               static          enabled      
            systemd-journald.socket                        static          enabled      
            systemd-journald@.socket                       static          enabled      
            systemd-networkd.socket                        enabled         enabled      
            systemd-rfkill.socket                          static          enabled      
            systemd-udevd-control.socket                   static          enabled      
            systemd-udevd-kernel.socket                    static          enabled      
            uuidd.socket                                   enabled         enabled      
            basic.target                                   static          enabled      
            blockdev@.target                               static          enabled      
            bluetooth.target                               static          enabled      
            boot-complete.target                           static          enabled      
            cloud-config.target                            static          enabled      
            cloud-init.target                              enabled-runtime enabled      
            cryptsetup.target                              static          enabled      
            ctrl-alt-del.target                            disabled        enabled      
            default.target                                 static          enabled      
            emergency.target                               static          enabled      
            final.target                                   static          enabled      
            friendly-recovery.target                       static          enabled      
            getty.target                                   static          enabled      
            graphical.target                               static          enabled      
            hibernate.target                               static          enabled      
            hybrid-sleep.target                            static          enabled      
            initrd-fs.target                               static          enabled      
            initrd-root-device.target                      static          enabled      
            initrd-root-fs.target                          static          enabled      
            initrd-switch-root.target                      static          enabled      
            initrd.target                                  static          enabled      
            local-fs.target                                static          enabled      
            multi-user.target                              static          enabled      
            network-online.target                          static          enabled      
            paths.target                                   static          enabled      
            printer.target                                 static          enabled      
            reboot.target                                  disabled        enabled      
            remote-cryptsetup.target                       disabled        enabled      
            remote-fs.target                               enabled         enabled      
            rescue-ssh.target                              static          enabled      
            runlevel0.target                               disabled        enabled      
            runlevel1.target                               static          enabled      
            runlevel2.target                               static          enabled      
            runlevel3.target                               static          enabled      
            runlevel4.target                               static          enabled      
            runlevel5.target                               static          enabled      
            runlevel6.target                               disabled        enabled      
            shutdown.target                                static          enabled      
            sigpwr.target                                  static          enabled      
            sleep.target                                   static          enabled      
            slices.target                                  static          enabled      
            smartcard.target                               static          enabled      
            sockets.target                                 static          enabled      
            sound.target                                   static          enabled      
            suspend-then-hibernate.target                  static          enabled      
            suspend.target                                 static          enabled      
            swap.target                                    static          enabled      
            sysinit.target                                 static          enabled      
            system-update-pre.target                       static          enabled      
            system-update.target                           static          enabled      
            timers.target                                  static          enabled      
            umount.target                                  static          enabled      
            anacron.timer                                  enabled         enabled      
            apt-daily-upgrade.timer                        enabled         enabled      
            apt-daily.timer                                enabled         enabled      
            e2scrub_all.timer                              enabled         enabled      
            fstrim.timer                                   enabled         enabled      
            fwupd-refresh.timer                            enabled         enabled      
            logrotate.timer                                enabled         enabled      
            man-db.timer                                   enabled         enabled      
            mdadm-last-resort@.timer                       static          enabled      
            mdcheck_continue.timer                         enabled         enabled      
            mdcheck_start.timer                            enabled         enabled      
            mdmonitor-oneshot.timer                        enabled         enabled      
            motd-news.timer                                enabled         enabled      
            snapd.snap-repair.timer                        enabled         enabled      
            systemd-tmpfiles-clean.timer                   static          enabled      
            xfs_scrub_all.timer                            disabled        enabled
         ```

         1. In here we do see somehting that sticks out -> `a-unkillable.service`
         2. Lets get more info about this
   2. Lets check the status of this process
      1. > systemctl status a-unkillable.service

         ```text
            ● a-unkillable.service - Unkillable exe
               Loaded: loaded (/etc/systemd/system/a-unkillable.service; enabled; vendor preset: enabled)
               Active: active (running) since Wed 2023-12-20 18:15:44 UTC; 22min ago
               Main PID: 583 (sudo)
                  Tasks: 5 (limit: 4710)
               Memory: 3.3M
               CGroup: /system.slice/a-unkillable.service
                        ├─ 583 /usr/bin/sudo /etc/systemd/system/a service
                        ├─ 624 /etc/systemd/system/a service
                        └─1982 unkillable proc

            Dec 20 18:15:46 tryhackme sudo[648]: Merry Christmas
            Dec 20 18:15:44 tryhackme sudo[583]:     root : TTY=unknown ; PWD=/ ; USER=root ; COMMAND=/etc/systemd/system/a service
            Dec 20 18:15:44 tryhackme sudo[583]: pam_unix(sudo:session): session opened for user root by (uid=0)
            Dec 20 18:15:44 tryhackme systemd[1]: Started Unkillable exe.
            Dec 20 18:27:47 tryhackme sudo[1986]: Merry Christmas
         ```

         1. So we now see that this service is constantly spawning "a", we also see a little hint: "Merry Christams"
7. GETTING RID OF THE SERVICE
   1. First we need to be root
      1. > sudo su
   2. Then lets stop the process
      1. > systemctl stop a-unkillable.service
   3. Now lets chekc the status
      1. > systemctl status a-unkillable.service

         ```text
            ● a-unkillable.service - Unkillable exe
               Loaded: loaded (/etc/systemd/system/a-unkillable.service; enabled; vendor preset: enabled)
               Active: inactive (dead) since Wed 2023-12-20 18:41:09 UTC; 6s ago
               Process: 583 ExecStart=/usr/bin/sudo /etc/systemd/system/a service (code=killed, signal=TERM)
               Main PID: 583 (code=killed, signal=TERM)

            Dec 20 18:15:46 tryhackme sudo[648]: Merry Christmas
            Dec 20 18:15:44 tryhackme sudo[583]:     root : TTY=unknown ; PWD=/ ; USER=root ; COMMAND=/etc/systemd/system/a service
            Dec 20 18:15:44 tryhackme sudo[583]: pam_unix(sudo:session): session opened for user root by (uid=0)
            Dec 20 18:15:44 tryhackme systemd[1]: Started Unkillable exe.
            Dec 20 18:27:47 tryhackme sudo[1986]: Merry Christmas
            Dec 20 18:41:09 tryhackme systemd[1]: Stopping Unkillable exe...
            Dec 20 18:41:09 tryhackme sudo[583]: pam_unix(sudo:session): session closed for user root
            Dec 20 18:41:09 tryhackme systemd[1]: a-unkillable.service: Succeeded.
            Dec 20 18:41:09 tryhackme systemd[1]: Stopped Unkillable exe.
         ```

         1. Success! 
         2. Now that we killed the process lets disable the service
   4. Disable the service
      1. > systemctl disable a-unkillable.service
         1. RESPONSE: Removed /etc/systemd/system/multi-user.target.wants/a-unkillable.service.
   5. Now lets check the service again
      1. > systemctl status a-unkillable.service

         ```text
            ● a-unkillable.service - Unkillable exe
               Loaded: loaded (/etc/systemd/system/a-unkillable.service; disabled; vendor preset: enabled)
               Active: inactive (dead)

            Dec 20 18:15:46 tryhackme sudo[648]: Merry Christmas
            Dec 20 18:15:44 tryhackme sudo[583]:     root : TTY=unknown ; PWD=/ ; USER=root ; COMMAND=/etc/systemd/system/a service
            Dec 20 18:15:44 tryhackme sudo[583]: pam_unix(sudo:session): session opened for user root by (uid=0)
            Dec 20 18:15:44 tryhackme systemd[1]: Started Unkillable exe.
            Dec 20 18:27:47 tryhackme sudo[1986]: Merry Christmas
            Dec 20 18:41:09 tryhackme systemd[1]: Stopping Unkillable exe...
            Dec 20 18:41:09 tryhackme sudo[583]: pam_unix(sudo:session): session closed for user root
            Dec 20 18:41:09 tryhackme systemd[1]: a-unkillable.service: Succeeded.
            Dec 20 18:41:09 tryhackme systemd[1]: Stopped Unkillable exe.
         ```

         1. So we see that the service is still loaded on the system so we need to remove that.
   6. Delete the service and process
      1. > rm -rf /etc/systemd/system/a
      2. > rm -rf /etc/systemd/system/a-unkillable.service
8. RELOAD
   1. Finally lets reload all service configurations to make sure it is gone!
      1. > systemctl daemon-reload


## QUESTIONS

1. What is the name of the service that respawns the process after killing it?
   1. `a-unkillable.service`
2. What is the path from where the process and service were running?
   1. `/etc/systemd/system`
3. The malware prints a taunting message. When is the message shown? Choose from the options below.
   1. Randomly
   2. After a set interval
   3. On process termination
   4. None of the above
   5. `4` - because it says `Merry Christmas`