# Day_17 [Traffic-Analysis] I Tawt I Taw A C2 Tat!

+ Deployable Machine: Yes

Description: Congratulations, you made it to Day 17! The story, however, is just getting started. There are more things to discover, examine, and analyse!  Until now, you have worked with multiple events, including prompt injection, log analysis, brute force, data recovery, exploitation, data exfiltration, suspicious drives, malware, injection, account takeover, phishing, and machine learning concepts. Yes, there are tons of anomalies, indicators of attack (IoA), and indicators of compromise (IoC). Santa's Security Operations Centre (SSOC) needs to see the big picture to identify, scope, prioritise, and evaluate these anomalies in order to manage the ongoing situation effectively. So, how can we zoom out a bit and create a timeline to set the investigation's initial boundaries and scope? McSkidy decides to focus on network statistics. When there are many network artefacts, it's a good choice to consider network in & out as well as load statistics to create a hypothesis. Now it's time to help the SSOC team by quickly checking network traffic statistics to gain insight into the ongoing madness! Let's go!

> IP: [10.10.140.110]

## LEARNING OBJECTIVES

1. Gain knowledge of the network traffic data format
2. Understand the differences between full packet captures and network flows
3. Learn how to process network flow data
4. Discover the SiLK tool suite
5. Gain hands-on experience in network flow analysis with SiLK

## OVERVIEW

