import os
import json
import logging
from textwrap import dedent, wrap
from typing import Dict, List, Any
import datetime
import asyncio
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ValidationError
from sentence_transformers import SentenceTransformer, util
from textblob import TextBlob, Word
import nltk
import re
from autocorrect import Speller
from rapidfuzz import fuzz
from pathlib import Path
import uuid

# Download required NLTK data
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
    description="Advanced expert system for identifying agricultural pests with transformer-based NLP and fuzzy matching.",
    version="2.3.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    chart: Dict[str, Any]  # Added for confidence visualization

class PestKnowledgeUpdate(BaseModel):
    pest: str
    symptoms: List[str]
    crops: List[str]
    regions: List[str]
    life_cycle: str
    economic_impact: str
    environmental_conditions: Dict[str, str]
    control_measures: Dict[str, List[str]]
    appearance: Dict[str, List[str]]
    synonyms: List[str]

class Config:
    def __init__(self):
        self.knowledge_base_file = os.getenv("KNOWLEDGE_BASE_FILE", "pest_knowledge.json")
        if not os.path.exists(self.knowledge_base_file):
            logger.info(f"Creating default knowledge base at {self.knowledge_base_file}")
            self.create_default_knowledge_base()

    def create_default_knowledge_base(self):
        default_knowledge = {
            "whitefly": {
                "crops": ["tomato", "cotton", "cucumber", "pepper", "eggplant", "sweet potato", "cassava"],
                "regions": ["tropical", "subtropical", "greenhouses"],
                "symptoms": ["sticky leaves", "tiny white insects", "yellowing leaves", "sooty mold", "virus transmission", "leaf wilting"],
                "control_measures": {
                    "chemical": ["insecticidal soap", "pyriproxyfen", "buprofezin", "dinotefuran"],
                    "biological": ["Encarsia formosa", "Eretmocerus spp.", "predatory beetles", "Macrolophus pygmaeus"],
                    "cultural": ["yellow sticky traps", "maintain weed-free fields", "use reflective mulch", "screen greenhouse vents"]
                },
                "life_cycle": "Eggs hatch in 5-10 days, lifecycle completes in 20-30 days.",
                "economic_impact": "Yield losses up to 50% in greenhouse crops; affects export quality due to virus transmission.",
                "environmental_conditions": {
                    "temperature": "20-30°C",
                    "humidity": "High",
                    "soil_type": "Well-drained"
                },
                "appearance": {
                    "color": ["white"],
                    "size": ["tiny", "small"]
                },
                "synonyms": ["white fly", "whiteflies", "Bemisia tabaci", "Trialeurodes vaporariorum"]
            }
        }
        try:
            with open(self.knowledge_base_file, "w", encoding='utf-8') as f:
                json.dump(default_knowledge, f, indent=2, ensure_ascii=False)
            logger.info(f"Default knowledge base created at {self.knowledge_base_file}")
        except Exception as e:
            logger.error(f"Failed to create default knowledge base: {str(e)}")
            raise FileNotFoundError(f"Failed to create knowledge base: {str(e)}")

