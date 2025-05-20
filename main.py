import os
import json
import logging
from logging.handlers import RotatingFileHandler
import yaml
import uuid
import nltk
import numpy as np
import argparse
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer
from textblob import TextBlob
from rapidfuzz import fuzz
import re

# Custom LogRecord to handle missing request_id
class CustomLogRecord(logging.LogRecord):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_id = getattr(self, 'request_id', 'N/A')

logging.setLogRecordFactory(CustomLogRecord)

# Logging setup
os.makedirs('logs', exist_ok=True)
logger = logging.getLogger('PestIdentification')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('logs/pest_identification.log', maxBytes=1000000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(request_id)s] - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Download NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/wordnet')
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')

# Load configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Pest-related keywords for input validation
PEST_KEYWORDS = [
    "pest", "insect", "bug", "bugs", "mite", "worm", "caterpillar", "aphid", "whitefly", "mealybug", "spider mite",
    "leaf", "leaves", "stem", "root", "fruit", "flower", "yellowing", "wilting", "sticky", "mold", "spots", "holes",
    "crop", "plant", "tomato", "maize", "corn", "cotton", "cucumber", "pepper", "eggplant", "lettuce", "cabbage",
    "damage", "infestation", "infested", "chewed", "control", "spray", "trap", "webbing", "honeydew", "stunted"
]

# Knowledge Base
class KnowledgeBase:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = self.load_knowledge()

    def load_knowledge(self) -> Dict:
        if not os.path.exists(self.file_path):
            default_data = {
                "whitefly": {
                    "crops": ["tomato", "cotton", "cucumber", "pepper", "eggplant"],
                    "regions": ["tropical", "subtropical", "greenhouses"],
                    "symptoms": ["sticky leaves", "tiny white insects", "yellowing leaves", "sooty mold", "white bugs"],
                    "control_measures": {
                        "chemical": ["insecticidal soap (1% solution)", "pyriproxyfen (0.5 mL/L)"],
                        "biological": ["Encarsia formosa (5 wasps/m²)", "Eretmocerus spp."],
                        "cultural": ["yellow sticky traps (1 trap/10 m²)", "reflective mulch"]
                    },
                    "life_cycle": "Eggs hatch in 5-10 days, lifecycle completes in 20-30 days.",
                    "economic_impact": "Yield losses up to 50% in greenhouse crops.",
                    "environmental_conditions": {
                        "temperature": "20-30°C",
                        "humidity": "High",
                        "soil_type": "Well-drained"
                    },
                    "appearance": {
                        "color": ["white"],
                        "size": ["tiny", "1-2 mm"]
                    },
                    "synonyms": ["white fly", "Bemisia tabaci"],
                    "version": 1
                },
                "aphid": {
                    "crops": ["tomato", "lettuce", "cabbage", "beans", "maize"],
                    "regions": ["temperate", "tropical"],
                    "symptoms": ["curled leaves", "sticky honeydew", "stunted growth", "green or black insects", "leaf curl"],
                    "control_measures": {
                        "chemical": ["neem oil (2% solution)", "imidacloprid (0.3 mL/L)"],
                        "biological": ["ladybugs (10 beetles/m²)", "lacewings"],
                        "cultural": ["remove infested leaves", "use companion plants like marigolds"]
                    },
                    "life_cycle": "Reproduces every 7-10 days, multiple generations per season.",
                    "economic_impact": "Can reduce yield by 20-40% if untreated.",
                    "environmental_conditions": {
                        "temperature": "15-25°C",
                        "humidity": "Moderate",
                        "soil_type": "Fertile"
                    },
                    "appearance": {
                        "color": ["green", "black"],
                        "size": ["small", "1-3 mm"]
                    },
                    "synonyms": ["plant lice", "Aphidoidea"],
                    "version": 1
                },
                "spider mite": {
                    "crops": ["tomato", "cucumber", "strawberry", "grapes"],
                    "regions": ["tropical", "subtropical", "arid"],
                    "symptoms": ["stippled leaves", "fine webbing", "yellowing leaves", "tiny red or yellow mites", "speckled leaves"],
                    "control_measures": {
                        "chemical": ["abamectin (0.15 mL/L)", "spiromesifen (0.5 mL/L)"],
                        "biological": ["Phytoseiulus persimilis (10 mites/m²)"],
                        "cultural": ["increase humidity", "regular leaf washing"]
                    },
                    "life_cycle": "Eggs hatch in 3-5 days, lifecycle completes in 10-20 days.",
                    "economic_impact": "Can cause 30-60% yield loss in severe infestations.",
                    "environmental_conditions": {
                        "temperature": "25-35°C",
                        "humidity": "Low",
                        "soil_type": "Well-drained"
                    },
                    "appearance": {
                        "color": ["red", "yellow"],
                        "size": ["tiny", "<1 mm"]
                    },
                    "synonyms": ["red spider mite", "Tetranychus urticae"],
                    "version": 1
                },
                "mealybug": {
                    "crops": ["grapes", "citrus", "tomato", "ornamentals"],
                    "regions": ["tropical", "subtropical", "greenhouses"],
                    "symptoms": ["white cottony masses", "sticky honeydew", "sooty mold", "stunted growth"],
                    "control_measures": {
                        "chemical": ["spirotetramat (0.5 mL/L)", "insecticidal soap (1% solution)"],
                        "biological": ["Cryptolaemus montrouzieri (5 beetles/m²)"],
                        "cultural": ["prune infested areas", "use water sprays to dislodge"]
                    },
                    "life_cycle": "Eggs hatch in 7-10 days, lifecycle completes in 30-40 days.",
                    "economic_impact": "Can cause 20-50% yield loss in severe cases.",
                    "environmental_conditions": {
                        "temperature": "20-30°C",
                        "humidity": "Moderate to high",
                        "soil_type": "Well-drained"
                    },
                    "appearance": {
                        "color": ["white", "cottony"],
                        "size": ["small", "2-4 mm"]
                    },
                    "synonyms": ["mealy bug", "Pseudococcidae"],
                    "version": 1
                }
            }
            with open(self.file_path, 'w') as f:
                json.dump(default_data, f, indent=2)
            return default_data
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def search(self, query: str) -> Dict:
        logger.info(f"Searching knowledge base for: {query}")
        for pest, data in self.data.items():
            if fuzz.partial_ratio(query.lower(), pest.lower()) > 80:
                logger.info(f"Found data for: {query}")
                return {pest: data}
        return {}

    def get(self, pest: str) -> Dict:
        return self.data.get(pest, {})

