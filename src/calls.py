import argparse
import json
import subprocess
import regex as re
import scipy
import statistics


class Function:
    name: str
    file: str
    start_line: int
    calls: list['Function']
    called_by: list['Function']


    def __init__(self, name: str, file:str, start_line:int):
        self.name = name
        self.file = file
        self.start_line = start_line
        self.calls = []
        self.called_by = []
    

    def add_call(self, call: 'Function') -> None:
        if call not in self.calls:
            self.calls.append(call)
        call.add_called_by(self)


    def add_called_by(self, caller: 'Function') -> None:
        if caller not in self.called_by:
            self.called_by.append(caller)
    

    def __hash__(self) -> int:
        return hash((self.name, self.file, self.start_line))
    

    def __eq__(self, other) -> bool:
        if not isinstance(other, Function):
            return NotImplemented
        return ((self.name, self.file, self.start_line) == (other.name, other.file, other.start_line))
    
    
    def __str__(self) -> str:
        return "File: " + self.file + "\nName: " + self.name + "\nLine: " + str(self.start_line) + "\nCalls: " + str(self.calls) + "\nCalled by: " + str(self.called_by)

    

def handle_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="The string path for the project of analysis")
    return parser.parse_args()


def process_project(project_path:str) -> None:
    p = subprocess.Popen("ctags --output-format=json --fields=+n -R * > tags.json", shell=True, cwd=project_path)
    p.wait()


def process_json(project_path:str, files:dict[str,list[Function]], functions:list[Function], function_names:dict[str:list[Function]]) -> None:
    lines = []
    with open(project_path + "/tags.json") as data:
        for line in data:
            lines.append(json.loads(line))
    
    for line in lines:
        if line['kind'] == 'function' or line['kind'] == 'method':
            line_number = int(line['line'])
            name = line['name']
            file = line['path']
            new = Function(name, file, line_number)
            if name in function_names:
                print("Duplicate Found: " + name + "\nOriginal: " + str(function_names[name][0]) +"\nNew: " + str(new))
                function_names[name].append(new)
                print("")
            else:
                function_names[name] = [new]
            if file in files:
                files[file].append(new)
            else:
                files[file] = [new]
            functions.append(new)


def organize_files(files:dict[str,list[Function]]) -> None:
    for key in files:
        files[key] = sorted(files[key], key=lambda x: x.start_line, reverse=True)


def find_calls(project_path: str, files:dict[str,list[Function]], function_names:dict[str:list[Function]]) -> None:
    pattern = "([A-Za-z0-9_]+)\("
    for f in files:
        with open(project_path + "/" + f) as f_read:
            full_text = f_read.readlines()
            for i in range(len(full_text)):
                line = full_text[i]
                matches = re.findall(pattern, line)
                for match in matches:
                    if match in function_names:
                        caller_line = i + 1
                        caller = None
                        for function in files[f]:
                            if function.start_line == caller_line:
                                break
                            elif function.start_line < caller_line:
                                caller = function
                                break
                        if caller is not None:
                            for function in function_names[match]: # Currently calls all duplicates. Can add special cases
                                caller.add_call(function)
                            

def main() -> None:
    args = handle_args()
    process_project(args.path)
    files = {}
    functions = []
    function_names = {}
    process_json(args.path, files, functions, function_names)
    organize_files(files)
    find_calls(args.path, files, function_names)
    util_in = []
    util_out = []
    util_count = 0
    non_in = []
    non_out = []
    non_count = 0
    for key in files:
        # print("--File: " + key + "--")
        for func in files[key]:
            if "util" in key.lower() or "helper" in key.lower():
                util_count += 1
                util_in.append(len(func.called_by))
                util_out.append(len(func.calls))
            else:
                non_count += 1
                non_in.append(len(func.called_by))
                non_out.append(len(func.calls))
            
            
            # print(func.name)
            # print("\ncalls:")
            # print(func.calls)

            # print("\ncalled by:")
            # print(func.called_by)
    print("Util Stats:")
    print("Util In:", statistics.median(util_in))
    print("Util Out:", statistics.median(util_out))
    print("Util Count:", util_count)
    
    print("Non-Util Stats:")
    print("Non-Util In:", statistics.median(non_in))
    print("Non-Util Out:", statistics.median(non_out))
    print("Non-Util Count:", non_count)
    
    print("In MWW")
    print(scipy.stats.mannwhitneyu(util_in, non_in))

    print("out MWW")
    print(scipy.stats.mannwhitneyu(util_out, non_out))

    print("--------\n\n")

if __name__ == '__main__':
    main()
