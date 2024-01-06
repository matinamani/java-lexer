import re

import pandas as pd

from tokens import KEYWORDS, PATTERNS


class Java_Lexer:
    def __init__(self, src_path: str):
        self.__src_path = src_path
        self.__read_src()
        self.__tokenization_pattern = re.compile(
            "|".join(f"(?P<{key}>{value})" for key, value in PATTERNS.items())
        )
        self.__pointer = {"ln": 0, "col": 0, "block": 0}
        self.__result = {
            "ln": [],
            "col": [],
            "block": [],
            "token": [],
            "type": [],
        }

    def __read_src(self):
        with open(self.__src_path) as src_file:
            self.raw_src = src_file.readlines()
        self.src_lines = list(map(str.strip, self.raw_src))

    def __tokenize_src(self):
        for line in self.src_lines:
            self.__pointer["ln"] += 1
            for match in self.__tokenization_pattern.finditer(line):
                for key, value in match.groupdict().items():
                    if value is not None:
                        self.__update_col(self.__pointer["ln"] - 1, value)
                        self.__update_block(value)
                        self.__append_row(key, value)

    def __update_col(self, line, token):
        self.__pointer["col"] = self.raw_src[line].find(token) + 1

    def __update_block(self, token):
        if token == "{":
            self.__pointer["block"] += 1
        elif token == "}":
            self.__pointer["block"] -= 1
        else:
            pass

    def __append_row(self, type, token):
        self.__result["ln"].append(self.__pointer["ln"])
        self.__result["col"].append(self.__pointer["col"])
        self.__result["block"].append(self.__pointer["block"])
        self.__result["type"].append(
            "keyword" if type == "identifier" and token in KEYWORDS else type
        )
        self.__result["token"].append(token)

    def __save_df(self):
        self.df = pd.DataFrame(self.__result)
        self.df.to_csv("results.csv", index=False)

    def run(self):
        self.__tokenize_src()
        self.__save_df()

    def show_src(self):
        for line in self.raw_src:
            print(line, end="")
