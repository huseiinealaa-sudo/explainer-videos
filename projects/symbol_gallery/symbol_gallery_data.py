"""symbol_gallery: every value shown on screen (all illustrative, no real plant or device).

Loop numbers and tags are examples in the ISA-5.1 form (letters + loop number); they name
no real instrument.
"""
from explainer.icons import icon_names

# Silent segments (seconds): one per section of the catalogue.
DURATIONS = {
    "title": 6.0,
    "icons_1": 11.0,
    "icons_2": 11.0,
    "valves": 12.0,
    "machines": 10.0,
    "flow": 10.0,
    "bubbles": 12.0,
    "lines": 11.0,
    "loop": 24.0,
    "end": 6.0,
}

# Icons: every vendored Tabler icon, in two pages.
ICONS = icon_names()
ICON_PAGES = [ICONS[:len(ICONS) // 2 + len(ICONS) % 2], ICONS[len(ICONS) // 2 + len(ICONS) % 2:]]
ICON_COLS = 7

# Instrument bubbles: (location, function letters, loop number, display name).
BUBBLES = [
    ("field", "FT", "101", "Field mounted"),
    ("panel", "PIC", "102", "Panel (primary location)"),
    ("behind_panel", "PY", "103", "Behind panel"),
    ("dcs", "FIC", "101", "DCS / shared display"),
    ("plc", "LSH", "104", "PLC"),
]

# Line types in catalogue order: (kind, display name).
LINES = [
    ("process", "Process flow line"),
    ("connection", "Process connection / impulse line"),
    ("pneumatic", "Pneumatic signal"),
    ("electrical", "Electrical signal"),
    ("capillary", "Capillary tube"),
    ("data", "Data link / software link"),
]

# The example control loop: tank -> pump -> flow element + FT -> FIC (DCS) -> FY (I/P) -> FV.
LOOP = "101"
LOOP_TAGS = {"FT": ("FT", LOOP), "FIC": ("FIC", LOOP), "FY": ("FY", LOOP), "FV": ("FV", LOOP)}
