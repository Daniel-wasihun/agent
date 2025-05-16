import os
import json
import logging
from textwrap import dedent
from typing import Dict, List, Optional
import datetime
import google.generativeai as genai
from dotenv import load_dotenv

# Set up logging with structured format
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/pest_identification.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [%(name)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

class Config:
    """Configuration class for storing environment variables and settings."""
    def __init__(self):
        load_dotenv()
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.gen_ai_model = os.getenv("GEN_AI_MODEL", "gemini-pro")
        self.knowledge_base_file = os.getenv("KNOWLEDGE_BASE_FILE", "pest_knowledge.json")
        
        if not self.gemini_api_key:
            logger.error("GEMINI_API_KEY not found in .env file")
            raise ValueError("GEMINI_API_KEY is required in .env file")

# Text Analysis Tool
class TextAnalysisTool:
    """Tool for analyzing text descriptions to identify potential pests."""
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
        logger.info("TextAnalysisTool initialized successfully")

    def analyze(self, description: str) -> Dict[str, List[str]]:
        """Analyze text description to identify potential pests."""
        try:
            if not description or not isinstance(description, str):
                logger.error("Invalid or empty description provided")
                return {"error": "Description must be a non-empty string"}
            
            tokens = description.lower().split()
            matched_pests = set()
            for token in tokens:
                for keyword, pests in self.keyword_map.items():
                    if keyword in token or token in keyword:
                        matched_pests.update(pests)
            
            pests = list(matched_pests) if matched_pests else ["unknown"]
            logger.info(f"Text analysis completed: Identified pests {pests}")
            return {"pests": pests}
        except Exception as e:
            logger.error(f"Error processing text description: {str(e)}")
            return {"error": f"Error processing text: {str(e)}"}

# Knowledge Base
class KnowledgeBase:
    """Knowledge base for storing and retrieving pest information."""
    def __init__(self, json_file: str):
        self.knowledge = {}
        json_path = os.path.abspath(json_file)
        try:
            if os.path.exists(json_path):
                with open(json_path, "r") as f:
                    self.knowledge = json.load(f)
                logger.info(f"Successfully loaded knowledge base from {json_path}")
            else:
                logger.error(f"Knowledge base file not found: {json_path}")
                raise FileNotFoundError(f"Knowledge base file not found: {json_path}")
        except Exception as e:
            logger.error(f"Error loading knowledge base: {str(e)}")
            raise

    def search(self, query: str) -> Dict[str, any]:
        """Search the knowledge base for pest information."""
        query = query.lower().strip()
        if not query:
            logger.error("Empty query provided to knowledge base search")
            return {}
        
        if query in self.knowledge:
            logger.info(f"Knowledge base search found data for: {query}")
            return {query: self.knowledge[query]}
        
        logger.info(f"No specific match for {query}, returning full knowledge base")
        return self.knowledge

# AgroPestAgent
class AgroPestAgent:
    """Main agent for pest identification using text analysis."""
    def __init__(self):
        self.config = Config()
        self.text_tool = TextAnalysisTool()
        self.knowledge_base = KnowledgeBase(self.config.knowledge_base_file)
        
        try:
            genai.configure(api_key=self.config.gemini_api_key)
            self.model = genai.GenerativeModel(self.config.gen_ai_model)
            logger.info("AgroPestAgent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini API: {str(e)}")
            self.model = None

    def analyze(self, description: str) -> Dict[str, any]:
        """Analyze text description to identify pests."""
        try:
            # Validate input
            if not description or not isinstance(description, str):
                logger.error("Invalid description provided")
                return {"error": "Description must be a non-empty string"}
            
            # Text analysis
            text_result = self.text_tool.analyze(description)
            if "error" in text_result:
                logger.error(f"Text analysis failed: {text_result['error']}")
                return {"error": text_result["error"]}
            
            # Combine results
            text_pests = text_result.get("pests", ["unknown"])
            
            # Gemini API analysis
            gemini_result = "Unable to get Gemini API response"
            if self.model:
                prompt = dedent(f"""
                    Analyze the following pest identification data:
                    - Text description: {description}
                    - Possible pests from text: {', '.join(text_pests)}
                    Provide a concise identification of the most likely pest and a brief explanation.
                """)
                try:
                    response = self.model.generate_content(prompt)
                    gemini_result = response.text
                    logger.info(f"Gemini API response received: {gemini_result[:100]}...")
                except Exception as e:
                    logger.error(f"Gemini API error: {str(e)}")
            
            # Determine most likely pest
            likely_pest = text_pests[0]
            
            # Fetch knowledge base data
            pest_data = self.knowledge_base.search(likely_pest).get(likely_pest, {})
            
            # Generate report
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
                "text_result": text_result,
                "gemini_result": gemini_result
            }
        except Exception as e:
            logger.error(f"Error in AgroPestAgent analysis: {str(e)}")
            return {"error": f"Error in analysis: {str(e)}"}

    def generate_report(self, likely_pest: str, text_pests: List[str], 
                       gemini_result: str, pest_data: Dict) -> str:
        """Generate a detailed pest identification report."""
        control_measures = pest_data.get("control_measures", {})
        report = dedent(f"""
            # Pest Identification Report
            
            ## Identified Pest
            - **Pest**: {likely_pest}
            
            ## Analysis Details
            - **Text Analysis**: Possible pests: {', '.join(text_pests)}
            - **Gemini AI Analysis**: {gemini_result}
            
            ## Pest Information
            - **Crops Affected**: {', '.join(pest_data.get('crops', ['Unknown']))}
            - **Regions**: {', '.join(pest_data.get('regions', ['Unknown']))}
            - **Symptoms**: {', '.join(pest_data.get('symptoms', ['Unknown']))}
            - **Life Cycle**: {pest_data.get('life_cycle', 'Unknown')}
            - **Economic Impact**: {pest_data.get('economic_impact', 'Unknown')}
            - **Environmental Conditions**:
                - **Temperature**: {pest_data.get('environmental_conditions', {}).get('temperature', 'Unknown')}
                - **Humidity**: {pest_data.get('environmental_conditions', {}).get('humidity', 'Unknown')}
                - **Soil Type**: {pest_data.get('environmental_conditions', {}).get('soil_type', 'Unknown')}
            
            ## Control Measures
            - **Chemical**: {', '.join(control_measures.get('chemical', ['None']))}
            - **Biological**: {', '.join(control_measures.get('biological', ['None']))}
            - **Cultural**: {', '.join(control_measures.get('cultural', ['None']))}
            
            Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """)
        
        report_path = f"pest_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        try:
            with open(report_path, "w") as f:
                f.write(report)
            logger.info(f"Report saved to {report_path}")
        except Exception as e:
            logger.error(f"Failed to save report: {str(e)}")
        
        return report

def main():
    """Main execution function for pest identification."""
    try:
        agent = AgroPestAgent()
        description = input("\nEnter a description of the pest symptoms: ").strip()
        
        if not description:
            logger.error("Empty description provided")
            print("Error: Description cannot be empty")
            return
        
        result = agent.analyze(description)
        
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print("\nPest Identification Result:")
            print(f"Identified Pest: {result['pest']}")
            print("\nReport:")
            print(result['report'])
    except Exception as e:
        logger.error(f"Main execution error: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()