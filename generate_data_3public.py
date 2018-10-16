from judging import judging
import random
import numpy as np
from pyemd import emd

cards = []
    card = ["A","K","Q","J","T","9"]
    flower = ["c","d"]
    for i in card:
        for j in flower:
            cards.append([i+j])
    with open('data_1.csv','w') as f:
        for k in range(500):
            print(k)
            state = random.sample(cards, 7)
            hand = state[:2][0][0] + state[:2][1][0]
            public = state[2:7][0][0] + state[2:7][1][0] + state[2:7][2][0] + state[2:7][3][0] + state[2:7][4][0]
            cards_ = cards.copy()
            for i in state:
                cards_.remove(i)
            win_rate = [0]*3
            #print(win_rate)
            for i in range(100):
                opponent = random.sample(cards_,2)[0][0] + random.sample(cards_,2)[1][0]
                win_rate[judging(hand, opponent, public)] += 1/100

            f.write(str(win_rate[0])+ "," + str(win_rate[1])+ "," + str(win_rate[2])+ '\n')