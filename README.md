# Hippocratic AI Coding Assignment
Welcome to the [Hippocratic AI](https://www.hippocraticai.com) coding assignment


## Blockdiagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         STORY GENERATION SYSTEM                         │
└─────────────────────────────────────────────────────────────────────────┘

                    ┌──────────────┐
                    │     USER     │
                    │   (Input)    │
                    └──────┬───────┘
                           │
                           │ Story Request
                           ▼
        ┌──────────────────────────────────────┐
        │   generate_story_loop()              │
        │   - Gets user request               │
        │   - Handles unsafe responses         │
        │   - Returns story dict               │
        └──────────────┬───────────────────────┘
                       │
                       │ user_request
                       ▼
        ┌──────────────────────────────────────┐
        │   generate_story()                   │
        │   - Safety checker                   │
        │   - Story generator                  │
        │   Returns: {status, story/message}    │
        └──────────────┬───────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
    status="unsafe"            status="ok"
        │                             │
        ▼                             ▼
    [Reject & Ask          ┌──────────────────────┐
     Again]                │   judge_story()       │
                           │   - Evaluates story   │
                           │   - Chain-of-thought  │
                           │   - Scores (0-10)     │
                           │   Returns: reasoning  │
                           └──────────┬───────────┘
                                      │
                           ┌──────────┴──────────┐
                           │                     │
                    score > 6.5          score <= 6.5
                           │                     │
                           ▼                     ▼
                    [Continue]        [Regenerate Story]
                                      │
                                      └──► generate_story_loop()
                                      
                           ┌──────────────────────┐
                           │  improvement_summary │
                           └──────────┬───────────┘
                                      │
                                      ▼
                    ┌──────────────────────────────────────┐
                    │   user_feedback()                    │
                    │   - Story coach                      │
                    │   - Asks for improvements           │
                    │   Returns: coach_response            │
                    └──────────┬───────────────────────────┘
                               │
                               │ Display to User
                               ▼
                    ┌──────────────────────────────────────┐
                    │     USER FEEDBACK LOOP               │
                    │   (Continues until blank input)      │
                    └──────────┬───────────────────────────┘
                               │
                               │ user_improvement
                               ▼
                    ┌──────────────────────────────────────┐
                    │   rewrite_story()                    │
                    │   - Creates new requirement         │
                    │   - Includes user's exact words     │
                    │   Returns: new_requirement JSON      │
                    └──────────┬───────────────────────────┘
                               │
                               │ new_requirement
                               ▼
                    ┌──────────────────────────────────────┐
                    │   generate_story()                   │
                    │   - Safety check                     │
                    │   - Generate new story               │
                    └──────────┬───────────────────────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
            status="unsafe"        status="ok"
                    │                     │
                    ▼                     ▼
            [Show Message &      ┌──────────────────────┐
             Ask Again]          │   judge_story()       │
                                 │   - Evaluate new     │
                                 │   - Update scores    │
                                 └──────────┬───────────┘
                                            │
                                            ▼
                                 [Update improvement_summary]
                                            │
                                            └──► [Loop Back to user_feedback()]
                                            
                    ┌──────────────────────────────────────┐
                    │   USER ENTERS BLANK                  │
                    │   → Exit Loop                        │
                    └──────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ KEY COMPONENTS:                                                          │
│ • generate_story(): Safety checker + Story generator                     │
│ • judge_story(): LLM judge with chain-of-thought reasoning              │
│ • user_feedback(): Story coach that asks for improvements               │
│ • rewrite_story(): Creates new requirement from user feedback           │
│ • Main Loop: Iterative refinement until user satisfaction              │
└─────────────────────────────────────────────────────────────────────────┘
```

## Instructions
The attached code is a simple python script skeleton. Your goal is to take any simple bedtime story request and use prompting to tell a story appropriate for ages 5 to 10.
- Incorporate a LLM judge to improve the quality of the story
- Provide a block diagram of the system you create that illustrates the flow of the prompts and the interaction between judge, storyteller, user, and any other components you add
- Do not change the openAI model that is being used. 
- Please use your own openAI key, but do not include it in your final submission.
- Otherwise, you may change any code you like or add any files

---

## Rules
- This assignment is open-ended
- You may use any resources you like with the following restrictions
   - They must be resources that would be available to you if you worked here (so no other humans, no closed AIs, no unlicensed code, etc.)
   - Allowed resources include but not limited to Stack overflow, random blogs, chatGPT et al
   - You have to be able to explain how the code works, even if chatGPT wrote it
- DO NOT PUSH THE API KEY TO GITHUB. OpenAI will automatically delete it

---

## What does "tell a story" mean?
It should be appropriate for ages 5-10. Other than that it's up to you. Here are some ideas to help get the brain-juices flowing!
- Use story arcs to tell better stories
- Allow the user to provide feedback or request changes
- Categorize the request and use a tailored generation strategy for each category

---

## How will I be evaluated
Good question. We want to know the following:
- The efficacy of the system you design to create a good story
- Are you comfortable using and writing a python script
- What kinds of prompting strategies and agent design strategies do you use
- Are the stories your tool creates good?
- Can you understand and deconstruct a problem
- Can you operate in an open-ended environment
- Can you surprise us

---

## Other FAQs
- How long should I spend on this? 
No more than 2-3 hours
- Can I change what the input is? 
Sure
- How long should the story be?
You decide