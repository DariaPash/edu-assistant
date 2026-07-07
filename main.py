from edu_assistant.assistant import create_response

INPUT_PROMPT = "Кто ты?"

response = create_response(
    llm_key="api",
    role="math_tutor",
    template="tutor_quick_answer",
    prompt=INPUT_PROMPT,
)
