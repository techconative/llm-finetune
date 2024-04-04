import pandas as pd
import json
import random
import math
import argparse

parser = argparse.ArgumentParser(description="Script for preparing data to be used with a language model.")

parser.add_argument(
    "--file_path", type=str, help="Path to the csv file containing the json data"
)

args = parser.parse_args()

def check_json(dsl):
    """
    Checks the given dsl to see if it is a valid JSON and prints any invalid dsl.

    Args:
        dsl: The dsl that will be checked.

    Returns:
        None
    """
    print(f"a: {dsl}")
    try:
        dsl = json.loads(dsl)
        json.loads(dsl)
    except ValueError as e:
        print("c")
        print(f"Invalid JSON: '{dsl}': {e}")
        input("Enter something (or just press Enter to continue): ")

def split(dsl_set_len, train=100, test=0, valid=0):
    if (train + test + valid) > 100:
        split = 100 - train
    split = math.ceil((dsl_set_len ))
    pass

def main(file_path):
    df = pd.read_csv(file_path, dtype=str, sep="\t").fillna("")

    COLUMNS=["instruction", "input", "output"]
    if not(df.columns.values == COLUMNS).all():
        raise ValueError(f"CSV columns must be {COLUMNS}, found {df.columns.values}")

    # Using unique dsl as key, the data is sorted by storing copies in a list.
    df_obj = {}
    for index, data in df.iterrows():
        dsl = json.dumps(data.output)
        if dsl in df_obj:
            df_obj[dsl].append(data)
        else:
            check_json(dsl)
            df_obj[dsl] = [data]

    del df

    train_split = []
    test_split = []
    valid_split = []
    seed_value = 5
    random.seed(seed_value)
    # Loops through each unique dsl list and splits them 80%-training, 10%-testing and 10%-validating.
    for dsl_set in df_obj:
        dsl_set_len = len(df_obj[dsl_set])
        split = math.ceil((dsl_set_len * 20)/100)
        test_count = math.ceil(split/2)
        valid_count = split - test_count

        # Samples are randomly chosen for the splitting using a seed.
        # The randomly chosen indices are reverse sorted to make it convenient to pop the data.
        random_numbers = random.sample(range(0, dsl_set_len), split)
        random_numbers.sort(reverse=True)
        
        print(random_numbers)
        print(f"dsl_set_len : {dsl_set_len}\nsplit : {split}\ntest_count : {test_count}\nvalid_count : {valid_count}\n\n")

        # Adding data to the test and valid splits.
        for i, index in enumerate(random_numbers):
            print(f"pop : {df_obj[dsl_set][index]}\n")
            try:
                # If the count for validity split is 0, then 1 sample from training is copied to it.
                if (valid_count == 0):
                    tmp = df_obj[dsl_set][index]
                    valid_split.append(tmp)
                    valid_count += 1
                if (i < test_count):
                    test_split.append(df_obj[dsl_set].pop(index))
                else:
                    valid_split.append(df_obj[dsl_set].pop(index))
            except:
                print(f"Invalid index {index} in df_obj[dsl_set]")
        
        # Add the rest of the dsl set to the training split.
        train_split.extend(df_obj[dsl_set])

    del df_obj

    train_df = pd.DataFrame(train_split)
    test_df = pd.DataFrame(test_split)
    valid_df = pd.DataFrame(valid_split)

    print(f"train: {len(train_df)} rows\ntest: {len(test_df)} rows\nvalid: {len(valid_df)} rows\n")

    train_df.to_csv('train_test.csv', index=False)
    test_df.to_csv("test_test.csv", index=False)
    valid_df.to_csv("valid_test.csv", index=False)


if __name__ == "__main__":
    main(args.file_path)