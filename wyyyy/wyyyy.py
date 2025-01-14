from redbot.core import commands
from redbot.cogs import audio
from json import loads
import json
import base64
import requests
import re
from Crypto.Cipher import AES
class Wyyyy(commands.Cog):
	"""Play song by netease music links!"""
	@commands.command()
	async def wyy(self, ctx, *, sharelink: str):
		"""Play a netease music share link."""
		rid = None
		if "song?" in sharelink:
			rid = re.search(r'\?id=(\d*)', sharelink)
		elif "song/" in sharelink:
			rid = re.search(r'song/(\d*)/', sharelink)
		else:
			await ctx.send("This is not a song link!")
		if rid:
			song_id = re.search(r'\d+',str(rid.group()))
			nonce = "0CoJUm6Qyw8W8jud"
			def AES_encrypt(text, key, iv):
				pad = 16 - len(text) % 16
				text = text + pad * chr(pad)
				text = text.encode("utf-8")
				encryptor = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
				encrypt_text = encryptor.encrypt(text)
				encrypt_text = base64.b64encode(encrypt_text)
				return encrypt_text.decode('utf-8')
			def asrsea(p1, p2):
				res = {}
				rand_num = "OFnV5T4hXEx90wxi" 
				vi = b"0102030405060708"
				h_encText = AES_encrypt(p1, p2, vi)
				h_encText = AES_encrypt(h_encText, rand_num, vi)
				res["encText"] = h_encText
				res["encSecKey"] = "6b2e91bfea2fff78e82f13d16405c8ba0bd54af4076218463931b5ebfdb177f61ee9fe3db8566edb19cc5a5badd0d2cd1435553c6caa40f39e45c35e0957ec67e3ad36e074b6ee0224083b17d96fb734fdc6d11d42ea8d1c71cdd170f9d93dd98c7cb22624e8765bbd93ffc1a98b834bc86d847a229241b8f3750571cf199621"
				return res
			req = json.dumps({
				"ids": [song_id.group()],
				"br": 999000,
				"csrf_token": '',
			})
			#await ctx.send(req)
			asrsea_res = asrsea(req, nonce)
			param_data = {
				"params": asrsea_res["encText"],
				"encSecKey": asrsea_res["encSecKey"]
			}
			headers = {
				"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0",
				"Content-Type": "application/x-www-form-urlencoded",
				"Origin": "http://music.163.com",
				"Referer": "https://music.163.com",
				"Host": "music.163.com",
				"X-Real-IP": "27.38.4.87"
			}
			cookies = {"os": "ios"}
			songapi = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
			r = requests.post(songapi, headers=headers, data=param_data, verify=False, cookies=cookies)
			url_best = re.search(r'http.*\.mp3',r.text).group()
			play = ctx.bot.get_command("play")
			await ctx.invoke(play, query = url_best)
		else:
			await ctx.send("Can't find song id!")
