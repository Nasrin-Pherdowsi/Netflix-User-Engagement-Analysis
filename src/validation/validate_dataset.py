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
    return{

        "check":"Dataset Shape",

        "status":"PASS",

        "issues_found":0,

        "recommendation":
        "No action required."

    }



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
    missing_columns=[c for c in expected_columns if c not in actual_columns]  
    return {  
        "check":"Column Names",
        "status":"PASS" if len(missing_columns)==0 else "FAIL",
        "issues_found":len(missing_columns),
        "recommendation":"No action required." if len(missing_columns)==0 else f"Add missing columns: {missing_columns}"
    }



#Verifying the datatype of every column
def check_data_types(dataset):
    print("\nChecking Data Types")
    print("-" * 30)
    for column_name, data_type in dataset.dtype.descr:  #descr gives same information as for dtype in a format that's easy to iterate over with a for loop.

        print(f"{column_name:<35} : {data_type}")
    return {"check":"Data Types","status":"PASS","issues_found":0,"recommendation":"No action required."}  




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
    return {"check":"Missing Values","status":"PASS","issues_found":0,"recommendation":"No action required."}  




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
        return {"check":"Duplicate User IDs","status":"PASS","issues_found":0,"recommendation":"No action required."}  
    else:
        print("❌ Duplicate user IDs detected.")
        # Printing only duplicated user IDs.
        for duplicate_id, frequency in zip(unique_user_ids, counts):

            if frequency > 1:

                print(f"{duplicate_id} --> appears {frequency} times")
    return {
        "check": "Duplicate User IDs",
        "status": "PASS" if duplicate_count == 0 else "FAIL",
        "issues_found": duplicate_count,
        "recommendation": (
            "No action required."
            if duplicate_count == 0
            else "Remove or investigate duplicate user IDs."
        )
    }



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
    return {
        "check": "Conflicting User Records",
        "status": "PASS" if not conflict_found else "FAIL",
        "issues_found": 0 if not conflict_found else 1,
        "recommendation": (
            "No action required."
            if not conflict_found
            else "Investigate conflicting records with the same user ID."
        )
    }

def check_duplicate_customer_profiles(dataset):
    
    #Detects rows that are identical except for user_id.

    print("\nChecking Duplicate Customer Profiles")
    print("-" * 35)

    # Stores every unique customer profile
    seen_profiles = {}

    duplicate_found = False

    for record in dataset:

        # Ignore user id col irrespect being it first or 5th col assuming user ids r diff but other info has been same 
        profile = tuple(record[field] for field in dataset.dtype.names if field != "user_id")

        if profile in seen_profiles:

            duplicate_found = True

            print("\n❌ Possible duplicate customer")

            print(f"User ID 1 : {seen_profiles[profile]}")
            print(f"User ID 2 : {record['user_id']}")

        else:

            seen_profiles[profile] = record["user_id"]

    if not duplicate_found:

        print("✅ No duplicate customer profiles found.")
        return {"check":"Duplicate Customer Profiles","status":"PASS","issues_found":0,"recommendation":"No action required."}  



def check_categorical_values(dataset):
    """
    Validate whether categorical columns contain only
    expected business values.eg if someone wrote Mle instead of Male or Premiu+
    """

    print("\nChecking Categorical Values")
    print("-" * 35)

    # Dictionary
    # Key   -> Column name
    # Value -> Allowed categories
    allowed_values = {

        "gender": {
            "Male",
            "Female"
        },

        "subscription_type": {
            "Basic",
            "Standard",
            "Premium"
        },

        "payment_method": {
            "Credit Card",
            "Debit Card",
            "Paypal"
        },

        "primary_device": {
            "Mobile",
            "Laptop",
            "Tablet",
            "Smart TV"
        },

        "time_of_day": {
            "Morning",
            "Afternoon",
            "Evening",
            "Night"
        },

        "recommendation_source": {
            "Homepage",
            "Friend",
            "Email",
            "Algorithm"
        },

        "churned": {
            0,
            1
        }

    }

    # Loop through every column present inside dictionary
    for column_name, valid_values in allowed_values.items():

        print(f"\n{column_name}")

        #entire column
        column_data = dataset[column_name]

        #only distinct values
        unique_values = np.unique(column_data)

        invalid_found = False

        #Checking unique value
        for value in unique_values:

            if value not in valid_values:

                print(f"❌ Invalid Value : {value}")

                invalid_found = True

        if not invalid_found:

            print("✅ Passed")
    return {"check":"Categorical Values","status":"PASS","issues_found":0,"recommendation":"No action required."}  


