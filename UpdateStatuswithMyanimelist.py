import requests
import time
import json
import objectpath
import urllib.request
import sys,os
from contextlib import contextmanager
from bs4 import BeautifulSoup
from pypresence import Presence
from urllib.request import Request, urlopen

# Get MAL Stats
url = "https://myanimelist.net/profile/username"
req = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
soup = BeautifulSoup(webpage, 'lxml')
subject_options = soup.find_all("span", attrs={"class": "di-ib fl-r lh10"})
#End Stats

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout
def test():
    rp = urllib.request.urlretrieve("http://127.0.0.1:8080/jsonrpc?request={%20%22jsonrpc%22:%20%222.0%22,%20%22method%22:%20%22Player.GetItem%22,%20%22params%22:%20{%20%22properties%22:%20[%20%22title%22,%20%22album%22,%20%22artist%22,%20%22season%22,%20%22episode%22,%20%22duration%22,%20%22showtitle%22,%20%22tvshowid%22,%20%22thumbnail%22,%20%22file%22,%20%22fanart%22,%20%22streamdetails%22%20],%20%22playerid%22:%201%20},%20%22id%22:%20%22VideoGetItem%22%20}", "kodi.json")
        # to test : get used time from http://127.0.0.1:8080/jsonrpc?request={%22jsonrpc%22:%222.0%22,%22method%22:%22Player.GetProperties%22,%22params%22:{%22playerid%22:1,%22properties%22:[%22speed%22,%22position%22,%20%22time%22]},%22id%22:1}
    client_id = 'myclientid' 
    RPC = Presence(client_id)  # Initialize the client class
    RPC.connect() # Start the handshake loop
    
    # get different json elements
    with open("kodi.json") as datafile:    data = json.load(datafile)
    data_tree = objectpath.Tree(data['result'])
    ep = tuple(data_tree.execute('$..episode'))
    season = tuple(data_tree.execute('$..season'))
    show = tuple(data_tree.execute('$..showtitle'))
    label = tuple(data_tree.execute('$..label'))
    dur = tuple(data_tree.execute('$..duration'))
    # end of json grab 
    
    Epp = int(ep[0])
    Sea = int(season[0])
    Sho = ''.join(show)
    lab  = ''.join(label)
    dura = int(dur[0])
    epoch_time = int(time.time())
    temps = time.strftime("%M:%S", time.localtime(dura))
    if len(str(Epp)) > 1:
        print(RPC.update(pid=5555, small_text = 'W : ' +''.join(subject_options[0].contents) + ', C : ' +''.join(subject_options[1].contents)+ ', H : ' +''.join(subject_options[2].contents)+ ', D : ' +''.join(subject_options[3].contents)+ ', P : ' + ''.join(subject_options[4].contents), small_image='mysmallimage', large_image='mylargeimage', state=Sho, details='S0'+str(Sea)+'E'+str(Epp)+ ' - ' + str(lab), start = epoch_time))
    else:
        print(RPC.update(pid=5555, small_text = 'W : ' +''.join(subject_options[0].contents) + ', C : ' +''.join(subject_options[1].contents)+ ', H : ' +''.join(subject_options[2].contents)+ ', D : ' +''.join(subject_options[3].contents)+ ', P : ' + ''.join(subject_options[4].contents), small_image='mysmallimage', large_image='mylargeimage', state=Sho, details='S0'+str(Sea)+'E0'+str(Epp)+ ' - ' + str(lab),start = epoch_time))
    time.sleep(dura)
    #time.sleep(60)
    RPC.clear(pid=os.getpid())
while True:
    with suppress_stdout():
        test()
