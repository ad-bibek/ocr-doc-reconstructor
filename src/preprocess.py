import cv2
import numpy as np

def preprocess_image(input_path, output_path):
    img = cv2.imread(input_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Increase contrast (helps with shadow near spine)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    
    # Denoise
    denoised = cv2.fastNlMeansDenoising(enhanced, h=10)
    
    cv2.imwrite(output_path, denoised)
    print(f"Saved preprocessed image to {output_path}")

if __name__ == "__main__":
    preprocess_image('input_samples/messy.jpg', 'input_samples/messy_preprocessed.png')