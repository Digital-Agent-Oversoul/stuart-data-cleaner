"""
Unified LLM Engine for Data Cleaning

This module consolidates the advanced LLM logic from the Contact Export script
and provides a unified interface with OpenAI + Ollama fallback system.
"""

import os
import json
import logging
import requests
from typing import Optional, Tuple, Dict, Any, Union
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class LLMResponse:
    """Result of LLM processing operation"""
    first_name: Optional[str]
    last_name: Optional[str]
    confidence: float
    processing_method: str
    metadata: Dict[str, Any]
    success: bool
    error_message: Optional[str] = None

@dataclass
class ProcessingStats:
    """Statistics for processing operations"""
    total_records: int
    llm_processed: int
    ollama_fallback: int
    rule_based_fallback: int
    errors: int
    start_time: datetime
    end_time: Optional[datetime] = None

class BudgetMonitor:
    """Monitor OpenAI API costs and trigger fallbacks"""
    
    def __init__(self, monthly_budget: float = 10.00, alert_threshold: float = 0.8):
        self.monthly_budget = monthly_budget
        self.alert_threshold = alert_threshold
        self.current_month_cost = 0.0
        self.current_month = datetime.now().month
        
    def check_budget(self, estimated_cost: float) -> bool:
        """Check if operation can proceed within budget"""
        if self.current_month != datetime.now().month:
            self.current_month_cost = 0.0
            self.current_month = datetime.now().month
            
        if self.current_month_cost + estimated_cost > self.monthly_budget * self.alert_threshold:
            logger.warning(f"Budget threshold reached: ${self.current_month_cost:.2f}/{self.monthly_budget:.2f}")
            return False
        return True
    
    def add_cost(self, cost: float):
        """Add cost to current month total"""
        self.current_month_cost += cost
        logger.info(f"Current month cost: ${self.current_month_cost:.2f}/{self.monthly_budget:.2f}")

class OpenAIProcessor:
    """OpenAI API integration for primary LLM processing"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini", max_tokens: int = 150, temperature: float = 0.1):
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        
    def parse_name(self, contact_name: str, customer_name: str, email: str) -> LLMResponse:
        """Parse name using OpenAI API"""
        try:
            import openai
            
            # Set the API key
            openai.api_key = self.api_key
            
            prompt = self._build_prompt(contact_name, customer_name, email)
            
            # Use the openai library instead of requests
            response = openai.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse JSON response
            parsed = json.loads(content)
            first_name = parsed.get('first_name')
            last_name = parsed.get('last_name')
            
            return LLMResponse(
                first_name=first_name,
                last_name=last_name,
                confidence=0.9,  # High confidence for OpenAI
                processing_method="openai",
                metadata={"model": self.model, "tokens_used": response.usage.total_tokens if response.usage else 0},
                success=True
            )
            
        except Exception as e:
            logger.error(f"OpenAI processing failed: {e}")
            return LLMResponse(
                first_name=None,
                last_name=None,
                confidence=0.0,
                processing_method="openai",
                metadata={"error": str(e)},
                success=False,
                error_message=str(e)
            )
    
    def _build_prompt(self, contact_name: str, customer_name: str, email: str) -> str:
        """Build the comprehensive prompt for name parsing (same as OpenAI)"""
        # Use the same comprehensive prompt as OpenAI for consistency
        return OpenAIProcessor._build_name_parsing_prompt(contact_name, customer_name, email)
    
    @staticmethod
    def _build_name_parsing_prompt(contact_name: str, customer_name: str, email: str) -> str:
        """Build the comprehensive prompt for name parsing (static method for sharing)"""
        return f"""You are a data cleaning expert. Extract the best person's name from the provided fields.

CRITICAL: Return ONLY valid JSON. NO comments, explanations, or additional text.

ANALYSIS PROCESS:
1. CHECK Customer Name for "LASTNAME, FIRSTNAME" format - this takes HIGHEST priority if it's a person name
2. EXAMINE Contact Name - if it's a clear person name (not company), use it as PRIMARY source
3. ANALYZE Email(s) - extract person names from email addresses ONLY when Contact Name is missing or incomplete
4. COMPARE all sources to find the most complete and accurate person name
5. NEVER use company name fragments as person names
6. PRIORITY ORDER: Customer Name (if person format) > Contact Name > Email extraction

