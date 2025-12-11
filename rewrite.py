from llm import call_model

def user_feedback(story: str, reasoning: dict) -> str:
    """
    This function does NOT rewrite the story yet.
    It:
      - Summarizes the story and the improvement suggestions.
      - Asks the user specific questions about what they want changed.
    """
    user_feedback_prompt = f"""
    You are a children's storyteller and a friendly story coach.

    You will be given:
    - A bedtime story for children ages 5–10
    - An automatic evaluation with suggestions for improvement

    Your task is:
    1) Understand the story and the improvement suggestions.
    - main characters by name.
    - the core plot and any clear moral or lesson.

    2) Tell the user hope you liked the story - mention the characters or theme in 1 line.

    2) Then, using the reasoning and improvement suggestions, ask the user
    1 question about how they would like the story to change.
    - Refer directly to characters, scenes, or moments from the story
        (for example: "the part where Alex and the dog race to the hill").
    - Focus on things like:
        • Length: shorter or longer
        • Tone: calmer, sweeter, more exciting, more emotional, etc.
        • Character development: deeper feelings, clearer goals, more growth
        • Story arc: clearer beginning–middle–end, a stronger problem and resolution
        • Slightly more mature themes (but still safe for ages 5–10)
        • More “kiddish” / playful elements

    3) Present the options in a simple, user-friendly way and involve the characters and plots and moral lessons they can answer easily. Ask only 1 question.
    Add a second question to ask if they want to change anything else. Refer to the improvement_summary for this say OR would you like a completely different story.
    - Focus on things like:
        • Length: shorter or longer
        • Tone: calmer, sweeter, more exciting, more emotional, etc.
        • Character development: deeper feelings, clearer goals, more growth
        • Story arc: clearer beginning–middle–end, a stronger problem and resolution
        • Slightly more mature themes (but still safe for ages 5–10)
        • More “kiddish” / playful elements

    Important:
    - Refrain from using bullets while asking the user questions.
    STORY:
    {story}

    EVALUATION REASONING (for your reference):
    {reasoning}
    """
    return call_model(user_feedback_prompt, max_tokens=500, temperature=0.8)


def rewrite_story(story: str, improvement_summary: str, user_improvement: str) -> str:
    """
    This function generates a new requirement for the next story version, based on:
    - The judge's improvement summary
    - The user's direct feedback and do not sanitize them or change them.

    It does NOT rewrite the story yet. It only returns a JSON object with "new_requirement".
    """

    rewrite_story_prompt = f"""
    You are a children's storyteller and a friendly story coach.

    You will be given:
    - The original bedtime story (for children ages 5–10)
    - An improvement summary written by a judge
    - User feedback describing how the story should be changed

    Your job is to carefully read all three and then write a single, clear "new requirement"
    that describes what the next version of the story should aim to be.

    1) Read and understand:
    - The main characters, setting, plot, tone, and moral of the original story.
      CRITICAL: Remember these details - you must reference them in Case B and C to maintain story continuity.
    - The judge's improvement summary (what could be better and why).
    - The user's feedback (what they actually want to change).

    2) Decide which of the following cases best matches the user feedback:

    CASE A: User wants a completely different story
        Indicators:
        - User says things like “change everything”, “new idea”, “write a different story”, mentions the same character or plots from the story
        or they provide new text/ideas that are not related to the original story.
        - User proposes new characters, a new plot, or a new setting.
        In this case, the new requirement should be based only on the user_improvement
        and improvement_summary.

    CASE B: User wants specific improvements to the existing story
        Indicators:
        - User mentions changes like “make it sweeter”, “longer”, “shorter”, “stronger arc”,
        “improve the ending”, “add character emotions”, “more kiddish”, etc.
        In this case, the new requirement should combine:
        - Remember the original story summary
        - The judge’s improvement summary
        - The user’s requested improvements
        into one coherent description of the improved version of the same story.

    CASE C: User gives no meaningful improvements
        Indicators:
        - User says “it’s fine”, “no changes”, “keep it”, or gives empty/very vague input.
        In this case, the new requirement should keep the core story the same, but incorporate
        the judge’s improvement summary in a light way (small refinements, not a full rewrite).

    3) Produce a FINAL JSON response with EXACTLY this structure:

    {{
    "new_requirement": "Write a story: [USER_FEEDBACK]. [Add story details]"
    }}
    
    CRITICAL RULES for the "new_requirement" field:
    - Replace [USER_FEEDBACK] with the user's EXACT words from USER FEEDBACK section
    - If Case A (completely different story): Format as "Write a story: [user's exact words]. [Then add story details/context]"
    - If Case B or C (improvements): Start with "Continue the original story about [character name and type from original story]. Do not re-introduce the characters or the story.
      The original story was: [brief 1-2 sentence summary of what happened]. Now: [user's exact feedback]. Also incorporate: [judge's improvement suggestions]."
      CRITICAL: Maintain the same character identity (e.g., if original was "Dan the dog", keep Dan as a dog, not change to a boy or different character)
    - The output must be valid JSON - no brackets, no placeholder text, no instruction text, no newlines in the string
    - Example for Case B: If original story is "Dan the dog who lost his ball" and user says "dan gets a new friend", 
      output: "Write a story: Continue the original story about Dan the dog. The original story was about Dan the dog who lost his ball and the children helped him find it. Now: dan gets a new friend. Add details about Dan the dog meeting a new friend and their adventures together."

    Rules for "new_requirement":
    - It should be written as if you are giving instructions to a storyteller
    who will write the next version.
    - It should be concrete and detailed (mention characters, tone, length,
    story arc, maturity level, etc.).
    - IMPORTANT: If the user's feedback contains inappropriate content (violence, harm, etc.),
      DO NOT sanitize or modify it. Pass it through EXACTLY as the user requested.
      The safety checker will handle inappropriate content later.
    - For appropriate content, it should be kid-safe and bedtime-friendly (for ages 5–10).

    You MUST respond with a single valid JSON object and nothing else.

    ORIGINAL STORY:
    {story}

    IMPROVEMENT SUMMARY FROM JUDGE:
    {improvement_summary}

    USER FEEDBACK:
    {user_improvement}
    """
    return call_model(rewrite_story_prompt, max_tokens=600, temperature=0.8)
