import re
from enum import Enum


class RegexType(Enum):
    """This Enum class is specifically used to determine the type of regex a pattern contains."""
    UNKNOWN = 0  # The default RegexType
    START = 1  # The regex indicates the target string starts with the given substring.
    END = 2  # The regex indicates the target string ends with the given substring.
    CONTAIN = 3  # The regex indicates the target string contains the given substring.


def analyze_regex(pattern: str) -> RegexType:
    """This function determines if the given string pattern contains any regex pattern, such as startswith, endswith,
    or contains. If yes, the corresponding type of regex will be returned."""
    # Check if the pattern is a valid regex
    try:
        re.compile(pattern)
    except re.error:
        return RegexType.UNKNOWN

    # A pattern with both starts and endswith is not supported
    if pattern.startswith('^') and pattern.endswith('$'):
        return RegexType.UNKNOWN

    # Check for starting pattern
    elif pattern.startswith('^'):
        # Remove '^' and check if the next character is not a special character
        if len(pattern) > 1 and not re.match(r'[\^$.|?*+(){}]', pattern[1]):
            return RegexType.START

    # Check for ending pattern, we use elif here because we do not support starting and ending pattern simultaneously
    elif pattern.endswith('$'):
        # Remove '$' and check if the preceding character is not a special character
        if len(pattern) > 1 and not re.match(r'[\^$.|?*+(){}]', pattern[-2]):
            return RegexType.END

    # Check for special regex characters. If found, it is some unsupported regex.
    elif re.search(r'[\^$.|?*+(){}\[\]\\]', pattern):
        return RegexType.UNKNOWN

    # All the other values, including plain texts, are considered as contain regex.
    return RegexType.CONTAIN
