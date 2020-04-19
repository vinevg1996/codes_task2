#!/usr/bin/python
from discrete_source import DiscreteSource

import sys
import json
import random

#q = 14
#R = 0.9
#delta = 0.3

#python3 task2.py json_files/single_coin.json 0.9 13 0.3 STAT

# Pr(x = 0) = 0.8952380952380953
# Pr(x = 1) = 0.10476190476190472

discreteSource = DiscreteSource(sys.argv)
#HighProbSet = discreteSource.CreateHighProbabilitySet(q, R, delta)
#prob = discreteSource.CheckProbabilityForSet(HighProbSet)
#print("len(HighProbSet) = ", len(HighProbSet))
#print("prob = ", prob)