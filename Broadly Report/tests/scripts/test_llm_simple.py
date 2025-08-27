import requests
import json
import sys
import os

# Add the current directory to the path so we can import from the main script
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from alert_contact_export_with_llm import llm_parse_name, LLM_MODEL, OLLAMA_BASE_URL, MAX_TOKENS, TEMPERATURE

def test_simple_prompt():
    """Test with a very simple prompt to see if LLM works at all"""
    
    simple_prompt = """Extract first and last name from this data. Return only JSON.

Contact Name: "JOHN SMITH"
Customer Name: ""
Email: "john.smith@example.com"

Return format: {"first_name": "John", "last_name": "Smith"}"""

    print("Testing with simple prompt...")
    print(f"Model: {LLM_MODEL}")
    print(f"URL: {OLLAMA_BASE_URL}")
    print(f"Prompt length: {len(simple_prompt)} characters")
    print()
    
    try:
        # Call Ollama API directly
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": LLM_MODEL,
                "prompt": simple_prompt,
                "stream": False,
                "context": [],
                "options": {
                    "temperature": 0.1,
                    "num_predict": 50
                }
            },
            timeout=30
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result.get('response', '').strip()
            print(f"Raw response: {repr(content)}")
            print()
            
            # Try to parse JSON
            try:
                # Clean up the response
                content_clean = content.strip()
                
                # Extract just the JSON object if there's extra text
                start_brace = content_clean.find('{')
                end_brace = content_clean.rfind('}')
                if start_brace != -1 and end_brace != -1 and end_brace > start_brace:
                    content_clean = content_clean[start_brace:end_brace + 1]
                
                print(f"Cleaned JSON: {content_clean}")
                
                parsed = json.loads(content_clean)
                first_name = parsed.get('first_name')
                last_name = parsed.get('last_name')
                
                print(f"Parsed result: first_name='{first_name}', last_name='{last_name}'")
                
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                print(f"Content that failed to parse: {repr(content_clean)}")
        else:
            print(f"API error: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

def test_llm_api_directly():
    """Test the LLM API directly to see what's happening"""
    
    # Test case
    contact_name = "JOHN SMITH"
    customer_name = ""
    email = "john.smith@example.com"
    
    prompt = f"""You are a data cleaning expert. Extract the best person's name from the provided fields.

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
- Always preserve the EXACT names from Contact Name when they are person names
- "SUSAN PARISH" + "sparish@berkeley.edu" = first="Susan", last="Parish" (use Contact Name, not email)
- "MIRIAM" + "mholland@sccoe.org" = first="Miriam", last="Holland" (complete from email when Contact Name incomplete)

EMAIL PARSING GUIDELINES:
- "mholland@domain.com" + Contact Name "MIRIAM": Miriam=first name, Holland=last name (complete the name)
- "SHEILA.SALENGA@domain.com" + Contact Name "SHEILA": Sheila=first name, Salenga=last name
- "sandy@domain.com" + business Customer Name: Sandy=first name (extract from email when no Contact Name)
- "Isela.CornejoEspinoza@domain.com": Isela=first name, Cornejo-Espinoza=last name (preserve hyphenation)
- "Lastname, Firstname <email@domain.com>": Extract "Firstname Lastname" as the person's name
- "Name <email@domain.com>": Extract names from the prefix part before < >
- "MBHOLLAND100@domain.com": M=first initial, B=middle initial, HOLLAND=last name
- "john.smith@domain.com": john=first name, smith=last name  
- "jkolander@company.com": j=first initial, kolander=last name
- COMPLETE NAMES: Use email to fill missing first or last names from Contact Name

MULTIPLE EMAIL HANDLING:
- "sandy@satoricellars.com; tom@satoricellars.com": Choose "sandy@" as it's more personal-sounding
- "SHEILA.SALENGA@LATTICE.COM; workplace-support@lattice.com": Choose the personal name email
- Choose the email most likely to be a person (not info@, sales@, workplace-support@, etc.)
- Personal emails (firstname.lastname@, firstinitiallastname@) over business emails
- Match email patterns with Contact Name when possible

COMPANY NAME DETECTION:
- ALWAYS extract person names from Contact Name + Email, even when Customer Name is a business
- "BLANCA" + "blanca.ortiz0@wdc.com" = "Blanca Ortiz" (extract last name from email)
- "JACKIE" + "JKOLANDER@company.com" = "Jackie Kolander" (extract last name from email)
- NEVER extract person names from clear business names like "SRI ANANDA BHAVAN RESTAURANT" 
- NEVER use fragments like "Area Asphalt", "India", "And Chill", "Restaurant", "Entertainment" as last names
- Company indicators: LLC, INC, CORP, GROUP, CENTER, CATERING, ENTERTAINMENT, RESTAURANT, BHAVAN, SCHOOL, CHURCH, UNIVERSITY, COLLEGE, HOSPITAL, CLINIC, FOUNDATION, ASSOCIATION, ORGANIZATION, INSTITUTE, SYSTEM, NETWORK, PARTNERS, ALLIANCE, PRODUCTIONS, STEAKHOUSE, WINE BAR, INNOVATION, TECHNOLOGY, REAL ESTATE, BOOSTER CLUB, TRADITION, RESIDENCE, DISTRICT, COUNTY, OFFICE, DEPARTMENT, DIVISION, BUREAU, AGENCY, AUTHORITY, COMMISSION, BOARD, COUNCIL, COMMITTEE, TEAM, STAFF, PERSONNEL, EMPLOYEES, WORKERS, MEMBERS, VOLUNTEERS, etc.
- NEVER extract "School", "Church", "University", "Hospital", "Foundation", "Association", "Organization", "Institute", "System", "Network", "Partners", "Alliance", "Productions", "Restaurant", "Steakhouse", "Wine Bar", "Innovation", "Technology", "Real Estate", "Booster Club", "Tradition", "Residence", "District", "County", "Office", "Department", "Division", "Bureau", "Agency", "Authority", "Commission", "Board", "Council", "Committee", "Team", "Staff", "Personnel", "Employees", "Workers", "Members", "Volunteers" as person names
- If Customer Name is business AND Contact Name is empty AND email has no clear person name, return null
- Business email patterns like "SABSV1111@gmail.com" (random letters/numbers) suggest no person name

HYPHENATED NAMES:
- "EWING - ERVIN" becomes "Ewing-Ervin" (remove spaces around hyphen)
- "CornejoEspinoza" from email becomes "Cornejo-Espinoza" (add hyphen for compound names)
- "MARTINEZ-GARCIA" stays "Martinez-Garcia"
- Always preserve hyphenated last names as single unit

MISSING INFORMATION:
- If only first name available and no reliable last name can be extracted, leave last name null
- Better to have incomplete but accurate data than incorrect data
- For pure business names with no person information, return null for both names

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
{{"first_name": "Subbu", "last_name": "Subramaniam"}}
{{"first_name": "Isela", "last_name": "Cornejo-Espinoza"}}
{{"first_name": "Suzanne", "last_name": "Ewing-Ervin"}}
{{"first_name": "Denny", "last_name": "Rahardjo"}}
{{"first_name": "Jocelyn", "last_name": null}}
{{"first_name": "Susan", "last_name": "Parish"}}  # For "SUSAN PARISH" + "sparish@berkeley.edu"
{{"first_name": "Miriam", "last_name": "Holland"}}  # For "MIRIAM" + "mholland@sccoe.org"
{{"first_name": null, "last_name": null}}
{{"first_name": null, "last_name": null}}  # For "ST. MARY'S SCHOOL" with no person name
{{"first_name": null, "last_name": null}}  # For "FIRST BAPTIST CHURCH" with no person name
{{"first_name": null, "last_name": null}}  # For "SANTA CLARA UNIVERSITY" with no person name
{{"first_name": null, "last_name": null}}  # For "STANFORD HOSPITAL" with no person name
{{"first_name": null, "last_name": null}}  # For "CITY OF PALO ALTO" with no person name

RESPONSE FORMAT: Return ONLY the JSON object. No explanations, comments, or reasoning."""

    print("Testing LLM API directly...")
    print(f"Model: {LLM_MODEL}")
    print(f"URL: {OLLAMA_BASE_URL}")
    print(f"Prompt length: {len(prompt)} characters")
    print()
    
    try:
        # Call Ollama API directly
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": LLM_MODEL,
                "prompt": prompt,
                "stream": False,
                "context": [],
                "options": {
                    "temperature": TEMPERATURE,
                    "num_predict": MAX_TOKENS
                }
            },
            timeout=60
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result.get('response', '').strip()
            print(f"Raw response: {repr(content)}")
            print()
            
            # Try to parse JSON
            try:
                # Clean up the response
                content_clean = content.strip()
                
                # Extract just the JSON object if there's extra text
                start_brace = content_clean.find('{')
                end_brace = content_clean.rfind('}')
                if start_brace != -1 and end_brace != -1 and end_brace > start_brace:
                    content_clean = content_clean[start_brace:end_brace + 1]
                
                print(f"Cleaned JSON: {content_clean}")
                
                parsed = json.loads(content_clean)
                first_name = parsed.get('first_name')
                last_name = parsed.get('last_name')
                
                print(f"Parsed result: first_name='{first_name}', last_name='{last_name}'")
                
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                print(f"Content that failed to parse: {repr(content_clean)}")
        else:
            print(f"API error: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

def test_llm_parsing():
    """Test the LLM parsing function with a simple case"""
    
    # Test case 1: Simple name
    print("Test 1: Simple name")
    contact_name = "JOHN SMITH"
    customer_name = ""
    email = "john.smith@example.com"
    
    print(f"Input: Contact='{contact_name}', Customer='{customer_name}', Email='{email}'")
    result = llm_parse_name(contact_name, customer_name, email)
    print(f"Result: {result}")
    print()

if __name__ == "__main__":
    test_simple_prompt()
    print("\n" + "="*50 + "\n")
    test_llm_api_directly()
    print("\n" + "="*50 + "\n")
    test_llm_parsing()