# Text Analysis Tool
class TextAnalysisTool:
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)
        self.knowledge_base = KnowledgeBase(config['knowledge_base_file'])
        self.pest_reference = "Pests cause damage to crops with symptoms like yellowing leaves, sticky residue, holes, or insect presence."

    def is_pest_related(self, description: str) -> bool:
        """Check if the description is pest-related using keywords, semantic similarity, and symptom matching."""
        description_lower = description.lower()
        keyword_count = sum(keyword in description_lower for keyword in PEST_KEYWORDS)

        # Single keyword or symptom match is sufficient
        if keyword_count >= 1:
            return True
        
        # Semantic similarity check
        desc_embedding = self.model.encode(description)
        ref_embedding = self.model.encode(self.pest_reference)
        similarity = float(np.dot(desc_embedding, ref_embedding) / 
                          (np.linalg.norm(desc_embedding) * np.linalg.norm(ref_embedding)))
        
        # Fuzzy symptom matching
        blob = TextBlob(description_lower)
        tokens = blob.words
        for pest, data in self.knowledge_base.data.items():
            symptoms = [s.lower() for s in data.get("symptoms", [])]
            for token in tokens:
                for symptom in symptoms:
                    if fuzz.partial_ratio(token, symptom) > 85:  # Fuzzy match for symptoms
                        return True
        
        return similarity > 0.65  # Lowered threshold for broader detection

    async def analyze(self, description: str) -> Dict:
        logger.info(f"Analyzing description: {description}")
        if len(description) > config['max_description_length']:
            raise ValueError(f"Description exceeds maximum length of {config['max_description_length']} characters.")
        if not description.strip():
            raise ValueError("Description cannot be empty.")

        # Sanitize input
        description = re.sub(r'[^\w\s.,-]', '', description)
        description_lower = description.lower()  # Define description_lower for scoring
        logger.debug(f"Sanitized description: {description}, lowercase: {description_lower}")

        # Check if pest-related
        if not self.is_pest_related(description):
            logger.info(f"Non-pest-related input detected: {description}")
            return {
                "pests": [],
                "likely_pest": None,
                "user_guidance": [
                    "This doesn't seem pest-related.",
                    "Try describing issues like 'My tomato leaves have tiny white bugs.'",
                    "Key details to include:",
                    "- Symptoms (e.g., yellow leaves, holes, sticky residue)",
                    "- Crops affected (e.g., tomato, maize)",
                    "- Pest traits (e.g., color, size, flying)"
                ]
            }

        blob = TextBlob(description_lower)
        tokens = blob.words
        symptoms = [token for token in tokens if any(symptom in token for symptom in [
            "sticky", "yellowing", "mold", "tiny", "white", "curled", "stippled", "webbing", "honeydew", 
            "stunted", "bugs", "insects", "mites", "holes", "chewed", "speckled"
        ])]

        pest_scores = []
        for pest, data in self.knowledge_base.data.items():
            # Combine symptoms, crops, and appearance for scoring
            symptom_text = " ".join(data.get("symptoms", []) + data.get("crops", []) + 
                                   [f"{k} {v}" for k, v in data.get("appearance", {}).items()])
            symptom_embedding = self.model.encode(symptom_text)
            description_embedding = self.model.encode(description)
            similarity = float(np.dot(description_embedding, symptom_embedding) / 
                             (np.linalg.norm(description_embedding) * np.linalg.norm(symptom_embedding)))
            
            # Fuzzy symptom match boost
            pest_symptoms = [s.lower() for s in data.get("symptoms", [])]
            symptom_score = 0
            for token in tokens:
                for symptom in pest_symptoms:
                    if fuzz.partial_ratio(token, symptom) > 85:
                        symptom_score += 0.1  # Boost for each match
            
            # Crop and appearance match boost
            crop_score = 0.05 if any(crop in description_lower for crop in data.get("crops", [])) else 0
            appearance_score = 0.05 if any(color in description_lower for color in data.get("appearance", {}).get("color", [])) else 0
            
            final_score = similarity + symptom_score + crop_score + appearance_score
            if final_score > 0.5:  # Lowered threshold
                pest_scores.append({"pest": pest, "confidence": final_score})

        top_pests = sorted(pest_scores, key=lambda x: x["confidence"], reverse=True)[:3]
        likely_pest = top_pests[0]["pest"] if top_pests else None

        if not top_pests:
            logger.info("No pests identified with sufficient confidence")
            return {
                "pests": [],
                "likely_pest": None,
                "user_guidance": [
                    "Couldn't identify a pest. Please provide more details, e.g., 'My tomato leaves have tiny white bugs.'",
                    "Key details to include:",
                    "- Symptoms (e.g., yellow leaves, holes, sticky residue)",
                    "- Crops affected (e.g., tomato, maize)",
                    "- Pest traits (e.g., color, size, flying)"
                ]
            }

        logger.info(f"Identified pests: {[p['pest'] for p in top_pests]}")

        user_guidance = [
            "For better accuracy, include details like:",
            "- Symptoms (e.g., yellow leaves, holes, sticky residue)",
            "- Crops affected (e.g., tomato, maize)",
            "- Pest traits (e.g., color, size, flying)",
            "Example: 'My tomato plants have yellowing leaves and tiny white bugs.'"
        ]

        return {
            "pests": top_pests,
            "likely_pest": likely_pest,
            "user_guidance": user_guidance
        }

