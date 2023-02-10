import json
def parseFunction(func):
    func,metadata = func.split("$$$$$$")
    metadata=json.loads(metadata)
    func = func.strip()
    return {"function_def": func,"name" : metadata['function_name'],"parameter_names": metadata['parameter']}

