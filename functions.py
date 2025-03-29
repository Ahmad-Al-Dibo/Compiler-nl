import re
import datetime as dt
from tools.system_variabels import ADMIN_ERRORS


def load_code(file_path: str):
    """
    Laadt de code uit een bestand en retourneert de inhoud als een string.
    """
    try:
        with open(file_path, 'r', encoding='utf8') as codef:
            return codef.read()
    except FileNotFoundError:
        ADMIN_ERRORS['E1001'] = {
            "message": "Bestand niet gevonden in load_code().",
            "details": f"[Errno 2] No such file or directory: '{file_path}'",
            "timestamp": str(dt.datetime.today()),
        }
        raise
    except PermissionError:
        ADMIN_ERRORS['E1002'] = {
            "message": "Toegangsrechten ontbreken in load_code().",
            "details": f"[Errno 13] Permission denied: '{file_path}'",
            "timestamp": str(dt.datetime.today()),
        }
        raise
    except OSError as e:
        ADMIN_ERRORS['E1003'] = {
            "message": "OS-fout bij openen van bestand in load_code().",
            "details": f"[Errno {e.errno}] {e.strerror}: '{file_path}'",
            "timestamp": str(dt.datetime.today()),
        }
        raise

def clean_code(loaded_data: str):
    """
    Splitst de ingelezen code in een lijst van regels en verwijdert lege regels.
    """
    return [line for line in loaded_data.split('\n') if line.strip()]


def linedata_line_by_line(lines: list):
    """
    Berekent de totale tekenlengte van elke regel.
    """
    line_lengths = {}
    for line_index, line in enumerate(lines, start=1):
        line_lengths[line_index] = len(line)
    return line_lengths

def elementsdata_line_by_line(lines: list):
    """
    Meet de lengte van elk element (woord, token) in elke regel.
    """
    element_lengths = {}
    for line_index, line in enumerate(lines, start=1):
        elements = line.split()
        element_lengths[str(line_index)] = {idx: str(len(element)) for idx, element in enumerate(elements)}
    return element_lengths

def elements_line_by_line(lines: list):
    """
    Extracts tokens per regel op basis van een regex die woorden, getallen, strings en operators herkent.
    Enkele aanhalingstekens worden correct als losse tokens gesplitst.
    """
    token_data = {}
    # Regex voor woorden, floats, integers, variabelen, operators en aanhalingstekens als aparte tokens
    pattern = r"\"[^\"]*\"|'[^']*'|\d+\.\d+|\d+|[a-zA-Z_]\w*|[+\-*/=<>!]+|[()]+|['\"]"


    for line_index, line in enumerate(lines, start=1):
        tokens = re.findall(pattern, line.strip())
        token_data[str(line_index)] = {idx: token for idx, token in enumerate(tokens)}

    return token_data

