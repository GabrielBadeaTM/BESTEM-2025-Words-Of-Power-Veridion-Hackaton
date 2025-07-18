# 💥 **Veridion Words of Power Challenge**
Can You Outsmart the System?

Unleash the power of words in a high-stakes battle of strategy and wit!

This is a **text-based game** where **every word is a weapon** — and **every move has a price**.

Some forces are defeated with strength, others with cunning, speed, or even resilience.

**Choose wisely**, because your goal isn’t just to survive — it's to **spend the least** and **outsmart your opponent**.

# 🔮 Context

In 2025, I participated in a hackathon-style competition organized by BEST in collaboration with Veridion. The contest involved teams of 2 to 4 people, selected based on multiple challenges.

Attached above is our full solution for the contest, along with a separate folder containing the part I personally developed for the technical challenge. Although this part might not seem very complex at first glance, I invested time especially on the second problem, which was more demanding. More detailes are found there.

## 📑 The Task Summary

The task is to develop an ML-based program that, given a random input word, selects a word from a predefined list that can “defeat” the input word. The selection should prioritize the word that is both the most effective in winning against the input and the least costly in terms of resources or complexity.

## ✨ Our Approach

To solve the challenge, we started with a pre-trained word embedding database that represents words as vectors in a multidimensional space. For each word in the provided list of useful tools, we identified and defined a "direction" vector. This direction represents all the words that are considered to be "defeated" by that particular word in the game. 

When a random word is given as input, our method calculates which direction vector is closest to the input word’s vector in the embedding space. By finding this closest match, we determine the correct response or "winning" word according to the game rules. 

This approach allowed us to efficiently and accurately decide the outcome without relying on simple fixed rules, using the relationships captured in the word embeddings to model the game logic.

## 🤝 Team Members