class TextAnalysisTool:
    def __init__(self, knowledge_base: Dict):
        self.knowledge_base = knowledge_base
        self.model = None
        self.fallback = False
        self.speller = Speller(lang='en', fast=True)
        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("SentenceTransformer model loaded successfully")
            self.embeddings_cache = self._precompute_embeddings()
        except Exception as e:
            logger.warning(f"Failed to load SentenceTransformer: {str(e)}. Falling back to TextBlob.")
            self.fallback = True
            try:
                test_blob = TextBlob("test")
                test_blob.words.lemmatize()
                Word("test").synsets
                logger.info("TextBlob fallback initialized")
            except Exception as e:
                logger.error(f"TextBlob initialization failed: {str(e)}")
                raise RuntimeError(f"TextBlob initialization failed: {str(e)}")

    def _precompute_embeddings(self) -> Dict[str, Dict[str, Any]]:
        cache = {}
        texts = []
        metadata = []
        for pest, data in self.knowledge_base.items():
            cache[pest] = {"symptoms": [], "crops": [], "conditions": [], "synonyms": [], "appearance": []}
            for symptom in data.get("symptoms", []):
                texts.append(symptom)
                metadata.append((pest, "symptoms", symptom))
            for crop in data.get("crops", []):
                texts.append(crop)
                metadata.append((pest, "crops", crop))
            for key, value in data.get("environmental_conditions", {}).items():
                if isinstance(value, str):
                    texts.append(value)
                    metadata.append((pest, "conditions", f"{key}: {value}"))
            texts.append(pest)
            metadata.append((pest, "synonyms", pest))
            for synonym in data.get("synonyms", []):
                texts.append(synonym)
                metadata.append((pest, "synonyms", synonym))
            for key, values in data.get("appearance", {}).items():
                for value in values:
                    texts.append(value)
                    metadata.append((pest, "appearance", f"{key}: {value}"))
        if texts and not self.fallback:
            embeddings = self.model.encode(texts, convert_to_tensor=False)
            for (pest, category, text), embedding in zip(metadata, embeddings):
                cache[pest][category].append({"text": text, "embedding": embedding})
        return cache

    def _preprocess_text(self, text: str) -> Dict[str, Any]:
        try:
            text = text.lower().strip()
            text = re.sub(r'[^\w\s]', ' ', text)
            corrected = self.speller(text)
            tokens = corrected.split()
            colors = [t for t in tokens if t in {"white", "black", "green", "brown", "red", "yellow"}]
            sizes = [t for t in tokens if t in {"tiny", "small", "medium", "large"}]
            damage = [t for t in tokens if t in {"destroy", "damage", "eat", "holes", "yellowing", "wilting", "sticky"}]
            color = colors[-1] if colors else None
            return {
                "text": corrected,
                "original": text,
                "color": color,
                "size": sizes[0] if sizes else None,
                "damage": damage[0] if damage else None
            }
        except Exception as e:
            logger.error(f"Text preprocessing failed: {str(e)}")
            raise RuntimeError(f"Text preprocessing failed: {str(e)}")

    async def _get_synonyms(self, word: str) -> List[str]:
        if self.fallback:
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
        return [word]

    async def is_pest_related(self, description: str) -> bool:
        try:
            processed = self._preprocess_text(description)
            desc_text = processed["text"]
            pest_keywords = {
                "insect", "bug", "pest", "mite", "aphid", "whitefly", "spider", "caterpillar", "larvae",
                "damage", "yellowing", "wilting", "holes", "sticky", "leaves", "plant", "crop", "tomato",
                "cabbage", "potato", "vegetable", "fruit", "tree"
            }
            for pest, data in self.knowledge_base.items():
                pest_keywords.update(data.get("symptoms", []))
                pest_keywords.update(data.get("crops", []))
                pest_keywords.update(data.get("synonyms", []))
                pest_keywords.add(pest.lower())
            extended_keywords = set(pest_keywords)
            for keyword in pest_keywords:
                extended_keywords.update(await self._get_synonyms(keyword))
            crop_or_symptom_mentioned = any(
                fuzz.ratio(desc_text.lower(), kw) > 70 for kw in extended_keywords
            )
            if self.fallback:
                tokens = TextBlob(desc_text).words.lemmatize()
                return any(fuzz.ratio(token, kw) > 70 for token in tokens for kw in extended_keywords) or crop_or_symptom_mentioned
            else:
                desc_embedding = self.model.encode(desc_text, convert_to_tensor=False)
                for keyword in extended_keywords:
                    keyword_embedding = self.model.encode(keyword, convert_to_tensor=False)
                    similarity = util.cos_sim(desc_embedding, keyword_embedding).item()
                    if similarity > 0.4 or fuzz.ratio(desc_text, keyword) > 70:
                        return True
                return crop_or_symptom_mentioned
        except Exception as e:
            logger.error(f"Pest-related check failed: {str(e)}")
            return True

    def get_hint(self, processed: Dict[str, Any]) -> str:
        base_hint = dedent("""
            Please provide a detailed description of the pest issue, including symptoms (e.g., yellowing leaves), affected crops (e.g., tomato), and pest appearance (e.g., color, size).
            For example: "My tomato plants have yellowing leaves and tiny white insects."
        """).strip()
        specific = []
        if processed.get("color") and not processed.get("size"):
            specific.append("What is the size of the pests (e.g., tiny, small, large)?")
        if processed.get("damage") and not processed.get("color"):
            specific.append("What is the color of the pests (e.g., white, black, green)?")
        if "vegetable" in processed["text"] and not any(c in processed["text"] for c in ["tomato", "cabbage", "potato"]):
            specific.append("Which vegetables are affected (e.g., tomato, cabbage, potato)?")
        if not specific:
            specific.append("Are the pests flying or crawling? Is there sticky residue or mold? Where are they located (e.g., leaf undersides)?")
        return f"{base_hint}\n\nAdditional details needed:\n- " + "\n- ".join(specific)

    async def analyze(self, description: str) -> Dict[str, Any]:
        try:
            if not isinstance(description, str):
                logger.error("Description is not a string")
                return {"error": "Description must be a string"}
            if not description.strip():
                logger.error("Description is empty")
                return {"error": "Description cannot be empty"}

            processed = self._preprocess_text(description)
            desc_text = processed["text"]
            if not await self.is_pest_related(description):
                logger.warning("Description may not be pest-related")
                return {"warning": "Description may not be pest-related. Assuming pest issue.", "hint": self.get_hint(processed)}

            pest_scores = []
            if self.fallback:
                desc_tokens = TextBlob(desc_text).words.lemmatize()
                desc_text_blob = " ".join(desc_tokens)
                for pest, data in self.knowledge_base.items():
                    score = 0
                    matches = {"symptoms": [], "crops": [], "conditions": [], "synonyms": [], "appearance": []}
                    symptoms = data.get("symptoms", [])
                    for symptom in symptoms:
                        symptom_tokens = TextBlob(self._preprocess_text(symptom)["text"]).words.lemmatize()
                        symptom_text = " ".join(symptom_tokens)
                        if symptom.lower() in desc_text_blob.lower() or any(fuzz.ratio(t, s) > 70 for t in desc_tokens for s in symptom_tokens):
                            score += 2
                            matches["symptoms"].append(symptom)
                        for syn in await self._get_synonyms(symptom_text):
                            if syn in desc_text_blob:
                                score += 1.5
                                matches["symptoms"].append(f"{symptom} (via synonym: {syn})")
                    crops = data.get("crops", [])
                    for crop in crops:
                        if fuzz.ratio(crop.lower(), desc_text_blob) > 70:
                            score += 1
                            matches["crops"].append(crop)
                    env_conditions = data.get("environmental_conditions", {})
                    for key, value in env_conditions.items():
                        if isinstance(value, str) and value.lower() in desc_text_blob:
                            score += 0.5
                            matches["conditions"].append(f"{key}: {value}")
                    pest_synonyms = await self._get_synonyms(pest) + data.get("synonyms", [])
                    if any(fuzz.ratio(syn, desc_text_blob) > 70 for syn in [pest.lower()] + pest_synonyms):
                        score += 1.5
                        matches["synonyms"].append(f"Pest name: {pest}")
                    appearance = data.get("appearance", {})
                    if processed["color"] and processed["color"] in appearance.get("color", []):
                        score += 1
                        matches["appearance"].append(f"Color: {processed['color']}")
                    if processed["size"] and processed["size"] in appearance.get("size", []):
                        score += 1
                        matches["appearance"].append(f"Size: {processed['size']}")
                    if len(matches["symptoms"]) > 1:
                        score *= 1.2
                    if score > 0:
                        pest_scores.append({
                            "pest": pest,
                            "score": score,
                            "confidence": min(score / 10, 1.0),
                            "matches": matches
                        })
            else:
                desc_embedding = self.model.encode(desc_text, convert_to_tensor=False)
                for pest, cache in self.embeddings_cache.items():
                    score = 0
                    matches = {"symptoms": [], "crops": [], "conditions": [], "synonyms": [], "appearance": []}
                    for item in cache["symptoms"]:
                        similarity = util.cos_sim(desc_embedding, item["embedding"]).item()
                        if similarity > 0.4 or fuzz.ratio(item["text"], desc_text) > 70:
                            score += 2 * max(similarity, fuzz.ratio(item["text"], desc_text) / 100)
                            matches["symptoms"].append(f"{item['text']} (similarity: {similarity:.2f})")
                    for item in cache["crops"]:
                        similarity = util.cos_sim(desc_embedding, item["embedding"]).item()
                        if similarity > 0.4 or fuzz.ratio(item["text"], desc_text) > 70:
                            score += 1 * max(similarity, fuzz.ratio(item["text"], desc_text) / 100)
                            matches["crops"].append(f"{item['text']} (similarity: {similarity:.2f})")
                    for item in cache["conditions"]:
                        similarity = util.cos_sim(desc_embedding, item["embedding"]).item()
                        if similarity > 0.4:
                            score += 0.5 * similarity
                            matches["conditions"].append(f"{item['text']} (similarity: {similarity:.2f})")
                    for item in cache["synonyms"]:
                        similarity = util.cos_sim(desc_embedding, item["embedding"]).item()
                        if similarity > 0.4 or fuzz.ratio(item["text"], desc_text) > 70:
                            score += 1.5 * max(similarity, fuzz.ratio(item["text"], desc_text) / 100)
                            matches["synonyms"].append(f"Pest name: {item['text']} (similarity: {similarity:.2f})")
                    appearance = self.knowledge_base[pest].get("appearance", {})
                    if processed["color"] and processed["color"] in appearance.get("color", []):
                        score += 1
                        matches["appearance"].append(f"Color: {processed['color']}")
                    if processed["size"] and processed["size"] in appearance.get("size", []):
                        score += 1
                        matches["appearance"].append(f"Size: {processed['size']}")
                    if len(matches["symptoms"]) > 1:
                        score *= 1.2
                    if score > 0:
                        confidence = 1 / (1 + np.exp(-score / 2))
                        pest_scores.append({
                            "pest": pest,
                            "score": score,
                            "confidence": min(confidence, 1.0),
                            "matches": matches
                        })

            if not pest_scores:
                logger.info("No pests matched the description")
                return {
                    "warning": "No pests matched exactly. Assuming unknown pest.",
                    "hint": self.get_hint(processed),
                    "pests": [{
                        "pest": "Unknown",
                        "score": 0,
                        "confidence": 0.0,
                        "matches": {"symptoms": [], "crops": [], "conditions": [], "synonyms": [], "appearance": []}
                    }]
                }

            pest_scores.sort(key=lambda x: x["score"], reverse=True)
            top_pests = [p for p in pest_scores if p["score"] >= pest_scores[0]["score"] * 0.7][:3]
            logger.info(f"Identified pests: {[p['pest'] for p in top_pests]}")
            return {"pests": top_pests}
        except Exception as e:
            logger.error(f"Text analysis error: {str(e)}")
            return {"error": f"Text analysis failed: {str(e)}"}

