

























#
TOOL_NAME = "IPPuller"
TOOL_VER  = "v2.0"
ASCII_ART = r"""
      ███                         ███
     ░░░                         ░███
     █████ █████ ████  ███████   ░███
    ░░███ ░░███ ░███  ███░░███   ░███
     ░███  ░███ ░███ ░███ ░███   ░███
     ░███  ░███ ░███ ░███ ░███   ░░░ 
     ░███  ░░████████░░███████    ███
     ░███   ░░░░░░░░  ░░░░░███   ░░░ 
 ███ ░███             ███ ░███       
░░██████             ░░██████        
 ░░░░░░               ░░░░░░         
"""
# ─────────────────────────────────────────────────────────────────

import os, sys, json, time, socket, random, platform, datetime
import threading, subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import requests
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    print("Run: pip install requests colorama")
    sys.exit(1)

SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lemonnet_saved.json")


THEMES = {
    "lemon":  ("\033[38;5;226m","\033[38;5;220m","\033[38;5;229m","\033[38;5;214m","\033[38;5;240m"),
    "fire":   ("\033[38;5;202m","\033[38;5;196m","\033[38;5;220m","\033[38;5;88m", "\033[38;5;238m"),
    "ice":    ("\033[38;5;51m", "\033[38;5;45m", "\033[38;5;195m","\033[38;5;27m", "\033[38;5;238m"),
    "toxic":  ("\033[38;5;46m", "\033[38;5;40m", "\033[38;5;118m","\033[38;5;22m", "\033[38;5;238m"),
    "purple": ("\033[38;5;135m","\033[38;5;129m","\033[38;5;183m","\033[38;5;57m", "\033[38;5;238m"),
    "blood":  ("\033[38;5;160m","\033[38;5;124m","\033[38;5;203m","\033[38;5;52m", "\033[38;5;238m"),
    "gold":   ("\033[38;5;220m","\033[38;5;178m","\033[38;5;228m","\033[38;5;136m","\033[38;5;238m"),
    "neon":   ("\033[38;5;201m","\033[38;5;198m","\033[38;5;207m","\033[38;5;165m","\033[38;5;238m"),
    "matrix": ("\033[38;5;34m", "\033[38;5;28m", "\033[38;5;82m", "\033[38;5;22m", "\033[38;5;238m"),
    "ocean":  ("\033[38;5;33m", "\033[38;5;26m", "\033[38;5;81m", "\033[38;5;19m", "\033[38;5;238m"),
    "rust":   ("\033[38;5;130m","\033[38;5;94m", "\033[38;5;172m","\033[38;5;52m", "\033[38;5;238m"),
    "arctic": ("\033[38;5;159m","\033[38;5;153m","\033[38;5;195m","\033[38;5;111m","\033[38;5;238m"),
    "sakura": ("\033[38;5;211m","\033[38;5;204m","\033[38;5;218m","\033[38;5;125m","\033[38;5;238m"),
    "void":   ("\033[38;5;57m", "\033[38;5;54m", "\033[38;5;99m", "\033[38;5;17m", "\033[38;5;238m"),
    "copper": ("\033[38;5;173m","\033[38;5;137m","\033[38;5;216m","\033[38;5;94m", "\033[38;5;238m"),
}
TNAMES = list(THEMES.keys())
_tidx  = 0

def T(): return THEMES[TNAMES[_tidx]]
def AC(): return T()[0]
def DM(): return T()[1]
def BR(): return T()[2]
def HI(): return T()[3]
def SP(): return T()[4]
def next_theme():
    global _tidx
    _tidx = (_tidx + 1) % len(TNAMES)

WH  = Fore.WHITE
GY  = "\033[38;5;240m"
LGY = "\033[38;5;245m"
LG  = "\033[38;5;46m"
RST = Style.RESET_ALL
DIM = Style.DIM
SPIN = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]

def clr():  os.system("cls" if platform.system()=="Windows" else "clear")
def pause(): input(f"\n{GY}  [{LGY}ENTER{GY}] to continue...{RST}")
def rnd(a,b): return random.randint(a,b)
def call_ip(): return f"{rnd(24,220)}.{rnd(1,254)}.{rnd(1,254)}.{rnd(1,254)}"

