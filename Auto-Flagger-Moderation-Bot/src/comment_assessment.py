import requests
import os
import openai
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.pipeline import make_pipeline

def assess_comment(comment_text, subreddit_rules):
    chatgpt_api_endpoint = os.environ['CHATGPT_API_ENDPOINT']
    chatgpt_api_key = os.environ['CHATGPT_API_KEY']

    headers = {
        'Authorization': f'Bearer {chatgpt_api_key}',
    }
    data = {
        'text': comment_text,
        'rules': subreddit_rules,
    }
    response = requests.post(chatgpt_api_endpoint, headers=headers, json=data)
    result = response.json()
    
    return result['score']

def assess_comment_relevance(comment_text, keywords):
    comment_tokens = comment_text.lower().split()
    
    keyword_matches = sum(1 for keyword in keywords if keyword.lower() in comment_tokens)
    
    relevance_score = (keyword_matches / len(keywords)) * 100
    
    return relevance_score

api_key = os.environ['OPEN_AI_API_KEY']

openai.api_key = api_key

def assess_comment_toxicity(comment_text):
    try:
        prompt = f"Assess the toxicity of the following comment:\n{comment_text}\nToxicity score:"

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1
        )

        score = float(response.choices[0].text.strip())

        scaled_score = __scale_to_1_to_5(score)

        return scaled_score
      
    except Exception as e:
        print(f"Error assessing toxicity: {str(e)}")
        return None

def __scale_to_1_to_5(toxicity_score):
    return 1 + (toxicity_score * 4)

with open('spam_classifier_model.pkl', 'rb') as model_file:
    spam_classifier = pickle.load(model_file)

tfidf_vectorizer = TfidfVectorizer(stop_words='english')

spam_classifier_pipeline = make_pipeline(tfidf_vectorizer, spam_classifier)

def assess_comment_spam(comment_text):
    try:

        spam_probability = spam_classifier_pipeline.predict_proba([comment_text])[0][1]

        if spam_probability > 0.5:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error assessing spam: {str(e)}")
        return None