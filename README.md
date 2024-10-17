# WhitegloveAI Consulting Agent
***This is an experimental project to explore the use of Swarm for AI consulting. Not for production use. We strongly recommend a human in the loop and proper training and knowledge transfer of AI solutions. Contact us for more @ https://www.whitegloveai.com***

AI consulting agent that uses the Swarm framework to analyze project specifications and build the neccesary artifacts repository for strategy and implementations.
```mermaid
graph TD
    U[User] -->|Input| CAIO[CAIO Agent]
    CAIO -->|collect_user_info| M[(metadata.json)]
    CAIO -->|create_strategy| S[project-name-master-plan.md]
    CAIO -->|pass_to_ai_architect| A[Architect Agent]
    A -->|create_design| D[project-name-solution-architecture.md]
    A -->|write_to_file| P[project-name-specifications.md]
    A -->|pass_to_ai_engineer| E[Engineer Agent]
    E -->|build_code| C[Generated Code Files]
    E -->|write_to_file| R[README.md]
    
    subgraph Artifact Folder
        M
        S
        D
        P
        C
        R
    end

    classDef agent fill:#2c3e50,stroke:#333,stroke-width:2px,color:white;
    classDef file fill:#34495e,stroke:#333,stroke-width:2px,color:white;
    class CAIO,A,E agent;
    class M,S,D,P,C,R file;
```

## Installation

```bash
# Create and activate virtual environment
python3 -m venv ./venv
source ./venv/bin/activate

# Install Swarm and dependencies
pip install git+https://github.com/openai/swarm.git
pip install -r requirements.txt
```

## Setup

Copy the .env.example file to .env and supply your OpenAI API key. 

## Usage

```bash
python index.py
```