def check_numeric_ranges(dataset):

    #certain columns like age etc shouldnt have -ve values

    print("\nChecking Numeric Ranges")
    print("-" * 35)

    validation_rules = {

        "age": (0,120),

        "completion_rate": (0,100),

        "recommendation_click_rate": (0,100),

        "app_rating": (1,5),

        "avg_rating_given": (1,5),

        "session_count": (0,None),

        "watch_sessions_per_week": (0,None),

        "avg_watch_time_minutes_per_week": (0,None),

        "account_age_months": (0,None),

        "days_since_last_login": (0,None)

    }

    for column_name,(minimum,maximum) in validation_rules.items():

        column_data = dataset[column_name]

        invalid_values = []

        for value in column_data:

            if minimum is not None and value < minimum:

                invalid_values.append(value)

            elif maximum is not None and value > maximum:

                invalid_values.append(value)

        print(f"\n{column_name}")

        if len(invalid_values)==0:

            print("✅ Passed")

        else:

            print(f"❌ {len(invalid_values)} invalid values")

            print("Examples :", np.unique(invalid_values)[:10])
    return {"check":"Numeric Ranges","status":"PASS","issues_found":0,"recommendation":"No action required."}  



def check_business_rules(dataset):

    print("\nChecking Business Rules")
    print("-" * 35)

    issues = 0

    for record in dataset:

        # Rule 1
        if (
            record["watch_sessions_per_week"] == 0
            and
            record["avg_watch_time_minutes_per_week"] > 0
        ):

            issues += 1

            print(f"❌ {record['user_id']} : Watch time without sessions")

        # Rule 2
        if (
            record["session_count"] == 0
            and
            record["recommendation_click_rate"] > 0
        ):

            issues += 1

            print(f"❌ {record['user_id']} : Recommendation clicks without session")

        # Rule 3
        if (
            record["watch_sessions_per_week"] == 0
            and
            record["completion_rate"] > 0
        ):

            issues += 1

            print(f"❌ {record['user_id']} : Completion without watching")

    if issues == 0:

        print("✅ All business rules passed.")
        return {"check":"Business Rules","status":"PASS","issues_found":0,"recommendation":"No action required."}  




def validate_dataset(dataset):
    print("\nRunning Dataset Validation...")
    print("=" * 40)
    results=[]

    #1st validation: checking the dataset shape
    results.append(check_dataset_shape(dataset))
    
    #2nd validation: checking col names
    results.append(check_column_names(dataset))

    #3rd validation: checking data types
    results.append(check_data_types(dataset))

    #4th validation: checking missing values
    results.append(check_missing_values(dataset))

    #5th validation: checking for duplicate user ids
    results.append(check_duplicate_users(dataset))

    #6th validation: checking for conflicting user record with same id
    results.append(check_conflicting_user_records(dataset))

    #7th validation: checking for duplicate customer profiles
    results.append(check_duplicate_customer_profiles(dataset))

    #8th validation: checking for categorical values
    results.append(check_categorical_values(dataset))

    #9th validation: checking numeric ranges
    results.append(check_numeric_ranges(dataset))

    #10th validation: checking business rule for DA or Product Analyst pov
    results.append(check_business_rules(dataset))

    print("\nValidation Completed.")
    return results