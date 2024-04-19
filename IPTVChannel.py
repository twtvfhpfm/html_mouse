import requests

class ChannelInfo:
    def __init__(self, name, url):
        self.name = name
        self.url = url

class IPTVChannel:
    def __init__(self):
        self.channels = []
        self.cursor = 0

    def getChannels(self, src):
        self.channels = []
        try:
            print("get channels from ", src)
            resp = requests.get(src)
            print("get success")
            lines = resp.content.decode('utf-8').splitlines()
            print("channels lines: ", len(lines))
            for i in range(len(lines)):
                print("line: ", lines[i])
                idx = lines[i].find("tvg-name=\"")
                if idx != -1:
                    print("find tvg-name")
                    start_idx = idx + 10
                    end_idx = lines[i].find('"', start_idx)
                    if end_idx != -1:
                        print("find end idx")
                        name = lines[i][start_idx:end_idx]
                        if lines[i+1].find('http') == 0:
                            print("find http in next line")
                            self.channels.append(ChannelInfo(name, lines[i+1]))
        except Exception as e:
            print(e)
            pass

    def next(self):
        self.cursor = (self.cursor + 1) % len(self.channels)
        return self.channels[self.cursor].url

    def prev(self):
        self.cursor = (self.cursor - 1 + len(self.channels)) % len(self.channels)
        return self.channels[self.cursor].url

    def get(self, idx):
        self.cursor = idx
        return self.channels[self.cursor].url


