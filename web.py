import os
import json
import logging
from textwrap import dedent, wrap
from typing import Dict, List, Any
import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from textblob import TextBlob, Word
import nltk
from nltk.tokenize import word_tokenize
import re

# Attempt to download required NLTK data
def ensure_nltk_corpora():
    corpora = ['punkt', 'wordnet', 'averaged_perceptron_tagger', 'brown', 'conll2000', 'movie_reviews', 'omw-1.4']
    for corpus in corpora:
        try:
            nltk.data.find(f'tokenizers/{corpus}' if corpus == 'punkt' else f'corpora/{corpus}')
        except LookupError:
            logging.info(f"Downloading NLTK corpus: {corpus}")
            nltk.download(corpus, quiet=True)

try:
    ensure_nltk_corpora()
except Exception as e:
    logging.error(f"Failed to download NLTK corpora: {str(e)}")

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/pest_identification.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Pest Identification API",
    description="Expert system for identifying agricultural pests with TextBlob-based NLP analysis.",
    version="1.2.2"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "http://localhost:8080", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Pydantic models
class PestDescription(BaseModel):
    description: str

class PestResponse(BaseModel):
    pest: str
    report: str
    text_result: Dict[str, List[Dict[str, Any]]]

class Config:
    def __init__(self):
        self.knowledge_base_file = os.getenv("KNOWLEDGE_BASE_FILE", "pest_knowledge.json")
        if not os.path.exists(self.knowledge_base_file):
            logger.error(f"Knowledge base file not found: {self.knowledge_base_file}")
            raise FileNotFoundError(f"Knowledge base file not found: {self.knowledge_base_file}")

