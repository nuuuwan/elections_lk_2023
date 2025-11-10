from elections_lk.base.ValueDict import ValueDict

NOT_COUNTED = "no vote"

COLOR_TO_PARTY_LIST = {
    "#cccccc": [NOT_COUNTED],
    "#444444": [ValueDict.OTHERS],
    "#222288": ["SLFP", "PA", "UPFA"],
    "#004400": ["ACMC", "MNA", "NC", "SLMC", "NUA"],
    "#008800": ["UNP", "NDF", "SJB"],
    "#009900": [],
    "#880000": ["SLPP", "OPPP"],
    "#880088": ["SLMP"],
    "#e0e0e0": ["IG", "IG2", "IG3"],
    "#8800ff": ["DUNF"],
    "#0088ff": ["SB"],
    "#ff0000": [
        "JVP",
        "NMPP",
        "NPP",
        "MEP",
        "USA",
        "SLPF",
        "DNA",
        "JJB",
        "LSSP",
        "CP",
        "NSSP",
    ],
    "#ff2200": [
        "ELMSP",
        "EPDP",
        "TMVP",
        "EROS",
    ],
    "#ff4400": ["CWC", "UPF"],
    "#ffcc00": ["SU", "JHU"],
    "#ffff00": ["AITC", "ITAK", "TULF", "ACTC", "IND9"],
    "#ffffff": ["ELJP", "INDI"],
    "#ff8822": ["IND16"],
    # Validation only
    "#0088f1": ["A"],
    "#ff4401": ["B"],
}

PARTY_TO_COLOR = {}
for color, party_list in COLOR_TO_PARTY_LIST.items():
    for party in party_list:
        PARTY_TO_COLOR[party] = color
