# CIS580-Code-Review-Assistant
The repository for the University of Michigan - Dearborn CIS580 Fall 2025 Term Project

This is a Code Review Assistant tool that can proactively determine project files that are most frequently coorelated with bug fixes. Detailed analytics can be generated of your repository with assistance from Ollama LLM.

# Instructions for Tool

1. Navigate to the project directory ( CIS580-Code-Review-Assistant )
2. Set up virtual environment:
    a. `python3 -m venv venv`
    b. `venv\Scripts\activate`

3. Install Required Packages
    a. `pip install -r requirements.txt`

4. Install Ollama LLM
    a. Install Ollama from https://ollama.com/download/windows
    b. Follow all default settings for installation.
	c. Run `ollama pull llama3`

5. Finally you are ready to run the application.
    a. `python main.py`
    b. Navigate to http://127.0.0.1:8080/ on your preferred browser.
    c. Click Select a repository and enter a local or remote repository in the following box.
    d. You can now view your results or save your results to the results.csv file.
