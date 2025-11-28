import requests, re, os, sys
from urllib.request import urlopen

def clear(): os.system('cls' if 'win' in sys.platform.lower() else 'clear')

def Author():
    print('__________.__        __                                 _        ')
    print('\______   \__| _____/  |_  ___________   ____   _______/  |_     ')
    print(' |     ___/  |/    \   __\/ __ \_  __ \_/ __ \ /  ___/\   __\    ')
    print(' |    |   |  |   |  \  | \  ___/|  | \/\  ___/ \___ \  |  |      ')
    print(' |____|   |__|___|  /__|  \_____>__|    \___  >____  > |__|      ')
    print('                  \/                        \/     \/            ')
    print('                            Downloader                           ')
    print('                         Coded By Obod Star                      ')
    print('                                                                 ')

class Pinterest:
    def __init__(self):
        self.ses   = requests.Session()
        self.pinid = []
        self.loop  = 0
        self.ok    = 0
        
    def GetID(self, url):
        try:
            headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language': 'en-US,en;q=0.9,id;q=0.8','cache-control': 'max-age=0','priority': 'u=0, i','sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"','sec-ch-ua-full-version-list': '"Google Chrome";v="135.0.7049.115", "Not-A.Brand";v="8.0.0.0", "Chromium";v="135.0.7049.115"','sec-ch-ua-mobile': '?0','sec-ch-ua-model': '""','sec-ch-ua-platform': '"Windows"','sec-ch-ua-platform-version': '"19.0.0"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'same-origin','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'}
            response = self.ses.get(url=url, headers=headers).text
            self.cookies = "; ".join([key+"="+value.replace('"','') for key, value in self.ses.cookies.get_dict().items()])
            self.csrftoken = re.search(r'csrftoken=(.*?);', str(self.cookies)).group(1)
            self.ImageID = re.search(r'"pinId":"(\d+)"', str(response)).group(1)
            entryid = re.search(r'"imageSpec_orig":{"url":"(.*?)"', str(response)).group(1)
            self.url_js = re.search(r'"https://s.pinimg.com/webapp/app-www-closeup-duplo-UnauthCloseupRelatedPins-(.*?)"', str(response)).group(1)
            self.pinid.append(entryid)
            self.loop +=1
            print('\r~ Mengumpulkan {} Foto '.format(self.loop), end='')
        except requests.exceptions.MissingSchema:
            print('')
            print('\r[*] Link Tidak Valid')
            exit()
        except requests.exceptions.ConnectionError:
            print('')
            print('\r[*] Koneksi Terputus')
            exit()
        except requests.exceptions.InvalidURL:
            print('')
            print('\r[*] Link Tidak Valid')
            exit()
        except requests.exceptions.ChunkedEncodingError:
            print('')
            print('\r[*] Koneksi Terputus')
            exit()
        except requests.exceptions.TooManyRedirects:
            print('')
            print('\r[*] Link Tidak Valid')
            exit()
        except requests.exceptions.Timeout:
            print('')
            print('\r[*] Koneksi Terputus')
            exit()
        except requests.exceptions.RequestException as e:
            print('')
            print('\r[*] Error: {}'.format(e))
            exit()
        except KeyboardInterrupt:
            exit()
            
    def GetHash(self):
        try:
            headers = {
                'Origin': 'https://id.pinterest.com',
                'sec-ch-ua-platform': '"Windows"',
                'Referer': 'https://id.pinterest.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
            }
            response = self.ses.get('https://s.pinimg.com/webapp/app-www-closeup-duplo-UnauthCloseupRelatedPins-{}'.format(self.url_js), cookies={'cookie': self.cookies}, headers=headers).text
            self.queryhash = re.findall(r'params:{id:"(.*?)",metadata', str(response))
            self.Dumps(queryhash=self.queryhash[1], nextpage=None)
        except KeyboardInterrupt:
            exit()

    def Dumps(self, queryhash, nextpage):
        headers = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9,id;q=0.8',
            'content-type': 'application/json',
            'origin': 'https://id.pinterest.com',
            'priority': 'u=1, i',
            'referer': 'https://id.pinterest.com/',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-full-version-list': '"Google Chrome";v="135.0.7049.115", "Not-A.Brand";v="8.0.0.0", "Chromium";v="135.0.7049.115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"19.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            'x-csrftoken': self.csrftoken,
            'x-pinterest-appstate': 'active',
            'x-pinterest-graphql-name': 'UnauthCloseupRelatedPinsFeedPaginationQuery',
            'x-pinterest-pws-handler': 'www/pin/[id].js',
            'x-pinterest-source-url': '/pin/{}/'.format(self.ImageID),
            'x-requested-with': 'XMLHttpRequest'
        }
        json_data = {
            'queryHash': queryhash,
            'variables': {
                'contextPinIds': None,
                'count': 50,
                'cursor': nextpage,
                'isAuth': False,
                'isDesktop': True,
                'pinId': self.ImageID,
                'searchQuery': None,
                'source': None,
                'topLevelSource': None,
                'topLevelSourceDepth': None,
            }
        }
        try:
            response = self.ses.post('https://id.pinterest.com/_/graphql/', cookies={'cookie': self.cookies}, headers=headers, json=json_data).text
            if 'upstream request timeout' in str(response):
                self.Dumps(queryhash=self.queryhash[0], nextpage=None)
            else:
                entryid = re.findall(r'"url":"https://i.pinimg.com/originals/(.*?)"', str(response))
                for x in entryid:
                    if x in self.pinid: continue
                    else:
                        self.loop +=1
                        self.pinid.append('https://i.pinimg.com/originals/'+x)
                        print('\r~ Mengumpulkan {} Foto '.format(self.loop), end='')
                hashpage = re.search(r'"hasNextPage":(.*?)}}', str(response)).group(1)
                if hashpage == 'true':
                    endcursor = re.search(r'"endCursor":"(.*?)"', str(response)).group(1)
                    self.Dumps(queryhash=self.queryhash[0], nextpage=endcursor)
                else:
                    print(f'\r[*] Berhasil Mengumpulkan {len(self.pinid)} Foto', end='')
                    self.Download_Foto()
        except (KeyboardInterrupt, AttributeError):
            print(f'\r[*] Berhasil Mengumpulkan {len(self.pinid)} Foto', end='')
            self.Download_Foto()
            
    def Download_Foto(self):
        try:
            path = 'D:\\belajar\osp-new\zfoto'
            os.makedirs(path, exist_ok=True)
            print('')
            total = int(input('[?] Berapa Jumlah Foto Yang Ingin Diunduh ? : '))
            print('')
            y = self.pinid[:total]
            for x in y:
                foto = urlopen(x).read()
                with open(f'{path}/{os.path.basename(x)}', 'wb') as r:
                    r.write(foto)
                r.close()
                self.ok +=1
                print('\r~ Berhasih Mengunduh {} Foto   '.format(self.ok), end='')
            print('\r[*] Berhasih Mengunduh {} Foto   '.format(self.ok), end='')
            print('')
            print('[*] Foto Tersimpan Di Folder {}   '.format(path), end='')
        except (KeyboardInterrupt, EOFError):
            print('')
            print('\r[*] Foto Tersimpan Di Folder {}   '.format(path))
            exit()
        except Exception as e:
            print('')
            print('\r[*] Error: {}'.format(e))
            exit()

if __name__ == '__main__':
    try:
        clear()
        Author()
        print()
        url = input('[?] Masukan Link Pinterest : ')
        print('')
        print('  Tekan CTRL + C Untuk Berhenti  ')
        print('')
        lo = Pinterest()
        lo.GetID(url=url)
        lo.GetHash()
    except KeyboardInterrupt: exit()


