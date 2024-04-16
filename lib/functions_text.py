def get_first_word(text: str) -> str:

    if not ' ' in text:
        return text.capitalize()

    for i, letter in enumerate(text):
        if letter == ' ':
            return text[:i].capitalize()
        
def transform_to_bool(text:str) -> bool:
    if text == 'TRUE': return True
    elif text == 'FALSE': return False