CUSTOMER NAME PRIORITY:
- "LASTNAME, FIRSTNAME" format: Use this when it contains person names
- "SAW, NAHA" becomes first="Naha", last="Saw" 
- "HAN, VICTOR" becomes first="Victor", last="Han" (prioritize over Contact Name)
- "SUBRAMANIAM, SUBBU" format: Use this over incomplete Contact Names like "SUBBU Y"
- If Customer Name is a business, still extract person names from Contact Name + Email

CONTACT NAME FORMATS:
- "LASTNAME, FIRSTNAME": "ERICKSON, MELISSA" becomes first="Melissa", last="Erickson"
- "FIRSTNAME LASTNAME": "JOHN SMITH" becomes first="John", last="Smith"
- "FIRSTNAME LASTNAME - LASTNAME2": "SUZANNE EWING - ERVIN" becomes first="Suzanne", last="Ewing-Ervin"
- "MULTIPLE PEOPLE & SEPARATOR": "KOREY KOENIG-DAMIENS & TAMERA" - extract the most relevant person name
  * If email matches one person (e.g., "tgarlock@berkeley.edu" matches "TAMERA"), use that person
  * "KOREY KOENIG-DAMIENS & TAMERA" + "tgarlock@berkeley.edu" = first="Tamera", last="Garlock"
  * "JOHN & JANE SMITH" + "jsmith@email.com" = first="Jane", last="Smith"
- Always preserve the EXACT names from Contact Name when they are person names
- "SUSAN PARISH" + "sparish@berkeley.edu" = first="Susan", last="Parish" (use Contact Name, not email)
- "MIRIAM" + "mholland@sccoe.org" = first="Miriam", last="Holland" (complete from email when Contact Name incomplete)
- "STACY ROCK" = first="Stacy", last="Rock" (clear person name, even with business email)

EMAIL PARSING GUIDELINES:
- "mholland@domain.com" + Contact Name "MIRIAM": Miriam=first name, Holland=last name (complete the name)
- "SHEILA.SALENGA@domain.com" + Contact Name "SHEILA": Sheila=first name, Salenga=last name
- "sandy@domain.com" + business Customer Name: Sandy=first name (extract from email when no Contact Name)
- "Isela.CornejoEspinoza@domain.com": Isela=first name, Cornejo-Espinoza=last name (preserve hyphenation)
- "tgarlock@berkeley.edu": t=first initial, garlock=last name (extract "Garlock" as last name)
- "Lastname, Firstname <email@domain.com>": Extract "Firstname Lastname" as the person's name
- "Name <email@domain.com>": Extract names from the prefix part before < >
- "MBHOLLAND100@domain.com": M=first initial, B=middle initial, HOLLAND=last name
- "john.smith@domain.com": john=first name, smith=last name  
- "jkolander@company.com": j=first initial, kolander=last name
- COMPLETE NAMES: Use email to fill missing first or last names from Contact Name

MULTIPLE EMAIL HANDLING:
- "sandy@satoricellars.com; tom@satoricellars.com": Choose "sandy@" as it's more personal-sounding
- "SHEILA.SALENGA@LATTICE.COM; workplace-support@lattice.com": Choose the personal name email
- "tgarlock@berkeley.edu;moving@berkeley.edu": Choose "tgarlock@" as it's more personal-sounding
- Choose the email most likely to be a person (not info@, sales@, workplace-support@, etc.)
- Personal emails (firstname.lastname@, firstinitiallastname@) over business emails
- Match email patterns with Contact Name when possible

