import csv
import pandas as pd
import numpy as np

class SparseMatrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.data = []
        self.row_indices = []
        self.col_indices = []

    def add_value(self, row, col, value):
        self.row_indices.append(row)
        self.col_indices.append(col)
        self.data.append(value)

    def is_serviceable(self, merchant_id, pincode):
        row_index = merchant_id
        col_index = pincode
        data_index = self._find_data_index(row_index, col_index)
        return data_index != -1

    def get_serviceable_pincodes(self, merchant_id):
        row_index = merchant_id
        col_indices = np.where(np.array(self.row_indices) == row_index)[0]
        return list(set(self.col_indices[i] for i in col_indices))

    def get_non_serviceable_pincodes(self, merchant_id):
        all_pincodes = set(range(self.cols))
        serviceable_pincodes = set(self.get_serviceable_pincodes(merchant_id))
        non_serviceable_pincodes = all_pincodes - serviceable_pincodes
        return list(non_serviceable_pincodes)

    def get_serviceable_merchant_ids(self, pincode):
        col_index = pincode
        row_indices = np.where(np.array(self.col_indices) == col_index)[0]
        return list(set(self.row_indices[i] for i in row_indices))

    def _find_data_index(self, row, col):
        indices = np.where((np.array(self.row_indices) == row) & (np.array(self.col_indices) == col))[0]
        return indices[0] if indices else -1


def main():
    # Read the dataset from CSV file
    dataset_path = "C:\\Users\\ungar\\Downloads\\merchantid.csv"  # Replace with the actual path to your CSV file
    with open(dataset_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        df = pd.DataFrame(reader)

    # Assuming there are 10 million merchants and 30,000 pincodes
    num_merchants = 10000000
    num_pincodes = 30000

    # Creating a sparse matrix
    sparse_matrix = SparseMatrix(num_merchants, num_pincodes)

    # Populating the sparse matrix with data from the dataset
    for index, row in df.iterrows():
        try:
            merchant_id, pincode, serviceability = int(row['Merchant_id']), int(row['pincodes']), row['serviceability status']
            sparse_matrix.add_value(merchant_id, pincode, serviceability)
        except ValueError:
            # Handle the case where conversion to integer fails
            print(f"Ignoring row {index} due to invalid data")

    # User input: Pincode to check serviceable merchants
    pincode_to_check = int(input("Enter the pincode to check serviceable merchants: "))
    serviceable_merchant_ids = sparse_matrix.get_serviceable_merchant_ids(pincode_to_check)
    print(f"Serviceable Merchant IDs in Pincode {pincode_to_check}: {serviceable_merchant_ids}")


if __name__ == "__main__":
    main()
