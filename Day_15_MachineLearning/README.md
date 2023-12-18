# Day_15 [Machine-Learning] Jingle Bell SPAM: Machine Learning Saves the Day!

+ Deployable Machine: Yes

Description: Over the past few weeks, Best Festival Company employees have been receiving an excessive number of spam emails. These emails are trying to lure users into the trap of clicking on links and providing credentials. Spam emails are somehow ending up in the mailing box. It looks like the spam detector in place since before the merger has been disabled/damaged deliberately. Suspicion is on McGreedy, who is not so happy with the merger. McSkidy has been tasked with building a spam email detector using Machine Learning (ML). She has been provided with a sample dataset collected from different sources to train the Machine Learning model.

> IP: [10.10.255.217]

## LEARNING OBJECTIVES

1. Different steps in a generic Machine Learning pipeline
2. Machine Learning classification and training models
3. How to split the dataset into training and testing data
4. How to prepare the Machine Learning model
5. How to evaluate the model's effectiveness

## OVERVIEW

1. Machine Learning Pipeline
   1. A Machine Learning pipeline refers to the series of steps involved in building and deploying an ML model. These steps ensure that data flows efficiently from its raw form to predictions and insights.
   2. A typical pipeline would include collecting data from different sources in different forms, preprocessing it and performing feature extraction from the data, splitting the data into testing and training data, and then applying Machine Learning models and predictions.

## STEPS

1. Deploy Machine
2. Download Script and Data sets
   1. > wget IP_ADDR:9999/emails_dataset.py
   2. > wget IP_ADDR:9999/test_emails.csv
   3. > wget IP_ADDR:9999/spam_detector.ipynb
3. JUPITER NOTEBOOK (Interactive python)
   1. Import Libraries
   2. Data Collection
   3. Data Preprocessing
   4. Train/Test Split dataset
   5. Model Training
   6. Model Evaluation
   7. Testing the Model

## QUESTIONS

1. What is the key first step in the Machine Learning pipeline?
   1. `Data Collection`
2. Which data preprocessing feature is used to create new features or modify existing ones to improve model performance?
   1. `Feature Engineering`
3. During the data splitting step, 20% of the dataset was split for testing. What is the percentage weightage avg of precision of spam detection?
   1. `0.98`
4. How many of the test emails are marked as spam?
   1. `3`
5. One of the emails that is detected as spam contains a secret code. What is the code?
   1. `I_HaTe_BesT_FestiVal`