COMPANY NAME DETECTION:
- ALWAYS extract person names from Contact Name + Email, even when Customer Name is a business
- "BLANCA" + "blanca.ortiz0@wdc.com" = "Blanca Ortiz" (extract last name from email)
- "JACKIE" + "JKOLANDER@company.com" = "Jackie Kolander" (extract last name from email)
- NEVER extract person names from clear business names like "SRI ANANDA BHAVAN RESTAURANT" 
- NEVER use business fragments as person names: "Capital", "Modern", "Senior Living", "Elementary", "Solutions", "Systems", "Research Corporation", "Print Solutions", "Design Decor", "Southern Kitchen", "Climate Week", "Real-Time Innovations", "De Anza", "Maggiore Tile", "Senior Living", "Streamlinevents", "Javier Events", "Cloud Kitchen", "West Gymnastics", "Deli Cafe", "Southern Creations"
- AGGRESSIVE BUSINESS DETECTION: Company indicators include: LLC, INC, CORP, GROUP, CENTER, CATERING, ENTERTAINMENT, RESTAURANT, BHAVAN, SCHOOL, CHURCH, UNIVERSITY, COLLEGE, HOSPITAL, CLINIC, FOUNDATION, ASSOCIATION, ORGANIZATION, INSTITUTE, SYSTEM, NETWORK, PARTNERS, ALLIANCE, PRODUCTIONS, STEAKHOUSE, WINE BAR, INNOVATION, TECHNOLOGY, REAL ESTATE, BOOSTER CLUB, TRADITION, RESIDENCE, DISTRICT, COUNTY, OFFICE, DEPARTMENT, DIVISION, BUREAU, AGENCY, AUTHORITY, COMMISSION, BOARD, COUNCIL, COMMITTEE, TEAM, STAFF, PERSONNEL, EMPLOYEES, WORKERS, MEMBERS, VOLUNTEERS, CAPITAL, MODERN, SENIOR, LIVING, ELEMENTARY, MIDDLE, HIGH, SOLUTIONS, SYSTEMS, INNOVATIONS, RESEARCH, CORPORATION, PRINT, DESIGN, DECOR, TILE, KITCHEN, CREATIONS, STREAMLINE, EXPECTATIONS, SUCCULENT, CACTUS, CLIMATE, WEEK, ZOO, HOTEL, CAFE, DELI, PLAZA, GYMNASTICS, GOVERNMENT, CITY, ARENA, AMERICAS, SOUTHERN, CLOUD, WEST, PACIFIC, LUXE, REAL-TIME, etc.
- NEVER extract these terms as person names: "School", "Church", "University", "Hospital", "Foundation", "Association", "Organization", "Institute", "System", "Network", "Partners", "Alliance", "Productions", "Restaurant", "Steakhouse", "Wine Bar", "Innovation", "Technology", "Real Estate", "Booster Club", "Tradition", "Residence", "District", "County", "Office", "Department", "Division", "Bureau", "Agency", "Authority", "Commission", "Board", "Council", "Committee", "Team", "Staff", "Personnel", "Employees", "Workers", "Members", "Volunteers", "Capital", "Modern", "Senior", "Living", "Elementary", "Solutions", "Systems", "Research", "Corporation", "Print", "Design", "Decor", "Kitchen", "Creations", "Climate", "Week", "Hotel", "Cafe", "Deli", "Gymnastics", "Government", "City", "Southern", "Cloud", "West", "Pacific"
- If Customer Name is business AND Contact Name is empty AND email has no clear person name, return null
- Business email patterns like "SABSV1111@gmail.com" (random letters/numbers) suggest no person name
- ONLY return null when ALL sources (Contact Name, Customer Name, Email) are clearly business-related
- Examples of business names that should return null: "SRI ANANDA BHAVAN RESTAURANT" (no Contact Name), "MANTRA INDIA" (Contact Name is business), "SABSV1111@gmail.com" (business abbreviation email with no Contact Name)
- If Contact Name is a clear person name (like "STACY ROCK"), extract it regardless of business email

HYPHENATED NAMES:
- "EWING - ERVIN" becomes "Ewing-Ervin" (remove spaces around hyphen)
- "CornejoEspinoza" from email becomes "Cornejo-Espinoza" (add hyphen for compound names)
- "MARTINEZ-GARCIA" stays "Martinez-Garcia"
- Always preserve hyphenated last names as single unit

MISSING INFORMATION:
- If only first name available and no reliable last name can be extracted, leave last name null
- Better to have incomplete but accurate data than incorrect data
- For pure business names with no person information, return null for both names

INPUT DATA:
Contact Name: "{contact_name}"
Customer Name: "{customer_name}"
Email: "{email}"

EXAMPLES:
{{"first_name": "Mercedes", "last_name": "Holland"}}
{{"first_name": "Melissa", "last_name": "Erickson"}}
{{"first_name": "Naha", "last_name": "Saw"}}
{{"first_name": "Miriam", "last_name": "Holland"}}
{{"first_name": "Sheila", "last_name": "Salenga"}}
{{"first_name": "Jackie", "last_name": "Kolander"}}
{{"first_name": "Victor", "last_name": "Han"}}
{{"first_name": "Sandy", "last_name": null}}
{{"first_name": "Stacy", "last_name": "Rock"}}
{{"first_name": "Sridhar", "last_name": "Lakshmikanthan"}}
{{"first_name": "Tamera", "last_name": "Garlock"}}

