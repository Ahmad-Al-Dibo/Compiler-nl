import re
import datetime as dt
from tools.system_variabels import (
    SYMBOL_MAP,
    VARIABLES_TOKENS,
    SYSTEM_VARIABLES,
    REPORTS,
    ADMIN_ERRORS,
    METHODS_TOKENS,
    NO_PRINT_SETTINGS_FILE_PATH
)

class Ruls:
    def __init__(self):
        self.variables = SYSTEM_VARIABLES
        self.kleur = TextColor

    def validate_rules(self, expression: str) -> bool:
        try:
            tokens = expression.split()

            if not tokens:
                raise ValueError("Lege expressies zijn niet toegestaan.")

            if tokens[0] in VARIABLES_TOKENS.values():
                #self.kleur.print_colored("VARIABLES_TOKENS:TRUE", TextColor.BLUE, TextColor.GREEN)

                if len(tokens) < 4 or tokens[2] != "=":
                    self.kleur.print_colored("VARIABLES_TOKENS-1:FALSE", TextColor.BLUE, TextColor.RED)
                    raise ValueError(f"Ongeldige declaratie: {' '.join(tokens)}")

                if not re.fullmatch(r"[a-zA-Z_]\w*", tokens[1]):
                    self.kleur.print_colored("VARIABLES_TOKENS-2:FALSE", TextColor.BLUE, TextColor.RED)
                    raise ValueError(f"Ongeldige identifier: '{tokens[1]}'")

                # Nieuwe regex: Laat complexe expressies toe (bijv. "1 + y" of "x * 2 - y")
                value = " ".join(tokens[3:])
                if not re.fullmatch(r"\(*\s*([a-zA-Z_]\w*|\d+(\.\d+)?)(\s*[+\-*/]\s*\(*\s*([a-zA-Z_]\w*|\d+(\.\d+)?))*\s*\)*", value):
                    self.kleur.print_colored("VARIABLES_TOKENS-3:FALSE", TextColor.BLUE, TextColor.RED)
                    raise ValueError(f"Ongeldige waarde: '{value}'")

                return True
            
            if tokens[0] in METHODS_TOKENS.values():
                if tokens[0] == "SETTINGS":
                    if tokens[1] == 'no_print':
                        if tokens[2] == '=':
                            with open(NO_PRINT_SETTINGS_FILE_PATH, "w") as no_print_settings:
                                no_print_settings.write(tokens[3])
                            return
                        else:
                            raise # Ik weet niet welke soort error
                return
                        

            #self.kleur.print_colored("validate:TRUE", TextColor.BLUE, TextColor.BACK_GREEN)
            return True

        except Exception as e:
            self.kleur.print_colored("validate:FALSE", TextColor.BLUE, TextColor.RED)
            ADMIN_ERRORS['E2001'] = {
                "message": "Validatiefout in validate_rules().",
                "details": str(e),
                "timestamp": str(dt.datetime.today()),
            }
            raise



    def berekenen(self, expression: str):
        try:
            self.validate_rules(expression)
            tokens = expression.split()
    
            # Variabele toewijzing (bijv. "var z = 1 + y")
            if tokens[0] == "VARIABLE":
                var_name = tokens[1]
                value_expression = " ".join(tokens[3:])
    
                # Vervang variabelen met hun waarden
                for var in sorted(self.variables.keys(), key=len, reverse=True):
                    value_expression = re.sub(rf"\b{var}\b", str(self.variables[var]), value_expression)
    
                # Evalueer de expressie en sla het resultaat op
                value = eval(value_expression, {}, {**self.variables})
                self.variables[var_name] = value
                return value
            
            if tokens[0] == "PRINTING":
                try:
                    value_expression = " ".join(tokens[1:])
                    for var in sorted(self.variables.keys(), key=len, reverse=True):
                        value_expression = re.sub(rf"\b{var}\b", str(self.variables[var]), value_expression)
                    print(eval(value_expression, {}, {**self.variables}))
                    return 
                except Exception as error:
                    raise error
                    

            if tokens[0] == "SETTINGS":
                return "Settings is changed and saved!"       
    
            # Vervang variabelen met hun waarden voor berekening
            for var in sorted(self.variables.keys(), key=len, reverse=True):
                expression = re.sub(rf"\b{var}\b", str(self.variables[var]), expression)
    
            # Converteer aangepaste symbolen naar Python-symbolen
            python_expression = expression.replace("isgelijk", "==")
            for symbol, python_operator in SYMBOL_MAP.items():
                python_expression = python_expression.replace(symbol, python_operator)
    
            return eval(python_expression)
    
        except Exception as e:
            ADMIN_ERRORS['E6002'] = {
                "message": "Fout bij berekening in berekenen().",
                "details": str(e),
                "timestamp": str(dt.datetime.today()),
            }
            raise ValueError(f"[E6002] Fout bij evaluatie: {e}")



class CreateSymbol:
    def __init__(self, input_d: dict):
        self.input_data = input_d

    def generate_symbol(self):
        try:
            output = []
            for _, elements in self.input_data.items():
                words = [SYMBOL_MAP.get(value, value) for value in elements.values()]
                output.append(" ".join(words))
            return output
        except Exception as e:
            ADMIN_ERRORS['E3001'] = {
                "message": "Fout bij het genereren van symbolen in generate_symbol().",
                "details": str(e),
                "timestamp": str(dt.datetime.today()),
            }
            raise

class TextColor:
    # Kleurcodes
    RESET = "\033[0m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Achtergrondkleuren
    BACK_BLACK = "\033[40m"
    BACK_RED = "\033[41m"
    BACK_GREEN = "\033[42m"
    BACK_YELLOW = "\033[43m"
    BACK_BLUE = "\033[44m"
    BACK_MAGENTA = "\033[45m"
    BACK_CYAN = "\033[46m"
    BACK_WHITE = "\033[47m"
    
    @staticmethod
    def print_colored(text, text_color=RESET, background_color=RESET):
        """Print een tekst in de opgegeven kleur en achtergrondkleur."""
        try:
            print(f"{text_color}{background_color}{text}{TextColor.RESET}")
        except Exception as e:
            ADMIN_ERRORS['E4001'] = {
                "message": "Fout bij print_colored().",
                "details": str(e),
                "timestamp": str(dt.datetime.today()),
            }
            raise

    @staticmethod
    def report_colored(reportitem: str, result: bool = False):
        try:
            REPORTS.append(reportitem)
        except Exception as e:
            ADMIN_ERRORS['E1001'] = {
                "message": "Fout bij toevoegen van rapport in report_colored().",
                "details": str(e),
                "timestamp": str(dt.datetime.today()),
            }
            raise

if __name__ == "__main__":
    kleur = TextColor()
    kleur.print_colored("Dit is rode tekst op een gele achtergrond.", TextColor.RED, TextColor.BACK_YELLOW)
    kleur.print_colored("Dit is groene tekst.", TextColor.GREEN)
    kleur.print_colored("Dit is blauwe tekst op een witte achtergrond.", TextColor.BLUE, TextColor.BACK_WHITE)
