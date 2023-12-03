import re
from enum import Enum


class RegexType(Enum):
    UNKNOWN = 0
    START = 1  # The regex
    END = 2
    CONTAIN = 3


def analyze_regex(pattern) -> RegexType:
    # Check if the pattern is a valid regex
    try:
        re.compile(pattern)
    except re.error:
        return RegexType.UNKNOWN

    # Check for starting pattern
    if pattern.startswith('^'):
        # Remove '^' and check if the next character is not a special character
        if len(pattern) > 1 and not re.match(r'[\^$.|?*+(){}]', pattern[1]):
            return RegexType.START

    # Check for ending pattern, we use elif here because we do not support starting and ending pattern simultaneously
    elif pattern.endswith('$'):
        # Remove '$' and check if the preceding character is not a special character
        if len(pattern) > 1 and not re.match(r'[\^$.|?*+(){}]', pattern[-2]):
            return RegexType.END

    elif re.search(r'[\^$.|?*+(){}\[\]\\]', pattern):
        return RegexType.UNKNOWN

    return RegexType.CONTAIN
