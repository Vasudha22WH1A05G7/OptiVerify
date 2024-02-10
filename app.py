from flask import Flask, render_template, request, jsonify
import csv
import pandas as pd
import numpy as np

app = Flask(__name__, template_folder='templates')

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

    def get_serviceable_merchant_ids(self, pincode):
        col_index = pincode
        row_indices = np.where(np.array(self.col_indices) == col_index)[0]
        return list(set(self.row_indices[i] for i in row_indices))

@app.route('/')
def index():
    return render_template('http://127.0.0.1:5500/ecommerce/project_directory/templates/web.html')

@app.route('/buyerlogin')
def buyer_login():
    return render_template('http://127.0.0.1:5500/ecommerce/project_directory/templates/buyer.html')

@app.route('/buyer')
def buyer():
    return render_template('buyer.html')

@app.route('/serviceability')
def serviceability():
    return render_template('serviceability.html')

@app.route('/get_serviceable_merchants', methods=['POST'])
def get_serviceable_merchants():
    pincode = int(request.json['pincode'])
    serviceable_merchant_ids = sparse_matrix.get_serviceable_merchant_ids(pincode)
    return jsonify({'merchant_ids': serviceable_merchant_ids})

if __name__ == "__main__":
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

    app.run(debug=True)
