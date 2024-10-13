import os
import json
from swarm import Swarm, Agent
from swarm.repl import run_demo_loop
from dotenv import load_dotenv

load_dotenv()

swarm = Swarm()

FOLDER = "agent_artifacts"

def create_artifact_folder(folder_name):
    artifact_folder = folder_name
    if not os.path.exists(artifact_folder):
        os.makedirs(artifact_folder)
    return artifact_folder

def write_to_file(content, filename, extension=".txt"):
    filepath = os.path.join(FOLDER, f"{filename}{extension}")
    with open(filepath, "w") as f:
        f.write(content)
    return filepath

def analyze_specifications(context_variables):
    """
    Analyze specifications to design AI solutions.
    
    Args:
        specifications (dict): A dictionary containing project specifications.
    
    Returns:
        str: Analyzed specifications with design proposals in Mermaid markdown format.
    """
    filepath = write_to_file(mermaid_diagram, "solution_design", ".md")
    return f"Solution design created and saved to {filepath}\n\n{mermaid_diagram}"

def build_code(specifications):
    """
    Build functional code based on provided specifications.
    
    Args:
        specifications (dict): A dictionary containing design specifications.
    
    Returns:
        str: The path to the generated code files.
    """
    code_content = specifications["code_content"]
    filepath = write_to_file(code_content, "generated_code", ".py")
    return f"Code generated and saved to {filepath}\n\n{code_content}"

def collect_user_info(context_variables):
    """
    Collects comprehensive user and company information and generates AI officer instructions.

    Returns:
        dict: Context variables containing user and company information.
    """
    context_variables = {
        "name": input("Enter your name: "),
        "position": input("Enter your position: "),
        "company_name": input("Enter your company name: "),
        "data_situation": input("Describe the data situation: "),
        "process_business_challenges": input("Describe the business challenges: "),
        "major_data_sources": input("Enter major data sources (comma-separated): ").split(","),
        "location": input("Enter your location: ")
    }
    
    filepath = write_to_file(json.dumps(context_variables, indent=2), "user_info", ".json")
    print(f"User info collected and saved to {filepath}")
    
    return context_variables

def ai_officer_instructions(context_variables):
    company_name = context_variables["company_name"]
    data_situation = context_variables["data_situation"]
    process_business_challenges = context_variables["process_business_challenges"]
    major_data_sources = context_variables["major_data_sources"]
    name = context_variables["name"]
    position = context_variables["position"]
    location = context_variables["location"]
    
    instructions = f"""
        You are the Chief AI Officer for {company_name}, responsible for overseeing the strategic implementation of AI across the organization. 
        You process and analyze business requirements to align AI initiatives with company goals.
        Current situation: {data_situation}
        Challenges: {process_business_challenges}
        Major data sources: {', '.join(major_data_sources)}
        You are assisting {name}, who is the {position} located in {location}.
        Your task is to provide strategic guidance on how to address these challenges and leverage AI effectively.
        
        Use analyze_specifications() to analyze the business requirements and pass the results to the AI Architect with pass_to_ai_architect() function.
    """


    return instructions

def architect_instructions(context_variables):
    instructions = f"""
        You are an AI Architect that provides deep specifications and analysis of business requirements from the Chief AI Officer.
        You process and analyze business requirements and specifications to design effective AI solutions.
        Always add the solution design to the artifact folder with write_to_file() function.
        All work should be done in the artifact folder.
    """
    return instructions

def engineer_instructions(context_variables):
    instructions = f"""
        You are an AI Engineer that builds functional code.
        You develop and implement code based on specifications to fulfill business requirements.
        Create the code in a new file in the artifact folder with write_to_file() function.
        All work should be done in the artifact folder write to a single .py file.
    """
    return instructions

def pass_to_ai_architect():
    return ai_architect_agent

def pass_to_ai_engineer():
    return ai_engineer_agent

ai_officer_agent = Agent(
    name="Smith",
    instructions=ai_officer_instructions,
    functions=[collect_user_info, pass_to_ai_architect, write_to_file]
)

ai_architect_agent = Agent(
    name="Jarvis",
    instructions=architect_instructions,
    functions=[write_to_file, pass_to_ai_engineer]
)

ai_engineer_agent = Agent(
    name="Jasmine",
    instructions=engineer_instructions,
    functions=[build_code, write_to_file]
)

if __name__ == "__main__":
    FOLDER = create_artifact_folder("agent_artifacts")
    run_demo_loop(ai_officer_agent, stream=True)