# AgroPestAgent
class AgroPestAgent:
    def __init__(self):
        self.knowledge_base = KnowledgeBase(config['knowledge_base_file'])
        self.text_tool = TextAnalysisTool(config['model_name'])
        logger.info("AgroPestAgent initialized")

    async def analyze(self, description: str) -> Dict:
        logger.info(f"Analyzing description: {description}")
        try:
            text_result = await self.text_tool.analyze(description)
            likely_pest = text_result.get("likely_pest")
            if not likely_pest:
                return {
                    "pest": None,
                    "report": "No pest identified or query is not pest-related.",
                    "text_result": text_result,
                    "chart": {},
                    "user_guidance": text_result["user_guidance"]
                }

            pest_data = self.knowledge_base.search(likely_pest).get(likely_pest, {})
            report = self.generate_report(description, likely_pest, pest_data, text_result)

            chart = {
                "type": "bar",
                "data": {
                    "labels": [p["pest"] for p in text_result["pests"]],
                    "datasets": [{
                        "label": "Confidence",
                        "data": [p["confidence"] for p in text_result["pests"]],
                        "backgroundColor": ["#4caf50", "#ff9800", "#f44336"],
                        "borderColor": ["#388e3c", "#f57c00", "#d32f2f"],
                        "borderWidth": 1
                    }]
                },
                "options": {
                    "scales": {
                        "y": {
                            "beginAtZero": True,
                            "title": {"display": True, "text": "Confidence Score"}
                        },
                        "x": {
                            "title": {"display": True, "text": "Pest"}
                        }
                    },
                    "plugins": {
                        "title": {"display": True, "text": "Pest Identification Confidence"}
                    }
                }
            }

            logger.info(f"Generated report for pest: {likely_pest}")
            return {
                "pest": likely_pest,
                "report": report,
                "text_result": text_result,
                "chart": chart,
                "user_guidance": text_result["user_guidance"]
            }
        except ValueError as e:
            logger.error(f"Analysis failed: {str(e)}")
            return {
                "pest": None,
                "report": str(e),
                "text_result": {"pests": [], "likely_pest": None, "user_guidance": [str(e)]},
                "chart": {},
                "user_guidance": [str(e)]
            }
        except Exception as e:
            logger.error(f"Unexpected error during analysis: {str(e)}")
            return {
                "pest": None,
                "report": f"Internal error: {str(e)}",
                "text_result": {"pests": [], "likely_pest": None, "user_guidance": [str(e)]},
                "chart": {},
                "user_guidance": [str(e)]
            }

    def generate_report(self, description: str, pest: str, pest_data: Dict, text_result: Dict) -> str:
        os.makedirs('reports', exist_ok=True)
        report_id = str(uuid.uuid4()).replace('-', '')
        report_path = f'reports/pest_report_{report_id}.txt'

        report = f"Pest Identification Report\n\n"
        report += f"Identified Pest: {pest}\n"
        report += f"Description: {description}\n"
        report += f"Confidence: {text_result['pests'][0]['confidence']:.2f}\n\n"
        report += "Details:\n"
        for key, value in pest_data.items():
            if isinstance(value, dict):
                report += f"  {key.replace('_', ' ').title()}:\n"
                for sub_key, sub_value in value.items():
                    report += f"    - {sub_key.replace('_', ' ').title()}: {sub_value}\n"
            else:
                report += f"  {key.replace('_', ' ').title()}: {value}\n"

        with open(report_path, 'w') as f:
            f.write(report)
        logger.info(f"Report saved to {report_path}")
        return report

