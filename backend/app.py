from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.PuzzleParser import parsePuzzle

import numpy as np

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
        return ("<h1>Hello</h1>")

@app.route("/parse_img", methods=['POST'])
def solve():
        if 'image' not in request.files:
                return 'No image in request', 400
        
        image_file = request.files['image']

        if image_file.filename == '':
                return 'No image selected', 400
        
        image_data = image_file.read()
        img = np.frombuffer(image_data, np.uint8)

        nums = parsePuzzle(img)

        return jsonify(nums=nums), 200
