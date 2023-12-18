# Day_14 [Machine-Learning] The Little Machine That Wanted to Learn

+ Deployable Machine: Yes

Description: The CTO has made our toy pipeline go wrong. By infecting elves at key positions in the toy-making process, he has poisoned the pipeline and caused the elves to make defective toys! McSkidy has started to combat the problem by placing control elves in the pipeline. These elves take measurements of the toys to try and narrow down the exact location of problematic elves in the pipeline by comparing the measurements of defective and perfect toys. However, this is an incredibly tedious and lengthy process, so he's looking to use machine learning to optimise it.

> IP: [10.10.84.88]

## LEARNING OBJECTIVES

1. What is machine learning?
2. Basic machine learning structures and algorithms
3. Using neural networks to predict defective toys

## OVERVIEW

1. ML refers to the process used to create a system that can mimic the behaviour we see in real life. Some examples are:
   1. Genetic algorithm: This ML structure aims to mimic the process of natural selection and evolution. By using rounds of offspring and mutations based on the criteria provided, the structure aims to create the "strongest children" through "survival of the fittest".
   2. Particle swarm: This ML structure aims to mimic the process of how birds flock and group together at specific points. By creating a swarm of particles, the structure aims to move all the particles to the optimal answer's grouping point.
   3. Neural networks: This ML structure is by far the most popular and aims to mimic the process of how neurons work in the brain. These neurons receive various inputs that are then transformed before being sent to the next neuron. These neurons can then be "trained" to perform the correct transformations to provide the correct final answer.

2. Learning Styles
   1. First on our list of ML basics to cover is the neural network's learning style. In order to train our neural network, we need to decide how we'll teach it. While there are many different styles and subsets of styles, we will only focus on the two main styles for now:
      1. Supervised learning: In this learning style, we guide the neural network to the answers we want it to provide. We ask the neural network to give us an answer and then provide it with feedback on how close it was to the correct answer. In this way, we are supervising the neural network as it learns. However, to use this learning style, we need a dataset where we know the correct answers. This is called a labelled dataset, as we have a label for what the correct answer should be, given the input.
      2. Unsupervised learning: In this learning style, we take a bit more of a hands-off approach and let the neural network do its own thing. While this sounds very strange, the main goal is to have the neural network identify "interesting things". Humans are quite good at most classification tasks – for example, simply looking at an image and being able to tell what colour it is. But if someone were to ask you, "Why is it that colour?" you would have a hard time explaining the reason. Humans can see up to three dimensions, whereas neural networks have the ability to work in far greater dimensions to see patterns. Unsupervised learning is often used to allow neural networks to learn interesting features that humans can't comprehend that can be used for classification. A very popular example of this is the restricted Boltzmann machine. Have a look here at the weird features the neural network learned to classify different digits.

3. Basic Structure
   1. Next on our list of ML basics to learn is the basic structure of a neural network. Sticking to the very basics of ML, a neural network consists of various different nodes (neurons) that are connected and has 3 main layers
      1. Input layer: This is the first layer of nodes in the neural network. These nodes each receive a single data input that is then passed on to the hidden layer. This means that the number of nodes in this layer always matches the network's number of inputs (or data parameters). For example, if our network takes the toy's length, width, and height, there will be three nodes in the input layer.
      2. Output layer: This is the last layer of nodes in the neural network. These nodes send the output from the network once it has been received from the hidden layer. Therefore, the number of nodes in this layer will always be the same as the network's number of outputs. For example, if our network outputs whether or not the toy is defective, we will have one node in the output layer for either defective or not defective (we could also do it with two nodes, but we won't go into that here).
      3. Hidden layer: This is the layer of nodes between the neural network's input and output layers. With a simple neural network, this will only be one layer of nodes. However, for additional learning opportunities, we could add more layers to create a deep neural network. This layer is where the neural network's main action takes place. Each node within the neural network's hidden layer receives multiple inputs from the nodes in the previous layer and will then transmit their answers to multiple nodes in the next layer.
   2. As mentioned before, we will simplify the maths quite a bit here! In essence, the node is receiving inputs from nodes in the previous layer, adding them together and then sending the output on to the next layer of nodes. There is, however, a little bit more detail in this step that's important to note:
      1. Inputs are not directly added. Instead, they are multiplied by a weight value first. This helps the neural network decide which inputs should contribute more to the output than others.
      2. The addition's output is not directly transmitted out. Instead, the output is first entered into what is called an activation function. In essence, this decides if the neuron (node) will be active or not. It does this by ensuring that the output, no matter the input, will always be a decimal between 0 and 1 (or between −1 and 1).

