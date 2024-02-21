import asyncio
import requests
import random

word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

response = requests.get(word_site)
WORDS = response.content.decode('utf-8').splitlines()

class asyncer():
    def __init__(self, oracle):
        self.oracle = oracle

    async def atalk(self):
        word = requests.get(self.oracle)
        return word.content.decode('utf-8')

async def main():
    asyncers = [asyncer('http://127.0.0.1:5000/random-word') for i in range(10)]
    
    res = await asyncio.gather(*[a.atalk() for a in asyncers])
    print(res)

    
if __name__=='__main__':
    asyncio.run(main())