# CLI Interface
def print_formatted_result(result: Dict, report_path: str):
    """Print the analysis result in a formatted manner to the console."""
    print("\n=== Pest Identification Result ===")
    
    pest = result.get("pest")
    print(f"\nIdentified Pest: {pest if pest else 'None'}")
    
    text_result = result.get("text_result", {})
    pests = text_result.get("pests", [])
    if pests:
        print("\nPossible Pests:")
        for p in pests:
            print(f"- {p['pest']} ({p['confidence']*100:.0f}%)")
    else:
        print("\nNo pests identified.")
    
    print(f"\nDetailed Report: (Saved to {report_path})")
    print(result.get("report", "No report available."))
    
    print("\nUser Guidance:")
    for guidance in result.get("user_guidance", []):
        print(f"- {guidance}")
    
    if result.get("chart", {}).get("data", {}).get("labels"):
        print("\nConfidence Scores (for visualization):")
        for label, confidence in zip(result["chart"]["data"]["labels"], result["chart"]["data"]["datasets"][0]["data"]):
            print(f"- {label}: {confidence:.2f}")
    else:
        print("\nNo chart data available.")

async def main():
    parser = argparse.ArgumentParser(description="Pest Identification CLI")
    parser.add_argument("--description", type=str, help="Pest issue description (e.g., 'My tomato plants have yellowing leaves and sticky residue')")
    args = parser.parse_args()

    try:
        agent = AgroPestAgent()
        
        # If description is provided via CLI argument, process it once and exit
        if args.description:
            request_id = str(uuid.uuid4())
            logger.info(f"Processing request {request_id}")
            description = args.description.strip()

            if not description:
                logger.error(f"Request {request_id} failed: Description cannot be empty")
                print("Error: Description cannot be empty.")
                return

            result = await agent.analyze(description)
            
            # Extract report path
            report_lines = result.get("report", "").split('\n')
            report_path = "Unknown"
            for line in report_lines:
                if line.startswith("Report saved to"):
                    report_path = line.split()[-1]
                    break
            
            # Save result to JSON
            os.makedirs('results', exist_ok=True)
            result_path = f'results/result_{request_id}.json'
            with open(result_path, 'w') as f:
                json.dump(result, f, indent=2)
            logger.info(f"Result saved to {result_path}")

            # Print formatted result
            print_formatted_result(result, report_path)
            logger.info(f"Request {request_id} processed successfully")
            return

        # Interactive mode: loop to keep asking for descriptions
        while True:
            request_id = str(uuid.uuid4())
            logger.info(f"Processing request {request_id}")

            print("\nEnter a description of the pest issue (e.g., 'My tomato plants have yellowing leaves and sticky residue')")
            description = input("Description: ").strip()

            # Exit loop if description is empty
            if not description:
                logger.info(f"Request {request_id}: Empty description provided, exiting")
                print("No description provided. Exiting.")
                break

            result = await agent.analyze(description)
            
            # Extract report path
            report_lines = result.get("report", "").split('\n')
            report_path = "Unknown"
            for line in report_lines:
                if line.startswith("Report saved to"):
                    report_path = line.split()[-1]
                    break
            
            # Save result to JSON
            os.makedirs('results', exist_ok=True)
            result_path = f'results/result_{request_id}.json'
            with open(result_path, 'w') as f:
                json.dump(result, f, indent=2)
            logger.info(f"Result saved to {result_path}")

            # Print formatted result
            print_formatted_result(result, report_path)
            logger.info(f"Request {request_id} processed successfully")

    except Exception as e:
        logger.error(f"Request {request_id} failed: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())