1. PCAP vs FLOW
   1. PCAP
      1. Model -> Packet capture
      2. Depth of Information -> Detailed granular data. Contains the packet details and payload
      3. Main Purpose -> Deep packet analytics
      4. Pros -> Provides high visibility of packet details
      5. Cons -> Hard to process, and requires time and resources to store and analyse. Encryption is an obstacle
      6. Available Fields -> Layer headers and payload data
   2. FLOW
      1. Model -> Protocol flow records
      2. Depth of Information -> Summary data. Doesn't contain the packet details and payload
      3. Main Purpose -> Summary of the traffic flow
      4. Pros -> Provides a high-level summary of the big picture. Encryption is not an obstacle (the flows don't use the packet payload)
      5. Cons -> Summary only; no payload
      6. Available Fields -> Packet metadata

2. Key data fields of PCAP format
   1. Link layer information
   2. Timestamp
   3. Packet length
   4. MAC addresses
      1. Source and destination MACs
   5. IP and port information
      1. Source and destination IP addresses
      2. Source and destination ports
   6. TCP/UDP information
   7. Application layer protocol details
   8. Packet data and payload

3. Key data fields of FLOW format
   1. IP and port information
      1. Source and destination IP addresses
      2. Source and destination ports
   2. IP protocol
   3. Volume details in byte and packet metrics
   4. TCP flags
   5. Time details
      1. Start time
      2. Duration
      3. End time
   6. Sensor info
   7. Application layer protocol information

## STEPS

1. Deploy Machine
2. Open Split Pane
3. SiLK Suite
   1. Find version
      1. > silk_config -v
         1. SiLK 3.19.1
   
   2. Flow File Properties with SilK Suite: **rwfileinfo**
      1. > rwfileinfo suspicious-flows.silk

         ```text
            suspicious-flows.silk:
            format(id)          FT_RWIPV6ROUTING(0x0c)
            version             16
            byte-order          littleEndian
            compression(id)     lzo1x(2)
            header-length       88
            record-length       88
            record-version      1
            silk-version        3.19.1
            count-records       11774
            file-size           152366
            command-lines       1  rwipfix2silk --silk-output=test.silk
         ```

   3. Reading Flow Files: **rwcut**
      1. > rwcut suspicious-flows.silk
      2. Fields we can cut on:
         1. Source IP: sIP
         2. Destination IP: dIP
         3. Source port: sPort
         4. Destination port: dPort
         5. Duration: duration
         6. Start time: sTime
         7. End time: eTime
      3. Get Time of 6th record
         1. > rwcut suspicious-flows.silk --fields=sTime --num-recs=6

            ```text
                                 sTime|
               2023/12/05T09:33:07.719|
               2023/12/05T09:33:07.725|
               2023/12/05T09:33:07.738|
               2023/12/05T09:33:07.741|
               2023/12/05T09:33:07.743|
               2023/12/05T09:33:07.755|
            ```

            1. The 6th one is `2023/12/05T09:33:07.755`

   4. Filtering the Event of Interest: **rwfilter**
      1. > rwfilter suspicious-flows.silk --proto=[VALUE_HERE]
      2. Need sPort of 6th UDP packet
         1. UDP is --proto=17
      3. > rwfilter suspicious-flows.silk --proto=17 --pass=stdout | rwcut --fields=dPort --num-recs=6

         ```text
            dPort|
               53|
            59580|
               53|
            47888|
               53|
            49950|
         ```

         1. The 6th UDP packet has dPort of `49950`

   5. Quick Statistics: **rwstats**
      1. > rwstats suspicious-flows.silk --fields=[FIELDS] --values=[VALUES]
      2. Lets get the % of dPort 53
         1. > rwstats suspicious-flows.silk --fields=dPort --values=records --count=10

            ```text
               dPort|   Records|  %Records|   cumul_%|
                  53|      4160| 35.332088| 35.332088|
                  80|      1658| 14.081875| 49.413963|
               40557|         4|  0.033973| 49.447936|
               53176|         3|  0.025480| 49.473416|
               50088|         3|  0.025480| 49.498896|
               50258|         3|  0.025480| 49.524376|
               52345|         3|  0.025480| 49.549856|
               47920|         3|  0.025480| 49.575335|
               50105|         3|  0.025480| 49.600815|
               52167|         3|  0.025480| 49.626295|
            ```

            1. dPort 53 has 35.332088%
      3. Lets take a look at the bytes value
         1. > rwstats suspicious-flows.silk --fields=sIP --values=bytes --count=9 --top

            ```text
                           sIP|               Bytes|    %Bytes|   cumul_%|
               175.219.238.243|              735229| 52.048036| 52.048036|
               175.175.173.221|              460731| 32.615884| 84.663920|
               175.215.235.223|              145948| 10.331892| 94.995813|
               175.215.236.223|               66320|  4.694899| 99.690712|
                181.209.166.99|                2744|  0.194252| 99.884964|
                253.254.236.39|                1380|  0.097692| 99.982656|
                205.213.108.99|                 152|  0.010760| 99.993416|
            ```

            1. In here we can see the byte value for the (top talker) = `735229` bytes
      4. Lets look into the communication of the top talkers
         1. > rwfilter suspicious-flows.silk --saddress=175.175.173.221 --dport=53 --pass=stdout | rwcut --fields=sIP,dIP,stime | head -10

            ```text
                           sIP|                                    dIP|                  sTime|
               175.175.173.221|                        175.219.238.243|2023/12/08T04:28:44.825|
               175.175.173.221|                        175.219.238.243|2023/12/08T04:28:45.678|
               175.175.173.221|                        175.219.238.243|2023/12/08T04:28:45.833|
               175.175.173.221|                        175.219.238.243|2023/12/08T04:28:46.743|
               175.175.173.221|                        175.219.238.243|2023/12/08T04:28:46.898|
               175.175.173.221|                        175.219.238.243|2023/12/08T04:28:47.753|
               175.175.173.221|                        175.219.238.243|2023/12/08T04:28:47.903|
               175.175.173.221|                        175.219.238.243|2023/12/08T04:28:48.764|
               175.175.173.221|                        175.219.238.243|2023/12/08T04:28:48.967|
            ```

            1. In here we see that there are 10 DNS connections withing 1 second - that is sketchy!
            2. In here we see the first sTime is `2023/12/08T04:28:44.825`
            3. We can check that 175.175.173.221 is the sender by looking at the other side 175.219.238.243
               1. > rwfilter suspicious-flows.silk --saddress=175.219.238.243 --dport=53 --pass=stdout | rwcut --fields=sIP,dIP,stime | head -10
                  1. 0 results, therefor no packets were sent from this IP
            4. This helps us determine that this is potenially a C2 -> `175[.]175[.]173[.]221`
      5. Lets look deeper into the C2 potential
         1. Remembering back to our quick stats we saw there was quite a few records, so lets look at the communications on this port
            1. > rwfilter suspicious-flows.silk --aport=80 --pass=stdout | rwstats --fields=sIP,dIP --count=10

               ```text
                              sIP|                                    dIP|   Records|  %Records|   cumul_%|
                  175.215.235.223|                        175.215.236.223|      1781| 51.788311| 51.788311|
                  175.215.236.223|                        175.215.235.223|      1658| 48.211689|100.000000|
               ```

               1. This shows the connection pairs that made all the noise
         2. Since we see the connection pairs lets look at the destination port to see where the load is at
            1. > rwfilter suspicious-flows.silk --aport=80 --pass=stdout | rwstats --fields=sIP,dIP,dPort --count=10

               ```text
                              sIP|                                    dIP|dPort|   Records|  %Records|   cumul_%|
                  175.215.236.223|                        175.215.235.223|   80|      1658| 48.211689| 48.211689|
                  175.215.235.223|                        175.215.236.223| 3290|         1|  0.029078| 48.240768|
                  175.215.235.223|                        175.215.236.223| 4157|         1|  0.029078| 48.269846|
                  175.215.235.223|                        175.215.236.223| 4871|         1|  0.029078| 48.298924|
                  175.215.235.223|                        175.215.236.223| 4515|         1|  0.029078| 48.328002|
                  175.215.235.223|                        175.215.236.223| 4629|         1|  0.029078| 48.357081|
                  175.215.235.223|                        175.215.236.223| 4138|         1|  0.029078| 48.386159|
                  175.215.235.223|                        175.215.236.223| 4765|         1|  0.029078| 48.415237|
                  175.215.235.223|                        175.215.236.223| 4020|         1|  0.029078| 48.444315|
                  175.215.235.223|                        175.215.236.223| 3248|         1|  0.029078| 48.473393|
               ```

               1. This shows us all the addresses that used port 80
               2. In here we see the reoccuring IP address making all the noise IP = `175[.]215[.]236[.]223`
         3. Now lets look at the frequency and flags
            1. > rwfilter suspicious-flows.silk --saddress=175.215.236.223 --pass=stdout | rwcut --fields=sIP,dIP,dPort,flag,stime | head

               ```text
                              sIP|                                    dIP|dPort|   flags|                  sTime|
                  175.215.236.223|                        175.215.235.223|   80| S      |2023/12/05T09:33:07.723|
                  175.215.236.223|                        175.215.235.223|   80| S      |2023/12/05T09:33:07.732|
                  175.215.236.223|                        175.215.235.223|   80| S      |2023/12/05T09:33:07.748|
                  175.215.236.223|                        175.215.235.223|   80| S      |2023/12/05T09:33:07.740|
                  175.215.236.223|                        175.215.235.223|   80| S      |2023/12/05T09:33:07.715|
                  175.215.236.223|                        175.215.235.223|   80| S      |2023/12/05T09:33:07.774|
                  175.215.236.223|                        175.215.235.223|   80| S      |2023/12/05T09:33:07.757|
                  175.215.236.223|                        175.215.235.223|   80| S      |2023/12/05T09:33:07.765|
                  175.215.236.223|                        175.215.235.223|   80| S      |2023/12/05T09:33:07.782|
               ```

               1. In here we see that SYN packets are being sent - and quite fast
         4. Now lets look specifically at ALL packets sent by this host
            1. > rwfilter suspicious-flows.silk --saddress=175.215.236.223 --pass=stdout | rwstats --fields=sIP,flag,dIP --count=10

               ```text
                              sIP|   flags|                                    dIP|   Records|  %Records|   cumul_%|
                  175.215.236.223| S      |                        175.215.235.223|      1658|100.000000|100.000000|
               ```

               1. In here we see a total of `1658` SYN records
               2. But even stragner, there are 0 ACK records
               3. So lets look at the destination
         5. Examin the destination port
            1. > rwfilter suspicious-flows.silk --saddress=175.215.235.223 --pass=stdout | rwstats --fields=sIP,flag,dIP --count=10

               ```text
                              sIP|   flags|                                    dIP|   Records|  %Records|   cumul_%|
                  175.215.235.223| S  A   |                        175.215.236.223|      1781|100.000000|100.000000|
               ```

               1. In here we see the destination port sends SYN-ACK to complete the threeway handshake. BUT!!! The source address only sends SYN, but there should be an ACK resposne to technically complete the handsahke, so this is very suspicious!!


## QUESTIONS

1. Which version of SiLK is installed on the VM?
   1. `3.19.1`
2. What is the size of the flows in the count records?
   1. `11774`
3. What is the start time (sTime) of the sixth record in the file?
   1. `2023/12/05T09:33:07.755`
4. What is the destination port of the sixth UDP record?
   1. `49950`
5. What is the record value (%) of the dport 53?
   1. `35.332088`
6. What is the number of bytes transmitted by the top talker on the network?
   1. `735229`
7. What is the sTime value of the first DNS record going to port 53?
   1. `2023/12/08T04:28:44.825`
8. What is the IP address of the host that the C2 potentially controls? (In defanged format: 123[.]456[.]789[.]0 )
   1. `175[.]175[.]173[.]221`
9.  Which IP address is suspected to be the flood attacker? (In defanged format: 123[.]456[.]789[.]0 )
   1. `175[.]215[.]236[.]223`
10. What is the sent SYN packet's number of records?
    1. `1658`