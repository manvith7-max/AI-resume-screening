import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Ensure required NLTK resources are downloaded silently
NLTK_RESOURCES = ["punkt", "punkt_tab", "stopwords", "wordnet", "omw-1.4"]
for resource in NLTK_RESOURCES:
    try:
        nltk.data.find(f"tokenizers/{resource}")
    except LookupError:
        try:
            nltk.data.find(f"corpora/{resource}")
        except LookupError:
            try:
                nltk.download(resource, quiet=True)
            except Exception:
                pass

lemmatizer = WordNetLemmatizer()

try:
    STOP_WORDS = set(stopwords.words("english"))
except Exception:
    STOP_WORDS = {"a", "an", "the", "and", "or", "in", "on", "at", "to", "for", "with", "by", "of", "is", "it", "this", "that"}

def clean_text(text):
    """
    Cleans raw resume or job description text for NLP processing.
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Replace newlines, tabs, and multiple spaces with a single space
    text = re.sub(r'[\r\n\t]+', ' ', text)
    
    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', ' ', text)
    
    # Remove special punctuation but keep alphanumeric and spaces
    text = re.sub(r'[^a-zA-Z0-9\s+#\.]', ' ', text)
    
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def preprocess_text(text):
    """
    Cleans, tokenizes, removes stop words, and lemmatizes input text.
    Returns a cleaned token string suitable for TF-IDF vectorization.
    """
    cleaned = clean_text(text)
    
    try:
        tokens = word_tokenize(cleaned)
    except Exception:
        tokens = cleaned.split()
        
    filtered_tokens = []
    for token in tokens:
        token = token.strip('.').strip()
        if token and token not in STOP_WORDS and len(token) > 1:
            lemmatized = lemmatizer.lemmatize(token)
            filtered_tokens.append(lemmatized)
            
    return " ".join(filtered_tokens)

def extract_keywords(text, top_n=20):
    """
    Returns the top N frequency keywords from cleaned text.
    """
    processed = preprocess_text(text)
    tokens = processed.split()
    freq = {}
    for token in tokens:
        freq[token] = freq.get(token, 0) + 1
    sorted_keywords = sorted(freq.items(), key=lambda item: item[1], reverse=True)
    return sorted_keywords[:top_n]
