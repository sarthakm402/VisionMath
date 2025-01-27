# Vision MATH
 
This project is a "Math Drawing Calculator" that lets users draw mathematical expressions directly on a canvas. The application uses OpenCV for the drawing interface, EasyOCR for recognizing handwritten text, and SymPy for evaluating mathematical expressions. It sup ports basic arithmetic, Pythagorean theorem calculations, and probability computations from drawn text.
  
## Features

- **Draw Expressions**: Allows users to draw math expressions (e.g., `3+5`, `4^2`, etc.) for evaluation.
- **Basic Math Evaluation**: Supports basic operations (addition, subtraction, multiplication, division, and exponentiation).
- **Pythagorean Evaluation**: Calculates the hypotenuse or missing leg based on Pythagorean theorem.
- **Probability Evaluation**: Calculates complement probabilities from fractions or decimal inputs.
- **OCR-based Text Extraction**: Recognizes handwritten text using EasyOCR and filters high-confidence results for evaluation.
- **Show Graph**: Is able to how graphs of the equqation prvided for better visualisation.

## Requirements 

- Python 3.x
- OpenCV (`cv2`)
- EasyOCR (`easyocr`)
- Numpy (`numpy`)
- SymPy (`sympy`)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sarthakm402/VisionMath.git
   

## Usage
#### Drawing Math Expressions:

Click and hold the left mouse button to draw on the canvas.
Release the button to stop drawing.
Recognizing and Evaluating Expressions:

Every 10 seconds, the application reads the canvas using OCR.
#### Supported expressions:
##### Basic Arithmetic: e.g., 3 + 5, 4 * 7, 2^3.
##### Pythagorean Calculations:  Use "T a, b" format (e.g., T 3, 4 for legs or T c, -a for hypotenuse and one leg).
##### Probability: Use "P x/y" or "P 0.x" format.
#### Result Display:

Results are shown on the canvas.
Errors are printed in the console.
#### Exit:

Press q to close the application.