- [Badea Catalin Gabriel](https://github.com/GabrielBadeaTM)
- [Constantin Cristiana Georgiana](https://github.com/bristiana)

## Note

Below is the detailed task description provided by the organizers.

# **🚀 The Challenge**

A game where:

1. The system provides a **word each round** (e.g., *Tornado, Hammer, Pandemic*).
2. The player must **choose a word** from a **predefined list** that "beats" the system's word.
3. Every word the player picks has a **cost ($)** — stronger words are more expensive.
4. If the player **fails to beat** the system’s word, they incur a **penalty**.
5. The game lasts **10 rounds**.
6. **Lowest total cost wins**, factoring in **win discounts** and **smart-play bonuses**!

---

## **🔍 How the Game Works**

1. **System generates a word** (e.g., *Flood*).
2. **Player selects a word** from the predefined list (e.g., *Drought*).
3. **The game checks** if the player's word “beats” the system’s word:
    - ✅ **Win**: Only the word’s cost is deducted.
    - ❌ **Loss**: The word’s cost + a penalty are deducted.
4. **Players play simultaneously** in each round.
5. **Repeat for 10 rounds**.
6. After 10 rounds, **final scores are calculated** with **special discounts and bonuses**.

---

## **📜 The Rules**

### **1️⃣ The Words**

- **System words** are randomly chosen from a secret list.
- **Player words** come from a **fixed 77-word list**, each with an associated cost.

### **2️⃣ Choosing a Word**

- Players can **only select from the predefined list**.
- Players **don’t know the system’s full word list**, so they must think strategically.

### **3️⃣ Winning & Losing a Round**

- A player’s word must **logically beat** the system’s word.
- If successful:
✅ The **word’s cost is deducted**, and the round continues.
- If unsuccessful:
❌ A **penalty fee** is deducted in addition to the word’s cost.

### **4️⃣ Game End & Scoring**

- **5% Discount per Round Won**:
After 10 rounds, you receive **5% off your total bill** for every round you won.
(e.g., win 7 rounds → 35% discount.)
- The **final score** = **total money spent** (cost of words + penalties).
- **Cheaper Win Bonus**:
If both players beat the system word, the **player who spent less** gets a **20% refund of their word's cost** for that round.
- **Final Score Formula**:

```python
Final Cost = ((Total Spent + 75 * Rounds Lost)  × (1 - (5% × Rounds Won))) - (Sum of Cheaper Win Refunds)
```

---

## **🎮 Example Game Playthrough**
Round | System Word | Player's Word | Word Cost ($) | Outcome | Total Cost ($)
1 | Candle | Fire | 22 | ✅ Wins | 22
2 | Hammer | Rock | 38 | ❌ Loses + $75 Penalty | 97
3 | Blueberries | Grizzly | 30 | ✅ Wins | 127
4 | Flood | Dam | 35 | ✅ Wins | 162
5 | Tank | H-bomb | 75 | ✅ Wins | 237

## **🎮 Example Game Playthrough**

| **Round** | **System Word** | **Player's Word** | **Word Cost ($)** | **Outcome** | **Total Cost ($)** |
| --- | --- | --- | --- | --- | --- |
| 1 | Candle | Fire | 22 | ✅ Wins | 22 |
| 2 | Hammer | Rock | 38 | ❌ Loses + $75 Penalty | 97 |
| 3 | Lion | Grizzly | 30 | ✅ Wins | 127 |
| 4 | Flood | Dam | 35 | ✅ Wins | 162 |
| 5 | Tank | H-bomb | 75 | ✅ Wins | 237 |

### **🏆 Strategy Tips**

- **Cheap words save money**, but may not always secure a win.
- **Powerful words are expensive**, but sometimes necessary to survive.
- **Abstract concepts** like *Persistence* or *Innovation* can outsmart bigger threats!
- **Efficiency is rewarded**:
    
    Winning **cheaply** is just as important as winning **frequently**.
    
- **Think ahead** — not every problem requires brute force.

## **✨ Bonus: Advanced Strategies**

- **Conservative players** win by being efficient and frugal.
- **Bullish players** dominate by winning big but risk spending too much money fast.
- **YOLO players**... well, they'll have fun anyway.

---

## **🛠️ What You Need to Build**

✔️ A way to make a **GET** request in order to get the words for each round

✔️ The logic that choses an adequate word to beat the system word (99% of work goes here)

✔️ A way to make a **POST** request with the **ID** of the chosen word

---

## **📖 Reference: Player Words, Costs & Penalties**

Below is the **full list of player words** along with their **cost ($)**. 
Use this as your reference when making strategic choices.

### **💰 Player Word List & Costs**

| **id** | **word** | **cost** |
| --- | --- | --- |
| 1 | Sandpaper | 8 |
| 2 | Oil | 10 |
| 3 | Steam | 15 |
| 4 | Acid | 16 |
| 5 | Gust | 18 |
| 6 | Boulder | 20 |
| 7 | Drill | 20 |
| 8 | Vacation | 20 |
| 9 | Fire | 22 |
| 10 | Drought | 24 |
| 11 | Water | 25 |
| 12 | Vacuum | 27 |
| 13 | Laser | 28 |
| 14 | Life Raft | 30 |
| 15 | Bear Trap | 32 |
| 16 | Hydraulic Jack | 33 |
| 17 | Diamond Cage | 35 |
| 18 | Dam | 35 |
| 19 | Sunshine | 35 |
| 20 | Mutation | 35 |
| 21 | Kevlar Vest | 38 |
| 22 | Jackhammer | 38 |
| 23 | Signal Jammer | 40 |
| 24 | Grizzly | 41 |
| 25 | Reinforced Steel Door | 42 |
| 26 | Bulldozer | 42 |
| 27 | Sonic Boom | 45 |
| 28 | Robot | 45 |
| 29 | Glacier | 45 |
| 30 | Love | 45 |
| 31 | Fire Blanket | 48 |
| 32 | Super Glue | 48 |
| 33 | Therapy | 48 |
| 34 | Disease | 50 |
| 35 | Fire Extinguisher | 50 |
| 36 | Satellite | 50 |
| 37 | Confidence | 50 |
| 38 | Absorption | 52 |
| 39 | Neutralizing Agent | 55 |
| 40 | Freeze | 55 |
| 41 | Encryption | 55 |
| 42 | Proof | 55 |
| 43 | Molotov Cocktail | 58 |
| 44 | Rainstorm | 58 |
| 45 | Viral Meme | 58 |
| 46 | War | 59 |
| 47 | Dynamite | 60 |
| 48 | Seismic Dampener | 60 |
| 49 | Propaganda | 60 |
| 50 | Explosion | 62 |
| 51 | Lightning | 65 |
| 52 | Evacuation | 65 |
| 53 | Flood | 67 |
| 54 | Lava | 68 |
| 55 | Reforestation | 70 |
| 56 | Avalanche | 72 |
| 57 | Earthquake | 74 |
| 58 | H-bomb | 75 |
| 59 | Dragon | 75 |
| 60 | Innovation | 75 |
| 61 | Hurricane | 76 |
| 62 | Tsunami | 78 |
| 63 | Persistence | 80 |
| 64 | Resilience | 85 |
| 65 | Terraforming Device | 89 |
| 66 | Anti-Virus Nanocloud | 90 |
| 67 | AI Kill Switch | 90 |
| 68 | Nanobot Swarm | 92 |
| 69 | Reality Resynchronizer | 92 |
| 70 | Cataclysm Containment Field | 92 |
| 71 | Solar Deflection Array | 93 |
| 72 | Planetary Evacuation Fleet | 94 |
| 73 | Antimatter Cannon | 95 |
| 74 | Planetary Defense Shield | 96 |
| 75 | Singularity Stabilizer | 97 |
| 76 | Orbital Laser | 98 |
| 77 | Time | 100 |

### **⚠️Penalties**

If the player's word **does not beat** the system word, they receive a **flat** **penalty fee** of `75$` in addition to the cost of their chosen word.

**Example:**

- If the **system word is "Rock"**, and the player **chooses "Fire" (cost $22)**, the word **doesn’t beat Rock** → they **spend $22 + incur a $75 penalty** = **$97 total spent**.

---

### **🧠 Strategy Reminders**

- **Cheap words help save money**, but may fail against strong system words, leading to **penalties**.
- **Expensive words are powerful**, but using them too much will drain money fast.
- **Balance risk & cost** to finish with the lowest total spending!

Use this reference to **make smart word choices and win the game**! 🚀
