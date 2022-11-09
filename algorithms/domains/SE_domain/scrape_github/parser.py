import os
import sys
import re


class JavaParser:
    """
    parse java repos from data folder and extract the code
    in order to get the classes and attributes
    """
    def __init__(self, filename):
        self.filename = filename
        self.classes = []
        self.attributes = []
        self.imports = []
        self.package = None
        self.parse()
    
    def parse(self):
        with open(self.filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                # using regex to find the classes
                match = re.search(r'class\s+(\w+)', line)
                if match:
                    self.classes.append(match.group(1))
                # find the package
                match = re.search(r'package\s+(\w+)', line)
                if match:
                    self.package = match.group(1)
                # find the imports get the full class
                match = re.search(r'import\s+(\w+)', line)
                if match:
                    self.imports.append(match.group(1))

                # find the attributes starting with private, public, protected end with ;
                match = re.search(r'(private|public|protected)\s+(\w+)\s+(\w+);', line)
                if match:
                    self.attributes.append(match.group(3))



class Walk:
    """
    walk through the repos and parse them
    """
    def __init__(self, path):
        self.path = path
        self.java_files = []
        self.parses = {}
        self.walk()
    
    def walk(self):
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith('.java'):
                    self.java_files.append(os.path.join(root, file))
    
    def parse(self):
        for file in self.java_files:
            parser = JavaParser(file)
            print("=" * 50)
            print(f"Filename: {file}")
            print(f"Classes: {parser.classes}")
            print(f"Attributes: {parser.attributes}")
            print(f"Imports: {parser.imports}")
            print(f"Package: {parser.package}")
            print("=" * 50)
            self.parses[file] = parser
        return self.parses

if __name__ == "__main__":
    walk = Walk('data')
    walk.parse()

