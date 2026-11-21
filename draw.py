# Draw the 21 November 2026 world-news front page. Deterministic, no network.
# Renders a newspaper front page to entry.png (1024x1024) using DejaVu fonts.
from PIL import Image, ImageDraw, ImageFont

CANVAS = 1024
BG = (247, 243, 231)          # paper
INK = (18, 18, 18)            # body text
MAST = (20, 28, 58)           # masthead navy
GOLD = (238, 186, 92)         # masthead date gold
ACCENT = (168, 28, 28)        # kicker red
TEAL = (12, 92, 88)           # stat boxes
MUTED = (102, 97, 86)         # footer grey
DIVIDER = (168, 162, 148)     # hairlines

SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(drw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    wrapped, current = [], ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if drw.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                wrapped.append(current)
            current = word
    if current:
        wrapped.append(current)
    return wrapped


def para(drw, x, y, width, text, size, leading, bold=False, colour=INK):
    """Draw a wrapped paragraph; returns the y below it."""
    fnt = font(SANS_B if bold else SANS, size)
    for line in wrap(drw, text, fnt, width):
        drw.text((x, y), line, font=fnt, fill=colour)
        y += leading
    return y


def kicker(drw, x, y, text, size=17):
    drw.text((x, y), text, font=font(SANS_B, size), fill=ACCENT)
    return y + 24


def rule(drw, x, y, width, weight=2, colour=INK):
    drw.line([(x, y), (x + width, y)], fill=colour, width=weight)
    return y


def headline(drw, x, y, width, text, size, leading):
    return para(drw, x, y, width, text, size, leading, bold=True)


page = Image.new("RGB", (CANVAS, CANVAS), BG)
d = ImageDraw.Draw(page)
M = 44                       # side margin
W = CANVAS - 2 * M           # content width

# ---------- masthead ----------
d.rectangle([0, 0, CANVAS, 110], fill=MAST)
d.text((M, 14), "THE WORLD IN ONE DAY", font=font(SERIF_B, 46), fill=(250, 247, 238))
d.text((M, 74), "SATURDAY  •  21 NOVEMBER 2026", font=font(SANS_B, 22), fill=GOLD)
d.text((CANVAS - M - 208, 76), "ONE DAY  •  ONE IMAGE", font=font(SANS, 16),
       fill=(198, 203, 218))

# ---------- lead: Peru quake ----------
y = 128
y = kicker(d, M, y, "PERU  •  JUNIN  •  STRUCK JUST AFTER MIDNIGHT UTC")
y = headline(d, M, y, W, "6.8 QUAKE SHAKES PERU", size=46, leading=50)
y = para(d, M, y + 4, W,
         "A magnitude 6.8 earthquake struck Peru's Andean region of Junin at "
         "19:09 local time on Friday — 00:09 UTC on Saturday — shaking buildings "
         "as far away as Lima, 320 km away, where residents ran into the streets. "
         "No casualties or major damage had been reported by Saturday morning.",
         size=20, leading=26)
y += 14

# stat strip: four boxes
facts = [("6.8", "MAGNITUDE"), ("129 KM", "DEEP, JUNIN REGION"),
         ("00:09 UTC", "SATURDAY, 21 NOV"), ("0", "DEATHS REPORTED")]
box_w = (W - 3 * 14) // 4
bx = M
for big, small in facts:
    d.rectangle([bx, y, bx + box_w, y + 60], outline=TEAL, width=3)
    d.text((bx + 12, y + 7), big, font=font(SANS_B, 20), fill=TEAL)
    d.text((bx + 12, y + 34), small, font=font(SANS_B, 13), fill=INK)
    bx += box_w + 14
y += 60 + 14
rule(d, M, y, W)
y += 14

# ---------- two columns: Poland / Riyadh ----------
half = (W - 30) // 2
x_right = M + half + 30
top = y
yy = kicker(d, M, top, "POLAND  •  NATO'S EASTERN FLANK")
yy = headline(d, M, yy, half, "RUSSIAN MISSILES LAND IN POLAND", size=25, leading=30)
yy = para(d, M, yy + 4, half,
          "Two Russian missiles and a suspected drone came down in Poland on "
          "Friday during Moscow's biggest strike on Ukraine this month — 400 "
          "drones and 110 missiles, eight killed in Kyiv. PM Donald Tusk called "
          "it an intentional provocation; NATO's chief is due in Warsaw today.",
          size=17, leading=23)
yy2 = kicker(d, x_right, top, "SAUDI ARABIA  •  RIYADH")
yy2 = headline(d, x_right, yy2, half, "THREE MISSILES DOWNED OVER RIYADH", size=25, leading=30)
yy2 = para(d, x_right, yy2 + 4, half,
           "Saudi air defences intercepted three Houthi ballistic missiles "
           "aimed at Riyadh in the early hours of Saturday — the third night "
           "in a row of emergency alerts in the capital, two days after a "
           "missile damaged the city's tallest tower. No casualties reported.",
           size=17, leading=23)
y = max(yy, yy2) + 12
rule(d, M, y, W)
y += 14

# ---------- full-width band: Denmark ----------
y = kicker(d, M, y, "DENMARK  •  COPENHAGEN")
y = headline(d, M, y, W, "DENMARK EXPELS RUSSIAN ATTACHE OVER MURDER PLOT", size=26, leading=31)
y = para(d, M, y + 4, W,
         "Danish intelligence says Russian services plotted to kill Ukrainian-American rapper "
         "Kyivstoner at a Copenhagen concert in September, using a banned gang. Police stopped "
         "the gunmen five minutes before showtime; two men face attempted-murder charges.",
         size=19, leading=25)
y += 10
rule(d, M, y, W)
y += 14

# ---------- bottom row: three boxes ----------
third = (W - 2 * 16) // 3
cards = [
    ("BRITAIN  •  EUROPE", "UK-EU DEAL SEALED",
     "Britain and the EU struck their biggest post-Brexit deal: 100,000 youth "
     "visas each way, food checks scrapped."),
    ("MARKETS", "AI ROUT DEEPENS",
     "US stocks slid into correction as the AI sell-off wiped out the Nasdaq's "
     "2026 gains — $4tn lost in a week."),
    ("HEALTH", "CANCER PILL HOPE",
     "A trial pill, daraxonrasib, made pancreatic tumours undetectable in 5 of "
     "61 patients; tumours shrank or vanished in 60.7%."),
]
bx = M
for kick, title, body in cards:
    d.rectangle([bx, y, bx + third, y + 112], outline=DIVIDER, width=2)
    d.text((bx + 14, y + 10), kick, font=font(SANS_B, 14), fill=ACCENT)
    ny = headline(d, bx + 14, y + 32, third - 28, title, size=19, leading=23)
    para(d, bx + 14, ny + 4, third - 28, body, size=13, leading=17)
    bx += third + 16
y += 112 + 8

# ---------- footer ----------
rule(d, M, y, W)
y += 8
y = para(d, M, y, W,
         "ALSO TODAY:  New York mayor unveils plan to close Rikers Island by 2032  •  "
         "India's NSE passes Nasdaq as the world's 5th-largest exchange",
         size=14, leading=19, colour=MUTED)
y = para(d, M, y + 2, W,
         "Fiona, the Cincinnati Zoo hippo who won the internet's heart, dies aged nine  •  "
         "Sources: Reuters, AP, Al Jazeera, ISW, BBC, FT",
         size=14, leading=19, colour=MUTED)
assert y <= CANVAS - 4, f"layout overflow: footer ends at y={y}"

page.save("entry.png", optimize=True)
print("saved entry.png", page.size, "footer ends y =", y)
