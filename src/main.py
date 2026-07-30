from src.ingestion.load_dataset import load_dataset
from src.validation.validate_dataset import validate_dataset

def main():

    dataset = load_dataset()
    validate_dataset(dataset)
    print(dataset.shape)        #shape is an attribute to get dimension of the array
    print(dataset.dtype.names)  #prints only column names

if __name__ == "__main__":
    main()  #this is the entry point of the program. It ensures that the code inside main() runs only when this file is executed directly, not when imported.
            #Functions inside the file can be imported into other files without triggering unwanted code execution.