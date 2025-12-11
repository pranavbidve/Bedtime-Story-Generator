from generate import generate_story, generate_story_loop
from judge import judge_story
from rewrite import user_feedback, rewrite_story

import re
import json
"""
If I had 2 more hours, I would have integrated MCP tools to make generate, rewrite, and judge work seamlessly together, 
allowing them to call each other and share context more efficiently. Another idea would be implementing A/B testing 
to compare different story generation approaches and judge which versions users prefer. Finally, I would add history 
management so that the system remembers previous story versions and can reference what changed in earlier iterations, 
enabling more coherent story development across multiple feedback cycles.
"""


def main():

    print(" Kids Bedtime Story Generator (Ages 5–10) \n")
    
    # 1) Generate a raw story based on the user request
    story = generate_story_loop()
    
    if story is None:
        return

    # 2) Judge the initial story (LLM judge with chain-of-thought)
    if story.get('status') != 'unsafe':
        raw_reasoning = judge_story(story['story'])
        reasoning = json.loads(raw_reasoning)
        print("\n=== Story Evaluation ===\n")
        print(reasoning)
        print(story.get('reasoning'))

        total = float(reasoning['scores']['TOTAL'])
    
    if total>6.5:
        reasoning_block = reasoning.get("reasoning", {})
        improvement_summary = reasoning_block.get("IMPROVEMENT_SUMMARY")
    else: 
        story = generate_story_loop()
    
    # 3) Loop: Get user feedback, rewrite story, judge, repeat until user enters blank
    retry_after_unsafe = False
    while True:
        # Only show coach feedback if we're not retrying after unsafe
        if not retry_after_unsafe:
            coach_response = user_feedback(story['story'], improvement_summary)
            print("\n=== Story Coach Feedback ===\n")
            print(coach_response)

        
        user_improvement = input("> ").strip()
        
        # If user enters blank, exit the loop
        if user_improvement == '':
            print("\nThank you! Story generation complete.")
            break
        
        # Reset retry flag
        retry_after_unsafe = False
        
        # 4) Rewrite story based on user feedback
        new_requirement_json = rewrite_story(story['story'], improvement_summary, user_improvement)
        print("\n=== New Requirement ===\n")
        print(new_requirement_json)
        
        # Parse the JSON response to extract the actual requirement string
        new_requirement_data = json.loads(new_requirement_json)
        new_requirement = new_requirement_data['new_requirement']

        # Generate new story
        new_story_response = generate_story(new_requirement)
        new_story = json.loads(new_story_response)
        
        # Check if story generation was successful
        if new_story.get('status') == 'unsafe':
            print("\n=== New Story ===\n")
            print(new_story.get('message', 'Story generation failed. The requirement was not appropriate for children.'))
            if new_story.get('reasoning'):
                print(f"\nReasoning: {new_story.get('reasoning')}")
            print("\nPlease provide different, kid-friendly feedback.\n")
            retry_after_unsafe = True
            continue
        
        print("\n=== New Story ===\n")
        print(new_story.get('story', ''))
        
        # Update story variable for next iteration
        story = new_story
        
        # 5) Judge the new story
        raw_new_story_reasoning = judge_story(new_story['story'])
        new_story_reasoning = json.loads(raw_new_story_reasoning)
        
        reasoning_block = new_story_reasoning.get("reasoning", {})
        improvement_summary = reasoning_block.get("IMPROVEMENT_SUMMARY")
        
        print("\n=== Story Evaluation ===\n")
        print(new_story_reasoning)


if __name__ == "__main__":
    main()
