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
                # find the package and get the whole package name with . in between
                match = re.search(r'package\s+(\w+(\.\w+)*)', line)
                if match:
                    self.package = match.group(1)
                # find the imports get the full class
                match = re.search(r'import\s+(\w+)', line)
                if match:
                    self.imports.append(match.group(1))

                # find the attributes starting with private, public, protected end with ;
                match = re.search(r'(private|public|protected)\s+(\w+)\s+(\w+);', line)
                if match:
                    self.attributes.append(match.group(2))



class Walk:
    """
    walk through the repos and parse them
    """
    def __init__(self, path):
        self.path = path
        self.java_files = []
        self.parses = {
            'classes': [],
            'attributes': [],
            'modules': []
        }
        self.all_parses = []
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
            for class_ in parser.classes:
                self.parses['classes'].append(class_)
            for att in parser.attributes:
                self.parses['attributes'].append(att)
            if parser.package:
                self.parses['modules'].append(parser.package.replace('.', '/'))
            self.all_parses.append(self.parses)
            self.parses = {
                'classes': [],
                'attributes': [],
                'modules': []
            }
        return self.all_parses
    
    def format_parses(self):
        formatted_parses = []
        classes = []
        all_classes = []
        attrs = []
        # we have [{'classes': [], 'attributes': [], 'modules': []}, ...] in self.all_parses
        # we want to get a list of all the attributes coresponing to a class and depengind on the module
        # make a list of [f"{model}/{class_}", [attr1, attr2, ...]]
        for parse in self.all_parses:
            for class_ in parse['classes']:
                classes.append(class_)
                all_classes.append({class_: parse['modules']})
            for attr in parse['attributes']:
                attrs.append(attr)
            for module in parse['modules']:
                if classes:
                    formatted_parses.append([f"{module}.{classes[0]}", attrs])
                classes = []
                attrs = []

        # if attrs not in clasess remove it
        for parse in formatted_parses:
            parse.append([])
            for attr in parse[1]:
                # if attr contains the words not in keys of all_classes remove it
                if any(attr in key for key in all_classes):
                    # parse[1].remove(attr)
                    # add like this f"module.class" to the attributes
                    parse[2].append(f"{list(filter(lambda x: attr in x, all_classes))[0][attr][0]}.{attr}")
                if not any(attr in key for key in all_classes):
                    # parse[1].remove(attr)
                    continue

        # make format_parses like this [f"{model}.{class_}->{module2}.{attr2}", ...]
        formatted_parses = [f"{parse[0]}->{attr}" for parse in formatted_parses for attr in parse[2]]
        return formatted_parses
            

if __name__ == "__main__":
    walk = Walk('data/uml-reverse-mapper')
    walk.parse()
    formatted_parse = walk.format_parses()
    print(formatted_parse)