class Classification {
  model_reasoning string @description(#"
    The reasoning steps of the model before outputing the result.
  "#)
  chosen_theme Chosen_Theme
}

class Chosen_Theme {
    title string
    description string
}

// Create a function to classify the json input
function Classify(json: string) -> Classification {
  client "OllamaLlama3" 
  prompt #"
    You are a classification assistant. Your job is to analyze a customer’s message and select the most appropriate theme from a provided list.

    You will receive a JSON object with:
    - a 'text' field: the message to classify
    - a 'themes' field: a list of possible themes, each with a title and a description

    Your task is to:
    1. Read and understand the customer's message
    2. Compare it carefully with each theme description
    3. Select the best matching theme
    4. Explain your reasoning clearly and concisely

    Input JSON:
    {{ json }}

    Return your result in the following JSON format:
    {{ ctx.output_format }}

    Make sure your explanation includes why this theme was chosen over the others.
  "#
}

// Test the function with a sample resume. Open the VSCode playground to run this.
test vaibhav_json {
  functions [Classify]
  args {
    json #"{
    "text": "I am calling because I have a problem with my internet connection",
    "themes": [
        {
            "title": "Technical support",
            "description": "The customer is calling for technical support"
        },
        {
            "title": "Billing",
            "description": "The customer is calling for billing issues"
        },
        {
            "title": "Refund",
            "description": "The customer is calling for a refund"
        }
    ]
}
    "#
  }
}
