import os
import re

results = []

def search_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                try:
                    search_file(os.path.join(root, file))
                except Exception as e:
                    #print(f"Error processing file {os.path.join(root, file)}: {e}")
                    continue

def search_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        file_content = file.read()
        variable_assignments = re.finditer(r"^(?P<var_name>\w*prompt\w*)\s*=\s*(?P<quote>['\"]{1,3})(?P<value>.*?)\2", file_content, re.DOTALL | re.MULTILINE)
        
        for match in variable_assignments:
            variable_name = match.group('var_name')
            variable_value = match.group('value')
            # print(f"File: {file_path}")
            # print(f"Variable name: {variable_name}")
            # print(f"Variable assignment: {variable_name} = {variable_value}\n")
            results.append((file_path.replace("/tmp/", r"./"), variable_name, variable_value))

if __name__ == "__main__":
    print("# About")
    print("- This is a collection of all variable assignments and their location in the [LangChain codebase](https://github.com/hwchase17/langchain), where the variable name contains 'prompt'.")
    print("- Only global variables are considered.")
    print("- See `langchain_analysis.py` for more information.")
    print("- This was a quick analysis script thrown together with ChatGPT -- feel free to reach out if I'm missing anything.")
    print("\n---\n")
    
    print("# LangChain Prompts")
    directory = "/tmp/langchain"
    search_files(directory)
    for file_path, variable_name, variable_value in results:
        print(f"## {variable_name} ({os.path.basename(file_path)})\n`{file_path}`\n```\n{variable_value}\n```\n")
