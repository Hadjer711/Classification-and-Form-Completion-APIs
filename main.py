from fastapi import FastAPI
from pydantic import BaseModel
from baml_client import b
import json
from collections import Counter

app = FastAPI()

class Theme(BaseModel):
    """
    Represents a theme used in the classification input.

    Attributes:
        title (str): The title of the theme.
        description (str): A short explanation of what the theme covers.
    """
    title: str
    description: str

class ClassificationInput(BaseModel):
    """
    Input model for the /classify endpoint.

    Attributes:
        text (str): The input text to be classified.
        themes (list[Theme]): A list of themes against which the input will be classified.
    """
    text: str
    themes: list[Theme]

class FormCompletionInput(BaseModel):
    """
    Input model for the /form_completion endpoint.

    Attributes:
        text (str): The text (e.g., conversation) from which to extract form fields.
    """
    text: str

@app.post("/classify")
async def classify(input: ClassificationInput):
    """
    Classifies the given text against provided themes using a BAML streaming model.

    Args:
        input (ClassificationInput): Input text and themes to classify.

    Returns:
        List of model output chunks or an error message.
    """
    try:
        json_input = json.dumps(input.dict())  # Convert dict to JSON string
        stream = b.stream.Classify(json_input)
        result = [chunk.model_dump() for chunk in stream]
        return result
    except Exception as e:
        print("Error in /classify:", e)
        return {"error": str(e)}

@app.post("/form_completion")
async def extract_complete_form(input: FormCompletionInput):
    """
    Extracts structured form data from a conversation-like input using a BAML streaming model.

    Args:
        input (FormCompletionInput): Text input containing a simulated dialogue.

    Returns:
        List of model output chunks or an error message.
    """
    try:
        json_input = json.dumps(input.dict())  # Convert dict to JSON string
        stream = b.stream.Form_Completetion(json_input)
        result = [chunk.model_dump() for chunk in stream]
        return result
    except Exception as e:
        print("Error in /form_completion:", e)
        return {"error": str(e)}


### Bonus 1: Probabilistic Text Classification

class ClassificationInputProbabilistic(BaseModel):
    text: str
    themes: list[Theme]
    repeat: int = 5  # Number of classification runs (default: 5)

@app.post("/classify_prob")
async def classify_prob(input: ClassificationInputProbabilistic):
    """
    Performs probabilistic classification by running the model multiple times
    and returning a confidence score for each theme based on frequency.

    Args:
        input (ClassificationInputProbabilistic): Text, themes, and repeat count.

    Returns:
        Dictionary with confidence scores and most likely label.
    """
    try:
        json_input = json.dumps(input.dict())

        counts = Counter()

        # Run classification multiple times
        for _ in range(input.repeat):
            response = b.Classify(json_input)  # non-streaming call
            result = response.model_dump()
            print(result)
            print('\n \n')

            # Expecting structure: {"chosen_theme": {"title": "..."}}
            if "chosen_theme" in result:
                theme_title = result["chosen_theme"]["title"]
                counts[theme_title] += 1

        total = sum(counts.values())
        if total == 0:
            return {"error": "No valid classifications were returned."}

        probabilities = {
            label: round(count / total, 2) for label, count in counts.items()
        }

        return {
            "text": input.text,
            "confidence_scores": probabilities,
            "most_likely": max(probabilities, key=probabilities.get)
        }

    except Exception as e:
        print("Error in /classify_prob:", e)
        return {"error": str(e)}