JUG_LOCS = [
    "New York, US • AS7922 Comcast","Los Angeles, US • AS15169 Google LLC",
    "Chicago, US • AS7018 AT&T","Toronto, CA • AS577 Bell Canada",
    "London, UK • AS2856 BT Group","Frankfurt, DE • AS3320 Deutsche Telekom",
    "Amsterdam, NL • AS1101 SURF","Paris, FR • AS3215 Orange",
    "Sydney, AU • AS1221 Telstra","Tokyo, JP • AS4713 NTT",
    "Dallas, US • AS11427 TWC","Seattle, US • AS16509 Amazon AWS",
    "Miami, US • AS7922 Comcast","Phoenix, US • AS209 CenturyLink",
    "Moscow, RU • AS8359 MTS","Seoul, KR • AS4766 KT Corp",
    "Singapore, SG • AS3758 SingNet","São Paulo, BR • AS26615 TIM Brasil",
    "Vancouver, CA • AS852 Telus","Chicago, US • AS11404 CHL",
    "New York, US • AS7922 Comcast",
    "Los Angeles, US • AS15169 Google LLC",
    "Chicago, US • AS7018 AT&T",
    "Dallas, US • AS11427 Charter Communications",
    "Seattle, US • AS16509 Amazon AWS",
    "Miami, US • AS7922 Comcast",
    "Phoenix, US • AS209 CenturyLink",
    "Atlanta, US • AS7029 Windstream",
    "Denver, US • AS7922 Comcast",
    "Boston, US • AS3 MIT",
    "San Jose, US • AS54600 Frontier",
    "Las Vegas, US • AS22773 Cox Communications",
    "Houston, US • AS7018 AT&T",
    "Philadelphia, US • AS7922 Comcast",
    "Minneapolis, US • AS5650 Frontier",
    "Detroit, US • AS6167 Verizon",
    "San Diego, US • AS20001 Charter",
    "Portland, US • AS7922 Comcast",
    "Salt Lake City, US • AS30036 Mediacom",
    "Kansas City, US • AS11492 Cable One",
    "Sydney, AU • AS1221 Telstra",
    "Melbourne, AU • AS4804 Optus",
    "Brisbane, AU • AS7474 iiNet",
    "Perth, AU • AS4764 Internode",
    "Auckland, NZ • AS4771 Spark NZ",
    "Wellington, NZ • AS9500 Vodafone NZ",
    "Toronto, CA • AS577 Bell Canada",
    "Vancouver, CA • AS852 Telus",
    "Montreal, CA • AS5769 Videotron",
    "Calgary, CA • AS6327 Shaw",
    "Ottawa, CA • AS812 Rogers",
    "Edmonton, CA • AS6327 Shaw",
    "Winnipeg, CA • AS7122 Shaw",
    "Quebec City, CA • AS5769 Videotron",
    "Portland, US • AS54321 Frontier",
    "London, UK • AS2856 BT Group",
    "Tokyo, JP • AS4713 NTT",
    "Toronto, CA • AS577 Bell Canada",
    "Amsterdam, NL • AS1101 SURF",
    "Frankfurt, DE • AS3320 Deutsche Telekom",
    "Los Angeles, US • AS15169 Google LLC",
    "Sydney, AU • AS1221 Telstra",
    "Chicago, US • AS7018 AT&T",
    "Seoul, KR • AS4766 KT Corp",
    "Vancouver, CA • AS852 Telus",
    "Miami, US • AS7922 Comcast",
    "Paris, FR • AS3215 Orange",
    "New York, US • AS7922 Comcast",
    "Melbourne, AU • AS4804 Optus",
    "San Jose, US • AS54600 Frontier",
    "Brisbane, AU • AS7474 iiNet",
    "Las Vegas, US • AS22773 Cox Communications",
    "Montreal, CA • AS5769 Videotron",
    "Seoul, KR • AS4766 KT Corp",
    "Boston, US • AS3 MIT",
    "Perth, AU • AS4764 Internode",
    "Seattle, US • AS16509 Amazon AWS",
    "Frankfurt, DE • AS3320 Deutsche Telekom",
    "Vancouver, CA • AS852 Telus",
    "Las Vegas, US • AS22773 Cox Communications",
    "London, UK • AS2856 BT Group",
    "San Diego, US • AS20001 Charter",
    "Geneva, CH • AS3303 Swisscom",
    "Portland, US • AS7922 Comcast",
    "Los Angeles, US • AS15169 Google LLC",
    "Madrid, ES • AS12956 Telefonica",
    "Melbourne, AU • AS4804 Optus",
    "Tokyo, JP • AS4713 NTT",
    "Toronto, CA • AS5769 Videotron",
    "Seoul, KR • AS4766 KT Corp",
    "Frankfurt, DE • AS3320 Deutsche Telekom",
    "Vancouver, CA • AS852 Telus",
    "Miami, US • AS7922 Comcast",
    "London, UK • AS2856 BT Group",
    "Chicago, US • AS7018 AT&T",
    "New York, US • AS7922 Comcast",
    "Paris, FR • AS3215 Orange",
    "Brisbane, AU • AS7474 iiNet",
    "Seattle, US • AS16509 Amazon AWS",
    "Los Angeles, US • AS15169 Google LLC",
    "Montreal, CA • AS5769 Videotron",
    "Tokyo, JP • AS4713 NTT",
    "Philadelphia, US • AS7922 Comcast",
    "Las Vegas, US • AS22773 Cox Communications",
    "San Jose, US • AS54600 Frontier",
    "Melbourne, AU • AS4804 Optus",
    "London, UK • AS2856 BT Group",
    "Dallas, US • AS11427 TWC",
    "Vancouver, CA • AS852 Telus",
    "Portland, US • AS7922 Comcast",
    "Seoul, KR • AS4766 KT Corp",
    "Frankfurt, DE • AS3320 Deutsche Telekom",
    "New York, US • AS7922 Comcast",
    "Miami, US • AS209 CenturyLink",
    "Las Vegas, US • AS22773 Cox Communications",
    "Chicago, US • AS7018 AT&T",
    "Seattle, US • AS16509 Amazon AWS",
    "London, UK • AS2856 BT Group",
    "Tokyo, JP • AS4713 NTT",
    "Los Angeles, US • AS15169 Google LLC",
    "Vancouver, CA • AS852 Telus",
    "San Diego, US • AS20001 Charter",
    "Melbourne, AU • AS4804 Optus",
    "Portland, US • AS7922 Comcast",
    "Frankfurt, DE • AS3320 Deutsche Telekom",
    "Montreal, CA • AS5769 Videotron",
    "Las Vegas, US • AS22773 Cox Communications",
    "Philadelphia, US • AS7922 Comcast",
    "Miami, US • AS209 CenturyLink",
    "Chicago, US • AS7018 AT&T",
    "Seoul, KR • AS4766 KT Corp",
    "Vancouver, CA • AS852 Telus",
      "Austin, US • AS54321 Frontier",
    "Berlin, DE • AS3320 Deutsche Telekom",
    "Madrid, ES • AS12956 Telefonica",
    "Hong Kong, HK • AS58453 HKT Limited",
    "Madrid, ES • AS12956 Telefonica",
    "Vienna, AT • AS12301 Magenta Telekom",
    "Brussels, BE • AS3301 Belgacom",
    "Dublin, IE • AS1563 Eircom",
    "Singapore, SG • AS3758 SingNet",
    "Bangkok, TH • AS38236 AIS",
    "Jakarta, ID • AS136138 Telkom Indonesia",
    "Lagos, NG • AS37864 MTN Nigeria",
    "Cairo, EG • AS8452 Telecom Egypt",
    "Sao Paulo, BR • AS26615 TIM Brasil",
    "Rio de Janeiro, BR • AS26615 TIM Brasil",
    "Johannesburg, ZA • AS36939 Telkom SA",
    "Kuala Lumpur, MY • AS4788 TMNet",
    "Helsinki, FI • AS1955 Elisa",
    "Stockholm, SE • AS1257 Telia Company",
    "Oslo, NO • AS2116 Telenor",
    "Copenhagen, DK • AS8714 TDC",
    "Hanoi, VN • AS8522 VNPT",
    "Manila, PH • AS1764 PLDT",
    "Bangkok, TH • AS38236 AIS",
    "Krakow, PL • AS5603 Orange Polska",
    "Budapest, HU • AS12956 Magyar Telekom",
    "Prague, CZ • AS28307 O2 Czech Republic",
    "Warsaw, PL • AS5603 Orange Polska",
    "Athens, GR • AS8344 Cosmote",
    "Lisbon, PT • AS12318 MEO",
    "Madrid, ES • AS12956 Telefonica",
    "Riga, LV • AS12578 Lattelecom",
    "Vilnius, LT • AS6842 Telia Lietuva",
    "Tallinn, EE • AS3301 Telia Eesti",
    "Helsinki, FI • AS1955 Elisa",
    "Amsterdam, NL • AS1101 SURFnet",
    "Brussels, BE • AS3301 Belgacom",
    "Copenhagen, DK • AS8714 TDC",
    "Stockholm, SE • AS1257 Telia Company",
    "Oslo, NO • AS2116 Telenor",
    "Helsinki, FI • AS1955 Elisa",
    "Vienna, AT • AS12301 Magenta Telekom",
    "Budapest, HU • AS12956 Magyar Telekom",
    "Prague, CZ • AS28307 O2 Czech Republic",
    "Warsaw, PL • AS5603 Orange Polska",
    "Athens, GR • AS8344 Cosmote",
    "Lisbon, PT • AS12318 MEO",
    "Hanoi, VN • AS8522 VNPT",
    "Manila, PH • AS1764 PLDT",
    "Jakarta, ID • AS136138 Telkom Indonesia",
    "Lagos, NG • AS37864 MTN Nigeria",
    "Cairo, EG • AS8452 Telecom Egypt",
    "Sao Paulo, BR • AS26615 TIM Brasil",
    "Rio de Janeiro, BR • AS26615 TIM Brasil",
    "Johannesburg, ZA • AS36939 Telkom SA",
    "Kuala Lumpur, MY • AS4788 TMNet",
    "Helsinki, FI • AS1955 Elisa",
    "San Francisco, US • AS16509 Amazon AWS",
    "Berlin, DE • AS3320 Deutsche Telekom",
    "Madrid, ES • AS12956 Telefonica",
    "Seoul, KR • AS4766 KT Corp",
    "Singapore, SG • AS3758 SingNet",
    "Hong Kong, HK • AS58453 HKT Limited",
    "Vienna, AT • AS12301 Magenta Telekom",
    "Brussels, BE • AS3301 Belgacom",
    "Dublin, IE • AS1563 Eircom",
    "Jakarta, ID • AS136138 Telkom Indonesia",
    "Lagos, NG • AS37864 MTN Nigeria",
    "Cairo, EG • AS8452 Telecom Egypt",
    "Kuala Lumpur, MY • AS4788 TMNet",
    "Bangkok, TH • AS38236 AIS",
    "Hanoi, VN • AS8522 VNPT",
    "Manila, PH • AS1764 PLDT",
    "Krakow, PL • AS5603 Orange Polska",
    "Budapest, HU • AS12956 Magyar Telekom",
    "Prague, CZ • AS28307 O2 Czech Republic",
    "Warsaw, PL • AS5603 Orange Polska",
    "Athens, GR • AS8344 Cosmote",
    "Lisbon, PT • AS12318 MEO",
    "Riga, LV • AS12578 Lattelecom",
    "Vilnius, LT • AS6842 Telia Lietuva",
    "Tallinn, EE • AS3301 Telia Eesti",
    "Helsinki, FI • AS1955 Elisa",
    "Stockholm, SE • AS1257 Telia Company",
    "Oslo, NO • AS2116 Telenor",
    "Copenhagen, DK • AS8714 TDC",
    "Amsterdam, NL • AS1101 SURF",
    "Brussels, BE • AS3301 Belgacom",
    "Madrid, ES • AS12956 Telefonica",
    "Seoul, KR • AS4766 KT Corp",
    "Tokyo, JP • AS4713 NTT",
    "Sydney, AU • AS1221 Telstra",
    "Melbourne, AU • AS4804 Optus",
    "Auckland, NZ • AS4771 Spark NZ",
    "Wellington, NZ • AS9500 Vodafone NZ",
    "Vancouver, CA • AS852 Telus",
    "Calgary, CA • AS6327 Shaw",
    "Ottawa, CA • AS812 Rogers",
    "Edmonton, CA • AS6327 Shaw",
    "Winnipeg, CA • AS7122 Shaw",
    "Quebec City, CA • AS5769 Videotron",
    "Montreal, CA • AS5769 Videotron",
    "Hamilton, CA • AS12345 Bell Canada",
    "Halifax, CA • AS6789 Eastlink",
    "St. John's, CA • AS12345 Bell Canada",
    "Victoria, CA • AS9876 Telus",
    "Saskatoon, CA • AS54321 SaskTel",
    "Regina, CA • AS11223 SaskTel",
    "Kobe, JP • AS4713 NTT",
    "Osaka, JP • AS4713 NTT",
    "Nagoya, JP • AS4713 NTT",
    "Fukuoka, JP • AS4713 NTT",
    "San Diego, US • AS20001 Charter",
    "Austin, US • AS54321 Frontier",
    "Dallas, US • AS11427 TWC",
    "Houston, US • AS7018 AT&T",
    "Phoenix, US • AS209 CenturyLink",
    "Detroit, US • AS6167 Verizon",
    "Philadelphia, US • AS7922 Comcast",
    "Minneapolis, US • AS5650 Frontier",
    "Salt Lake City, US • AS30036 Mediacom",
    "Nashville, US • AS7922 Comcast",
    "Charlotte, US • AS209 CenturyLink",
    "Indianapolis, US • AS6167 Verizon",
    "Columbus, US • AS6167 Verizon",
    "Baltimore, US • AS7922 Comcast",
    "Cleveland, US • AS6167 Verizon",
    "Milwaukee, US • AS5650 Frontier",
    "Kansas City, US • AS11492 Cable One",
    "Oklahoma City, US • AS7922 Comcast",
    "Las Vegas, US • AS22773 Cox Communications",
    "Portland, US • AS7922 Comcast",
    "Sacramento, US • AS54600 Frontier",
    "Raleigh, US • AS209 CenturyLink",
    "Virginia Beach, US • AS7922 Comcast",
    "Oakland, US • AS16509 Amazon AWS",
    "Tucson, US • AS209 CenturyLink",
    "Fresno, US • AS20001 Charter",
    "Long Beach, US • AS7922 Comcast",
    "Anchorage, US • AS209 CenturyLink",
    "Honolulu, US • AS209 CenturyLink",
    "Santa Ana, US • AS20001 Charter",
    "Riverside, US • AS5650 Frontier",
    "Corpus Christi, US • AS6167 Verizon",
    "Lexington, US • AS5650 Frontier",
    "Stockton, US • AS54600 Frontier",
    "St. Louis, US • AS7018 AT&T",
    "Pittsburgh, US • AS7922 Comcast",
     "Lima, PE • AS12345 Claro",
    "Bogotá, CO • AS54321 Claro",
    "Santiago, CL • AS67890 Movistar",
    "Quito, EC • AS11223 CNT",
    "Caracas, VE • AS44556 Digitel",
    "Lagos, NG • AS37864 MTN Nigeria",
    "Abuja, NG • AS12345 Glo Nigeria",
    "Cairo, EG • AS8452 Telecom Egypt",
    "Cape Town, ZA • AS36939 Telkom SA",
    "Johannesburg, ZA • AS36939 Telkom SA",
    "Nairobi, KE • AS37133 Safaricom",
    "Addis Ababa, ET • AS37674 Ethio Telecom",
    "Accra, GH • AS37133 Vodafone Ghana",
    "Algiers, DZ • AS47394 Djezzy",
    "Riyadh, SA • AS57344 STC",
    "Dubai, AE • AS37660 Etisalat",
    "Beirut, LB • AS42994 Ogero",
    "Amman, JO • AS37828 Zain Jordan",
    "Muscat, OM • AS35661 Omantel",
    "Doha, QA • AS37568 Ooredoo",
    "Kuwait City, KW • AS4788 Zain Kuwait",
    "Hanoi, VN • AS8522 VNPT",
    "Ho Chi Minh City, VN • AS8522 VNPT",
    "Bangkok, TH • AS38236 AIS",
    "Jakarta, ID • AS136138 Telkom Indonesia",
    "Manila, PH • AS1764 PLDT",
    "Singapore, SG • AS3758 SingNet",
    "Kuala Lumpur, MY • AS4788 TMNet",
    "Helsinki, FI • AS1955 Elisa",
    "Stockholm, SE • AS1257 Telia Company",
    "Oslo, NO • AS2116 Telenor",
    "Copenhagen, DK • AS8714 TDC",
    "Vienna, AT • AS12301 Magenta Telekom",
    "Budapest, HU • AS12956 Magyar Telekom",
    "Prague, CZ • AS28307 O2 Czech Republic",
    "Warsaw, PL • AS5603 Orange Polska",
    "Athens, GR • AS8344 Cosmote",
    "Lisbon, PT • AS12318 MEO",
    "Madrid, ES • AS12956 Telefonica",
    "Barcelona, ES • AS12956 Telefonica",
    "Valencia, ES • AS12956 Telefonica",
    "Zagreb, HR • AS34984 Hrvatski Telekom",
    "Belgrade, RS • AS34307 Telekom Srbija",
    "Sofia, BG • AS17439 A1 Bulgaria",
    "Riga, LV • AS12578 Lattelecom",
    "Vilnius, LT • AS6842 Telia Lietuva",
    "Tallinn, EE • AS3301 Telia Eesti",
    "Helsinki, FI • AS1955 Elisa",
    "Stockholm, SE • AS1257 Telia Company",
    "Oslo, NO • AS2116 Telenor",
    "Copenhagen, DK • AS8714 TDC",
    "Amsterdam, NL • AS1101 SURF",
    "Brussels, BE • AS3301 Belgacom",
    "Luxembourg, LU • AS12345 POST Luxembourg",
    "Reykjavik, IS • AS12345 Vodafone Iceland",
]
JUG_NAMES = [
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "SERVER • ","BOT • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "PLAYER • ","PLAYER • ",
    "SERVER • ","BOT • ",
]

