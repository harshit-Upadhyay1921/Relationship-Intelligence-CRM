def interaction_summary_prompt(interactions):
    return f"""
You are an AI CRM assistant.

Summarize these customer interactions.

Focus on:

- Important relationship context
- Interests
- Goals
- Important discussions
- Pending follow-ups

Interactions:

{interactions}

Keep the summary under 200 words.
"""

def follow_up_suggestion_prompt(summary, latest_interaction):
    return f"""
You are an AI CRM assistant.

Based on the relationship summary and latest interaction, generate one professional follow-up suggestion.

Relationship Summary:
{summary}

Latest Interaction:
{latest_interaction}

Return ONLY:

Suggested Follow-up:
(2-3 sentences)

Reason:
(1 sentence)
"""