from src.ingestion.load_dataset import load_dataset
from src.validation.validate_dataset import validate_dataset
from src.validation.validation_report import generate_validation_report, save_validation_report

def main():

    dataset = load_dataset()
    results = validate_dataset(dataset)
    #generate_validation_report(results)
    #save_validation_report(results)
    print(results)
    

if __name__ == "__main__":
    main()  #this is the entry point of the program. It ensures that the code inside main() runs only when this file is executed directly, not when imported.
            #Functions inside the file can be imported into other files without triggering unwanted code execution.