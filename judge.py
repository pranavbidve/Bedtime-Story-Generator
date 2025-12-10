from llm import call_model

def judge_story(story_text: str) -> dict:
    """
    Returns: {
        'reasoning': str,  # The judge's explanation
        'scores': {        # Dictionary of scores out of 10
            'age_appropriate': float,
            'safety': float,
            'story_structure': float,
            'bedtime_suitable': float,
            'overall': float
        }
    }
    """

    judge_prompt = f"""
    You are a STRICT judge for bedtime stories for children ages 5-10.
    You will be given a story and 4 evaluation criteria below. 
    Your job is to only evaluate the story based on the criteria provided under the headings.
    If they do not meet then strictly do not give a score above 5 for that criterion.
    Overall score is the weighted average of the 4 criteria.
    The weightage for each criterion is as follows:
    - AGE_APPROPRIATE: 0.35
    - SAFETY: 0.25
    - STORY_STRUCTURE: 0.15
    - BEDTIME_SUITABLE: 0.25

    STORY TO EVALUATE:
    {story_text}

    EVALUATION CRITERIA:
    1. AGE_APPROPRIATE (0-10)
    - Give a score more than 5 if the story has friendship, kindness, curiosity, and positive emotional growth for children ages 5-10, otherwise give a score less than 5.
    - Have a detailed reasoning on why it is or is not appropriate for children ages 5-10 and where it could be improved.

    2. SAFETY (0-10)
    - Give a score of 0 if the story contains violence, scary themes, or inappropriate content; otherwise give a score more than 5.
    - Have a detailed reasoning on why the story is or is not safe - include keywords, phrases, situations, characters and where it could be improved.

    3. STORY_STRUCTURE (0-10)
    - Give a score more than 6 if the story has a clear beginning, middle, end with a story arc; otherwise give a score less than 6.
    - Give a score more than 8 if the story has a simple, concrete vocabulary aligned with a Grade 1–3 reading level; otherwise give a score less than 8.
    - Have a detailed reasoning if the story breaks abruptly, is too fast paced, cannot be read in one sitting, and suggest ways of improvement.

    4. BEDTIME_SUITABLE (0-10)
    - Give a score more than 8 if the story has a soothing narrative tone designed to help children relax before sleep; otherwise give a score less than 8.
    - Give a score more than 5 if the story has a calm, peaceful tone suitable for bedtime; otherwise give a score less than 5.
    - Have a detailed reasoning if the story is too loud, chaotic or exciting and suggest ways of improvement.

    5. OVERALL (0-10): Weighted average considering all factors
    - Be honest: most stories are not perfect and most are not 10/10 for any criterion.
    - A score of 10 should be extremely rare. Only give 10 if the story meets every requirement flawlessly, with no weaknesses, and you would not change anything meaningful about it.

    EVALUATION PROCESS:
    1. First, read the story carefully.
    2. Think through each criterion step-by-step.
    3. Provide reasoning for your scores.
    4. Calculate the overall score using the weights.

    RESPONSE FORMAT (IMPORTANT):
    You MUST respond with a single valid JSON object and NOTHING else. 
    Do NOT include any prose outside the JSON. Do NOT use Markdown or code fences.

    The JSON must have this exact structure:

    

    {{
    "reasoning": {{
        "AGE_APPROPRIATE": "<Provide 2–3 sentences explaining how the themes, vocabulary, and emotional tone fit (or do not fit) children ages 5–10. You MUST refer to exact sentences, phrases, and character name actions from the story. Describe precisely which parts may be too mature or unclear for this age group, and state exactly where (e.g., 'in the second paragraph when the character X does Y…') improvements should be made.>",
        "SAFETY": "<Provide 2–3 sentences identifying specific words, scenes, character behaviors, or descriptions that are safe or unsafe. You MUST cite concrete examples from the story (e.g., 'the line where the dragon roars loudly…', 'the phrase \"sharp claws\" in sentence 4…'). Clearly explain exactly where safety improvements should be applied and what should be changed to make the moment safer for children.>",
        "STORY_STRUCTURE": "<Provide 2–3 sentences analyzing whether the beginning, middle, and end are clear and coherent. Refer to exact points in the story, such as 'in the opening paragraph…', 'at the transition to the middle section…', or 'in the final two sentences…'. You MUST identify exact locations where pacing feels too fast/slow, where transitions are abrupt, or where the plot becomes confusing, and state exactly what structural improvement should be made.>",
        "BEDTIME_SUITABLE": "<Provide 2–3 sentences evaluating the calmness and soothing tone of the story. You MUST cite exact lines, character actions, or scenes that are too exciting, loud, chaotic, or energetic (e.g., 'the scene in paragraph 3 where the dog jumps and shouts…'). State precisely where the tone disrupts bedtime suitability and describe specific changes to make those moments more relaxing.>",
        "IMPROVEMENT_SUMMARY": "<Summarize ONLY the criteria that need improvement. Reference exact lines, scenes, or character moments (e.g., 'the sentence where X happens…'). Provide 1–2 very concrete and actionable rewrites or adjustments that directly target those exact story locations.>"
    }},
    "scores": {{
        "AGE_APPROPRIATE": <number between 0 and 10>,
        "SAFETY": <number between 0 and 10>,
        "STORY_STRUCTURE": <number between 0 and 10>,
        "BEDTIME_SUITABLE": <number between 0 and 10>,
        "TOTAL": <overall weighted score between 0 and 10, as a number (can be decimal)>
    }}
    }}

    

    Make sure:
    - All scores are numeric (not strings).
    - TOTAL is correctly computed using the given weights.
    - The JSON is syntactically valid.
    - You respond with ONLY the JSON object, no other text before or after it.
    - Do NOT wrap the JSON in markdown code blocks or any other formatting.
    """

    return call_model(judge_prompt, max_tokens=700, temperature=0.01)