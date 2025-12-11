from generate import generate_story
from judge import judge_story
from rewrite import user_feedback, rewrite_story

import re
import json
"""
Before submitting the assignment, describe here in a few sentences what you would have built next if you spent 2 more hours on this project:

"""


example_request = "A story about a girl named Alice and her best friend Bob, who she kills eveually with a knife."

example_story = """
Once upon a time, in a cozy little house on the edge of a quiet town, there lived a sweet little cat named Whiskers. Whiskers did crimes and killed 1000s of mice. Whiskers was a playful kitty who loved to chase butterflies and nap in the warm sunshine. But most of all, Whiskers loved to sleep.

Every night, just as the sun started to set and the stars began to twinkle in the sky, Whiskers would curl up in a soft patch of moonlight and drift off to dreamland. Her fluffy tail would twitch, her whiskers would quiver, and she would purr softly as she fell into a deep sleep.

As Whiskers slept, she would dream of magical places filled with endless fields of catnip and trees that whispered secrets in the wind. She would chase imaginary mice through meadows of wildflowers and bask in the glow of the moon as it shone down upon her.

And when morning came, Whiskers would wake up refreshed and ready for a new day of adventures. She would stretch and yawn, then hop down from her favorite spot and wander outside to explore the world around her.

But no matter how exciting her days were, Whiskers always looked forward to the peaceful slumber that awaited her each night. For in her dreams, she could be anything she wanted to be and go anywhere her heart desired.

And so, Whiskers lived happily ever after, dreaming sweet dreams and sleeping soundly each and every night. The end. Goodnight, sweet dreams.
"""

reasoning_1 = """
REASONING:
- AGE_APPROPRIATE:
The story of Whiskers the cat is age-appropriate for children ages 5-10 as it includes themes of friendship, curiosity, and positive emotional growth. The story focuses on the importance of sleep and dreaming, which can resonate with children in this age group. The vocabulary used is simple and easy to understand for young readers.

- SAFETY:
The story is safe for children as it does not contain any violence, scary themes, or inappropriate content. It is a wholesome and heartwarming tale that promotes positive values and a sense of comfort for young readers.

- STORY_STRUCTURE:
The story has a clear beginning, middle, and end with a well-defined story arc. The pacing is appropriate, and the narrative flows smoothly from one scene to the next. The vocabulary used is suitable for a Grade 1-3 reading level, making it accessible for young readers.

- BEDTIME_SUITABLE:
The tone of the story is calm, soothing, and bedtime-appropriate. It creates a peaceful atmosphere that can help children relax before sleep. There are no loud or chaotic elements that would disrupt the bedtime feel.

- IMPROVEMENT_SUMMARY:
Overall, the story of Whiskers the cat is well-suited for children ages 5-10. It promotes positive values and a sense of comfort, with a clear story structure and bedtime-appropriate tone. No significant improvements are needed.

"""


reasoning_2 = """
REASONING:
- AGE_APPROPRIATE:
The story of Whiskers the cat is not entirely age-appropriate for children ages 5-10. While the themes of friendship, curiosity, and positive emotional growth are present, the mention of Whiskers doing crimes and killing mice may not be suitable for young children. This could be improved by focusing on more positive and relatable activities for the cat.

- SAFETY:
The story contains a mention of Whiskers doing crimes and killing mice, which may be considered violent and inappropriate for young children. This could be alarming or disturbing for some children and may not create a safe and comforting bedtime environment. To improve safety, it is important to avoid any violent or scary themes in children's bedtime stories.

- STORY_STRUCTURE:
The story has a clear beginning, middle, and end with a coherent story arc. However, the mention of Whiskers doing crimes and killing mice feels out of place and disrupts the flow of the otherwise peaceful narrative. To improve the story structure, it is important to ensure that all elements of the story contribute to a cohesive and engaging narrative.

- BEDTIME_SUITABLE:
While the story has a soothing tone overall, the mention of Whiskers doing crimes and killing mice may create a sense of unease or discomfort before bedtime. To make the story more suitable for bedtime, it is important to maintain a consistent calming tone throughout the narrative and avoid any elements that may be too exciting or unsettling for children.

- IMPROVEMENT_SUMMARY:
To improve the story for children ages 5-10, it is essential to focus on positive and relatable activities for the cat, avoid any violent or disturbing themes, ensure that all elements of the story contribute to a cohesive narrative, and maintain a consistent calming tone throughout the bedtime story.

- OVERALL:
AGE_APPROPRIATE: 4/10
SAFETY: 2/10
STORY_STRUCTURE: 6/10
BEDTIME_SUITABLE: 4/10
TOTAL: 4.3/10
4.3
"""

def generate_story_loop():
    while True:
        user_request = input("What kind of bedtime story would you like?\n> ").strip()
        if not user_request:
            print("No request given. Exiting.")
            return

        raw_response = generate_story(user_request)
        story = json.loads(raw_response)

        print(story)

        if story.get('status') == 'unsafe':
            print("\n" + story.get('message'))
            continue
        else:
            print("Story")
            print(story.get('story', ''))
            print("\n================\n")
            break