class TextAnalysisTool:
    def __init__(self, knowledge_base: Dict):
        self.knowledge_base = knowledge_base
        try:
            # Test TextBlob functionality
            test_blob = TextBlob("test")
            test_blob.words.lemmatize()
            Word("test").synsets
            logger.info("TextAnalysisTool initialized with TextBlob and NLTK")
        except Exception as e:
            logger.error(f"TextBlob initialization failed: {str(e)}")
            raise RuntimeError(
                "TextBlob initialization failed. Ensure NLTK corpora are installed by running:\n"
                "python -m textblob.download_corpora\n"
                f"Error: {str(e)}"
            )

    def _preprocess_text(self, text: str) -> List[str]:
        """Tokenize, lemmatize, and clean the input text."""
        try:
            text = text.lower().strip()
            text = re.sub(r'[^\w\s]', ' ', text)
            blob = TextBlob(text)
            tokens = blob.words.lemmatize()
            return tokens
        except Exception as e:
            logger.error(f"Text preprocessing failed: {str(e)}")
            raise RuntimeError(f"Text preprocessing failed: {str(e)}")

    def _get_synonyms(self, word: str) -> List[str]:
        """Get synonyms for a word using TextBlob's WordNet integration."""
        try:
            synonyms = set()
            word_obj = Word(word.lower())
            for synset in word_obj.synsets:
                for lemma in synset.lemmas():
                    synonyms.add(lemma.name().lower().replace('_', ' '))
            return list(synonyms)
        except Exception as e:
            logger.error(f"Synonym lookup failed for '{word}': {str(e)}")
            return []

    def is_pest_related(self, description: str) -> bool:
        """Check if the description is related to agricultural pests."""
        try:
            pest_keywords = set()
            for pest, data in self.knowledge_base.items():
                pest_keywords.update(data.get("symptoms", []))
                pest_keywords.update(data.get("crops", []))
                pest_keywords.add(pest.lower())
            extended_keywords = set()
            for keyword in pest_keywords:
                extended_keywords.add(keyword.lower())
                extended_keywords.update(self._get_synonyms(keyword))

            tokens = self._preprocess_text(description)
            return any(token in extended_keywords for token in tokens)
        except Exception as e:
            logger.error(f"Pest-related check failed: {str(e)}")
            raise RuntimeError(f"Pest-related check failed: {str(e)}")

    def get_hint(self) -> str:
        """Provide a user-friendly hint for correcting the description."""
        return dedent("""
            Please provide a description related to agricultural pests, including specific symptoms or affected crops.
            For example: "My tomato plants have yellowing leaves and sticky residue" or 
            "I found holes in the leaves of my cabbage."
        """).strip()

    def analyze(self, description: str) -> Dict[str, List[Dict[str, Any]]]:
        try:
            if not isinstance(description, str):
                logger.error("Description is not a string")
                return {"error": "Description must be a string"}
            if not description.strip():
                logger.error("Description is empty")
                return {"error": "Description cannot be empty"}
            if not self.is_pest_related(description):
                logger.warning("Description is not pest-related")
                return {"error": "Description does not appear to be related to agricultural pests.", "hint": self.get_hint()}

            desc_tokens = self._preprocess_text(description)
            desc_text = " ".join(desc_tokens)

            pest_scores = []
            for pest, data in self.knowledge_base.items():
                score = 0
                matches = {"symptoms": [], "crops": [], "conditions": []}

                # Symptom matching (high weight)
                symptoms = data.get("symptoms", [])
                for symptom in symptoms:
                    symptom_tokens = self._preprocess_text(symptom)
                    symptom_text = " ".join(symptom_tokens)
                    if symptom.lower() in description.lower() or any(t in desc_tokens for t in symptom_tokens):
                        score += 2
                        matches["symptoms"].append(symptom)
                    # Check synonyms
                    for syn in self._get_synonyms(symptom_text):
                        if syn in desc_text:
                            score += 1.5
                            matches["symptoms"].append(f"{symptom} (via synonym: {syn})")

                # Crop matching (medium weight)
                crops = data.get("crops", [])
                for crop in crops:
                    if crop.lower() in desc_tokens:
                        score += 1
                        matches["crops"].append(crop)

                # Environmental condition matching (low weight)
                env_conditions = data.get("environmental_conditions", {})
                for key, value in env_conditions.items():
                    if isinstance(value, str) and value.lower() in desc_text:
                        score += 0.5
                        matches["conditions"].append(f"{key}: {value}")

                # Boost score for pest name or synonyms
                pest_synonyms = self._get_synonyms(pest)
                if pest.lower() in desc_tokens or any(syn in desc_tokens for syn in pest_synonyms):
                    score += 1.5
                    matches["symptoms"].append(f"Pest name: {pest}")

                # Adjust score based on symptom specificity
                if len(matches["symptoms"]) > 1:
                    score *= 1.2  # Bonus for multiple symptom matches
                if len(matches["symptoms"]) == 0 and len(matches["crops"]) == 0:
                    score = 0  # No relevant matches

                if score > 0:
                    pest_scores.append({
                        "pest": pest,
                        "score": score,
                        "confidence": min(score / 10, 1.0),  # Normalize to 0-1
                        "matches": matches
                    })

            if not pest_scores:
                logger.info("No pests matched the description")
                return {"error": "No pests matched the description.", "hint": self.get_hint()}

            pest_scores.sort(key=lambda x: x["score"], reverse=True)
            top_pests = [p for p in pest_scores if p["score"] >= pest_scores[0]["score"] * 0.7]
            logger.info(f"Identified pests: {[p['pest'] for p in top_pests]}")
            return {"pests": top_pests}
        except Exception as e:
            logger.error(f"Text analysis error: {str(e)}")
            return {
                "error": (
                    f"Text analysis failed: {str(e)}\n"
                    "This may be due to missing NLTK corpora. Please run:\n"
                    "python -m textblob.download_corpora\n"
                    "or check https://nltk.org/data.html for manual installation."
                )
            }

class KnowledgeBase:
    def __init__(self, json_file: str):
        self.knowledge = {}
        json_path = os.path.abspath(json_file)
        try:
            if os.path.exists(json_path):
                with open(json_path, "r", encoding='utf-8') as f:
                    self.knowledge = json.load(f)
                logger.info(f"Loaded knowledge base from {json_path}")
            else:
                logger.error(f"Knowledge base not found: {json_path}")
                raise FileNotFoundError(f"Knowledge base not found: {json_path}")
        except Exception as e:
            logger.error(f"Knowledge base load error: {str(e)}")
            raise

    def search(self, query: str) -> Dict[str, Any]:
        query = query.lower().strip()
        if not query:
            logger.error("Empty query")
            return {}
        if query in self.knowledge:
            logger.info(f"Found data for: {query}")
            return {query: self.knowledge[query]}
        logger.info(f"No match for {query}")
        return {}

