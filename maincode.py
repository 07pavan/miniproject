import difflib
import pyttsx3
from translate import Translator
import os
import csv
import PyPDF2


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
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            content.append(page.extract_text())
    return '\n'.join(content)


# Function to determine file type and read content
def read_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == '.txt':
        return read_txt(file_path)
    elif file_extension.lower() == '.csv':
        return read_csv(file_path)
    elif file_extension.lower() == '.pdf':
        return read_pdf(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a TXT, CSV, or PDF file.")


# Function to calculate similarity
def plagiarism_check(text1, text2):
    similarity_ratio = difflib.SequenceMatcher(None, text1, text2).ratio()
    return similarity_ratio * 100  # Convert to percentage


# Main script
try:
    print("Supported file formats: TXT, CSV, PDF")
    
    # Get file paths from the user
    file1 = input("Enter the path of the first file: ").strip()
    file2 = input("Enter the path of the second file: ").strip()
    
    # Read content from files
    text1 = read_file(file1)
    text2 = read_file(file2)
    
    # Check for plagiarism
    similarity = plagiarism_check(text1, text2)
    print(f"Similarity: {similarity:.2f}%")
    
    # Initialize text-to-speech engine
    engine = pyttsx3.init()
    
    # Interpret similarity
    detect_message = ""
    if similarity > 80:
        detect_message = "High similarity detected! Possible plagiarism."
    else:
        detect_message = "Similarity is within acceptable range."
    
    print(detect_message)
    engine.say(detect_message)
    engine.runAndWait()
    
    # Language translation
    languages = {
        "hi": "Hindi",
        "kn": "Kannada"
    }
    print("Available languages for translation:")
    for code, lang in languages.items():
        print(f"{code} - {lang}")
    
    # Take language choice from user
    language_code = input("Enter the language code you want to translate to (e.g., 'hi' for Hindi): ").strip()
    
    # Initialize translator for the chosen language
    translator = Translator(to_lang=language_code)
    
    # Automatically translate the detected message
    try:
        translation = translator.translate(detect_message)
        print(f"Translation in {languages.get(language_code, 'selected language')}: {translation}")
        
        # Text-to-Speech for translated text
        engine.say(translation)
        engine.runAndWait()
    except Exception as e:
        print(f"Translation failed: {e}")
except Exception as e:
    print(f"Error: {e}")