class KnowledgeBase:
    def __init__(self, json_file: str):
        self.json_file = json_file
        self.knowledge = {}
        self.load()

    def load(self):
        json_path = os.path.abspath(self.json_file)
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

    def update(self, pest: str, data: Dict[str, Any]):
        try:
            self.knowledge[pest] = data
            with open(self.json_file, "w", encoding='utf-8') as f:
                json.dump(self.knowledge, f, indent=2, ensure_ascii=False)
            logger.info(f"Updated knowledge base with pest: {pest}")
        except Exception as e:
            logger.error(f"Knowledge base update error: {str(e)}")
            raise

class AgroPestAgent:
    def __init__(self):
        self.config = Config()
        self.knowledge_base = KnowledgeBase(self.config.knowledge_base_file)
        self.text_tool = TextAnalysisTool(self.knowledge_base.knowledge)
        logger.info("AgroPestAgent initialized")

    async def analyze(self, description: str) -> Dict[str, Any]:
        try:
            logger.info(f"Analyzing description: {description}")
            text_result = await self.text_tool.analyze(description)
            if "error" in text_result:
                logger.error(f"Text analysis failed: {text_result['error']}")
                return text_result

            top_pests = text_result.get("pests", [{"pest": "Unknown", "confidence": 0}])
            likely_pest = top_pests[0]["pest"]
            pest_data = self.knowledge_base.search(likely_pest).get(likely_pest, {})
            report = self.generate_report(
                likely_pest=likely_pest,
                text_pests=top_pests,
                pest_data=pest_data,
                processed=self.text_tool._preprocess_text(description)
            )
            chart = self.generate_chart(top_pests)
            logger.info(f"Generated report for pest: {likely_pest}")
            return {
                "pest": likely_pest,
                "report": report,
                "text_result": text_result,
                "chart": chart
            }
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}

    def generate_chart(self, top_pests: List[Dict]) -> Dict[str, Any]:
        labels = [p["pest"] for p in top_pests]
        confidences = [p["confidence"] for p in top_pests]
        colors = ["#4CAF50", "#FFC107", "#F44336"]  # Green, Yellow, Red
        return {
            "type": "bar",
            "data": {
                "labels": labels,
                "datasets": [{
                    "label": "Confidence Score",
                    "data": confidences,
                    "backgroundColor": colors[:len(labels)],
                    "borderColor": colors[:len(labels)],
                    "borderWidth": 1
                }]
            },
            "options": {
                "scales": {
                    "y": {
                        "beginAtZero": True,
                        "max": 1,
                        "title": {
                            "display": True,
                            "text": "Confidence"
                        }
                    },
                    "x": {
                        "title": {
                            "display": True,
                            "text": "Possible Pests"
                        }
                    }
                },
                "plugins": {
                    "title": {
                        "display": True,
                        "text": "Pest Identification Confidence"
                    }
                }
            }
        }

    def generate_report(self, likely_pest: str, text_pests: List[Dict], pest_data: Dict, processed: Dict[str, Any]) -> str:
        control_measures = pest_data.get("control_measures", {})
        confidence = text_pests[0]["confidence"] if text_pests else 0
        matched_indicators = []
        for match_type in ["symptoms", "crops", "conditions", "synonyms", "appearance"]:
            matched_indicators.extend(text_pests[0]["matches"].get(match_type, []))
        next_steps = self.get_next_steps(likely_pest, processed)
        sections = [
            "**Pest Identification Report**\n",
            "**Identified Pest**\n",
            f"**Pest**: {likely_pest}\n",
            f"**Confidence**: {confidence:.2%}\n",
            "**Analysis Details**\n",
            f"**Possible Pests**: {', '.join(f'{p['pest']} ({p['confidence']:.2%})' for p in text_pests)}\n",
            f"**Matched Indicators**: {', '.join(matched_indicators) or 'None'}\n",
            "**Pest Information**\n",
            f"**Crops Affected**: {', '.join(pest_data.get('crops', ['Unknown']))}\n",
            f"**Regions**: {', '.join(pest_data.get('regions', ['Unknown']))}\n",
            f"**Symptoms**: {', '.join(pest_data.get('symptoms', ['Unknown']))}\n",
            f"**Appearance**: Color: {', '.join(pest_data.get('appearance', {}).get('color', ['Unknown']))}, Size: {', '.join(pest_data.get('appearance', {}).get('size', ['Unknown']))}\n",
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
            "**Next Steps**\n" + "\n".join(f"- {step}" for step in next_steps) + "\n",
            f"**Generated on**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        ]
        wrapped_report = []
        for line in sections:
            wrapped_lines = wrap(line, width=80, subsequent_indent="  ")
            wrapped_report.extend(wrapped_lines)
        report = "\n".join(wrapped_report)
        report_path = f"pest_report_{uuid.uuid4().hex}.txt"
        try:
            with open(report_path, "w", encoding='utf-8') as f:
                f.write(report)
            logger.info(f"Report saved to {report_path}")
        except Exception as e:
            logger.error(f"Report save error: {str(e)}")
        return report

    def get_next_steps(self, pest: str, processed: Dict[str, Any]) -> List[str]:
        steps = []
        if pest == "whitefly":
            steps.append("Inspect leaf undersides for eggs or nymphs, which are tiny and white.")
            steps.append("Apply insecticidal soap or neem oil, targeting leaf undersides.")
            steps.append("Check nearby plants for spread, as whiteflies are highly mobile.")
        elif pest == "aphid":
            steps.append("Check for sticky honeydew or sooty mold on leaves.")
            steps.append("Use a strong water spray to dislodge aphids or apply neem oil.")
            steps.append("Introduce ladybugs or lacewings to control aphid populations.")
        else:
            steps.append("Inspect affected plants closely to confirm pest presence.")
            steps.append("Apply general pest control measures like neem oil or insecticidal soap.")
            steps.append("Monitor nearby crops for similar symptoms.")
        steps.append(self.text_tool.get_hint(processed))
        return steps

@app.post("/identify-pest", response_model=PestResponse)
async def identify_pest(description: PestDescription):
    try:
        logger.info(f"Received request with payload: {description.dict()}")
        agent = AgroPestAgent()
        result = await agent.analyze(description.description)
        if "error" in result:
            logger.error(f"API error: {result['error']}")
            raise HTTPException(status_code=400, detail=result)
        return result
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/update-knowledge")
async def update_knowledge(update: PestKnowledgeUpdate):
    try:
        logger.info(f"Received knowledge update request for pest: {update.pest}")
        agent = AgroPestAgent()
        agent.knowledge_base.update(update.pest, update.dict())
        agent.text_tool = TextAnalysisTool(agent.knowledge_base.knowledge)
        logger.info(f"Knowledge base updated and embeddings refreshed for pest: {update.pest}")
        return {"message": f"Knowledge base updated for pest: {update.pest}"}
    except ValidationError as e:
        logger.error(f"Validation error in knowledge update: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid data format: {str(e)}")
    except Exception as e:
        logger.error(f"Knowledge update error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)