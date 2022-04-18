from selenium import webdriver
import time
import hashlib
import os
import warnings
import argparse

warnings.filterwarnings("ignore", category=DeprecationWarning)

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', help="mix url", type=str)
parser.add_argument('-n', '--number', help="how many videos? (type n for 24n+1 videos)", type=int)
args = parser.parse_args()
tmp_file="yt_tmp.txt"
prg_file="yt_prg.txt"

given_number = 2
if args.url:
    url = args.url
else:
    url=input("Youtube mix playlist url: ")
if url.find("list")==-1:
    print("url does not contain youtube mix")
if args.number:
    given_number=args.number
else:
    given_number=int(input("How many videos do you want? (type 1 for 25 videos, 2 for 49 videos, n for 24n+1 videos): "))

browserProfile = webdriver.ChromeOptions()
browserProfile.add_argument("--lang=en-us")
headless = True
if headless == True:
    browserProfile.add_argument("--headless")
    browserProfile.add_argument("--window-size=1920,1080")
    browserProfile.add_argument("--disable-notifications")
    browserProfile.add_argument('--log-level=3')
try:
    browser = webdriver.Chrome('chromedriver.exe', options=browserProfile)
except Exception as e:
    if os.path.isfile(f"{os.getcwd()}/chrome_driver/chromedriver.exe"):
        if os.path.isfile("chromedriver.exe"):
            os.remove("chromedriver.exe")
        browser = webdriver.Chrome(
            f'{os.getcwd()}/chrome_driver/chromedriver.exe', options=browserProfile)
    else:
        if os.path.isfile("chromedriver.exe"):
            print("Your chromedriver.exe is not up to date, automatic update started")
        k = []
        ll = 0
        k.append(str(e).replace(" ", "\n").split())
        for i in k:
            while True:
                try:
                    i[ll]
                except IndexError:
                    print("Please download chromedriver.exe")
                    exit()
                if i[ll] == "is":
                    version = i[ll+1]
                    if version[0:3] == "101":
                        ver_url = "101.0.4951.15"
                    elif version[0:3] == "100":
                        ver_url = "100.0.4896.60"
                    elif version[0:2] == "99":
                        ver_url = "99.0.4844.51"
                    else:
                        ver_url = version
                    import wget
                    import zipfile
                    wget.download(
                        f"https://chromedriver.storage.googleapis.com/{ver_url}/chromedriver_win32.zip", f"chromedriver.zip")
                    with zipfile.ZipFile(f"chromedriver.zip", 'r') as zip_ref:
                        if not os.path.isdir("chrome_driver"):
                            zip_ref.extractall("chrome_driver")
                            zip_ref.close()
                            os.remove("chromedriver.zip")
                            cwd = os.getcwd()
                            try:
                                browser = webdriver.Chrome(
                                    f'{cwd}/chrome_driver/chromedriver.exe', options=browserProfile)
                                if os.path.isfile("chromedriver.exe"):
                                    os.remove("chromedriver.exe")
                                break
                            except:
                                print(
                                    f"Your version is {version}, please download chromedriver.exe manually into {os.getcwd()}")
                                exit()
                        else:
                            os.remove("chromedriver.zip")
                            print(
                                f"\nDelete chrome_driver file in {os.getcwd()} and run again")
                            exit()
                else:
                    ll = ll+1
browser.get(f"{url}")

a = []
ii = 0

while ii < given_number:
    time.sleep(3)
    with open(f"{tmp_file}", "a", encoding="utf-8") as f:
        eles = browser.find_elements_by_css_selector(
            "a.yt-simple-endpoint.style-scope.ytd-playlist-panel-video-renderer")
        for i in eles:
            f.write(i.get_attribute("href")+"\n")
            a.append(i.get_attribute("href"))
        browser.get(f"{a[-1]}")
        ii = ii+1

with open(f"{tmp_file}", "r", encoding="utf-8") as f:
    lines = f.readlines()
    for l in lines:
        res = l[0:l.index("index=")-1]
        with open(f"{prg_file}", "a", encoding="utf-8") as d:
            d.write(res+"\n")

list_name=url.find("list=")+5
list_name_2=url.find("&start")
if list_name_2==-1:
    final_file=f"list {url[list_name:]} - {24*given_number+1}.txt"
else:
    final_file=f"list {url[list_name:list_name_2]} - {24*given_number+1}.txt"
completed_lines_hash = set()
output_file = open(f"{final_file}", "w", encoding="utf-8")
for line in open(f"{prg_file}", "r", encoding="utf-8"):
  hashValue = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()
  if hashValue not in completed_lines_hash:
    output_file.write(line)
    completed_lines_hash.add(hashValue)
output_file.close()

os.remove(f"{tmp_file}")
os.remove(f"{prg_file}")

print(str(len(open(f'{final_file}','r').readlines()))+f" urls registered in file '{final_file}'")
