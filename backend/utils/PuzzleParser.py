import cv2 as cv2
import sys
from imutils import contours
from pytesseract import image_to_string
import numpy as np
from PIL import Image

def parsePuzzle(image):
    try:
        img = cv2.imdecode(image, cv2.IMREAD_COLOR)
        if img is None:
            print("Failed to decode image")
            sys.stdout.flush()
            return "0" * 81

        print(f"Image shape: {img.shape}")
        sys.stdout.flush()

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        max_dimension = 600
        height, width = img.shape[:2]
        if height > max_dimension or width > max_dimension:
            scale = max_dimension / max(height, width)
            img = cv2.resize(img, (int(width * scale), int(height * scale)))
            print(f"Resized image to: {img.shape}")
            sys.stdout.flush()
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,57,5)

        # Filter out all numbers and noise to isolate only boxes
        cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
                area = cv2.contourArea(c)
                if area < 1000:
                        cv2.drawContours(thresh, [c], -1, (0,0,0), -1)

        # Fix horizontal and vertical lines
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,5))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, vertical_kernel, iterations=9)
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,1))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, horizontal_kernel, iterations=4)

        # Sort by top to bottom and each row by left to right
        invert = 255 - thresh
        cnts = cv2.findContours(invert, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        (cnts, _) = contours.sort_contours(cnts, method="top-to-bottom")

        sudoku_rows = []
        row = []
        for (i, c) in enumerate(cnts, 1):
            area = cv2.contourArea(c)
            if area < 50000:
                row.append(c)
                if i % 9 == 0:  
                    (cnts, _) = contours.sort_contours(row, method="left-to-right")
                    sudoku_rows.append(cnts)
                    row = []

        # Iterate through each box
        sudoku_string = ""
        for row in sudoku_rows:
            for c in row:
                try:
                    mask = np.zeros(img.shape, dtype=np.uint8)
                    cv2.drawContours(mask, [c], -1, (255,255,255), -1)
                    result = cv2.bitwise_and(img, mask)
                    result[mask==0] = 255

                    result_pil = Image.fromarray(result)

                    dig = image_to_string(result_pil, config='--psm 10')
                    dig = dig.strip()

                    if(dig.isdigit()):
                      sudoku_string += dig
                    else:
                      sudoku_string += "0"
                except Exception as cell_error:
                    print(f"Error processing cell: {str(cell_error)}")
                    sys.stdout.flush()
                    sudoku_string += "0"  # Use 0 for cells that fail
        
        if len(sudoku_string) != 81:
            print(f"Generated string length: {len(sudoku_string)}")
            sys.stdout.flush()
            if len(sudoku_string) < 81:
                sudoku_string += "0" * (81 - len(sudoku_string))
            else:
                sudoku_string = sudoku_string[:81]

        return sudoku_string
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        sys.stdout.flush()
        return "0" * 81  # Return empty puzzle
