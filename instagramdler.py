import sys
import requests
import time
import urllib.request
import os
import json

INSTAGRAM_USERNAME = "xcoteam"

class Instagram_Downloader:
    def __init__(self, username):
        self.username = username
        self.user_id = ""
        self.jsondata = ""
        self.apilabel = "graphql"
        self.hash_timeline = ""

    def create_download_directory(self):
        try:
            os.mkdir(self.username)
            print("Directory ", self.username, " created.")
        except FileExistsError:
            print("Directory ", self.username, " already exists.")

    def get_total_photos(self):
        return int((self.jsondata.json()[self.apilabel]["user"]["edge_owner_to_timeline_media"]["count"])) 

    def set_user_id(self):
        self.user_id = int(self.jsondata.json()[self.apilabel]["user"]["id"])

    def get_end_cursor_timeline_media(self):
        return self.jsondata.json()[self.apilabel]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]
    
    def write_resume_end_cursor_timeline_media(self):
        f = open("resume_"+self.username+".txt", "w")   
        f.write(str(self.get_end_cursor_timeline_media()))
        f.close()

    def read_resume_end_cursor_timeline_media(self):
        if os.path.isfile("resume_"+self.username+".txt"):
            with open("resume_"+self.username+".txt") as f:
                self.hash_timeline = f.readline().strip()
                print ("****************\nResume mode ON\n****************")
                return True
        else:
            print ("Not resume pending")
            return False
    
    def remove_resume_file(self):
        if os.path.exists("resume_"+self.username+".txt"):
            os.remove("resume_"+self.username+".txt")

    def set_apilabel(self,label):
        self.apilabel = label
    
    def has_next_page(self):
        return self.jsondata.json()[self.apilabel]["user"]["edge_owner_to_timeline_media"]["page_info"]["has_next_page"]

    def get_jsondata_instagram(self):
        headers = {
            "Host": "www.instagram.com",
            "User-Agent": "from XCO haker's"
        }
        if self.apilabel=="graphql":
            self.jsondata = requests.get("https://www.instagram.com/" + self.username + "/feed/?__a=1", headers=headers)  
            self.hash_timeline = self.get_end_cursor_timeline_media()
            self.set_user_id()   
        else:
            self.jsondata = requests.get("https://www.instagram.com/xcoteam/" + str(self.hash_timeline) + "%22%7D", headers=headers)
            if user.has_next_page():
                self.hash_timeline = self.get_end_cursor_timeline_media()
        if (self.jsondata.status_code==200):
            print("----------------\nJson url loaded:\n----------------\nhttps://www.instagram.com/xcoteam/" + str(self.hash_timeline) + "%22%7D")
        else:
            print("ERROR:")
        return self.jsondata

    def download_photos(self):
        i = 0 
        for match in self.jsondata.json()[self.apilabel]["user"]["edge_owner_to_timeline_media"]["edges"]: 
            time.sleep(0.5) 
            print("Downloading IMAGE:\n" +match["node"]["display_url"])
            filename = self.username + "/" + self.jsondata.json()[self.apilabel]["user"]["edge_owner_to_timeline_media"]["edges"][i]["node"]["shortcode"] + ".jpg"
            try:
                if not os.path.exists(filename ):
                    urllib.request.urlretrieve(match["node"]["display_url"], filename)
                else:
                    print("file img "+ filename+ " downloaded")
            except urllib.error.HTTPError as e:
                print(str(e.code) + " Error")
            i = i + 1

    def download_videos(self):
        i = 0 
        if 'edge_felix_video_timeline' in self.jsondata.json()[self.apilabel]["user"]:
            for match in self.jsondata.json()[self.apilabel]["user"]["edge_felix_video_timeline"]["edges"]: 
                time.sleep(0.5) 
                print("Downloading VIDEO:\n" +match["node"]["video_url"])
                filename = self.username + "/" + self.jsondata.json()[self.apilabel]["user"]["edge_felix_video_timeline"]["edges"][i]["node"]["shortcode"] + ".mp4"
                try:
                    if not os.path.exists(filename ):
                        urllib.request.urlretrieve(match["node"]["video_url"], filename)
                    else:
                        print("file film: "+ filename+ " going to download")
                except urllib.error.HTTPError as e:
                    print(str(e.code) + " Can't download video")
                i = i + 1
 

try:
    user = Instagram_Downloader(INSTAGRAM_USERNAME)
    user.create_download_directory()
    user.get_jsondata_instagram()
    user.download_photos()
    user.download_videos()
    user.set_apilabel("data")
    user.read_resume_end_cursor_timeline_media()
    while True:
        time.sleep(5)
        user.get_jsondata_instagram()
        user.download_photos()
        user.download_videos()
        user.write_resume_end_cursor_timeline_media()
        if user.has_next_page() == False:
            user.remove_resume_file()
            print("\n\n all post from "+INSTAGRAM_USERNAME+" downloaded")
            break
except:
    print("Downloaded")
    