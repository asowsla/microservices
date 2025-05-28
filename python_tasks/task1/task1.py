import string

def is_palindrome_check(text: str) -> bool:
    prepared_text = str.maketrans("", "", string.punctuation + " ")
    cleaned_text = str(text).translate(prepared_text).lower()
    return cleaned_text == cleaned_text[::-1]

def test_run() -> None:
    test_cases = [
        ("Yo! Banana Boy?", True),
        ("Radars.", False),
        (9889, True),
        (12343210, False),
        ("$!a11a!$", True)
        ]

    for text, expected in test_cases:
        result = is_palindrome_check(text)
        print(f"'{text}' --- expected: {expected}, result: {result}")

if __name__ == "__main__":  
    test_run()