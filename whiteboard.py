
import cv2
import numpy as np
import easyocr
import time
import re

reader = easyocr.Reader(['en'])
drawing = False
last_point = None
frame1 = np.zeros((600, 800, 3), dtype=np.uint8)

# Initialize a set to store unique extracted text
extracted_text_set = set()
def draw(event, x, y, flags, param):
    global drawing, last_point, frame1
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        last_point = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.line(frame1, last_point, (x, y), (255, 255, 255), thickness=10)
            last_point = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        last_point = None

def evaluate_expression(expression):
    try:
        expression = expression.replace('^', '**')
        result = eval(expression)
        return result
    except Exception as e:
        return f"Error: {str(e)}"


def find_and_evaluate_math(text):
    pattern1 = re.compile(r'(\d+)\s*([\+\-\*\/\^])\s*(\d+)')  
    pattern2=re.compile(r'(\d+)\s*([\+\-\*\/\^])\s*(\d+)\s*([\+\-\*\/\^])\s*(\d+)')
    match1= pattern1.match(text)
    match2=pattern2.match(text)
    if match1:
        num1, operator1, num2 = match1.groups()
        
        expression = f"{num1} {operator1} {num2}"
        result = evaluate_expression(expression)

        print(f"Evaluating: {expression} = {result}")
    if match2:
        num1, operator1,  num2,operator2,num3 = match2.groups()
        expression=f"{num1} {operator1}  {num2} {operator2} {num3} "
        result = evaluate_expression(expression)
        print(f"Evaluating: {expression} = {result}")

cv2.namedWindow('Drawing Frame')
cv2.setMouseCallback('Drawing Frame', draw)

last_time = time.time()

while True:
    cv2.imshow('Drawing Frame', frame1)
    
   
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

    # Exit loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

