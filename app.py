from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

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

def create_sparse_matrix():
    dataset_path = "merchantid.csv"
    df = pd.read_csv(dataset_path)

    print("DataFrame Columns:", df.columns)
    print("First few rows of the DataFrame:\n", df.head())

    sparse_matrix = SparseMatrix(rows=10000000, cols=30000)

    for _, row in df.iterrows():
        merchant_id = row['MerchantID']
        pincode = row['Pincode']
        is_serviceable = row['IsServiceable']
        if is_serviceable:
            sparse_matrix.add_value(merchant_id, pincode, 1)

    return sparse_matrix

@app.route('/get_serviceable_merchants', methods=['POST'])
def get_serviceable_merchants():
    data = request.json
    pincode = int(data['pincode'])
    serviceable_merchants = sparse_matrix.get_serviceable_merchant_ids(pincode)
    return jsonify({'merchant_ids': serviceable_merchants})

if __name__ == '__main__':
    sparse_matrix = create_sparse_matrix()
    app.run(host="0.0.0.0", port=5000, debug=True)
