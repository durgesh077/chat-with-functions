import os
from dotenv import load_dotenv
import json
from flask import Flask, request ,render_template, make_response
openai = __import__("openai")
openai.api_key = os.getenv("OPENAI_API_KEY")
from utils.parseFunction import parseFunction

app = Flask(__name__,
            static_url_path='/static', 
            static_folder='build/static',
            template_folder='build')
load_dotenv()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def api():
    print("hello")
    print(request.json['prompt'])
    prompt = """
    convert the following text command as a javascript language's arrow function with proper indentation without comments without  test cases and without explanation
    also give the name of the function and the parameter names in the following format

    -whenever necessary parse the parameter to convert into required datatype as I'll pass the parameter as string
    -answer same as previous if similar question is asked 
    -always give arrow function
    -no extra spaces, new lines, or comments or tabs outside the function definition body
    -no comments in function body
    -do not explain the function
    -no comments in function body or outside the function definition body
    -the function should return result in string format (i.e. asked query like print 1-100 then function should return 1-100 as string)
    -only and only 1 function 
    -please don't explain function as it will be rendered by javascript engine
    -function naming convention :- word separated by underscore
    -separate function definition and metadata with $$$$$ i.e. exactly 5 dollar signs
    -after $$$$$ it should be parsable by json.loads and should return a dictionary with keys function_name, parameter
    -parameter type should be string, int, float, boolean, list, object


    example input:- add two numbers

    example output:-

    two_number_sum = (a,b,prefix)=>{\n\tconst ans=a+b;\n\t  return ans;\n }$$$$$${"function_name": "two_number_sum" ,  "parameter": [["a","int"],["b","int"], ["c","string"]]}
    
    function declaration on following :-
    
    %s
        """%request.json['prompt']
    try:
        completions = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=2048,
            n=1,
            stop=None,
            temperature=1,
        )
        message = completions.choices[0].text
        # print(message)
        response = parseFunction(message)
        # print(response)
        return response
    except Exception as e:
        print(e)
        return make_response('unable to create function',400)


if __name__ == "__main__":
    app.run()
