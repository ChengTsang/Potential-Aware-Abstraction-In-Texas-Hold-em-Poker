from judging import judging
import random
import numpy as np
from pyemd import emd

centroids_2 = []
with open("centroids_2.csv") as file:
    for line in file:
      string_line = line.split(",")
      line_1,line_2,line_3,line_4,line_5 = float(string_line[0]), float(string_line[1]), float(string_line[2]), float(string_line[3]), float(string_line[4])
      centroid = [line_1, line_2, line_3, line_4, line_5]
      #print(dataPoint)
      centroids_2.append(centroid)
centroids = []
with open("centroids.csv") as file:
    for line in file:
      string_line = line.split(",")
      line_1,line_2,line_3 = float(string_line[0]), float(string_line[1]), float(string_line[2])
      centroid = [line_1, line_2, line_3]
      #print(dataPoint)
      centroids.append(centroid)

#card = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
#flower = ["c", "d", "h", "s"]
card = ["A", "K", "Q", "J", "T", "9"]
flower = ["c", "d"]
cards = []
for i in card:
    for j in flower:
        cards.append([i+j])
with open('data_3.csv','w') as f:
    for k in range(500):
        print(k)
        state = random.sample(cards, 5)
        hand = state[:2][0][0] + state[:2][1][0]
        public = state[2:5][0][0] + state[2:5][1][0] + state[2:5][2][0]
        cards_ = cards.copy()
        for i in state:
            cards_.remove(i)
        cha_2 = [0]*len(centroids_2)
        matrix_2 = np.array([[0, 1/5.0, 2/5.0, 3/5.0, 4/5.0], [1/5.0, 0, 1/5.0, 2/5.0, 3/5.0], [2/5.0, 1/5.0, 0 , 1/5, 2/5],[3/5,2/5,1/5,0,1/5],[4/5.0,3/5.0,2/5.0,1/5.0,0]])
        for j in range(7):
            public_4 = random.sample(cards_, 1)[0]
            public_4_ = public_4[0]
            public_ = public + public_4_
            cards__ = cards_.copy()
            cards__.remove(public_4)
            cha = [0] * len(centroids)
            matrix = np.array([[0, 1 / 3.0, 2 / 3.0], [1 / 3.0, 0, 1 / 3.0], [2 / 3.0, 1 / 3.0, 0]])
            for i in range(6):
                public_5 = random.sample(cards__,1)[0]
                public_5_ = public_5[0]
                public__ = public_ + public_5_
                cards___ = cards__.copy()
                cards___.remove(public_5)
                win_rate = [0] * 3
                for _ in range(100):
                    opponent = random.sample(cards___,2)[0][0] + random.sample(cards___,2)[1][0]
                    win_rate[judging(hand, opponent, public__)] += 1/100
                min_distance_index = 0
                min_distance = 10000
                for i in range(len(centroids)):
                    distance = emd(np.array(win_rate), np.array(centroids[i]), matrix)
                    if distance < min_distance :
                        #print(i)
                        min_distance_index = i
                        min_distance = distance
                cha[min_distance_index] += 1.0
            min_distance_index = 0
            min_distance = 10000
            print(cha)
            print(centroids_2[i])
            for i in range(len(centroids_2)):
                distance = emd(np.array(cha), np.array(centroids_2[i]), matrix_2)
                if distance < min_distance:
                    # print(i)
                    min_distance_index = i
                    min_distance = distance
            cha_2[min_distance_index] += 1
                #print(cha)
        to_str = ''
        for i in cha_2:
            to_str = to_str + str(i) + ','
        f.write(to_str + '\n')