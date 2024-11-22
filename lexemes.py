keywords = ["HAI", "KTHXBYE", "WAZZUP", 
            "BUHBYE", "BTW", "OBTW", 
            "TLDR", "I HAS A", "ITZ", 
            "R", "SUM OF", "DIFF OF", 
            "PRODUKT OF", "QUOSHUNT OF", 
            "MOD OF", "BIGGR OF", "SMALLR OF", 
            "BOTH OF", "EITHER OF", "WON OF", 
            "NOT", "ANY OF", "ALL OF", 
            "BOTH SAEM", "DIFFRINT", "SMOOSH", 
            "MAEK", "A", "IS NOW A", "VISIBLE", 
            "GIMMEH", "O RLY?", "YA RLY", 
            "MEBBE", "NO WAI", "OIC", "WTF?", 
            "OMG", "OMGWTF", "IM IN YR", 
            "UPPIN", "NERFIN", "YR", "TIL", 
            "WILE", "IM OUTTA YR", "HOW IZ I", 
            "GTFO", "IF U SAY SO", "FOUND YR", 
            "I IZ", "MKAY", "AN", "+"]

separatedkeywords = ["I", "HAS", "A", "SUM", 
                     "DIFF", "PRODUKT", "QUOSHUNT", 
                     "MOD", "BIGGR", "SMALLR", "BOTH", 
                     "ANY", "ALL", "EITHER", "WON", 
                     "OF", "SAEM", "NOW", "O", "RLY", 
                     "YA", "RLY?", "NO", "WAI", "IM", 
                     "IN", "OUTTA", "YR", "HOW", "IF", 
                     "U", "SAY", "SO", "FOUND", "IZ",
                     "IS", "NOW"]

NUMBR = "^-?\d+$"
NUMBAR = "^-?\d+\.\d+$"
YARN = "^\".*\"$"
TROOF = "^(WIN|FAIL)$"
TYPE = "^(NUMBR|NUMBAR|YARN|TROOF|NOOB)$"
IDENTIFIER = "^[a-zA-Z][_a-zA-Z\d]*$"

DATA_TYPES = ["NUMBR", "NUMBAR", "YARN", "TROOF", "NOOB"]

EXPR_KEYWORDS = ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", 
                    "MOD OF", "BIGGR OF", "SMALLR OF", 
                    "BOTH OF", "EITHER OF", "WON OF",
                    "BOTH SAEM", "DIFFRINT",
                    "ALL OF", "ANY OF"
                    "NOT"]

BIN_EXPR_KEYWORDS = ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", 
                    "MOD OF", "BIGGR OF", "SMALLR OF", 
                    "BOTH OF", "EITHER OF", "WON OF",
                    "BOTH SAEM", "DIFFRINT",
                    ]

INF_EXPR_KEYWORDS = ["ALL OF", "ANY OF"]

STMT_KEYWORDS = ["VISIBLE", "GIMMEH"]