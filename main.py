from os import environ as env
from typing import Union

from fastapi import FastAPI, Request
from openai import OpenAI, RateLimitError
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# defaults to getting the key using os.environ.get("OPENAI_API_KEY")
# if you saved the key under a different environment variable name, you can do something like:
# client = OpenAI(
#     api_key=os.environ.get("OPENAI_API_KEY"),
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = env['OPENAI_API_KEY']
client = OpenAI(api_key=api_key)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/answer/{question}")
async def generate_answer(question: str):

    try:
        # Define the prompt message with the desired text
        prompt_message = "Generate a code example based on the given question and provide the response as a JSON object. The object should include the code as a string and the language as a string."

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt_message},
                {"role": "user", "content": question}
            ]
        )

        return {"answer": completion.choices[0].message}
    except RateLimitError as e:
        return {"error": "Rate limit exceeded. Please try again later."}


@app.get("/wrong_answer/{answer}")
async def generate_wrong_answer(answer: str):
    # List to store wrong answers
    wrong_answers = []

    # Generate wrong answers using helper functions
    wrong_answers.append(get_answer_one(answer))
    wrong_answers.append(get_answer_two(answer))
    wrong_answers.append(get_answer_three(answer))

    # Return JSON response with the list of wrong answers
    return {"wrong_answers": wrong_answers}


def get_answer_one(answer: str) -> str:
    answer = answer.replace('>', '<')
    answer = answer.replace('<', '<=')
    answer = answer.replace('==', '!=')
    answer = answer.replace('>', '>=')
    return answer


def get_answer_two(answer: str) -> str:
    answer = answer.replace(':', '?')
    answer = answer.replace('+', '-')
    answer = answer.replace('1', '0')
    answer = answer.replace('|', '&')
    return answer


def get_answer_three(answer: str) -> str:
    answer = answer.replace('<', '>')
    answer = answer.replace('<=', '<')
    answer = answer.replace('!=', '==')
    answer = answer.replace('>=', '>')
    return answer
