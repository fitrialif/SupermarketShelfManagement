import sys
import os
import string
import random
import itertools
import copy

support = 0
basket_list = []
baskets = {}
actual_max_basket_size = 0
actual_itemsets_list = []
actual_temp = []
actual_itemsets_dict = {}
actual_item_list =[]
actual_item_count = {}
repeat = 0
iterations = 1
fraction = 0.6
frequents = []

with open(sys.argv[1]) as inputfile:
    for line in inputfile:
        line = line.strip('\n')
        line = line.split(',')
        basket_list.append(line)

for i in range(1, len(basket_list)+1):
    baskets[i] = basket_list[i-1]

support = int(sys.argv[2])

for basket in basket_list:
    if len(basket) > actual_max_basket_size:
        actual_max_basket_size = len(basket)

from itertools import combinations
for basket in basket_list:
    for i in range(1,len(basket)+1):
        actual_itemsets_list.append([",".join(map(str,comb)) for comb in combinations(sorted(basket), i)])

for each_list in actual_itemsets_list:
    for each_comb in each_list:
        actual_temp.append(each_comb.split(','))

for i in range(1, actual_max_basket_size+1):
    actual_itemsets_dict[i] = []

for basket in basket_list:
    for item in basket:
        actual_item_list.append(item)
        actual_item_count[item] = 0
    actual_item_list = list(set(actual_item_list))
    actual_item_list = sorted(actual_item_list)

for basket in basket_list:
    for item in basket:
        actual_item_count[item] += 1

for each_list in actual_temp:
    actual_itemsets_dict[len(each_list)].append(each_list)
