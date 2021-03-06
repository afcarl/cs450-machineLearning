from collections import Counter

import numpy as np
from learndata import LearnData as ld
from learndata import ManipulateData as md
# from sklearn import tree


def calc_entropy(p):
    if p != 0:
        return -p * np.log2(p)
    else:
        return 0


def calc_info_gain(data, targets, feature):
    gain = 0
    n_data = len(data)

    # List the values that feature can take
    values = []
    for datapoint in data:
        if datapoint[feature] not in values:
            values.append(datapoint[feature])

    feature_counts = np.zeros(len(values))
    entropy = np.zeros(len(values))
    the_entropy = 0.0
    value_index = 0
    # Find where those values appear in data[feature] and the corresponding class
    for value in values:
        data_index = 0
        new_targets = []
        for datapoint in data:
            if datapoint[feature] == value:
                # feature_counts[value_index] += 1
                new_targets.append(targets[data_index])
            data_index += 1

        # Get the values in new_targets
        class_values = []
        for aclass in new_targets:
            if class_values.count(aclass) == 0:
                class_values.append(aclass)
        class_counts = np.zeros(len(class_values))
        class_index = 0
        for classValue in class_values:
            for aclass in new_targets:
                if aclass == classValue:
                    class_counts[class_index] += 1
            class_index += 1

        for class_index in range(len(class_values)):
            entropy[value_index] += calc_entropy(float(class_counts[class_index]) / sum(class_counts))
        gain += float(feature_counts[value_index])/n_data * entropy[value_index]
        value_index += 1

    return gain

def make_tree(data, targets, feature_names):

    n_data = len(data)
    n_features = len(data[0])

    #  Get the target names
    frequency = [x[1] for x in Counter(targets).most_common()]

    # Calculate total entropy
    total_entropy = 0
    for i in frequency:
        total_entropy += calc_entropy(float(i) / n_data)

    default = targets[np.argmax(frequency)]
    if n_data == 0 or n_features == 0:
        # Have reached an empty branch
        return default
    elif Counter(targets[0]) == n_data:
    # elif len(targets[0]) == n_data:
        # Only 1 class remains
        return targets[0]
    else:
        # Choose which feature is best
        gain = np.zeros(n_features)
        for feature in range(n_features):
            g = calc_info_gain(data, targets, feature)
            gain[feature] = total_entropy - g
        best_feature = np.argmax(gain)
        tree = {feature_names[best_feature]: {}}

        # Get the unique values
        values = []
        for datapoint in data:
            if datapoint[best_feature] not in values:
                values.append(datapoint[best_feature])

        # Find the possible feature values
        for value in values:
        # Find the datapoints with each feature value
            new_data = []
            new_targets = []
            index = 0
            for datapoint in data:
                if datapoint[best_feature] == value:
                    if best_feature == 0:
                        datapoint = datapoint[1:]
                        new_names = feature_names[1:]
                    elif best_feature == n_features:
                        datapoint = datapoint[:-1]
                        new_names = feature_names[:-1]
                    else:
                        datapoint = datapoint[:best_feature]
                        datapoint.extend(datapoint[best_feature + 1:])
                        new_names = feature_names[:best_feature]
                        new_names.extend(feature_names[best_feature + 1:])
                    new_data.append(datapoint)
                    new_targets.append(targets[index])
                index += 1
            # Now recurse to the next level
            subtree = make_tree(new_data, new_targets, new_names)
            # and on returning, add the subtree on to the tree
            tree[feature_names[best_feature]][value] = subtree
        return tree

def pretty(d, indent=0):
    for key, value in d.items():
        print('|\t\t' * int(indent/2) + str(key))
        if isinstance(value, dict):
            pretty(value, indent+1)
        else:
            print('|\t\t' * int((indent+1)/2) + str(value))

# def test_tree(tree, data, target):
#     keys = list(tree.keys())[0]
#     values = list(tree.values())[0]
#     ans = data[keys]
#     sub_keys = list(values.keys())
#
#     for key in sub_keys:
#         if key == ans:
#             break
#         else:
#             counter += 1
#
#     try:
#         sub_tree = list(values.values())[counter]
#     except:
#         sub_tree = list(values.values())[0]
#
#     tree = test_tree(sub_tree, data, target)
#
#     return tree

def main():
    split = 0.7

    # Irisis Data
    print("Irises Data:")
    iris = ld.load_dataset('iris')
    X_data, X_target, y_data, y_target = md.split_data(iris, split)

    columns = [i for i in range(len(X_data[0]))]

    iris_tree = make_tree(X_data, X_target, columns)
    print(iris_tree)
    pretty(iris_tree)
    # print(test_tree(tree, y_data, y_target))

    # Lenses Data
    # print("Lenses Data:")
    # lens = ld.load_dataset('lenses')
    # X_data, X_target, y_data, y_target = md.split_data(lens, split)
    #
    # columns = [i for i in range(len(X_data[0]))]
    # tree = make_tree(X_data, X_target, columns)
    # print(tree)

    # Lenses Data
    print("House Votes Data:")
    votes = ld.load_dataset('house-votes')
    votes = np.fliplr(votes)
    # print(votes)
    X_data, X_target, y_data, y_target = md.split_data(votes, split)
    # print(X_data)
    # print(X_target)

    columns = [i for i in range(len(X_data[0]))]
    tree = make_tree(X_data, X_target, columns)
    print(tree)
    pretty(tree)

if __name__ == '__main__':
    main()
