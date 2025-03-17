import re
import unicodedata

#from ztext_cleaner import norm_config
from norm_cf import*  # noqa: F403

def text_normalize(text, iso_code, lower_case=True, remove_numbers=True, remove_brackets=False):

    """Given a text, normalize it by changing to lower case, removing punctuations, removing words that only contain digits and removing extra spaces

    Args:
        text : The string to be normalized
        iso_code :
        remove_numbers : Boolean flag to specify if words containing only digits should be removed

    Returns:
        normalized_text : the string after all normalization  

    """

    config = norm_conf.get(iso_code, norm_conf["*"])  # noqa: F405

    for field in ["lower_case", "punc_set","del_set", "mapping", "digit_set", "unicode_norm"]:
        if field not in config:
            config[field] = norm_conf["*"][field]  # noqa: F405


    text = unicodedata.normalize(config["unicode_norm"], text)

    # Convert to lower case

    if config["lower_case"] and lower_case:
        text = text.lower()

    # brackets
    
    # always text inside brackets with numbers in them. Usually corresponds to "(Sam 23:17)"
    text = re.sub(r"\([^\)]*\d[^\)]*\)", " ", text)
    if remove_brackets:
        text = re.sub(r"\([^\)]*\)", " ", text)

    # Apply mappings

    for old, new in config["mapping"].items():
        text = re.sub(old, new, text)

    # Replace punctutations with space

    punct_pattern = r"[" + config["punc_set"]

    punct_pattern += "]"

    normalized_text = re.sub(punct_pattern, " ", text)

    # remove characters in delete list

    delete_patten = r"[" + config["del_set"] + "]"

    normalized_text = re.sub(delete_patten, "", normalized_text)

    # Remove words containing only digits
    # We check for 3 cases  a)text starts with a number b) a number is present somewhere in the middle of the text c) the text ends with a number
    # For each case we use lookaround regex pattern to see if the digit pattern in preceded and followed by whitespaces, only then we replace the numbers with space
    # The lookaround enables overlapping pattern matches to be replaced

    if remove_numbers:

        digits_pattern = "[" + config["digit_set"]

        digits_pattern += "]+"
# add a list of general devise handling as Euro, Fcfa,etc
        complete_digit_pattern = (
            r"^"
            + digits_pattern
            + "(?=\s)|(?<=\s)"
            + digits_pattern
            + "(?=\s)|(?<=\s)"
            + digits_pattern
            + "$"
        )

        normalized_text = re.sub(complete_digit_pattern, "*", normalized_text)

    if config["rm_diacritics"]:
        from unidecode import unidecode
        normalized_text = unidecode(normalized_text)

    # Remove extra spaces
    normalized_text = re.sub(r"\s+", " ", normalized_text).strip()

    return normalized_text