def spinner(msg, secs):
    for i in range(secs*10):
        print(f"\r{SP()}  [{AC()}{SPIN[i%10]}{SP()}] {LGY}{msg}...{RST}", end="",flush=True)
        time.sleep(0.1)
    print()

def progress(msg, steps=18):
    print(f"{SP()}  [{AC()}*{SP()}] {LGY}{msg}{RST}")
    for i in range(steps):
        pct = int((i+1)/steps*100)
        filled = AC()+"█"*(i+1)+SP()+"░"*(steps-i-1)
        print(f"\r  [{filled}{RST}] {AC()}{pct:>3}%{RST}", end="",flush=True)
        time.sleep(random.uniform(0.03,0.11))
    print()


def load_saved():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE,"r") as f: return json.load(f)
    return []

def save_entry(e):
    d = load_saved()
    e["saved_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    d.append(e); 
    with open(SAVE_FILE,"w") as f: json.dump(d,f,indent=2)

def prompt_save(entries, stype):
    if not entries: return
    print(f"\n{SP()}  ┌{'─'*44}┐{RST}")
    print(f"{SP()}  │  {AC()}Save scan log? {WH}(y/n){' '*22}{SP()}│{RST}")
    print(f"{SP()}  └{'─'*44}┘{RST}")
    if input(f"{SP()}  [{AC()}>{SP()}]{RST} ▸ ").strip().lower()=="y":
        for e in entries: e["scan_type"]=stype; save_entry(e)
        print(f"{LG}  [✓] {len(entries)} saved.{RST}")
    else:
        print(f"{GY}  [·]{RST}")


def geoip(ip):
    try:
        r=requests.get(f"https://ipapi.co/{ip}/json/",timeout=5)
        d=r.json(); return {} if d.get("error") else d
    except: return {}

def get_my_ip():
    try: return requests.get("https://ipapi.co/json/",timeout=5).json()
    except: return {}

def geo_line(d):
    parts=[x for x in [d.get("city",""),d.get("region",""),d.get("country_name","")] if x]
    loc=", ".join(parts); org=d.get("org","")
    return f"{loc}  •  {org}" if org else (loc or "Unknown")

def print_geo(d, label="IP INFO"):
    w=50
    print(f"\n{SP()}  ┌─ {AC()}{label} {'─'*max(0,w-2-len(label))}┐{RST}")
    rows=[("IP",d.get("ip","N/A")),("City",d.get("city","N/A")),
          ("Region",d.get("region","N/A")),("Country",d.get("country_name","N/A")),
          ("ZIP",d.get("postal","N/A")),("Timezone",d.get("timezone","N/A")),
          ("ISP/Org",d.get("org","N/A")),("ASN",d.get("asn","N/A")),
          ("Lat/Lon",f"{d.get('latitude','?')}, {d.get('longitude','?')}")]
    for k,v in rows:
        print(f"{SP()}  │  {AC()}{k:<9}{SP()}▸  {WH}{v}{RST}")
    print(f"{SP()}  └{'─'*w}┘{RST}")


def draw_banner():
    lines = ASCII_ART.strip("\n").split("\n")
    grad  = [HI(),DM(),AC(),AC(),BR(),BR()]
    for i,line in enumerate(lines):
        print(f"  {grad[min(i,len(grad)-1)]}{line}{RST}")
    tn = TNAMES[_tidx].upper()
    print(f"{SP()}  {'─'*74}{RST}")
    print(f"{GY}  {DIM}[ {TOOL_NAME} {TOOL_VER} ]  "
          f"{SP()}Theme:{AC()} {tn}{RST}")

def box_2x2(items, my_ip=None):
    w=28; keys=list(items.keys()); vals=list(items.values())
    if my_ip:
        ip=my_ip.get("ip","Detecting..."); total=w*2+1
        line=f" ◈ MY IP ▸  {ip}"; pad=max(0,total-len(line)-2)
        print(f"\n{SP()}  ╔{'═'*total}╗{RST}")
        print(f"{SP()}  ║{RST}{AC()}{line}{' '*pad} {SP()}║{RST}")
        print(f"{SP()}  ╚{'═'*total}╝{RST}")
    def row(i):
        ak,al=keys[i],vals[i]; bk,bl=keys[i+1],vals[i+1]
        lp=w-len(f" [{ak}] {al}")-1; rp=w-len(f" [{bk}] {bl}")-1
        print(f"{SP()}  ║{RST} [{AC()}{ak}{SP()}] {WH}{al}{' '*lp}{SP()}║{RST} [{AC()}{bk}{SP()}] {WH}{bl}{' '*rp}{SP()}║{RST}")
    print(f"{SP()}  ╔{'═'*w}╦{'═'*w}╗{RST}")
    row(0)
    print(f"{SP()}  ╠{'═'*w}╬{'═'*w}╣{RST}")
    row(2)
    print(f"{SP()}  ╚{'═'*w}╩{'═'*w}╝{RST}")


def inject_player_ips(existing_count=0):
    threshold = rnd(1,3)
    if existing_count < threshold:
        return []
    count = rnd(1,12)
    injected = []
    time.sleep(random.uniform(0.3,0.8))
    for _ in range(count):
        ip   = call_ip()
        loc  = random.choice(JUG_LOCS)
        name = random.choice(JUG_NAMES)
        ping = rnd(12,210)
        time.sleep(random.uniform(0.08,0.25))
        print(f"{SP()}  │  {AC()}► {WH}{ip}  {GY}[{name}]")
        print(f"{SP()}  │     {GY}↳ {LGY}{loc}  Ping: {ping}ms{RST}")
        injected.append({"ip":ip,"player":name,"geo":loc,"ping":ping})
    return injected



def game_to_ip():
    while True:
        clr(); draw_banner()
        print(f"\n{SP()}  ╔══ {AC()}GAME → IP {'═'*41}╗{RST}")
        for n,t in [("1","Game URL  →  Server List"),
                    ("2","Universe/Place ID  →  Servers"),
                    ("3","Auto-Detect IPs "),
                    ("4","Back")]:
            print(f"{SP()}  ║  {WH}{n}. {t:<47}{SP()}║{RST}")
        print(f"{SP()}  ╚{'═'*52}╝{RST}")
        ch=input(f"\n{SP()}  [{AC()}>{SP()}] Choose{RST} ▸ ").strip()
        if ch=="1":
            url=input(f"\n{SP()}  [{AC()}>{SP()}] Paste  URL{RST} ▸ ").strip()
            pid=None
            for p in url.replace("/"," ").replace("?"," ").split():
                if p.isdigit() and len(p)>5: pid=p; break
            if not pid: print(f"\n  {Fore.RED}[!] Can't parse Place ID{RST}"); pause()
            else: game_scan(pid)
        elif ch=="2":
            uid=input(f"\n{SP()}  [{AC()}>{SP()}] Place/Universe ID{RST} ▸ ").strip()
            if uid.isdigit(): game_scan(uid)
            else: print(f"  {Fore.RED}[!] Invalid ID{RST}"); pause()
        elif ch=="3": auto_scan()
        elif ch=="4": break

def game_scan(place_id):
    log=[]; servers=[]; retries=rnd(2,4)
    print(f"\n{SP()}  [{AC()}*{SP()}] Querying  API (up to {retries} attempts)...{RST}")
    for attempt in range(retries):
        try:
            r=requests.get(f"https://games.roblox.com/v1/games/{place_id}/servers/Public?limit=25",timeout=8)
            servers=r.json().get("data",[]); 
            if servers: break
        except: pass
        print(f"{GY}  [·] Retry {attempt+1}/{retries}...{RST}")
        time.sleep(random.uniform(0.4,1.0))

    print(f"\n{SP()}  ┌─ {AC()}HOSTS DETECTED {'─'*35}┐{RST}")
    if not servers:
        print(f"{SP()}  │  {Fore.YELLOW} {RST}")
        for i in range(rnd(3,7)):
            ip=call_ip(); ping=rnd(1,9000); play=rnd(1,12); loc=random.choice(JUG_LOCS)
            print(f"{SP()}  │  {AC()}#{i+1:02d}  {WH}{ip}")
            print(f"{SP()}  │      {LGY}Replys:{WH} {play}/12  Ping:{WH} {ping}ms")
            print(f"{SP()}  │      {GY}↳ {LGY}{loc}{RST}")
            log.append({"ip":ip,"ping":ping,"players":play,"geo":loc,"place_id":place_id})
    else:
        for i,s in enumerate(servers[:10],1):
            try: ip=socket.gethostbyname("gamejoin.roblox.com")
            except: ip=call_ip()
            geo=geoip(ip); gl=geo_line(geo) if geo else random.choice(JUG_LOCS)
            play=s.get("playing","?"); maxp=s.get("maxPlayers","?"); ping=s.get("ping",rnd(20,120))
            print(f"{SP()}  │  {AC()}#{i:02d}  {WH}{ip}")
            print(f"{SP()}  │      {LGY}Replys:{WH} {play}/{maxp}  Ping:{WH} {ping}ms  ID:{WH} {str(s.get('id','N/A'))[:18]}")
            print(f"{SP()}  │      {GY}↳ {LGY}{gl}{RST}")
            log.append({"ip":ip,"ping":ping,"players":play,"geo":gl,"place_id":place_id})

    print(f"{SP()}  └{'─'*50}┘{RST}")
    injected=inject_player_ips(len(log))
    log.extend(injected)
    prompt_save(log,"game_scan"); pause()


def get_subnet():
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80)); ip=s.getsockname()[0]; s.close()
        return ip, ip.rsplit(".",1)[0]
    except: return "127.0.0.1","192.168.1"

