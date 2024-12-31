import cv2
import pytesseract
from pytesseract import Output
import pyttsx3

# Initialize pytesseract OCR engine

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Replace <path_to_tesseract_executable> with the path to your Tesserac  t executable

# Initialize text-to-speech engine
engine = pyttsx3.init()


def read_text_from_image(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Perform OCR using Tesseract
    results = pytesseract.image_to_data(gray, output_type=Output.DICT)

    # Extract text and coordinates
    for i, text in enumerate(results['text']):
        if text:
            x, y, w, h = results['left'][i], results['top'][i], results['width'][i], results['height'][i]
            confidence = int(results['conf'][i])
            if confidence > 60:  # Threshold confidence level
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                # Read detected text
                engine.say(text)
                engine.runAndWait()

    return image


def main():
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    # Set the window size
    cap.set(3, 640)
    cap.set(4, 480)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect text from the frame
        frame = read_text_from_image(frame)

        # Display the frame
        cv2.imshow('OCR from Webcam', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