class AgroPestAgent:
    def __init__(self):
        self.config = Config()
        self.knowledge_base = KnowledgeBase(self.config.knowledge_base_file)
        self.text_tool = TextAnalysisTool(self.knowledge_base.knowledge)
        logger.info("AgroPestAgent initialized")

    def analyze(self, description: str) -> Dict[str, Any]:
        try:
            logger.info(f"Analyzing description: {description}")
            text_result = self.text_tool.analyze(description)
            if "error" in text_result:
                logger.error(f"Text analysis failed: {text_result['error']}")
                return text_result

            top_pests = text_result.get("pests", [{"pest": "unknown", "confidence": 0}])
            likely_pest = top_pests[0]["pest"]
            pest_data = self.knowledge_base.search(likely_pest).get(likely_pest, {})
            report = self.generate_report(
                likely_pest=likely_pest,
                text_pests=top_pests,
                pest_data=pest_data
            )
            logger.info(f"Generated report for pest: {likely_pest}")
            return {
                "pest": likely_pest,
                "report": report,
                "text_result": text_result
            }
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}

    def generate_report(self, likely_pest: str, text_pests: List[Dict], pest_data: Dict) -> str:
        control_measures = pest_data.get("control_measures", {})
        confidence = text_pests[0]["confidence"] if text_pests else 0
        matched_indicators = []
        for match_type in ["symptoms", "crops", "conditions"]:
            matched_indicators.extend(text_pests[0]["matches"][match_type])
        sections = [
            "**Pest Identification Report**\n",
            "**Identified Pest**\n",
            f"**Pest**: {likely_pest}\n",
            f"**Confidence**: {confidence:.2%}\n",
            "**Analysis Details**\n",
            f"**Possible Pests**: {', '.join(p['pest'] for p in text_pests)}\n",
            f"**Matched Indicators**: {', '.join(matched_indicators) or 'None'}\n",
            "**Pest Information**\n",
            f"**Crops Affected**: {', '.join(pest_data.get('crops', ['Unknown']))}\n",
            f"**Regions**: {', '.join(pest_data.get('regions', ['Unknown']))}\n",
            f"**Symptoms**: {', '.join(pest_data.get('symptoms', ['Unknown']))}\n",
            f"**Life Cycle**: {pest_data.get('life_cycle', 'Unknown')}\n",
            f"**Economic Impact**: {pest_data.get('economic_impact', 'Unknown')}\n",
            "**Environmental Conditions**\n",
            f"**Temperature**: {pest_data.get('environmental_conditions', {}).get('temperature', 'Unknown')}\n",
            f"**Humidity**: {pest_data.get('environmental_conditions', {}).get('humidity', 'Unknown')}\n",
            f"**Soil Type**: {pest_data.get('environmental_conditions', {}).get('soil_type', 'Unknown')}\n",
            "**Control Measures**\n",
            f"**Chemical**: {', '.join(control_measures.get('chemical', ['None']))}\n",
            f"**Biological**: {', '.join(control_measures.get('biological', ['None']))}\n",
            f"**Cultural**: {', '.join(control_measures.get('cultural', ['None']))}\n",
            f"**Generated on**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        ]
        wrapped_report = []
        for line in sections:
            wrapped_lines = wrap(line, width=80, subsequent_indent="  ")
            wrapped_report.extend(wrapped_lines)
        report = "\n".join(wrapped_report)
        report_path = f"pest_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(report_path, "w", encoding='utf-8') as f:
                f.write(report)
            logger.info(f"Report saved to {report_path}")
        except Exception as e:
            logger.error(f"Report save error: {str(e)}")
        return report

@app.post("/identify-pest", response_model=PestResponse)
async def identify_pest(description: PestDescription):
    try:
        logger.info(f"Received request with payload: {description.dict()}")
        agent = AgroPestAgent()
        result = agent.analyze(description.description)
        if "error" in result:
            logger.error(f"API error: {result['error']}")
            raise HTTPException(status_code=400, detail=result)
        return result
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
