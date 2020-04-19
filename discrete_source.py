#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import os
import json
import random
import math

class DiscreteSource:
    data = {}
    coins_probability = {}
    entropy = 0
    info_disp = 0
    N = 0
    is_stat_process = False

    def __init__(self, argv):
        with open(argv[1], "r", encoding="utf-8") as read_file:
            self.data = json.load(read_file)    
        R = float(argv[2])
        q = float(argv[3])
        delta = float(argv[4])
        if (argv[5] == "STAT"):
            is_stat_process = True
            self.CalculateProbabilityForStationaryProcess()
            print("self.coins_probability:", self.coins_probability)
            self.entropy = self.CalculateEntropy()
            self.info_disp = self.CalculateInfoDispersion()
            print("entropy = ", self.entropy)
            print("info_disp = ", self.info_disp)
            HighProbSet = self.CreateHighProbabilitySet(q, R, delta)
            prob_ForHighProbSet = self.CheckProbabilityForSet(HighProbSet)
            print("prob_ForHighProbSet = ", prob_ForHighProbSet)
            out_file = open(argv[6], 'w')
            self.WriteToFile(out_file, HighProbSet, q)
        elif (argv[5] == "NO_STAT"):
            is_stat_process = False
            self.coins_probability['0'] = float(argv[7])
            self.coins_probability['1'] = float(argv[8])
            self.entropy = self.CalculateEntropy()
            self.info_disp = self.CalculateInfoDispersion()
            print("entropy = ", self.entropy)
            print("info_disp = ", self.info_disp)
            HighProbSet = self.CreateHighProbabilitySet(q, R, delta)
            prob_ForHighProbSet = self.CheckProbabilityForSet(HighProbSet)
            print("prob_ForHighProbSet = ", prob_ForHighProbSet)
            out_file = open(argv[6], 'w')
            self.WriteToFile(out_file, HighProbSet, q)
        return

    def WriteToFile(self, out_file, HighProbSet, q):
        #print("HighProbSet:", HighProbSet)
        #_______________________
        string = "{0:{fill" + "}" + "{0}b".format(str(int(q))) + "}"
        for j in range(0, len(HighProbSet)):
            dig_str = string.format(j, fill='0')
            out_file.write(HighProbSet[j])
            out_file.write(":  ")
            out_file.write(dig_str)
            out_file.write("\n")
        return

    def CalculateProbabilityForStationaryProcess(self): 
        coins_probability = {}
        results_dict = self.data['models']['монета_1'][0].keys()
        coins_dict = self.data['switches']['switch_0'][0].keys()
        for result in results_dict:
            coins_probability[result] = 0
            for curr_coin in coins_dict:
                Pr_choose_coin = float(self.data['switches']['switch_0'][0][curr_coin])
                Pr_result = float(self.data['models'][curr_coin][0][result])
                coins_probability[result] += Pr_choose_coin * Pr_result
        self.coins_probability = dict(coins_probability)
        return

    def CalculateEntropy(self):
        for prob in self.coins_probability.values():
            self.entropy += (-1) * prob * math.log2(prob)
        return self.entropy

    def CalculateInfoDispersion(self):
        info_sqr = 0.0
        for prob in self.coins_probability.values():
            math_prob = math.log2(prob) ** 2
            info_sqr += prob * math_prob
        self.info_disp = info_sqr - (self.entropy ** 2)
        return self.info_disp

    def CheckProbabilityForSet(self, HighProbSet):
        prob_sum = 0
        product = 1
        for string in HighProbSet:
            product = 1
            for sym in string:
                prob = self.coins_probability[sym]
                product = product * prob
            prob_sum += product
        #print("prob_sum = ", prob_sum)
        return prob_sum

    def CreateHighProbabilitySet(self, q, R, delta):
        if (R < self.entropy):
            print("Code does not exist: R < H")
            return
        a = (1.0 / ((R - self.entropy) ** 2)) * (self.info_disp / delta)
        n_min = int(a) + 1
        print("n_min = ", n_min)
        if (q <= n_min * self.entropy):
            print("Code does not exist: q <= n * H")
        is_find_code = False
        i = 0
        while not(is_find_code):
            n = n_min + i
            print("n = ", n)
            if (q < n * R):
                sqr_epsilon = float(self.info_disp) / float(n * delta)
                epsilon = math.sqrt(sqr_epsilon)
                print("epsilon = ", epsilon)
                HighProbSet = list()
                full_set = 2 ** n
                string = "{0:{fill" + "}" + "{0}b".format(str(n)) + "}"
                code_words = 0
                left_entropy = self.entropy - epsilon
                right_entropy = self.entropy + epsilon
                print("full_set = ", full_set)
                print("left_entropy = ", left_entropy)
                print("right_entropy = ", right_entropy)
                for j in range(0, full_set):
                    dig_str = string.format(j, fill='0')
                    info = self.CalculateInfo(dig_str)
                    average_info = float(info) / float(n)
                    if ((average_info >= left_entropy) and (average_info <= right_entropy)):
                        HighProbSet.append(str(dig_str))
                        code_words = code_words + 1
                if (code_words <= 2 ** q):
                    print("code_words = ", code_words)
                    print("len(HighProbSet) = ", len(HighProbSet))
                    is_find_code = True
            else:
                print("q < n * R")
            i = i + 1
        return HighProbSet

    def DebugCreateHighProbabilitySet(self, q, R, delta):
        if (R < self.entropy):
            print("Code does not exist: R < H")
            return
        a = (1.0 / ((R - self.entropy) ** 2)) * (self.info_disp / delta)
        n_min = int(a) + 1
        print("n_min = ", n_min)
        if (q <= n_min * self.entropy):
            print("Code does not exist: q <= n * H")
        is_find_code = False
        i = 0
        #while not(is_find_code):
        while (i < 2):
            print("i = ", i)
            n = n_min + i
            print("n = ", n)
            
            sqr_epsilon = float(self.info_disp) / float(n * delta)
            epsilon = math.sqrt(sqr_epsilon)
            print("epsilon = ", epsilon)
            HighProbSet = list()
            full_set = 2 ** n
            string = "{0:{fill" + "}" + "{0}b".format(str(n)) + "}"
            code_words = 0
            left_entropy = self.entropy - epsilon
            right_entropy = self.entropy + epsilon
            print("full_set = ", full_set)
            print("left_entropy = ", left_entropy)
            print("right_entropy = ", right_entropy)
            for j in range(0, full_set):
                dig_str = string.format(j, fill='0')
                info = self.CalculateInfo(dig_str)
                average_info = float(info) / float(n)
                if ((average_info >= left_entropy) and (average_info <= right_entropy)):
                    code_words = code_words + 1
                    HighProbSet.append(str(dig_str))
                    code_words = code_words + 1
            print("code_words = ", code_words)
            i = i + 1
        return HighProbSet

    def CalculateInfo(self, string):
        product = 1
        for sym in string:
            #prob = self.coins_probability[int(sym)]
            prob = self.coins_probability[sym]
            product = product * prob
        return (-1) * math.log2(product)

    def CreateHighProbabilitySetForCoding(self, q, R, delta):
        if (R < self.entropy):
            print("Code does not exist: R < entropy")
            return
        a = (1.0 / ((R - self.entropy) ** 2)) * (self.info_disp / delta)
        i = 1
        while True:
            n = int(a) + i
            lower_bound_q = n * self.entropy + math.sqrt((float(n) * self.info_disp) / delta)
            upper_bound_q = n * R
            if (int(upper_bound_q) >= lower_bound_q):
                new_q = int(lower_bound_q) + 1
                print("new_q = ", new_q)
                break
            i = i + 1
        print("lower_bound_q = ", lower_bound_q)
        print("upper_bound_q = ", upper_bound_q)
        print("n = ", n)
        sqr_epsilon = float(self.info_disp) / float(n * delta)
        epsilon = math.sqrt(sqr_epsilon)
        upper_bound_for_epsilon = ((float(new_q) / float(n)) - self.entropy)
        print("epsilon = ", epsilon)
        if (epsilon > upper_bound_for_epsilon):
            print("Code does not exist for this epsilon: epsilon > upper_bound_for_epsilon")
            return
        HighProbSet = list()
        full_set = 2 ** n
        #reg3_str = "{0:{fill}5b}".format(reg3, fill='0') 
        string = "{0:{fill" + "}" + "{0}b".format(str(n)) + "}"
        code_words = 0
        left_entropy = self.entropy - epsilon
        right_entropy = self.entropy + epsilon
        print("left_entropy = ", left_entropy)
        print("right_entropy = ", right_entropy)
        for i in range(0, full_set):
            if (i % 10000 == 0):
                print("i = ", i)
                print("code_words = ", code_words)
            dig_str = string.format(i, fill='0')
            #print("dig_str = ", dig_str)
            info = self.CalculateInfo(dig_str)
            average_info = float(info) / float(n)
            #print("average_info = ", average_info)
            if ((average_info >= left_entropy) and (average_info <= right_entropy)):
                code_words = code_words + 1
        return
