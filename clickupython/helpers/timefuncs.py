from word2number import w2n
from timefhuman import timefhuman
from datetime import datetime
from clickupython import exceptions
import pendulum as time

SCALES = {
    "min": 60,
    "mins": 60,
    "minute": 60,
    "minutes": 60,
    "hour": 3600,
    "hours": 3600,
    "day": 86400,
    "days": 86400,
    "week": 604800,
    "weeks": 604800,
    "month": 2419200,
    "months": 2419200,
    "year": 31536000,
    "years": 31536000,
}


def fuzzy_time_to_unix(text: str):
    """
    Converts a human readable time and date to a Unix timestamp

    Args: text - a human readable date in string form

    Returns: a Unix timestamp
    """
    try:
        now = time.now()
        timestamp = datetime.timestamp(timefhuman(text, now))
        return str(int(timestamp * 1000))
    except BaseException:
        print("\n")
        raise exceptions.ClickupClientError(
            "The date you entered was not convertable to a Unix timestamp. Check the format and spelling.",
            "Time conversion error",
        )


def fuzzy_time_to_seconds(text: any) -> int:
    """
    Converts a human readable duration of time into seconds

    Args: text - a human readable period of time

    Returns: seconds of the duration as an int
    """

    # Check if the input is a timestamp
    try:
        return str(int(text))

    # Not a timestamp, so let's interpret the fuzzy string
    except ValueError:
        text = text.lower()
        pairs = []
        for word in text.split():
            if word in SCALES:
                value = text[: text.find(word)]
                try:
                    pairs.append((int(value), SCALES[word]))
                except ValueError:
                    pairs.append((w2n.word_to_num(value), SCALES[word]))
                    text = text[text.find(word) :]

        return sum(pair[0] * pair[1] for pair in pairs)


if __name__ == "__main__":
    print(fuzzy_time_to_seconds("36 hours"))
    print(fuzzy_time_to_unix("december 1st"))
    print(fuzzy_time_to_seconds("3333029384"))
