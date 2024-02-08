# AI Agent Workflow
Using CrewAI framework, this Project implements a LLM-powered Agent workflow that enables integration and seamless communication amongst Agents, such that they're able to collaboratively perform a given task.\
Consisting of three Agents - Researcher, Writer and Examiner - the workflow is aimed at generating assessment question and answers, given a specific topic.\
Under the hood, an Open-sourced LLM from Ollama (mistral-7b) is used for text generation.

## Participating Agents
1. **Researcher**: Develops ideas for teaching someone new to the subject.
2. **Writer**: Uses the Researcher's ideas to write a piece of text to explain the topic.
3. **Examiner**: Crafts 2-3 test questions to evaluate understanding of the created text, along with the correct answers.

## Installation
1. On Linux, install Ollama CLI:
    ```
    curl https://ollama.ai/install.sh | sh
    ```
2. Using Ollama CLI, download mistral-7B manifest
    ```
    ollama run mistral
    ```

3. Clone this repository to your local machine:
    ```
    git clone https://github.com/Xelvise/AI-Agent-Workflow.git
    ```
4. Navigate to the project directory:
    ```
    cd AI-Agent-Workflow
    ```
5. Create and activate a Virtual Environment: (Optional, but recommended)
     ```
     conda create -p <Environment_Name> python==<python version> -y
     ```
    ```
     conda activate <Environment_Name>/
    ```
6. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```

## Usage
1. Run the ```workflow.py``` script to execute the CrewAI agent workflow:
    ```
    python workflow.py
    ```
2. Follow the prompts in the terminal to input the desired topic or keywords for question generation.
3. View the generated text and test questions, along with their correct answers.