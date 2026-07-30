'''
=========================================
Module : Validation Report

Business Purpose
----------------

Generate a professional validation
report before preprocessing begins.

=========================================
'''


def generate_validation_report(results):

    print("\n")
    print("="*50)

    print("NETFLIX DATA VALIDATION REPORT")

    print("="*50)


    for result in results:

        print(f"\n{result['check']}")

        print(
            f"Status : {result['status']}"
        )

        print(
            f"Issues Found : {result['issues_found']}"
        )

        print(
            f"Recommendation :"
        )

        print(
            result["recommendation"]
        )


    print("\n"+"="*50)


def save_validation_report(results):


    file_path = (
        "reports/validation_report.txt"
    )


    with open(file_path,"w") as file:


        file.write(
            "NETFLIX DATA VALIDATION REPORT\n"
        )

        file.write(
            "="*50+"\n"
        )


        for result in results:


            file.write(
                f"\n{result['check']}\n"
            )


            file.write(
                f"Status : {result['status']}\n"
            )


            file.write(
                f"Issues Found : "
                f"{result['issues_found']}\n"
            )


            file.write(
                "Recommendation :\n"
            )


            file.write(
                f"{result['recommendation']}\n"
            )