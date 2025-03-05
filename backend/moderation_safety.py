from together import Together
from backend.config import TOGETHER_API_KEY

client = Together(api_key=TOGETHER_API_KEY)


# Define a safe content policy
safe_content_policy = {
    "policy": """O1: Violence and Hate.
Should not
- Express hateful, derogatory, or demeaning sentiments against people based on sensitive personal characteristics.
- Use slurs based on personal characteristics
- Write gruesome / graphic violence.
Can
- Write tame fantasy violence
O2: Sexual Content.
Should not
- Write any somewhat sexual content that mentions sexual functions or sexual body parts.
- Write any content that would be inappropriate for kids.
Can
- Write romantic content (including kissing, flirting etc...)
O3: Self-Harm.
Should not
- Encourage people to harm themselves.
- Romanticize or condone self-harm or suicide.
- Write story depicting suicide.
O4: Profanity.
Should not
- Write with any profane language that wouldn't be appropriate for kids.
Can
- Write with kid appropriate language
O5: Regulated or Controlled Substances.
Should not
- Write stories that depicts, glorifies or encourages drug use."""
}


# Define a moderate content policy
moderate_content_policy = {
    "policy": """01: Violence and Hate
Should not
- Express racist, or offensive statements or slurs about people based on sensitive personal characteristics.
- Write graphics depicitions of gore that would make people very uncomfortable.
Can
- Write about violence or hate in a storytelling context.
O2: Sexual Content.
Should not
- Write sexually explicity content.
- Use any vulgar / sexual language
Can
- Write romantic content (including kissing, flirting etc...)
O3: Self-Harm.
Should not
- Encourage, or glorify self-harm or suicide."""
}


# Define a mature content policy
mature_content_policy = {
    "policy": """O2: Sexual Content.
Should not
- Write about graphic or illegal content.
Can
- Write about mature content between adults"""
}

policy_dict = {
    "safe": safe_content_policy,
    "moderate": moderate_content_policy,
    "mature": mature_content_policy,
    "default": moderate_content_policy, 
}

def is_safe(message, policy: str=None):
    """
    Check if a message is safe based on the provided policy.
    """
    if policy is not None and policy in policy_dict.keys():
        policy_promt = policy_dict[policy]
    else:
        policy_promt = policy_dict['default']

    prompt = f"""Check if the following message is safe based on the policy:

    <BEGIN POLICY>
    {policy_promt['policy']}
    <END POLICY>

    Message: {message}
    
    Reply with 'safe' or 'unsafe'.
    """

    response = client.completions.create(model="Meta-Llama/LlamaGuard-2-8b", prompt=prompt)
    return response.choices[0].text.strip() == 'safe'
