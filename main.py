from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
  headers = {
      'authority': 'www.barchart.com',
      'accept': 'application/json',
      'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
      'referer': 'https://www.barchart.com/futures/quotes/CL*0/futures-prices?timeFrame=daily&page=all',
      'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
  }

  params = {
      'symbolType': '1',
      'symbolCode': 'STK',
      'hasOptions': '0',
  }

  response = requests.get(
      f'https://www.barchart.com/symbols/$SPX/modules/dashboard',
      params=params,
      headers=headers,
  )
  xsrf = response.cookies.get(name='XSRF-TOKEN')
  laravel_token = response.cookies.get(name='laravel_token')
  laravel_session = response.cookies.get(name='laravel_session')
  market = response.cookies.get(name='market')
  keys = {'xsrf':xsrf, 'laravel_token':laravel_token, 'laravel_session':laravel_session, 'market':market}
  return keys

  cookies = {
      'laravel_token': laravel_token,
      'laravel_session': laravel_session,
  }

  headers = {
      'authority': 'www.barchart.com',
      'accept': '*/*',
      'accept-language': 'en-US,en;q=0.9',
      'referer': 'https://www.barchart.com/futures/quotes/CA*0/futures-prices',
      'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
      'x-xsrf-token': xsrf.replace('%3D','=')
  }

  params = {
      'symbol': symbol,
      'data': 'daily',
      'maxrecords': '10000',
      'volume': 'contract',
      'order': 'asc',
      'dividends': 'false',
      'backadjust': 'false',
      'daystoexpiration': '1',
      'contractroll': 'expiration',
  }

  response = requests.get(
      'https://www.barchart.com/proxies/timeseries/queryeod.ashx',
      params=params,
      cookies=cookies,
      headers=headers,
  )
  data = pd.DataFrame([i.split(',') for i in response.text.split('\n')][:-2], columns = ['symbol', 'date', 'open', 'high', 'low', 'close', 'volume', 'open_interst'])
  return data
