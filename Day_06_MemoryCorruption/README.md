# Day_06 [Memory-Corruption] Memories of Christmas Past

+ Deployable Machine: Yes

Description: Throughout the merger, we have detected some worrying coding practices from the South Pole elves. To ensure their code is up to our standards, some Frostlings from the South Pole will undergo a quick training session about memory corruption vulnerabilities, all courtesy of the B team. Welcome to the training!

> IP: [10.10.90.33]

## LEARNING OBJECTIVES

1. Understand how specific languages may not handle memory safely.
2. Understand how variables might overflow into adjacent memory and corrupt it.
3. Exploit a simple buffer overflow to directly change memory you are not supposed to access.

## OVERVIEW

1. Memory Corruption
   1. Remember that whenever we execute a program (this game included), all data will be processed somehow through the computer's RAM (random access memory). In this videogame, your coin count, inventory, position, movement speed, and direction are all stored somewhere in the memory and updated as needed as the game goes on.
2. Debug
   1. ASCII view: The memory contents will be shown in ASCII encoding. It is useful when trying to read data stored as strings.
   2. HEX view: The memory contents will be shown in HEX. This is useful for cases where the data you are trying to monitor is a raw number or other data that can't be represented as ASCII strings.

## CHALLENGE

1. Investigating the "scroogerocks!" Case
   1. Armed with the debugging panel, McHoneyBell starts the lesson. As a first step, she asks you to restart your game (refreshing the website should work) and open the debug interface in HEX mode. The Frostlings have labelled each of the variables stored in memory, making it easy to trace them.
   2. Van TwinkleMcHoneyBell wants you to focus your attention on the coins variable. Go to the computer and generate a coin. As expected, you should see the coin count increase in the user interface and the debug panel simultaneously. We now know where the coin count is stored.
   3. McHoneyBell then points out that right before the coins memory space, we have the player_name variable. She also notes that the player_name variable only has room to accommodate 12 bytes of information.
   4. "But why does this matter at all?" asks a confused Van Twinkle. "Because if you try to change your name to scroogerocks!, you would be using 13 characters, which amounts to 13 bytes," replies McHoneyBell. Van Twinkle, still perplexed, interrupts: "So what would happen with that extra byte at the end?" McHoneyBell says: "It will overflow to the first byte of the coins variable."
   5. To prove this point, McHoneyBell proposes replicating the same experiment, but this time, we will get 13 coins and change our names to aaaabbbbccccx. Meanwhile, we'll keep our eyes on the debug panel. Let's try this in our game and see what happens.
   6. All of a sudden, we have 120 coins! The memory space of the coins variable now holds 78.

## STEPS

1. Deploy Machine
2. Navigate to webiste
   1. It looks to be a game where we can 
      1. Get coins from the computer
      2. Purchase items
      3. Change your name
      4. Debugger
         1. This allows you to see the memory aaddress values
3. BUFFER OVERFLOW
   1. We need to get enough coins from the computer to be able to change our name
      1. Press `space` on computer till "PC-Broken"  = 16 coins
   2. Take coins to change name
      1. Change name to `AAAABBBBCCCCDEFG`
         1. This fills the first 12 bytes and then the last 4 are overwritten with `DEFG` which are our "COINS"
         2. Now looking at the debug panel we have `44 45 46 47` in our coin memory address which means our coins are = `1195787588`
         3. Now we have enought to get the star
   3. Purchase star
      1. Talk to the store and enter ItemID `d`
      2. We are told that it was "impossible to win" and are given a nutcracker instead and it is added to our inventory
   4. Interact with tree
      1. Still says we don't have the star
   5. INVENTORY
      1. So lets go back and change our name so we overflow the INVENTORY memory addresses
      2. To overflow the inventory we need to fill 60 bytes worth of memory slots, but the last 16 need to be `abcdef1234567890` that way we hit one of each value for the inventory
      3. So the first 44 are "A"'s and then ABCDEF1234567890
      4. Change name to `AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAabcdef1234567890`
      5. SUCCESS! We now have one of everythng in the inventory
   6. TREE
      1. Press "space" to interact with the tree and get the flag
      2. FLAG: `THM{mchoneybell_is_the_real_star}`
4. MEMORY-IMAGE

   ```text
      player_name |41|41|41|41|
                  |42|42|42|42|
                  |43|43|43|43|
      coins       |4f|4f|50|53|
      shopk_name  |00|68|6f|70|
                  |6b|65|65|70|
                  |65|72|00|00|
   ```

   1. Need to decode `4f4f5053`, but because of little endian we need to input the values as `53504f4f` -> FROM HEX TO DECIMAL -> `1397772111`


## QUESTIONS

1. If the coins variable had the in-memory value in the image below, how many coins would you have in the game?
   1. `1397772111`
2. What is the value of the final flag?
   1. `THM{mchoneybell_is_the_real_star}`
