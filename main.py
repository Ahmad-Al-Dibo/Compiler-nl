import sys
import datetime as dt
from model import CreateSymbol, Ruls
from tokens import write_token
from tools.system_variabels import ADMIN_ERRORS, NO_PRINT_SETTINGS_FILE_PATH, REPORTS

def process_code(output_symbol_code, ruls: Ruls = Ruls()):
    """
    Verwerkt code regel voor regel, evalueert deze en logt fouten.
    """
    for line in output_symbol_code:
        try:
            value_output = ruls.berekenen(line)
            with open(NO_PRINT_SETTINGS_FILE_PATH, 'r') as read_no_print_settings_file:
                value_no_print_setting = read_no_print_settings_file.read()
            if value_no_print_setting == "true":
                print(value_output)
        except ValueError as e:
            error_code = "E2001"
            ADMIN_ERRORS[error_code] = {
                "message": f"Fout tijdens evaluatie van regel.",
                "details": f"Regel: '{line}' | Foutmelding: {str(e)}",
                "timestamp": str(dt.datetime.today()),
            }
            print(f"[{error_code}] {e} in regel: {line}")

import os
import datetime as dt
from model import CreateSymbol
from tokens import write_token
from tools.system_variabels import ADMIN_ERRORS

def handle_file_input(filepath):
    """
    Verwerkt code uit een bestand, genereert symbolen en voert de code uit.

    Args:
        filepath (str): Pad naar het bestand dat moet worden verwerkt.

    Raises:
        FileNotFoundError: Als het bestand niet gevonden wordt.
        MemoryError: Als de invoer te groot is.
        PermissionError: Als er geen leesrechten zijn.
        OSError: Bij andere bestandsgerelateerde fouten.
        Exception: Voor andere onverwachte fouten.
    """
    symbole = CreateSymbol({})
    
    # ✅ **Controleer of het bestand bestaat en leesbaar is voordat we het openen**
    if not os.path.exists(filepath):
        error_code = "E1001"
        ADMIN_ERRORS[error_code] = {
            "message": "Bestand niet gevonden in handle_file_input().",
            "details": f"Bestandspad: {filepath}",
            "timestamp": str(dt.datetime.today()),
        }
        print(f"[{error_code}] Bestand niet gevonden: {filepath}")
        return  # Stop de functie direct

    if not os.path.isfile(filepath):
        error_code = "E1007"
        ADMIN_ERRORS[error_code] = {
            "message": "Opgegeven pad is geen geldig bestand.",
            "details": f"Pad: {filepath}",
            "timestamp": str(dt.datetime.today()),
        }
        print(f"[{error_code}] Ongeldig bestandspad: {filepath}")
        return

    if not os.access(filepath, os.R_OK):
        error_code = "E1008"
        ADMIN_ERRORS[error_code] = {
            "message": "Geen leesrechten voor het bestand.",
            "details": f"Bestandspad: {filepath}",
            "timestamp": str(dt.datetime.today()),
        }
        print(f"[{error_code}] Geen leesrechten voor het bestand: {filepath}")
        return

    try:
        # ✅ **Verwerk de code uit het bestand**
        code_data = write_token(filepath=filepath)
        
        # Controleer of `write_token` geldige data retourneerde
        if not code_data or len(code_data) < 3:
            error_code = "E1009"
            ADMIN_ERRORS[error_code] = {
                "message": "Ongeldige gegevens ontvangen van write_token().",
                "details": f"Gegevens: {code_data}",
                "timestamp": str(dt.datetime.today()),
            }
            print(f"[{error_code}] Fout: write_token() gaf ongeldige data terug.")
            return

        symbole.input_data = code_data[2]
        output = symbole.generate_symbol()

        # ✅ **Voer de code veilig uit**
        process_code(output)

    except MemoryError:
        error_code = "E1005"
        ADMIN_ERRORS[error_code] = {
            "message": "Het bestand is te groot om te verwerken.",
            "details": f"Bestandspad: {filepath}",
            "timestamp": str(dt.datetime.today()),
        }
        print(f"[{error_code}] Het bestand is te groot en kan niet worden verwerkt.")

    except PermissionError:
        error_code = "E1002"
        ADMIN_ERRORS[error_code] = {
            "message": "Geen toegang tot het bestand.",
            "details": f"Bestandspad: {filepath}",
            "timestamp": str(dt.datetime.today()),
        }
        print(f"[{error_code}] Geen toegang tot het bestand: {filepath}")

    except OSError as e:
        error_code = "E1003"
        ADMIN_ERRORS[error_code] = {
            "message": "OS-fout bij openen van bestand.",
            "details": f"[Errno {e.errno}] {e.strerror}: '{filepath}'",
            "timestamp": str(dt.datetime.today()),
        }
        print(f"[{error_code}] OS-fout bij openen van bestand: {e}")

    except ValueError as e:
        error_code = "E1006"
        ADMIN_ERRORS[error_code] = {
            "message": "Ongeldige invoer in handle_file_input().",
            "details": str(e),
            "timestamp": str(dt.datetime.today()),
        }
        print(f"[{error_code}] Ongeldige invoer: {e}")

    except Exception as e:
        error_code = "E1010"
        ADMIN_ERRORS[error_code] = {
            "message": "Onverwachte fout bij verwerken van bestand.",
            "details": str(e),
            "timestamp": str(dt.datetime.today()),
        }
        print(f"[{error_code}] Onverwachte fout bij verwerken van bestand: {e}")


def handle_interactive_input():
    """
    Interactieve modus waarin de gebruiker code invoert.
    """
    print("Compiler Ahmad Al Dibo - Interactieve modus!\n")
    symbole = CreateSymbol({})
    while True:
        try:
            linecode = input("CodeI>>> ")
            if linecode == "ADMIN":
                for i in ADMIN_ERRORS.values():
                    print(i)
                print("\n\n\n")
                for i in REPORTS:
                    print(i)
            if not linecode.strip():
                continue
            code_data = write_token(code=linecode)
            symbole.input_data = code_data[2]
            output = symbole.generate_symbol()
            process_code(output)
        except KeyboardInterrupt:
            print("\nAfsluiten...")
            break
        except Exception as e:
            print(f"[E1003] Onverwachte fout: {e}")

def main():
    """
    Bepaalt of de code wordt uitgevoerd met een bestand of in interactieve modus.
    """
    sys_args = sys.argv
    if len(sys_args) > 1:
        filepath = sys_args[1]
        if filepath.endswith(".txt"):
            handle_file_input(filepath)
        else:
            print("[E1004] Ongeldig bestandstype. Gebruik een .txt bestand.")
    else:
        handle_interactive_input()

if __name__ == "__main__":
    main()