def main():

    # NEED to do somthing if the user wnats a story whihc is not approaprte.

    print("=== Kids Bedtime Story Generator (Ages 5–10) ===\n")

    # 1) Generate a raw story based on the user request
    while True:
        user_request = input("What kind of bedtime story would you like?\n> ").strip()
        # user_request = "rabit wiht a turtle firend"
        if not user_request:
            print("No request given. Exiting.")
            return

        raw_response = generate_story(user_request)
        story = json.loads(raw_response)

        print(story)

        if story.get('status') == 'unsafe':
            print("\n" + story.get('message'))
            continue
        else:
            print("Story")
            print(story.get('story', ''))
            print("\n================\n")
            break

    # 2) Judge the initial story (LLM judge with chain-of-thought)
    if story.get('status') != 'unsafe':
        raw_reasoning = judge_story(story['story'])
        reasoning = json.loads(raw_reasoning)
        total = float(reasoning['scores']['TOTAL'])

        reasoning_block = reasoning.get("reasoning", {})
        improvement_summary = reasoning_block.get("IMPROVEMENT_SUMMARY")

        if improvement_summary:
            print(improvement_summary)
            print(reasoning)


    # testing_story = "Once upon a time in a peaceful village, there lived a dog named Benny. Benny was known as the village coward because he was afraid of almost everything. He would jump at the sound of a falling leaf and run away from his own shadow. Despite his fears, Benny had a kind heart and always tried to help others. One day, when a storm hit the village, everyone was scared and looking for shelter. Benny, although trembling with fear, bravely guided his friends to a safe cave where they could wait out the storm. His friends were amazed at his courage and kindness. From that day on, Benny was no longer seen as a coward, but as a brave and caring friend. The villagers learned that courage is not the absence of fear, but the ability to do what is right even when you are afraid. And so, Benny the dog became a hero in the village, showing everyone that true bravery comes from the heart."

    # reasoning = {'reasoning': {'AGE_APPROPRIATE': 'The story of Benny the dog showcases themes of kindness, courage, and friendship, which are suitable for children ages 5-10. The emotional growth of Benny from being a coward to a hero can resonate with young readers. However, the concept of fear and bravery might need some simplification to ensure full understanding by the younger audience.', 'SAFETY': "The story is safe for children as it does not contain violence or scary themes. It promotes positive values like kindness and courage. To enhance safety, some descriptions of Benny's fears could be toned down to avoid triggering anxiety in sensitive children.", 'STORY_STRUCTURE': "The story follows a clear beginning, middle, and end structure with a well-defined story arc. The transformation of Benny from a coward to a hero is evident throughout the narrative. However, the pacing could be improved by elaborating on Benny's internal struggles and gradual growth to enhance engagement.", 'BEDTIME_SUITABLE': 'The narrative tone of the story is soothing and positive, making it suitable for bedtime reading. The message of courage and kindness can leave children with a sense of comfort before sleep. To further enhance bedtime suitability, the story could include more calming descriptions of nature or gentle actions to create a more relaxing atmosphere.', 'IMPROVEMENT_SUMMARY': "The story could be improved by simplifying the concepts of fear and bravery for better understanding by young readers. Additionally, enhancing the pacing by detailing Benny's internal struggles and incorporating more calming descriptions could further engage children in the bedtime narrative."}, 'scores': {'AGE_APPROPRIATE': 7, 'SAFETY': 8, 'STORY_STRUCTURE': 7, 'BEDTIME_SUITABLE': 8, 'TOTAL': 7.45}}
    # reasoning_block = reasoning.get("reasoning", {})
    # improvement_summary = reasoning_block.get("IMPROVEMENT_SUMMARY")

    coach_response = user_feedback(story['story'], improvement_summary)
    print("\n=== Story Coach Feedback ===\n")
    print(coach_response)
    user_improvement = input("")


    #4) Ask user if they want changes

    new_requirement_json = rewrite_story(story['story'], improvement_summary, user_improvement)
    print("\n=== New Requirement ===\n")
    print(new_requirement_json)
    
    # Parse the JSON response to extract the actual requirement string
    new_requirement_data = json.loads(new_requirement_json)
    new_requirement = new_requirement_data['new_requirement']

    new_story = generate_story(new_requirement)
    new_story = json.loads(new_story)
    print("\n=== New Story ===\n")
    print(new_story)

    raw_new_story_reasoning = judge_story(new_story['story'])
    new_story_reasoning = json.loads(raw_new_story_reasoning)
  
    print(new_story_reasoning)

    # coach_response = rewrite_story(story['story'], improvement_summary)
    # print("\n=== Story Coach Feedback ===\n")
    # print(coach_response)

    #5) Get user feedback

    #6) Rewrite using judge reasoning + user feedback

    #7) (Optional) re-judge the improved story


if __name__ == "__main__":
    main()
