import difflib
import pyttsx3
from translate import Translator


# Function to calculate similarity
def plagiarism_check(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        text1 = f1.read()
        text2 = f2.read()

    # Compute similarity ratio
    similarity_ratio = difflib.SequenceMatcher(None, text1, text2).ratio()
    return similarity_ratio * 100  # Convert to percentage


# Get file names from the user
file1 = input("Enter the path of the first file: ")
file2 = input("Enter the path of the second file: ")

# Check for plagiarism
similarity = plagiarism_check(file1, file2)
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