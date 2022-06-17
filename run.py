#!/usr/bin/python3
import sys
import time
import pandas as pd
from itertools import combinations
from collections import defaultdict

OUTPUT_FILE = "output.txt"

def dump_frequent_itemsets(itemsets, min_sup):
    """
    Writes frequent itemsets in sorted order to output.txt
    @param itemsets: dictionary of frequent itemsets with their support value
    @param min_sup: minimum support
    @return:
    """

    with open(OUTPUT_FILE, "w") as f:
        f.write(f"=== Frequent Itemsets (min_sup={min_sup*100}%) ===\n")

        itemsets_sorted = list(itemsets)
        itemsets_sorted.sort(key=lambda x: itemsets[x], reverse=True)

        for elem in itemsets_sorted:
            f.write(f"{sorted(list(elem))}, {itemsets[elem]:.6f}%\n")


def dump_association_rules(conf_rules, min_conf):
    """
    Appends high confidence rules in sorted order to output.txt
    @param conf_rules: high confidence rules as dict
    @param min_conf: minimum confidence
    @return:
    """

    with open(OUTPUT_FILE, "a") as f:
        f.write(f"\n=== High Confidence Association Rules (min_conf={min_conf*100}%) ===\n")

        rules_sorted = list(conf_rules)
        rules_sorted.sort(key=lambda x: conf_rules[x][0], reverse=True)

        for elem in rules_sorted:
            f.write(f"{sorted(list(elem[0]))} => {list(elem[1])} "
                    f"(Conf: {conf_rules[elem][0]:.6f}%, Supp: {conf_rules[elem][1]:.6f}%)\n")


def calculate_frequent_itemsets(data, min_sup):
    """
    Computes candidate and frequent itemsets
    @param data: dataset where each row if of format [Txn_serial_no, [T1, T2, T3, ...]]
    @param min_sup: minimum support
    @return: dictionary with <itemset (as frozenset), support> pairs
    """

    freq_itemsets_output = dict()

    # Extracting individual items from data
    individual_items = []
    for _, basket in data:
        for item in basket:
            if item not in individual_items:
                individual_items.append(item)
    individual_items = sorted(individual_items)

    min_sup_count = int(min_sup * len(data))

    print(f"Running for k: 1")
    candidates = defaultdict(int)
    for item in individual_items:
        for _, basket in data:
            if item in basket:
                candidates[frozenset([item])] += 1

    freq_itemsets = defaultdict(int)
    for candidate, count in candidates.items():
        if count >= min_sup_count:
            freq_itemsets[candidate] = count * 100 / len(data)

    # Add L1 to final output
    for key, val in freq_itemsets.items():
        freq_itemsets_output[key] = val

    prev_itemsets = freq_itemsets
    for k in range(2, len(individual_items) + 1):
        print(f"Running for k: {k}")
        new_candidates = set()

        # considering keys of previous frequent itemset
        prev_itemsets = list(prev_itemsets)

        # Creating new candidates from previous frequent itemset
        for i in range(0, len(prev_itemsets)):
            for j in range(i + 1, len(prev_itemsets)):
                t = prev_itemsets[i].union(prev_itemsets[j])
                if len(t) == k:
                    new_candidates.add(t)

        # Pruning candidates
        print("Pruning Candidates...")

        # Converting previous itemset list to a set
        prev_itemsets = set(prev_itemsets)

        candidates_to_prune = list()
        for c in new_candidates:
            for subset in list(map(set, combinations(c, len(c) - 1))):
                if subset not in prev_itemsets:
                    candidates_to_prune.append(c)
                    break

        # print("Removing Candidates...")
        for pc in candidates_to_prune:
            new_candidates.remove(pc)

        print("Done pruning candidates.")
        new_candidates = list(new_candidates)
        candidates_count = defaultdict(int)
        for i in new_candidates:
            for _, basket in data:
                if i.issubset(set(basket)):
                    candidates_count[i] += 1

        print(f"Generating frequent itemsets for k: {k}...")
        freq_itemsets = defaultdict(int)
        for candidate, count in candidates_count.items():
            if count >= min_sup_count:
                freq_itemsets[candidate] = count * 100 / len(data)

        for key, val in freq_itemsets.items():
            freq_itemsets_output[key] = val

        if len(freq_itemsets) == 0:
            print(f"No frequent itemsets detected for k: {k}. "
                  f"Done with frequent itemsets generation.")
            break
        else:
            print(f"Done generating frequent itemsets for k: {k}")

        prev_itemsets = freq_itemsets

    return freq_itemsets_output


def calculate_high_conf_rules(frequent_itemsets, min_conf):
    """
    Calculate high confidence association rules
    @param frequent_itemsets: frequent itemsets dict with their support value
    @param min_conf: minimum confidence
    @return:
    """

    high_conf_rules = dict()
    for itemset, support in frequent_itemsets.items():
        # Ignoring L1
        if len(itemset) == 1:
            continue

        subsets = list(map(frozenset, combinations(itemset, len(itemset) - 1)))

        for lhs_itemset in subsets:
            rhs_itemset = itemset - lhs_itemset
            confidence = support * 100 / frequent_itemsets[lhs_itemset]

            if confidence >= min_conf * 100:
                # for rule a->b, storing (a, b): (conf, support)
                high_conf_rules[tuple([lhs_itemset, rhs_itemset])] = tuple([confidence, support])

    return high_conf_rules


def extract_association_rules(dataset_file, min_sup=0.01, min_conf=0.5):
    """

    @param dataset_file: integrated dataset csv file
    @param min_sup: minimum support for apriori algorithm
    @param min_conf: minimum confidence for apriori algorithm
    @return:
    """

    df = pd.read_csv(dataset_file)

    data = df.values.tolist()

    for index, item in enumerate(data):
        item = [x for x in item if str(x) != 'nan']
        data[index] = [index]
        data[index].append(list(item))

    frequent_itemsets = calculate_frequent_itemsets(data, min_sup)
    dump_frequent_itemsets(frequent_itemsets, min_sup)

    print("Generating high confidence association rules...")
    high_conf_rules = calculate_high_conf_rules(frequent_itemsets, min_conf)
    print("Association Rules Generated.")
    dump_association_rules(high_conf_rules, min_conf)

def main():
    if len(sys.argv) < 4:
        print(f"Incorrect Usage: {sys.argv[0]} <integrated dataset filename> <minimum support> <minimum confidence>")
        return

    dataset_file = sys.argv[1]

    min_sup = float(sys.argv[2])
    if min_sup < 0 or min_sup > 1:
        print(f"Minimum support should be between 0 and 1.")
        return

    min_conf = float(sys.argv[3])
    if min_conf < 0 or min_conf > 1:
        print(f"Minimum confidence should be between 0 and 1.")
        return

    start = time.time()
    print(f"Start Time: {start}")
    extract_association_rules(dataset_file, min_sup, min_conf)
    end = time.time()
    print(f"Elapsed time: {end - start} seconds.")


if __name__ == "__main__":
    main()