RESPONSE FORMAT: Return ONLY the JSON object. No explanations, comments, or reasoning."""

class OllamaProcessor:
    """Ollama local LLM integration for fallback processing"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "qwen2.5:7b-instruct-q4_K_M", max_tokens: int = 150, temperature: float = 0.1):
        self.base_url = base_url
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        
    def parse_name(self, contact_name: str, customer_name: str, email: str) -> LLMResponse:
        """Parse name using Ollama local LLM"""
        try:
            # Input validation: Check for empty/None values
            if not contact_name or str(contact_name).strip() == '' or str(contact_name).lower() in ['nan', 'none', 'null']:
                contact_name = ''
            if not customer_name or str(customer_name).strip() == '' or str(customer_name).lower() in ['nan', 'none', 'null']:
                customer_name = ''
            if not email or str(email).strip() == '' or str(email).lower() in ['nan', 'none', 'null']:
                email = ''
            
            # If all inputs are empty, return null names without calling LLM
            if not contact_name and not customer_name and not email:
                logger.debug("All input fields are empty, returning null names")
                return LLMResponse(
                    first_name=None,
                    last_name=None,
                    confidence=0.0,
                    processing_method="ollama",
                    metadata={"model": self.model, "reason": "empty_input"},
                    success=True
                )
            
            prompt = self._build_prompt(contact_name, customer_name, email)
            
            # Debug: Log the prompt being sent
            logger.debug(f"Ollama prompt for {contact_name}|{customer_name}|{email}: {prompt[:200]}...")
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "context": [],  # Reset context to prevent contamination
                    "options": {
                        "temperature": self.temperature,
                        "num_predict": self.max_tokens
                    }
                },
                timeout=60
            )
            
            if response.status_code != 200:
                raise Exception(f"Ollama API error: {response.status_code}")
            
            result = response.json()
            content = result.get('response', '').strip()
            
            # Debug: Log the raw response
            logger.debug(f"Ollama raw response: {content}")
            
            # Also log the full result for debugging
            logger.debug(f"Ollama full result: {result}")
            
            # Parse JSON response with improved error handling
            parsed = self._parse_ollama_response(content)
            
            # Debug: Log the parsed result
            logger.debug(f"Ollama parsed result: {parsed}")
            
            return LLMResponse(
                first_name=parsed.get('first_name'),
                last_name=parsed.get('last_name'),
                confidence=0.7,  # Medium confidence for Ollama
                processing_method="ollama",
                metadata={"model": self.model, "response_length": len(content), "raw_response": content},
                success=True
            )
            
        except Exception as e:
            logger.error(f"Ollama processing failed: {e}")
            return LLMResponse(
                first_name=None,
                last_name=None,
                confidence=0.0,
                processing_method="ollama",
                metadata={"error": str(e)},
                success=False,
                error_message=str(e)
            )
    
    def _build_prompt(self, contact_name: str, customer_name: str, email: str) -> str:
        """Build the comprehensive prompt for name parsing (same as OpenAI)"""
        # Use the same comprehensive prompt as OpenAI for consistency
        return OpenAIProcessor._build_name_parsing_prompt(contact_name, customer_name, email)
    
    def _parse_ollama_response(self, content: str) -> Dict[str, Any]:
        """Parse Ollama response with improved error handling (from working script)"""
        try:
            # Try to clean up common JSON formatting issues
            content_clean = content.strip()
            
            # Remove any trailing comments or explanations after the JSON
            if '//' in content_clean:
                # Find the first // and remove everything after it, then try to close JSON
                comment_pos = content_clean.find('//')
                json_part = content_clean[:comment_pos].strip()
                # Check if we need to close brackets/braces
                if json_part.endswith(','):
                    json_part = json_part[:-1]  # Remove trailing comma
                if json_part.count('{') > json_part.count('}'):
                    json_part += '}'
                content_clean = json_part
            
            # Extract just the JSON object if there's extra text
            start_brace = content_clean.find('{')
            end_brace = content_clean.rfind('}')
            if start_brace != -1 and end_brace != -1 and end_brace > start_brace:
                content_clean = content_clean[start_brace:end_brace + 1]
            
            # Try to parse the JSON
            parsed = json.loads(content_clean)
            
            # Validate that we have the expected structure
            if not isinstance(parsed, dict):
                logger.warning(f"Ollama response is not a dict: {type(parsed)}")
                return {"first_name": None, "last_name": None}
            
            # Ensure we have the expected keys
            if 'first_name' not in parsed or 'last_name' not in parsed:
                logger.warning(f"Ollama response missing expected keys: {list(parsed.keys())}")
                # Try to map common variations
                if 'first' in parsed:
                    parsed['first_name'] = parsed.pop('first')
                if 'last' in parsed:
                    parsed['last_name'] = parsed.pop('last')
                if 'firstName' in parsed:
                    parsed['first_name'] = parsed.pop('firstName')
                if 'lastName' in parsed:
                    parsed['last_name'] = parsed.pop('lastName')
            
            logger.debug(f"Successfully parsed Ollama response: {parsed}")
            return parsed
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Ollama JSON response: {e}")
            logger.error(f"Raw content was: {content}")
            return {"first_name": None, "last_name": None}
        except Exception as e:
            logger.error(f"Unexpected error parsing Ollama response: {e}")
            return {"first_name": None, "last_name": None}
    
    def test_simple_parsing(self) -> Dict[str, Any]:
        """Test simple name parsing to debug issues"""
        try:
            # Test with a very simple prompt
            simple_prompt = """Extract the first and last name from this data. Return only JSON.

Contact Name: "John Smith"
Customer Name: "Smith, John"
Email: "john.smith@email.com"

Return: {"first_name": "John", "last_name": "Smith"}"""
            
            logger.info("🧪 Testing Ollama with simple prompt...")
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": simple_prompt,
                    "stream": False,
                    "context": [],
                    "options": {
                        "temperature": 0.1,
                        "num_predict": 100
                    }
                },
                timeout=30
            )
            
            if response.status_code != 200:
                return {"error": f"HTTP {response.status_code}", "success": False}
            
            result = response.json()
            content = result.get('response', '').strip()
            
            logger.info(f"🧪 Ollama raw test response: {content}")
            
            # Try to parse the response
            parsed = self._parse_ollama_response(content)
            logger.info(f"🧪 Ollama parsed test response: {parsed}")
            
            return {
                "success": True,
                "raw_response": content,
                "parsed_response": parsed,
                "model": self.model
            }
            
        except Exception as e:
            logger.error(f"🧪 Ollama test failed: {e}")
            return {"error": str(e), "success": False}

