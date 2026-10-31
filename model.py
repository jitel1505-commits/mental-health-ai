import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

class MentalHealthRiskAnalyzer:
    def __init__(self):
        # Training data: sample text inputs mapped to risk tiers (0: Low, 1: Moderate, 2: High/Urgent)
        X_train = [
            "I feel a bit stressed about my exams next week.",
            "Feeling slightly down today, but hanging in there.",
            "Had a good day overall, just minor work fatigue.",
            "I am feeling constantly anxious and having trouble sleeping for days.",
            "Everything feels overwhelming and I am losing interest in my hobbies.",
            "I feel lonely and burnt out most of the time now.",
            "I feel completely hopeless and want to end it all.",
            "I can't take this pain anymore, I don't want to wake up.",
            "Thinking about hurting myself because there is no way out."
        ]
        y_train = [0, 0, 0, 1, 1, 1, 2, 2, 2] # 0 = Low, 1 = Moderate, 2 = High Risk
        
        # Build NLP Pipeline
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), stop_words='english')),
            ('clf', LogisticRegression(class_weight='balanced'))
        ])
        self.pipeline.fit(X_train, y_train)
        
        # Critical keywords triggering mandatory crisis triage
        self.crisis_keywords = ['suicide', 'kill', 'die', 'hurt myself', 'end it all', 'want to end', 'hopeless']

    def analyze(self, text: str) -> dict:
        text_lower = text.lower()
        
        # Step 1: Safety override for critical crisis keywords
        is_crisis = any(kw in text_lower for kw in self.crisis_keywords)
        
        if is_crisis:
            prediction = 2
            confidence = 0.99
        else:
            prediction = self.pipeline.predict([text])[0]
            probabilities = self.pipeline.predict_proba([text])[0]
            confidence = float(np.max(probabilities))
            
        # Step 2: Map prediction to clinical outputs
        risk_levels = {
            0: {
                "level": "Low Risk / Mild Stress",
                "color": "green",
                "guidance": "Your input indicates mild everyday stress or normal emotional fluctuations.",
                "first_aid": "Practice mindfulness, maintain regular sleep schedules, and talk to friends or family.",
                "triage": "Monitor symptoms. Routine self-care is recommended."
            },
            1: {
                "level": "Moderate Risk / Elevated Distress",
                "color": "orange",
                "guidance": "Your input suggests persistent anxiety, burnout, or emotional fatigue that is impacting your day.",
                "first_aid": "Consider structured breathing exercises, journaling, reducing caffeine, and scheduling a check-in with a counselor.",
                "triage": "Recommended: Consult a campus counselor or primary care mental health professional within the week."
            },
            2: {
                "level": "High Risk / Urgent Professional Support Needed",
                "color": "red",
                "guidance": "Your input highlights severe emotional distress or statements of self-harm risk.",
                "first_aid": "Reach out immediately to a trusted emergency contact, mental health crisis helpline, or emergency services.",
                "triage": "URGENT TRIAGE: Immediate psychiatric or emergency medical intervention required."
            }
        }
        
        result = risk_levels[prediction]
        result["confidence_score"] = round(confidence * 100, 2)
        return result
