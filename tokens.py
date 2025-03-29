from functions import (
    load_code, 
    clean_code, 
    elementsdata_line_by_line, 
    linedata_line_by_line, 
    elements_line_by_line,
)
import datetime as dt
from tools.system_variabels import (
    MAX_LINES,
    ADMIN_ERRORS
)

def write_token(filepath: str = None, code: str = None):
    """
    Verwerkt code-invoer (uit bestand of string) en retourneert:
    - Lijnlengtes
    - Lengtes van elementen per regel
    - Tokens per regel
    
    Args:
        filepath (str, optional): Pad naar een bestand.
        code (str, optional): Directe code-invoer.

    Returns:
        tuple: (length_per_line, length_elements_per_line, elements_per_line)

    Raises:
        ValueError: Als geen geldige invoer is opgegeven.
        MemoryError: Als de invoer te groot is.
        FileNotFoundError: Als het bestand niet gevonden wordt.
    """
    try:
        if filepath:
            code = load_code(filepath)
        elif not code:
            raise ValueError("[E3001] Geef 'filepath' of 'code' op.")

        pc_code = clean_code(code)

        if len(pc_code) > MAX_LINES:
            error_code = "E3002"
            ADMIN_ERRORS[error_code] = {
                "message": "Het bestand bevat meer regels dan toegestaan.",
                "details": f"Aantal regels: {len(pc_code)}, Maximum: {MAX_LINES}",
                "timestamp": str(dt.datetime.today()),
            }
            raise MemoryError(f"[{error_code}] Het bestand is groter dan toegestaan!")

        return (
            linedata_line_by_line(pc_code),
            elementsdata_line_by_line(pc_code),
            elements_line_by_line(pc_code),
        )

    except Exception as e:
        error_code = "E3003"
        ADMIN_ERRORS[error_code] = {
            "message": "Onverwachte fout in write_token().",
            "details": str(e),
            "timestamp": str(dt.datetime.today()),
        }
        raise

from tools.system_variabels import TOKENS


#print(write_token(code="var x = 'string'")[2])