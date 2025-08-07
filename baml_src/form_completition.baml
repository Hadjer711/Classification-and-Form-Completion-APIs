class Completed_Form {
  title string
  type string
  properties Properties
}
class Properties {
    personal_info Personal_Info
    contact_info Contact_Info
}

class Personal_Info {
    type string
    properties Personal_Properties

}

class Personal_Properties {
    first_name string @description(#"The customer's first name"#)
    last_name string @description(#"The customer's last name"#)
    gender Gender @description(#"The customer's gender"#)
}

enum Gender {
    Male
    Female
    Other
}

class Contact_Info {
    type string?
    properties Contact_Properties?

}
class Contact_Properties {
    email string? @description(#"The customer's email address"#)
    phone string? @description(#"The customer's phone number"#)
    preferred_contact_method Preferred_Contact_Method? @description(#"The customer's preferred method of contact"#)
    call_reasons string[]? @description(#"The reasons for the call"#)
}

enum Preferred_Contact_Method {
    Email
    Phone
}

// Create a function to complete a form
function Form_Completetion(json: string) -> Completed_Form {
  client "OllamaLlama3" 
  prompt #"
    You are a form extraction assistant.

    Your task is to extract structured customer information from a transcript of a conversation between an agent and a customer.

    The input will be a JSON object that contains a single key:
    - `text`: the full transcript

    Do not invent or assume information that was not stated.

    Input transcript:
    {{ json }}

    Now return the completed form in the required structure :
    {{ ctx.output_format }}
  "#
}

test vaibhav_json {
  functions [Form_Completetion]
  args {
    json #"{
    "text": "Agent: Good morning! Thank you for reaching out. I’ll need to collect some basic details to assist you better. Could you please provide your first and last name? Customer: Sure! My name is John Doe. Agent: Thank you, John. May I also ask for your gender? Customer: I'd prefer not to share that at the moment. Agent: No problem at all. Now, for contact purposes, could you share your email address? Customer: Yes, my email is johndoe@example.com. Agent: Great! Do you have a phone number where we can reach you? Customer: I’d rather not provide that right now. Agent: That’s completely fine. How would you prefer us to contact you—by email or phone? Customer: Please contact me via Email. Agent: Understood! Lastly, can you share the reason for your call today? Customer: I’m not ready to specify that just yet. Agent: That’s okay, John! I’ve noted everything down. If you need any further assistance, feel free to reach out. Have a great day!"
}
    "#
  }
}
