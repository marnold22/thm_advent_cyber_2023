# Day_02 [Log-Analysis] O Data, All Ye Faithful

+ Deployable Machine: Yes
+ Website: Yes

Description: After yesterday’s resounding success, McHoneyBell walks into AntarctiCrafts’ office with a gleaming smile. She takes out her company-issued laptop from her knapsack and decides to check the news. “Traffic on the North-15 Highway? Glad I skied into work today,” she boasts. A notification from the Best Festival Company’s internal communication tool (HollyChat) pings. It’s another task. It reads, “The B-Team has been tasked with understanding the network of AntarctiCrafts’ South Pole site”. Taking a minute to think about the task ahead, McHoneyBell realises that AntarctiCrafts has no fancy technology that captures events on the network. “No tech? No problem!” exclaims McHoneyBell. She decides to open up her Python terminal…

> IP: [10.10.179.155]

## LEARNING OBJECTIVES

1. Get an introduction to what data science involves and how it can be applied in Cybersecurity
2. Get a gentle (We promise) introduction to Python
3. Get to work with some popular Python libraries such as Pandas and Matplotlib to crunch data
4. Help McHoneyBell establish an understanding of AntarctiCrafts’ network

## OVERVIEW

## NOTES

1. Data Science 101
   1. The core element of data science is interpreting data to answer questions. Data science often involves programming, statistics, and, recently, the use of Artificial Intelligence (AI) to examine large amounts of data to understand trends and patterns and help businesses make predictions that lead to informed decisions. The roles and responsibilities of a data scientist include:

## Exercise

1. Okay, great! We've learned how to process data using Pandas and Matplotlib. Continue onto the "Workbook.ipynb" Notebook located at 4_Capstone on the VM. Remember, everything you need to answer the questions below has been provided in the Notebooks on the VM. You will just need to account for the new dataset "network_traffic.csv".
2. Use python to examine data

## STEPS

1. Deploy Machine
2. Deplot Split-View
3. Copy "network_traffic.csv" to local machine
4. Create python script (see script.py in folder)
   1. Question 1
      1. Need packet count

         ```py
            df = pd.read_csv('network_traffic.csv')
            print(df.count())
         ```

         ```text
            PacketNumber    100
            Timestamp       100
            Source          100 
            Destination     100 
            Protocol        100
            dtype: int64
         ```

   2. Question 2
      1. Need max number if ip addresses

         ```py
            df= pd.read_csv('network_traffic.csv')
            print(df['Source'].value_counts())
         ```

         ```text
            10.10.1.4     15
            10.10.1.6     14
            10.10.1.3     13
            10.10.1.2     12
            10.10.1.9     11
            10.10.1.8      9
            10.10.1.10     8
            10.10.1.1      8
            10.10.1.7      5
            10.10.1.5      5
            Name: count, dtype: int64
         ```

   3. Question 3
      1. Need to find most frequent protocol

         ```py
            df = pd.read_csv('network_traffic.csv')
            print(df['Protocol'].value_counts())
         ```

         ```text
            Protocol 
            ICMP    27 
            DNS     25 
            HTTP    24 
            TCP     24
            Name: count, dtype: int64
         ```

## QUESTIONS

1. How many packets were captured (looking at the PacketNumber)?
   1. `100`
2. What IP address sent the most amount of traffic during the packet capture?
   1. `10.0.1.4`
3. What was the most frequent protocol?
   1. `ICMP`