4. Feed-Forward Loop
   1. The feed-forward loop is how we send data through the network and get an answer on the other side. Once our network has been trained, this is the only step we perform. At this point, we stop training and simply want an answer from the network. Here is how:
      1. Normalise all of the inputs: To allow our neural network to decide which inputs are most important in helping it to decide the answer, we need to normalise them. As mentioned before, each node in the network tries to keep its answer between 0 and 1. If we have one input with a range of 0 to 50 and another with a range of 0 to 2, our network won't be able to properly consume the input. Therefore, we normalise the inputs first by adjusting them so that their ranges are all the same. In our example here, we would take the inputs with a 0 to 50 range and divide all of them by 25 to change their ranges to 0 to 2.
      2. Feed the inputs to our nodes in the input layer: Once normalised, we can provide one data entry for each input node in our network.
      3. Propagate the data through the network: At each node, we add all the inputs and run them through the activation function to get the node's output. This output then becomes the input for the next layer of nodes. We repeat this process until we get to our network's output layer.
      4. Read the output from the network: At the output layer of the network, we receive the output from our nodes. The answer will be a decimal between 0 and 1, but, for decision-making, we'll round it to get a binary answer from each output node.

5. Back-Propagation
   1. When we are training our network, the feed-forward loop is only half of the process. Once we receive the answers from our network, we need to tell it how close it was to the correct answer. Here is how:
      1. Calculate the difference in received outputs vs expected outputs: As mentioned before, the activation function will provide a decimal answer between 0 and 1. Since we know that the answer has to be either 0 or 1, we can calculate the difference in the answer. This difference tells us how close the neural network was to the correct answer.
      2. Update the weights of the nodes: Using the difference calculated in the previous step, we can start to update the weights of each input to the nodes in the output layer. We won't dive too deep into this update process, as it often involves a bit of complex maths to decide what update should be made.
      3. Propagate the difference back to the other layers: This is where the term back-propagation comes from. Once the weights of the nodes in the output layer have been updated, we can calculate what the difference would be for the previous nodes. Once again, this difference is then used to update the weights of the nodes in that layer before being propagated backwards even more. We continue this process of back-propagation until the weights for the input layer have been updated.

6. Dataset Splits
   1. Overtraining is a big problem with neural networks. We are training them with data where we know the answers, so it's possible for the network to simply learn the answers, not how to calculate the answer. To combat this, we need to validate that our neural network is learning the process and not the answers. This validation also tells us when we need to stop our learning process. To perform this validation, we have to split our dataset into the three datasets below:
      1. Training data: This is our largest dataset. We use it to train the network. Usually, this is about 70–80% of the original dataset.
      2. Validation data: This dataset is used to validate the network's training. After each training round, we send this data through our network to determine its performance. If the performance starts to decline, we know we're starting to overtrain and should stop the process. Usually, this is about 10–15% of the original dataset.
      3. Testing data: This dataset is used to calculate the final performance of the network. The network won't see this data at all until we are done with the training process. Once training is complete, we send through the testing dataset to determine the performance of our network. Usually, this is about 10–15% of the original dataset.

## STEPS

1. Deploy Machine
2. Download the datasets and starter detector.py
   1. > wget IP:8888/detector.py
   2. > wget IP:8888/testing_dataset.csv
   3. > wget IP:8888/training_dataset.csv
3. BUILD PYTHON SCRIPT
   1. Create Datasets (80/20 split)
      1. train_X, validate_X, train_y, validate_y = train_test_split(X, y, test_size=0.2)
   2. Normalization of data
      1. scaler = StandardScaler()
      2. scaler.fit(train_X)
      3. train_X = scaler.transform(train_X)
      4. validate_X = scaler.transform(validate_X)
      5. test_X = scaler.transform(test_X)
   3. Training Neural Network 
      1. Classifier Code
         1. clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(15, 2), max_iter=10000)
      2. Classifier Training Code
         1. clf.fit(train_X, train_y)
      3. Classifier Validation
         1. y_predicted = clf.predict(validate_X)
      4. Classifier Testing Prediction
         1. y_test_predictions = clf.predict(test_X)
4. RUN CODE
   1. > python3 decoder.py
   2. Output is predticions.txt
5. UPLOAD
   1. Now lets upload our predections.txt file
   2. Navigate to [http://websiteforpredictions.thm:8000/]
   3. Upload file
   4. FLAG: `THM{Neural.Networks.are.Neat!}`

## QUESTIONS

1. What is the other term given for Artificial Intelligence or the subset of AI meant to teach computers how humans think or nature works?
   1. `Machine Learning`
2. What ML structure aims to mimic the process of natural selection and evolution?
   1. `Genetic Algorithm`
3. What is the name of the learning style that makes use of labelled data to train an ML structure?
   1. `Supervised learning`
4. What is the name of the layer between the Input and Output layers of a Neural Network?
   1. `Hidden Layer`
5. What is the name of the process used to provide feedback to the Neural Network on how close its prediction was?
   1. `Back-Propagation`
6. What is the value of the flag you received after achieving more than 90% accuracy on your submitted predictions?
   1. `THM{Neural.Networks.are.Neat!}`