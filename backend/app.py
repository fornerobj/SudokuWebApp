from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.PuzzleParser import parsePuzzle
from utils.SudokuSolver import makeGrid, solvePuzzle, makePuzzleString

import numpy as np

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
        return ("<h1>Hello</h1>")

@app.route("/parse_img", methods=['POST'])
def parse():
        if 'image' not in request.files:
                return 'No image in request', 400
        
        image_file = request.files['image']

        if image_file.filename == '':
                return 'No image selected', 400
        
        image_data = image_file.read()
        img = np.frombuffer(image_data, np.uint8)

        nums = parsePuzzle(img)

        return jsonify(nums=nums), 200

@app.route('/solve')
def solve():
        if 'puzzle' not in request.args:
                return 'No puzzle in request', 400

        puzzle = request.args['puzzle']
        print(puzzle)
        grid = makeGrid(puzzle)
        solution = solvePuzzle(grid)
        if solution:
                solutionString = makePuzzleString(grid)
        else:
                solutionString = puzzle
        response = {
                "solution": solutionString,
                "success" : solution
        }
        return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