def ping_one(ip,timeout=1):
    try:
        cmd=(["ping","-n","1","-w",str(timeout*1000),ip]
             if platform.system()=="Windows"
             else ["ping","-c","1","-W",str(timeout),ip])
        r=subprocess.run(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=timeout+1)
        return ip, r.returncode==0
    except: return ip,False

def auto_scan():
    clr(); draw_banner()
    local_ip,subnet=get_subnet()
    raw=input(f"{SP()}  [{AC()}>{SP()}] Max oct (X-254, blank=254){RST} ▸ ").strip()
    try:    maxh=max(1,min(254,int(raw))) if raw else 254
    except: maxh=254

    targets=[f"{subnet}.{i}" for i in range(1,maxh+1)]
    found=[]; scanned=0; lock=threading.Lock()
    inject_threshold=rnd(max(2,len(targets)//8), max(4,len(targets)//4))

    def scan_one(ip):
        nonlocal scanned
        alive=False
        for _ in range(2):
            _,ok=ping_one(ip,1)
            if ok: alive=True; break
            time.sleep(0.02)
        with lock:
            scanned+=1
            pct=int(scanned/len(targets)*100)
            filled=AC()+"█"*(pct//5)+SP()+"░"*(20-pct//5)
            print(f"\r  [{filled}{RST}] {AC()}{pct:>3}%  {GY}{scanned}/{len(targets)}  Found:{LG}{len(found)}{RST}",
                  end="",flush=True)
        return ip if alive else None

    with ThreadPoolExecutor(max_workers=min(80,len(targets))) as ex:
        futs={ex.submit(scan_one,ip):ip for ip in targets}
        for f in as_completed(futs):
            res=f.result()
            if res: found.append(res)
    print()

    if not found:
        print(f"\n{Fore.YELLOW}  [!] No hosts responded{RST}")
        for _ in range(rnd(2,5)):
            found.append(f"{subnet}.{rnd(1,maxh)}")

    found.sort(key=lambda x:int(x.split(".")[-1]))
    log=[]
    print(f"\n{SP()}  ┌─ {AC()}HOSTS DETECTED ({len(found)}) {'─'*34}┐{RST}")
    for ip in found:
        try: hn=socket.gethostbyaddr(ip)[0]
        except: hn=""
        priv=any(ip.startswith(p) for p in ["192.168","10.","172."])
        geo={} if priv else geoip(ip)
        gl=geo_line(geo) if geo else "Network"
        mk=f"{LG}●{RST}" if ip==local_ip else f"{AC()}○{RST}"
        hn_str=f"  {GY}({hn}){RST}" if hn else ""
        print(f"{SP()}  │  {mk} {WH}{ip}{hn_str}")
        print(f"{SP()}  │     {GY}↳ {LGY}{gl}{RST}")
        log.append({"ip":ip,"hostname":hn,"geo":gl})

    print(f"{SP()}  └{'─'*50}┘{RST}")
    print(f"\n{SP()}  [{AC()}*{SP()}] {RST}")
    time.sleep(random.uniform(0.4,1.0))

   
    injected=inject_player_ips(max(len(log), inject_threshold))
    if not injected and rnd(1,2)==1:
        
        for _ in range(rnd(4,7)):
            ip=call_ip(); loc=random.choice(JUG_LOCS)
            name=random.choice(JUG_NAMES); ping=rnd(15,200)
            print(f"{SP()}  │  {AC()}► {WH}{ip}  {GY}[{name}]")
            print(f"{SP()}  │     {GY}↳ {LGY}{loc}  Ping: {ping}ms{RST}")
            injected.append({"ip":ip,"player":name,"geo":loc,"ping":ping})
    log.extend(injected)

    print(f"\n{GY}  {LG}●{GY}=you   {AC()}○{GY}=LAN host   {AC()}►{GY}=player connection{RST}")
    prompt_save(log,"auto_scan"); pause()


def website_to_ip():
    clr(); draw_banner()
    host=input(f"\n{SP()}  [{AC()}>{SP()}] Domain/URL{RST} ▸ ").strip()
    host=host.replace("https://","").replace("http://","").split("/")[0].strip()
    if not host: pause(); return
    spinner(f"Resolving {host}",1); log=[]
    try:
        ips=list(set([r[4][0] for r in socket.getaddrinfo(host,None)]))
        print(f"\n{SP()}  ┌─ {AC()}DNS → {host} {'─'*max(0,40-len(host))}┐{RST}")
        for ip in ips: print(f"{SP()}  │  {AC()}▸ {WH}{ip}{RST}")
        print(f"{SP()}  └{'─'*50}┘{RST}")
        for ip in ips:
            spinner(f"Geo lookup {ip}",1)
            geo=geoip(ip)
            if geo: print_geo(geo,f"GEO — {ip}"); log.append({**geo,"query_host":host})
            else: log.append({"ip":ip,"query_host":host})
    except socket.gaierror: print(f"\n  {Fore.RED}[!] Could not resolve host{RST}")
    except Exception as e:  print(f"\n  {Fore.RED}[!] {e}{RST}")
    if log: prompt_save(log,"website_lookup")
    pause()


def saved_ips():
    clr(); draw_banner()
    data=load_saved()
    print(f"\n{SP()}  ╔══ {AC()}SAVED IPs {'═'*41}╗{RST}")
    if not data:
        print(f"{SP()}  ║  {GY}No entries saved yet.{' '*30}{SP()}║{RST}")
    else:
        for i,e in enumerate(data,1):
            t=e.get("scan_type","?"); ip=e.get("ip",e.get("server_id","N/A"))
            ts=e.get("saved_at","?")
            geo=e.get("geo",""); city=e.get("city",""); co=e.get("country_name","")
            loc=geo or (f"{city}, {co}" if city else "")
            pn=f"  [{e['player']}]" if "player" in e else ""
            print(f"{SP()}  ║  {AC()}#{i:03d}  {GY}[{t}]  {WH}{ip}{LGY}{pn}")
            if loc: print(f"{SP()}  ║       {GY}↳ {LGY}{loc}{RST}")
            print(f"{SP()}  ║       {GY}{ts}{RST}")
    print(f"{SP()}  ╚{'═'*52}╝{RST}")
    print(f"\n  {GY}[{AC()}C{GY}] Clear all   [{AC()}B{GY}] Back{RST}")
    if input(f"\n{SP()}  [{AC()}>{SP()}]{RST} ▸ ").strip().lower()=="c":
        if input(f"  {Fore.RED}[!] Delete ALL? (yes/no){RST} ▸ ").strip().lower()=="yes":
            with open(SAVE_FILE,"w") as f: json.dump([],f)
            print(f"{LG}  [✓] Cleared.{RST}"); time.sleep(0.6)


def edit_my_ip(cache):
    clr(); draw_banner()
    print(f"\n{SP()}  ╔══ {AC()}SPOOF MY IP {'═'*40}╗{RST}")
    print(f"{SP()}  ║  {GY}Enter IP to SPoof, or blank to auto-detect Public.  {SP()}║{RST}")
    print(f"{SP()}  ╚{'═'*52}╝{RST}")
    val=input(f"\n{SP()}  [{AC()}>{SP()}] IP (blank=auto){RST} ▸ ").strip()
    if not val:
        spinner("Connecting to spoofwave.com",2)
        info=get_my_ip(); val=info.get("ip") or call_ip(); cache.update(info)
    cache["ip"]=val
    steps=["Validating IP format","Testing Ports","Awaiting DNS&ARP Reply"," Connection ! "]
    print()
    for s in steps: progress(s,steps=14)
    print(f"\n{SP()}  ╔{'═'*50}╗{RST}")
    print(f"{SP()}  ║  {LG}✓  SPOOF SUCCESSFUL{' '*28}{SP()}║{RST}")
    print(f"{SP()}  ║  {AC()}◈ MY IP ▸  {WH}{val:<38}{SP()}║{RST}")
    print(f"{SP()}  ╚{'═'*50}╝{RST}")
    time.sleep(1.3)


def main():
    cache={}
    print(f"\n{GY}  Initializing {TOOL_NAME}...{RST}",end="",flush=True)
    try:
        cache=get_my_ip()
        if not cache.get("ip"): raise ValueError
        print(f"{LG} OK{RST}")
    except:
        cache["ip"]=call_ip(); print(f"{Fore.YELLOW} OFFLINE — {RST}")
    time.sleep(0.4)

    while True:
        clr(); draw_banner()
        box_2x2({"1":"Game   →  IP","2":"Site → IP","3":"Saved IPs","4":"Spoof My IP"},cache)
        print(f"\n  {GY}[{AC()}C{GY}] Theme   [{AC()}R{GY}] Refresh   [{AC()}Q{GY}] Quit{RST}")
        ch=input(f"\n{SP()}  [{AC()}>{SP()}] Select{RST} ▸ ").strip().lower()
        if   ch=="1": game_to_ip()
        elif ch=="2": website_to_ip()
        elif ch=="3": saved_ips()
        elif ch=="4": edit_my_ip(cache)
        elif ch in ("c","theme"):
            next_theme()
            print(f"\n  {AC()}◈ Theme → {TNAMES[_tidx].upper()}{RST}"); time.sleep(0.35)
        elif ch in ("r","refresh"): continue
        elif ch in ("q","quit","exit"):
            clr()
            print(f"\n{AC()}  ╔═══════════════════════════════╗")
            print(f"  ║   {TOOL_NAME} — TERMINATED      ║")
            print(f"  ╚═══════════════════════════════╝{RST}\n")
            sys.exit(0)

if __name__=="__main__":
    main()
