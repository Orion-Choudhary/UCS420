import cv2
import easyocr
import re
import difflib
import pyttsx3

# load medicine bottle image
image = cv2.imread("medicine_bottle.jpg")

# initialize easyocr reader for english
reader = easyocr.Reader(['en'], gpu=False)

# extract text lines from image
results = reader.readtext(image, detail=0)
raw_text = " ".join(results)

# drug database for fuzzy entity matching
KNOWN_DRUGS = ["paracetamol", "amoxicillin", "ibuprofen", "metformin", "cetirizine", "atorvastatin", "aspirin", "omeprazole"]

# match detected words against known drugs
drug_name = "Unknown medication"
for word in re.findall(r"\b[A-Za-z]{4,}\b", raw_text.lower()):
    match = difflib.get_close_matches(word, KNOWN_DRUGS, n=1, cutoff=0.7)
    if match:
        drug_name = match[0].capitalize()
        break

# extract dosage patterns
dosage_match = re.search(r"\b\d+\s*(?:mg|ml|mcg|g)\b", raw_text, re.IGNORECASE)
dosage = dosage_match.group(0) if dosage_match else "Not specified"

# extract intake frequency
freq_match = re.search(r"\b(?:once|twice|thrice|\d+\s*times)\s*(?:a|per)?\s*day\b", raw_text, re.IGNORECASE)
frequency = freq_match.group(0) if freq_match else "Not specified"

# extract expiry date in mm/yy or mm/yyyy format
exp_match = re.search(r"\b(0[1-9]|1[0-2])[\/\-](20\d{2}|\d{2})\b", raw_text)
expiry = exp_match.group(0) if exp_match else "Not found"

# compile guidance text for cognitive assistance
advice = f"Medication: {drug_name}. Dosage: {dosage}. Frequency: {frequency}. Expiry: {expiry}."

# initialize text to speech engine
engine = pyttsx3.init()

# speak medication guidance
engine.say(advice)
engine.runAndWait()