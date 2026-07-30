'''==========================================
Module: Dataset Validation

Business Purpose
----------------
Before analyzing Netflix user behavior,
we need to ensure our dataset is reliable.

=========================================='''

import numpy as np

def check_dataset_shape(dataset):
    # checks the shape of dataset(rows,col)

    total_rows = dataset.shape[0] #normal 2D array: (50,20) but here its a structured array so shape is more like (50,)
                                  #hence every row already contains all columns.So shape[0] = number of records (rows)
    total_columns = len(dataset.dtype.names) # no of columns exist

    print("\nDataset Summary")
    print("-" * 30)
    print(f"Rows    : {total_rows}")
    print(f"Columns : {total_columns}")



def check_column_names(dataset):
    
    #Check whether all expected columns are present in the dataset.

    # dtype.names returns a tuple containing all col names from the structured array
    actual_columns = dataset.dtype.names

    expected_columns = (
        "user_id",
        "age",
        "gender",
        "region",
        "subscription_type",
        "payment_method",
        "primary_device",
        "account_age_months",
        "favorite_genre",
        "time_of_day",
        "recommendation_source",
        "session_count",
        "avg_watch_time_minutes_per_week",
        "watch_sessions_per_week",
        "completion_rate",
        "avg_rating_given",
        "app_rating",
        "recommendation_click_rate",
        "days_since_last_login",
        "churned",
    )

    print("\nChecking Column Names")
    print("-" * 30)

    # Comparing every expected column with the columns actually present in the dataset
    for column in expected_columns:

        if column in actual_columns:
            print(f"✅ {column}")

        else:
            print(f"❌ Missing : {column}")

    print(f"\nTotal Expected Columns : {len(expected_columns)}")
    print(f"Total Loaded Columns   : {len(actual_columns)}")



#Verifying the datatype of every column
def check_data_types(dataset):
    print("\nChecking Data Types")
    print("-" * 30)
    for column_name, data_type in dataset.dtype.descr:  #descr gives same information as for dtype in a format that's easy to iterate over with a for loop.

        print(f"{column_name:<35} : {data_type}")




def check_missing_values(dataset):
    print("\nChecking Missing Values")
    print("-" * 30)
    for column_name in dataset.dtype.names:
        column_data = dataset[column_name]
        missing_count = 0
        #Numeric columns: Missing values are represented as np.nan

        #String columns:Missing values are usually empty strings ""
        if np.issubdtype(column_data.dtype, np.number):
            missing_count = np.sum(np.isnan(column_data))  #np.isnan returns a boolean array eg -> (true , false , true)
        else:
            missing_count = np.sum(column_data == "") # counting empty string val

        print(f"{column_name:<35} : {missing_count}")




def check_duplicate_users(dataset):
    #checking for unique user ids
    print("\nChecking Duplicate User IDs")
    print("-" * 30)
    user_ids = dataset["user_id"]
    unique_user_ids, counts = np.unique(user_ids, return_counts=True) #only unique user ids will be returned with their count
    total_users = len(user_ids) 
    unique_users = len(unique_user_ids)
    duplicate_user_ids = unique_user_ids[counts > 1]

    duplicate_count = len(duplicate_user_ids)
    print(f"Total Records      : {total_users}")
    print(f"Unique User IDs    : {unique_users}")
    print(f"Duplicate User IDs : {duplicate_count}")
    if duplicate_count == 0:
        print("✅ No duplicate user IDs found.")
    else:
        print("❌ Duplicate user IDs detected.")
        # Printing only duplicated user IDs.
        for duplicate_id, frequency in zip(unique_user_ids, counts):

            if frequency > 1:

                print(f"{duplicate_id} --> appears {frequency} times")



def check_conflicting_user_records(dataset):
    #Detecting duplicate user IDs whose remaining information differs
    user_ids = dataset["user_id"]

    unique_user_ids = np.unique(user_ids)

    conflict_found = False

    for user_id in unique_user_ids:

        rows = dataset[user_ids == user_id]
        if len(rows) <= 1:
            continue

        first_record = rows[0]

        for other_record in rows[1:]:

            if not np.array_equal(first_record, other_record):
                print(f"\n❌ Conflict found for User ID : {user_id}")

                print("\nRecord 1")
                print(first_record)

                print("\nRecord 2")
                print(other_record)

                conflict_found = True

    if not conflict_found:

        print("✅ No conflicting user records found.")



def validate_dataset(dataset):
    print("\nRunning Dataset Validation...")
    print("=" * 40)

    #1st validation: checking the dataset shape
    check_dataset_shape(dataset)
    
    #2nd validation: checking col names
    check_column_names(dataset)

    #3rd validation: checking data types
    check_data_types(dataset)

    #4th validation: checking missing values
    check_missing_values(dataset)

    #5th validation: checking for duplicate user ids
    check_duplicate_users(dataset)

    #6th validation: checking for conflicting user record with same id
    check_conflicting_user_records(dataset)

    print("\nValidation Completed.")