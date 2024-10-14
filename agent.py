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

def write_to_file(content, filename):
    filepath = os.path.join(FOLDER, f"{filename}")
    with open(filepath, "w") as f:
        f.write(content)
    return filepath

def create_strategy(context_variables):
    """
    Analyze specifications to design AI solutions.
    
    Args:
        specifications (dict): A dictionary containing project specifications.
    
    Returns:
        str: Analyzed specifications with design proposals in Mermaid markdown format.
    """
    instructions = f"""
        PROVIDE A STRATEGY FOR THE PROJECT. INCLUDE TECH STACK, TIMELINES, LEVELS OF EFFORT, SCOPE OF WORK,

        OUTPUT THE STRATEGY IN A FILE CALLED project-name-master-plan.md with write_to_file() function.
    """
    return instructions

def create_design(context_variables):
    """
    Analyze specifications to design AI solutions.
    
    Args:
        specifications (dict): A dictionary containing project specifications.
    
    Returns:
        str: Analyzed specifications with design proposals in Mermaid markdown format.
    """
    instructions = f"""
        PROVIDE A MERMAID DIAGRAM OF THE DESIGN. CODE ONLY. PROVIDE SEVERAL DEPLOYMENT SCENARIOS FOR PUBLIC AND PRIVATE CLOUD NETWORKS.

        OUTPUT THE MERMAID DIAGRAM IN A FILE CALLED project-name-solution-architecture.md with write_to_file() function.
    """
    return instructions

def build_code(specifications):
    """
    Build functional code based on provided specifications.
    
    Args:
        specifications (dict): A dictionary containing design specifications.
    
    Returns:
        str: The path to the generated code files.
    """
    code_content = specifications["code_content"]
    filepath = write_to_file(code_content, "generated_code")
    return f"Code generated and saved to {filepath}\n\n{code_content}"

def collect_user_info(context_variables):
    """
    Collects comprehensive user and company information and generates AI officer instructions.

    Returns:
        dict: Context variables containing user and company information.
    """

    file_path = os.path.join(FOLDER, "metadata.json")
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            context_variables = json.load(f)
        print(f"User info loaded from {file_path}")
        return context_variables
    else:
        context_variables = {
            "name": input("What is your name: "),
            "position": input("What is your professional title: "),
            "company_name": input("What is your company name: "),
            "project_name": input("What do you want to name this project: "),
            "data_situation": input("Describe the data situation: "),
            "process_business_challenges": input("Describe the business challenges: "),
            "major_data_sources": input("Enter major data sources (comma-separated): ").split(","),
            "location": input("Where are you located: ")
        }
        
        filepath = write_to_file(json.dumps(context_variables, indent=2), "metadata.json")
        print(f"User info collected and saved to {filepath}")
        
        return context_variables

def caio_instructions(context_variables):
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
        
        Use create_strategy() to analyze the business requirements and pass the results to the AI Architect with pass_to_ai_architect() function.
    """
    return instructions

def architect_instructions(context_variables):
    instructions = f"""
        You are an AI Architect that provides deep specifications and analysis of strategy from the Chief AI Officer strategy.
        You process and analyze business requirements and specifications to design effective AI solutions.
        Always add the solution design to the artifact folder with write_to_file() and create_design() functions.
        All work MUST SAVED in the artifact folder titled project-name-specifications.md

        Be very detailed in your specifications and analysis 
    """
    return instructions

def engineer_instructions(context_variables):
    instructions = f"""
        You are an AI Engineer that builds functional code.
        You create a subdirectory in the {FOLDER} with the name of the project.
        You develop and implement code based on specifications to fulfill business requirements.
        You receive specifications from the AI Architect and build the code in a new file in the artifact folder with write_to_file() function.
        Create the code in a new file in the artifact folder with write_to_file() function. CODE ONLY.
        All work should be done in the artifact folder write in either python or golang.

        ONCE THE CODE ONLY FILES ARE GENERATED, WRITE AN ADDITIONAL FILE CALLED README.md explaining setups, dependencies, and how to run the code.
    """
    return instructions

def pass_to_ai_architect():
    return ai_architect_agent

def pass_to_ai_engineer():
    return ai_engineer_agent

caio_agent = Agent(
    name="CAIO",
    instructions=caio_instructions,
    functions=[collect_user_info, create_strategy, pass_to_ai_architect, write_to_file]
)

ai_architect_agent = Agent(
    name="Architect",
    instructions=architect_instructions,
    functions=[create_design, write_to_file, pass_to_ai_engineer]
)

ai_engineer_agent = Agent(
    name="Engineer",
    instructions=engineer_instructions,
    functions=[build_code, write_to_file]
)

if __name__ == "__main__":
    FOLDER = create_artifact_folder("artifacts")
    run_demo_loop(caio_agent, stream=True, debug=True)