import re
import nltk

# Safe NLTK Resource Initialization
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

try:
    from nltk.stem import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
except Exception:
    lemmatizer = None

try:
    from nltk.corpus import stopwords
    STOP_WORDS = set(stopwords.words("english"))
except Exception:
    STOP_WORDS = {
        "a", "an", "the", "and", "or", "in", "on", "at", "to", "for", "with", "by", "of", "is", "it", 
        "this", "that", "be", "are", "was", "were", "from", "as", "about", "into", "through", "during", 
        "before", "after", "above", "below", "up", "down", "out", "off", "over", "under", "again", "further"
    }

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
    if not cleaned:
        return ""
    
    try:
        from nltk.tokenize import word_tokenize
        tokens = word_tokenize(cleaned)
    except Exception:
        # Regex fallback tokenization if NLTK punkt is unavailable
        tokens = re.findall(r'\b[a-zA-Z0-9+#\.]+\b', cleaned)
        
    filtered_tokens = []
    for token in tokens:
        token = token.strip('.').strip()
        if token and token not in STOP_WORDS and len(token) > 1:
            if lemmatizer:
                try:
                    lemmatized = lemmatizer.lemmatize(token)
                except Exception:
                    lemmatized = token
            else:
                lemmatized = token
            filtered_tokens.append(lemmatized)
            
    res = " ".join(filtered_tokens)
    return res if res else cleaned

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
