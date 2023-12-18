# Day_16 [Machine-Learning] Can't CAPTCHA this Machine!

+ Deployable Machine: Yes

Description: McGreedy has locked McSkidy out of his Elf(TM) HQ admin panel by changing the password! To make it harder for McSkidy to perform a hack-back, McGreedy has altered the admin panel login so that it uses a CAPTCHA to prevent automated attacks. A CAPTCHA is a small test, like providing the numbers in an image, that needs to be performed to ensure that you are a human. This means McSkidy can’t perform a brute force attack. Or does it? After the great success of using machine learning to detect defective toys and phishing emails, McSkidy is looking to you to help him build a custom brute force script that will make use of ML to solve the CAPTCHA and continue with the brute force attack. There is, however, a bit of irony in having a machine solve a challenge specifically designed to tell humans apart from computers.

> IP: [10.10.255.217]

## LEARNING OBJECTIVES

1. Complex neural network structures
2. How does a convolutional neural networks function?
3. Using neural networks for optical character recognition
4. Integrating neural networks into red team tooling

## OVERVIEW

1. Convolutional Neural Networks
   1. In essence, CNNs are normal neural networks that simply have the feature-extraction process as part of the network itself. This time, we’re not just using maths but combining it with linear algebra. Again, we won’t dive too deep into the maths here to keep things simple.
   2. Can be broken into 3 main categories
      1. Feature extraction
      2. Fully connected layers
      3. Classification

2. In order to crack CAPTCHAs, we will have to go through the following steps:
   1. Gather CAPTCHAs so we can create labelled data
   2. Label the CAPTCHAs to use in a supervised learning model
   3. Train our CAPTCHA-cracking CNN
   4. Verify and test our CAPTCHA-cracking CNN
   5. Export and host the trained model so we can feed it CAPTCHAs to solve
   6. Create and execute a brute force script that will receive the CAPTCHA, pass it on to be solved, and then run the brute force attack

## STEPS

1. Deploy Machine
2. Show Split Pane
3. Start Docker Container
   1. > docker run -d -v /tmp/data:/tempdir/ aocr/full
4. Get Containers ID
   1. > docker ps
      1. ID -> 1f728dc73b92
5. Execute
   1. > docker exec -it 1f728dc73b92 /bin/bash
   2. We are now connected to the container
6. Navigate to OCR
   1. > cd /ocr/
7. Open HQAdmin webportal on VM
   1. [http://hqadmin.thm:8000]
8. Lets get the CAPTCHA image from the login page
   1. > curl http://hqadmin.thm:8000/
   2. In here we see the base64 for the image, luckily there is already a script that grabs this for us
   3. > ls -alh raw_data/dataset/
9. Convert our training text file into TensorFlow
   1. > aocr dataset ./labels/training.txt ./training.tfrecords
10. TRAINING & TESTING
    1. Navigate to the "labels" folder as it has our tensorflow data for training and testing
       1. > cd /labels
    2. Run training
       1. > aocr train training.tfrecords
    3. Run testing
       1. > aocr test testing.tfrecords
       2. After a few steps lets look

         ```text
            2023-12-18 23:01:26,910 root  INFO     Step 1 (0.292s). Accuracy: 100.00%, loss: 0.000108, perplexity: 1.00011, probability: 99.93% 100% (33702)
            2023-12-18 23:01:26,993 root  INFO     Step 2 (0.079s). Accuracy: 100.00%, loss: 0.000246, perplexity: 1.00025, probability: 99.85% 100% (40760)
         ```

11. Now we need to host our CNN to send it CAPTCHA's through the bruteforce script
    1. > cd /ocr/ && cp -r model /tempdir/
12. Exit out and kill the original container
    1. > exit
13. TensorFlow serve will run docker now
    1. > docker run -t --rm -p 8501:8501 -v /tmp/data/model/exported-model:/models/ -e MODEL_NAME=ocr tensorflow/serving
    2. We can access this through [http://localhost:8501/v1/models/ocr/]
14. BRUTE-FORCE
    1. Run the python bruteforcer from the desktop
       1. > cd ~/Desktop/bruteforcer && python3 bruteforce.py
          1. RESPONSE: `[+] Access Granted!! -- Username: admin Password: ReallyNotGonnaGuessThis`
15. SIGN-IN
    1. Now lets go back to the hqadmin and log in
       1. Access Granted.... Flag: `THM{Captcha.Can't.Hold.Me.Back}`


## QUESTIONS

1. What key process of training a neural network is taken care of by using a CNN?
   1. `Feature Extraction`
2. What is the name of the process used in the CNN to extract the features?
   1. `Convolution`
3. What is the name of the process used to reduce the features down?
   1. `Pooling`
4. What off-the-shelf CNN did we use to train a CAPTCHA-cracking OCR model?
   1. `Attention OCR`
5. What is the password that McGreedy set on the HQ Admin portal?
   1. `ReallyNotGonnaGuessThis`
6. What is the value of the flag that you receive when you successfully authenticate to the HQ Admin portal?
   1. `THM{Captcha.Can't.Hold.Me.Back}`