class RuleBasedProcessor:
    """Rule-based fallback for when LLM processing fails"""
    
    def parse_name(self, contact_name: str, customer_name: str, email: str) -> LLMResponse:
        """Parse name using rule-based logic"""
        try:
            first_name, last_name = self._extract_names_rules(contact_name, customer_name, email)
            
            return LLMResponse(
                first_name=first_name,
                last_name=last_name,
                confidence=0.5,  # Lower confidence for rule-based
                processing_method="rule_based",
                metadata={"method": "rule_based_fallback"},
                success=True
            )
            
        except Exception as e:
            logger.error(f"Rule-based processing failed: {e}")
            return LLMResponse(
                first_name=None,
                last_name=None,
                confidence=0.0,
                processing_method="rule_based",
                metadata={"error": str(e)},
                success=False,
                error_message=str(e)
            )
    
    def _extract_names_rules(self, contact_name: str, customer_name: str, email: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract names using rule-based logic"""
        # Basic rule-based extraction as fallback
        # This is a simplified version - the LLM handles the complex cases
        
        if contact_name is None or str(contact_name).strip() == '':
            contact_name = None
        if customer_name is None or str(customer_name).strip() == '':
            customer_name = None
        if email is None or str(email).strip() == '':
            email = None
            
        # Simple extraction logic
        first_name = None
        last_name = None
        
        # Try to extract from contact name first
        if contact_name:
            parts = str(contact_name).strip().split()
            if len(parts) >= 2:
                first_name = parts[0].title()
                last_name = ' '.join(parts[1:]).title()
            elif len(parts) == 1:
                first_name = parts[0].title()
        
        # If no contact name, try customer name
        if not first_name and customer_name:
            if ',' in customer_name:
                # "LASTNAME, FIRSTNAME" format
                parts = customer_name.split(',')
                if len(parts) >= 2:
                    last_name = parts[0].strip().title()
                    first_name = parts[1].strip().title()
            else:
                parts = customer_name.strip().split()
                if len(parts) >= 2:
                    first_name = parts[0].title()
                    last_name = ' '.join(parts[1:]).title()
                elif len(parts) == 1:
                    first_name = parts[0].title()
        
        # Try to extract from email if still no names
        if not first_name and email:
            email_part = email.split('@')[0]
            if '.' in email_part:
                parts = email_part.split('.')
                if len(parts) >= 2:
                    first_name = parts[0].title()
                    last_name = parts[1].title()
            else:
                # Single word email - might be initials or first name
                if len(email_part) > 1:
                    first_name = email_part.title()
        
        return first_name, last_name

class LLMEngine:
    """Unified LLM engine with OpenAI + Ollama fallback system"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize LLM engine with configuration
        
        Args:
            config: Configuration dictionary with 'openai' and 'ollama' sections
        """
        self.config = config
        self.stats = ProcessingStats(
            total_records=0,
            llm_processed=0,
            ollama_fallback=0,
            rule_based_fallback=0,
            errors=0,
            start_time=datetime.now()
        )
        
        # Initialize OpenAI processor if API key is available
        openai_config = config.get('openai', {})
        if openai_config.get('api_key'):
            self.openai_processor = OpenAIProcessor(
                api_key=openai_config['api_key'],
                model=openai_config.get('model', 'gpt-4o-mini'),
                max_tokens=openai_config.get('max_tokens', 150),
                temperature=openai_config.get('temperature', 0.1)
            )
        else:
            self.openai_processor = None
            logger.warning("OpenAI API key not provided, OpenAI processing disabled")
        
        # Initialize Ollama processor
        ollama_config = config.get('ollama', {})
        self.ollama_processor = OllamaProcessor(
            base_url=ollama_config.get('base_url', 'http://localhost:11434'),
            model=ollama_config.get('model', 'qwen2.5:7b-instruct-q4_K_M'),
            max_tokens=150,  # Use proven working limit from working script
            temperature=0.1
        )
        
        # Initialize rule-based processor
        self.rule_processor = RuleBasedProcessor()
        
        # Initialize budget monitor
        self.budget_monitor = BudgetMonitor(
            monthly_budget=config.get('monthly_budget', 10.00),
            alert_threshold=config.get('alert_threshold', 0.8)
        )
        
        # Get retry configuration
        self.max_retries = config.get('max_retries', 3)
        self.retry_delay_ms = config.get('retry_delay_ms', 1000)
        self.show_progress = config.get('show_progress', True)
        
        # Perform health checks
        self._perform_health_checks()
    
    def _perform_health_checks(self):
        """Check availability of OpenAI and Ollama services"""
        logger.info("🔍 Performing LLM service health checks...")
        
        # Check OpenAI
        if self.openai_processor:
            try:
                # Test with a simple prompt
                test_response = self.openai_processor.parse_name("John", "Smith", "john.smith@email.com")
                if test_response.success:
                    logger.info("✅ OpenAI: Service available and responding correctly")
                else:
                    logger.warning(f"⚠️  OpenAI: Service responding but with errors: {test_response.error_message}")
            except Exception as e:
                logger.error(f"❌ OpenAI: Service unavailable - {e}")
        else:
            logger.info("ℹ️  OpenAI: Not configured (no API key)")
        
        # Check Ollama
        try:
            # Test with a simple prompt
            test_response = self.ollama_processor.parse_name("John", "Smith", "john.smith@email.com")
            if test_response.success:
                logger.info("✅ Ollama: Service available and responding correctly")
                # Log the actual response for debugging
                logger.info(f"   Ollama test response: first_name='{test_response.first_name}', last_name='{test_response.last_name}'")
                
                # If we got None values, run the simple test
                if test_response.first_name is None and test_response.last_name is None:
                    logger.warning("⚠️  Ollama returned None values - running simple test...")
                    simple_test = self.ollama_processor.test_simple_parsing()
                    if simple_test.get("success"):
                        logger.info(f"🧪 Simple test result: {simple_test.get('parsed_response')}")
                    else:
                        logger.error(f"🧪 Simple test failed: {simple_test.get('error')}")
            else:
                logger.warning(f"⚠️  Ollama: Service responding but with errors: {test_response.error_message}")
        except Exception as e:
            logger.error(f"❌ Ollama: Service unavailable - {e}")
        
        # Check rule-based processor
        try:
            test_response = self.rule_processor.parse_name("John", "Smith", "john.smith@email.com")
            if test_response.success:
                logger.info("✅ Rule-based: Fallback processor working correctly")
            else:
                logger.warning(f"⚠️  Rule-based: Fallback processor has issues: {test_response.error_message}")
        except Exception as e:
            logger.error(f"❌ Rule-based: Fallback processor unavailable - {e}")
        
        logger.info("🔍 Health checks completed")
    
    def parse_name(self, contact_name: str, customer_name: str, email: str) -> LLMResponse:
        """
        Parse name using multi-tier LLM system with retry logic and progress reporting
        
        Args:
            contact_name: Contact name field
            customer_name: Customer name field  
            email: Email address field
            
        Returns:
            LLMResponse with parsed name and processing details
        """
        self.stats.total_records += 1
        
        # Try OpenAI first (if available)
        if self.openai_processor:
            if self.show_progress:
                print(f"🔄 Processing: {contact_name} | {customer_name} | {email}")
            
            for attempt in range(self.max_retries):
                try:
                    if self.show_progress and attempt > 0:
                        print(f"   ⚠️  Retry {attempt + 1}/{self.max_retries} for OpenAI")
                    
                    result = self.openai_processor.parse_name(contact_name, customer_name, email)
                    
                    if result.success:
                        self.stats.llm_processed += 1
                        if self.show_progress:
                            print(f"   ✅ OpenAI: {result.first_name} {result.last_name} (confidence: {result.confidence:.2f})")
                        return result
                    else:
                        if self.show_progress:
                            print(f"   ❌ OpenAI failed: {result.error_message}")
                        
                except Exception as e:
                    if self.show_progress:
                        print(f"   ❌ OpenAI error (attempt {attempt + 1}): {str(e)}")
                    
                    # Wait before retry (if not the last attempt)
                    if attempt < self.max_retries - 1:
                        import time
                        time.sleep(self.retry_delay_ms / 1000.0)
                    continue
            
            if self.show_progress:
                print(f"   🔄 OpenAI failed after {self.max_retries} attempts, trying Ollama...")
        
        # Try Ollama as fallback
        if self.show_progress:
            print(f"   🔄 Trying Ollama fallback...")
            
        for attempt in range(self.max_retries):
            try:
                if attempt > 0:
                    print(f"   ⚠️  Retry {attempt + 1}/{self.max_retries} for Ollama")
                
                result = self.ollama_processor.parse_name(contact_name, customer_name, email)
                
                if result.success:
                    self.stats.ollama_fallback += 1
                    if self.show_progress:
                        print(f"   ✅ Ollama: {result.first_name} {result.last_name} (confidence: {result.confidence:.2f})")
                    return result
                else:
                    if self.show_progress:
                        print(f"   ❌ Ollama failed: {result.error_message}")
                    
            except Exception as e:
                if self.show_progress:
                    print(f"   ❌ Ollama error (attempt {attempt + 1}): {str(e)}")
                
                # Wait before retry (if not the last attempt)
                if attempt < self.max_retries - 1:
                    import time
                    time.sleep(self.retry_delay_ms / 1000.0)
                continue
        
        if self.show_progress:
            print(f"   🔄 Ollama failed after {self.max_retries} attempts, using rule-based fallback...")
        
        # Use rule-based processing as final fallback
        try:
            result = self.rule_processor.parse_name(contact_name, customer_name, email)
            self.stats.rule_based_fallback += 1
            if self.show_progress:
                print(f"   ✅ Rule-based: {result.first_name} {result.last_name} (confidence: {result.confidence:.2f})")
            return result
        except Exception as e:
            self.stats.errors += 1
            if self.show_progress:
                print(f"   ❌ Rule-based failed: {str(e)}")
            
            # Return error response
            return LLMResponse(
                first_name=None,
                last_name=None,
                confidence=0.0,
                processing_method="error",
                metadata={"error": str(e)},
                success=False,
                error_message=f"All processing methods failed: {str(e)}"
            )
    
    def get_stats(self) -> ProcessingStats:
        """Get current processing statistics"""
        self.stats.end_time = datetime.now()
        return self.stats
    
    def reset_stats(self):
        """Reset processing statistics"""
        self.stats = ProcessingStats(
            total_records=0,
            llm_processed=0,
            ollama_fallback=0,
            rule_based_fallback=0,
            errors=0,
            start_time=datetime.now()
        )
