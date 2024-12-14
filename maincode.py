import os
import difflib
from googletrans import Translator  # Translation
from gtts import gTTS  # Text-to-Speech
from PIL import Image  # Image handling
import fitz  # PDF reading
import csv


# Function to read content from a text file
def read_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


# Function to read content from a CSV file
def read_csv(file_path):
    content = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            content.append(' '.join(row))
    return '\n'.join(content)


# Function to read content from a PDF file
def read_pdf(file_path):
    content = []
    with fitz.open(file_path) as pdf:
        for page in pdf:
            content.append(page.get_text())
    return '\n'.join(content)


# Function to read content from various file types
def read_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == '.txt':
        return read_txt(file_path)
    elif file_extension.lower() == '.csv':
        return read_csv(file_path)
    elif file_extension.lower() == '.pdf':
        return read_pdf(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")


# Function to calculate similarity
def plagiarism_check(text1, text2):
    similarity_ratio = difflib.SequenceMatcher(None, text1, text2).ratio()
    return similarity_ratio * 100  # Convert to percentage


# Function to display hand sign based on similarity using Pillow
def display_hand_sign(similarity):
    if similarity > 80:
        hand_sign_image = "D:\\rock\handsign.jpg"  # Path to high similarity hand sign image
    elif similarity > 50:
        hand_sign_image = "D:\\rock\handsign.jpg"  # Path to medium similarity hand sign image
    else:
        hand_sign_image = "D:\\rock\handsign.jpg"  # Path to low similarity hand sign image

    # Display the image
    try:
        img = Image.open(hand_sign_image)
        img.show()
    except FileNotFoundError:
        print("Hand sign image not found!")


# Main script
if _name_ == "_main_":
    print("Supported file formats: TXT, CSV, PDF")

    # Get file paths from the user
    file1 = input("Enter the path of the first file: ").strip()
    file2 = input("Enter the path of the second file: ").strip()

    try:
        # Read content from files
        text1 = read_file(file1)
        text2 = read_file(file2)

        # Check for plagiarism
        similarity = plagiarism_check(text1, text2)
        print(f"Similarity: {similarity:.2f}%")

        # Interpret similarity
        detect_message = (
            "High similarity detected! Possible plagiarism."
            if similarity > 80
            else "Similarity is within acceptable range."
        )

        print(detect_message)

        # Convert detect_message to speech
        tts = gTTS(detect_message, lang="en")
        tts.save("output.mp3")
        os.system("start output.mp3")  # Play the audio file

        # Display hand sign based on similarity
        display_hand_sign(similarity)

        # Language translation
        translator = Translator()
        languages = {"hi": "Hindi", "kn": "Kannada"}
        print("Available languages for translation:")
        for code, lang in languages.items():
            print(f"{code} - {lang}")

        language_code = input(
            "Enter the language code you want to translate to (e.g., 'hi' for Hindi): "
        ).strip()

        try:
            translation = translator.translate(detect_message, dest=language_code).text
            print(f"Translation in {languages.get(language_code, 'selected language')}: {translation}")

            # Convert translated text to speech
            tts_translation = gTTS(translation, lang=language_code)
            tts_translation.save("translation.mp3")
            os.system("start translation.mp3")

        except Exception as e:
            print(f"Translation failed: {e}")

    except Exception as e:
        print(f"Error: {e}")
