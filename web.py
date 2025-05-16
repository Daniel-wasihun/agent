import os
import json
import logging
from textwrap import dedent, wrap
from typing import Dict, List
import datetime
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/pest_identification.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)
app = FastAPI(
    title="Pest Identification API",
    description="API for identifying agricultural pests.",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
class PestDescription(BaseModel):
    description: str
class PestResponse(BaseModel):
    pest: str
    report: str
    gemini_result: str
    text_result: Dict[str, List[str]]
class Config:
    def __init__(self):
        load_dotenv()
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.gen_ai_model = os.getenv("GEN_AI_MODEL", "gemini-pro")
        self.knowledge_base_file = os.getenv("KNOWLEDGE_BASE_FILE", "pest_knowledge.json")
        if not self.gemini_api_key:
            logger.error("Missing GEMINI_API_KEY")
            raise ValueError("GEMINI_API_KEY required")
class TextAnalysisTool:
    def __init__(self):
        self.keyword_map = {
            "yellowing": ["aphid", "whitefly", "spider_mite", "leafhopper", "mealybug", "scale_insect"],
            "sticky": ["aphid", "whitefly", "mealybug"],
            "tiny white": ["whitefly"],
            "chewed": ["fall_armyworm", "cutworm", "corn_earworm", "colorado_potato_beetle", "armyworm"],
            "holes": ["fall_armyworm", "cabbage_looper", "diamondback_moth", "corn_earworm"],
            "wilting": ["thrips", "wireworm", "stem_borer"],
            "discoloration": ["spider_mite", "leafhopper", "green_stink_bug"],
            "webbing": ["spider_mite", "diamondback_moth"],
            "sooty mold": ["whitefly", "mealybug", "scale_insect"],
            "frass": ["fall_armyworm", "corn_earworm", "cabbage_looper", "stem_borer", "armyworm"],
            "tunneling": ["stem_borer", "wireworm"],
            "bronzing": ["thrips", "spider_mite"],
            "defoliation": ["colorado_potato_beetle", "armyworm", "fall_armyworm"],
            "stippling": ["spider_mite", "thrips", "leafhopper"],
            "galls": ["scale_insect"],
            "rotting fruit": ["fruit_fly"],
            "boll damage": ["boll_weevil"],
            "sap sucking": ["leafhopper", "green_stink_bug", "tarnished_plant_bug"],
            "plant distortion": ["tarnished_plant_bug", "thrips"],
            "punctured": ["fruit_fly", "boll_weevil"],
            "white waxy": ["mealybug"],
            "deformed fruit": ["tarnished_plant_bug"],
            "cut stems": ["cutworm"],
            "damaging": ["fall_armyworm", "cutworm", "corn_earworm", "colorado_potato_beetle", "armyworm"],
            "eating": ["fall_armyworm", "cutworm", "corn_earworm", "colorado_potato_beetle", "armyworm"]
        }
        logger.info("TextAnalysisTool initialized")
    def analyze(self, description: str) -> Dict[str, List[str]]:
        try:
            if not isinstance(description, str):
                logger.error("Description is not a string")
                return {"error": "Description must be a string"}
            if not description.strip():
                logger.error("Description is empty")
                return {"error": "Description cannot be empty"}
            tokens = description.lower().split()
            matched_pests = set()
            for token in tokens:
                for keyword, pests in self.keyword_map.items():
                    if keyword in token or token in keyword:
                        matched_pests.update(pests)
            pests = list(matched_pests) if matched_pests else ["unknown"]
            logger.info(f"Identified pests: {pests}")
            return {"pests": pests}
        except Exception as e:
            logger.error(f"Text analysis error: {str(e)}")
            return {"error": f"Text analysis failed: {str(e)}"}
class KnowledgeBase:
    def __init__(self, json_file: str):
        self.knowledge = {}
        json_path = os.path.abspath(json_file)
        try:
            if os.path.exists(json_path):
                with open(json_path, "r") as f:
                    self.knowledge = json.load(f)
                logger.info(f"Loaded knowledge base from {json_path}")
            else:
                logger.error(f"Knowledge base not found: {json_path}")
                raise FileNotFoundError(f"Knowledge base not found: {json_path}")
        except Exception as e:
            logger.error(f"Knowledge base load error: {str(e)}")
            raise
    def search(self, query: str) -> Dict[str, any]:
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
        self.text_tool = TextAnalysisTool()
        self.knowledge_base = KnowledgeBase(self.config.knowledge_base_file)
        try:
            genai.configure(api_key=self.config.gemini_api_key)
            self.model = genai.GenerativeModel(self.config.gen_ai_model)
            logger.info("AgroPestAgent initialized")
        except Exception as e:
            logger.error(f"Gemini API init error: {str(e)}")
            self.model = None
    def analyze(self, description: str) -> Dict[str, any]:
        try:
            logger.info(f"Analyzing description: {description}")
            text_result = self.text_tool.analyze(description)
            if "error" in text_result:
                logger.error(f"Text analysis failed: {text_result['error']}")
                return {"error": text_result["error"]}
            text_pests = text_result.get("pests", ["unknown"])
            gemini_result = "Unable to get AI response"
            if self.model:
                prompt = dedent(f"""
                    Analyze pest description:
                    Description: {description}
                    Possible pests: {', '.join(text_pests)}
                    Provide a concise identification of the most likely pest and a brief explanation.
                """)
                try:
                    response = self.model.generate_content(prompt)
                    gemini_result = response.text
                    logger.info(f"Gemini response: {gemini_result[:100]}...")
                except Exception as e:
                    logger.error(f"Gemini API error: {str(e)}")
            likely_pest = text_pests[0]
            pest_data = self.knowledge_base.search(likely_pest).get(likely_pest, {})
            report = self.generate_report(
                likely_pest=likely_pest,
                text_pests=text_pests,
                gemini_result=gemini_result,
                pest_data=pest_data
            )
            logger.info(f"Generated report for pest: {likely_pest}")
            return {
                "pest": likely_pest,
                "report": report,
                "gemini_result": gemini_result,
                "text_result": text_result
            }
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    def generate_report(self, likely_pest: str, text_pests: List[str], 
                       gemini_result: str, pest_data: Dict) -> str:
        control_measures = pest_data.get("control_measures", {})
        sections = [
            "Pest Identification Report",
            "Identified Pest",
            f"Pest: {likely_pest}",
            "Analysis Details",
            f"Possible pests: {', '.join(text_pests)}",
            f"AI Analysis: {gemini_result}",
            "Pest Information",
            f"Crops Affected: {', '.join(pest_data.get('crops', ['Unknown']))}",
            f"Regions: {', '.join(pest_data.get('regions', ['Unknown']))}",
            f"Symptoms: {', '.join(pest_data.get('symptoms', ['Unknown']))}",
            f"Life Cycle: {pest_data.get('life_cycle', 'Unknown')}",
            f"Economic Impact: {pest_data.get('economic_impact', 'Unknown')}",
            "Environmental Conditions",
            f"Temperature: {pest_data.get('environmental_conditions', {}).get('temperature', 'Unknown')}",
            f"Humidity: {pest_data.get('environmental_conditions', {}).get('humidity', 'Unknown')}",
            f"Soil Type: {pest_data.get('environmental_conditions', {}).get('soil_type', 'Unknown')}",
            "Control Measures",
            f"Chemical: {', '.join(control_measures.get('chemical', ['None']))}",
            f"Biological: {', '.join(control_measures.get('biological', ['None']))}",
            f"Cultural: {', '.join(control_measures.get('cultural', ['None']))}",
            f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ]
        wrapped_report = []
        for line in sections:
            wrapped_lines = wrap(line, width=80, subsequent_indent="  ")
            wrapped_report.extend(wrapped_lines)
        report = "\n".join(wrapped_report)
        report_path = f"pest_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(report_path, "w") as f:
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
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)