
import cv2
import numpy as np
import easyocr
import time
import re
import sympy as sp

# Initialize easyocr reader
reader = easyocr.Reader(['en'])

drawing = False
last_point = None
frame1 = np.zeros((800, 800, 3), dtype=np.uint8)
extracted_text_set = set()

# Mouse drawing function
def draw(event, x, y, flags, param):
    global drawing, last_point, frame1
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        last_point = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.line(frame1, last_point, (x, y), (255, 255, 255), thickness=5)
            last_point = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        last_point = None

# Function to evaluate basic math expressions
def evaluate_expression(expression):
    try:
        expression = expression.replace('^', '**')  # Replacing ^ with ** for power
        result = eval(expression)
        return result
    except Exception as e:
        return f"Error: {str(e)}"

# Function to find and evaluate math expressions in text
def find_and_evaluate_math(text):
    pattern = re.compile(r'[0-9+\-*/^().\s]+')  # Simplified pattern to match math expressions
    pythagoras_pattern = re.compile(r'[Tt]\s+([+-]?\d+)\s*,?\s*([+-]?\d+)')  # Match Pythagorean expressions
    prob_pattern = re.compile(r'[Pp]\s+((\d+/\d+)|(\d*\.?\d+))')  # Match fractions or decimals in probabilities

    match_math = pattern.match(text)
    match_pythagoras = pythagoras_pattern.match(text)
    prob_math = prob_pattern.match(text)

    if match_math:
        try:
            result = evaluate_expression(text)
            print(f"Evaluating: {text} = {result}")
            cv2.putText(frame1, str(result), org=(70, 70), fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                        fontScale=1, color=(255, 255, 255), thickness=2)
        except Exception as e:
            print(f"Error evaluating expression: {text}, Error: {e}")

    elif match_pythagoras:
        first, second = match_pythagoras.groups()
        try:
            first, second = int(first), int(second)

            # Case 1: Both values are legs of a triangle
            if first > 0 and second > 0:
                hypotenuse = (first**2 + second**2) ** 0.5
                print(f"Given legs a={first}, b={second}: Hypotenuse c={hypotenuse:.2f}")
                cv2.putText(frame1, str(hypotenuse), org=(70, 70), fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                            fontScale=1, color=(255, 255, 255), thickness=2)
            # Case 2: Hypotenuse and one leg
            elif first > 0 and second <= 0:
                legb = abs(second)
                if first > legb:
                    lega = (first**2 - legb**2) ** 0.5
                    print(f"Given hypotenuse c={first} and leg b={legb}: Leg a={lega:.2f}")
                    cv2.putText(frame1, str(lega), org=(70, 70), fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                                fontScale=1, color=(255, 255, 255), thickness=2)
            else:
                print("Invalid Pythagorean input.")
        except ValueError:
            print("Invalid input for Pythagorean theorem.")
    
    elif prob_math:
        fraction_or_decimal = prob_math.group(1)  # This gets the full fraction or decimal string
        
        try:
            if '/' in fraction_or_decimal:  # If it's a fraction
                num, dum = fraction_or_decimal.split('/')
                num = int(num)  # Convert numerator to integer
                dum = int(dum)  # Convert denominator to integer

                if dum != 0:
                    probability = num / dum
                    result = 1 - probability
                    print(f"Fraction detected: {num}/{dum} = {probability}, Result: {result}")
                    cv2.putText(frame1, f"Result: {result:.4f}", org=(70, 70), 
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, 
                                color=(255, 255, 255), thickness=2)
                else:
                    raise ValueError("Denominator cannot be zero.")
            else:  # It's a decimal
                probability = float(fraction_or_decimal)
                result = 1 - probability
                print(f"Decimal detected: {probability}, Result: {result}")
                cv2.putText(frame1, f"Result: {result:.4f}", org=(70, 70), 
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, 
                            color=(255, 255, 255), thickness=2)
    
        except ValueError as e:
            print(f"Error in probability calculation: {e}")

# Initialize OpenCV window and mouse callback
cv2.namedWindow('Drawing Frame')
cv2.setMouseCallback('Drawing Frame', draw)

last_time = time.time()

# Main loop
while True:
    cv2.imshow('Drawing Frame', frame1)

    # Process every 10 seconds
    if np.sum(frame1) > 0 and (time.time() - last_time) > 10.0:
        extracted_text = reader.readtext(frame1)
        for (bbox, text, prob) in extracted_text:
            text = text.strip()
            print(f"Extracted Text: {text} (Confidence: {prob:.2f})")

            if prob > 0.5:
                extracted_text_set.add(text)

        last_time = time.time()

        for text in extracted_text_set:
            find_and_evaluate_math(text)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