#print actual_item_count
def toivonen():
    random_sample = []
    sample_max_basket_size = 0
    frequent_itemsets = {}
    candidate_itemsets = {}
    item_list = []
    item_count = {}
    singletons = []
    flag = 0
    negative_border = []
    random_numbers = []
    threshold = 0
    temp2 = []
    singletons_temp = []
    sample_itemsets_list = []
    sample_temp = []
    sample_itemsets_dict = {}
    candidates_temp = []
    temp1 = []
    real_candidates = []
    negative_border_temp = []
    global frequents
    frequents = []
    threshold = support * fraction * 0.8

    while len(random_numbers) != int(len(basket_list)*fraction):
        rNo = random.randint(1, len(basket_list))
        if rNo not in random_numbers:
            random_numbers.append(rNo)
    #print random_numbers

    for rNo in random_numbers:
        random_sample.append(baskets[rNo])
    #print random_sample

    for basket in random_sample:
        if len(basket) > sample_max_basket_size:
            sample_max_basket_size = len(basket)

    from itertools import combinations
    for basket in random_sample:
        for i in range(1,len(basket)+1):
            sample_itemsets_list.append([",".join(map(str,comb)) for comb in combinations(sorted(basket), i)])

    for each_list in sample_itemsets_list:
        for each_comb in each_list:
            sample_temp.append(each_comb.split(','))

    for i in range(1, sample_max_basket_size+1):
        sample_itemsets_dict[i] = []

    for each_list in sample_temp:
        sample_itemsets_dict[len(each_list)].append(each_list)

    for i in range(1, sample_max_basket_size+1):
        frequent_itemsets[i] = []
        candidate_itemsets[i] = []

    for basket in random_sample:
        for item in basket:
            item_list.append(item)
            item_count[item] = 0
    item_list = list(set(item_list))
    item_list = sorted(item_list)

    for basket in random_sample:
        for item in basket:
            item_count[item] += 1

    for item in item_count:
        if item_count[item] >= threshold:
            singletons_temp.append(item)

    for item in item_list:
        if item not in singletons_temp:
            extra = [item]
            negative_border.append(extra)

    for item in singletons_temp:
        if actual_item_count[item] >= support:
            singletons.append(item)

    for item in singletons:
        extra = [item]
        frequent_itemsets[1].append(extra)
        #frequents.append(extra)

    #print frequent_itemsets[1]
    #print negative_border

    if negative_border != []:
        for itemset in negative_border:
            for item in itemset:
                if actual_item_count[item] >= support:
                    flag = 1
                    return flag

    for i in range(2, sample_max_basket_size+1):
        temp1.append([",".join(map(str,comb)) for comb in combinations(sorted(singletons), i)])

    for each_list in temp1:
        for each_comb in each_list:
            temp2.append(each_comb.split(','))

    for each_list in temp2:
        candidate_itemsets[len(each_list)].append(each_list)

    #print sample_itemsets_dict

    for p in range(2, sample_max_basket_size+1):
        if p == 2:
            for itemset1 in candidate_itemsets[p]:
                count = 0
                for itemset2 in sample_itemsets_dict[p]:
                    if itemset1 == itemset2:
                        count += 1
                if count >= threshold:
                    candidates_temp.append(itemset1)

            #print candidates_temp

            for itemset in candidate_itemsets[p]:
                if itemset not in candidates_temp:
                    negative_border.append(itemset)

            #print negative_border

            for itemset1 in candidates_temp:
                count = 0
                for itemset2 in actual_itemsets_dict[p]:
                    if itemset1 == itemset2:
                        count += 1
                if count >= support:
                    frequent_itemsets[p].append(itemset1)

            #print frequent_itemsets[p]

            if negative_border != []:
                for itemset1 in negative_border:
                    count = 0
                    for itemset2 in actual_itemsets_dict[p]:
                        if itemset1 == itemset2:
                            count += 1
                    if count >= support:
                        flag = 1
                        return flag

        else:
            if frequent_itemsets[p-1] != []:
                for itemset in candidate_itemsets[p]:
                    immediate_subset = []
                    immediate_subset_temp = []
                    immediate_subset_temp.append([",".join(map(str,comb)) for comb in combinations(itemset, p-1)])

                    for each_list in immediate_subset_temp:
                        for each_comb in each_list:
                            immediate_subset.append(each_comb.split(','))

                    count = 0
                    for each_list in immediate_subset:
                        if each_list in frequent_itemsets[p-1]:
                            count += 1
                    if count == len(immediate_subset):
                        real_candidates.append(itemset)

                    real_candidates.sort()
                    real_candidates = list(real_candidates for real_candidates,_ in itertools.groupby(real_candidates))

                    for itemset1 in real_candidates:
                        count = 0
                        for itemset2 in sample_itemsets_dict[p]:
                            if itemset1 == itemset2:
                                count += 1
                        if count >= threshold:
                            candidates_temp.append(itemset1)

                    for itemset in real_candidates:
                        if itemset not in candidates_temp:
                            negative_border_temp.append(itemset)

                    for itemset1 in candidates_temp:
                        count = 0
                        for itemset2 in actual_itemsets_dict[p]:
                            if itemset1 == itemset2:
                                count += 1
                        if count >= support:
                            frequent_itemsets[p].append(itemset1)

                    #print frequent_itemsets[p]
                    for itemset in negative_border_temp:
                        immediate_subset = []
                        immediate_subset_temp = []
                        immediate_subset_temp.append([",".join(map(str,comb)) for comb in combinations(itemset, p-1)])

                        for each_list in immediate_subset_temp:
                            for each_comb in each_list:
                                immediate_subset.append(each_comb.split(','))

                        count = 0
                        for each_list in immediate_subset:
                            if each_list in frequent_itemsets[p-1]:
                                count += 1
                        if count == len(immediate_subset):
                            negative_border.append(itemset)

                    negative_border.sort()
                    negative_border = list(negative_border for negative_border,_ in itertools.groupby(negative_border))


                    if negative_border != []:
                        for itemset1 in negative_border:
                            count = 0
                            for itemset2 in actual_itemsets_dict[p]:
                                if itemset1 == itemset2:
                                    count += 1
                            if count >= support:
                                flag = 1
                                return flag
            else:
                for p in range(1, sample_max_basket_size+1):
                    if frequent_itemsets[p] != []:
                        for itemset in sorted(frequent_itemsets[p]):
                            frequents.append(itemset)
                flag = 0
                return flag


repeat = toivonen()
while repeat == 1:
    iterations += 1
    repeat = toivonen()

print str(iterations)
print str(fraction)
print frequents