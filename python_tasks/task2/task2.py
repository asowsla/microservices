from typing import Callable

def strings_filter(filter: Callable[[str], bool], data: list[str]) -> list[str]:
    return [s for s in data if filter(s)]

def main() -> None:
    strings = ["algorithm", "neural network", "123abc", "meme", "!work"]
    
    print(strings_filter(lambda s: " " not in s, strings))
    print(strings_filter(lambda s: not s.startswith("a"), strings))
    print(strings_filter(lambda s: len(s) >= 5, strings))    

if __name__ == "__main__":
    main()