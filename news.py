import json, os, re, html, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from pathlib import Path

KST = timezone(timedelta(hours=9))
CATEGORIES = {
 '반도체': '반도체 HBM SK하이닉스 삼성전자',
 '국내 주식': '코스피 코스닥 증시',
 '미국 주식': '미국 증시 나스닥 S&P500',
 '경제': '한국 경제 금리 환율',
 'AI 기술': '인공지능 AI 기술 데이터센터',
}
HEADERS = {'User-Agent':'Mozilla/5.0 (compatible; MyDailyNews/1.0)'}

def fetch(query, limit=8):
    params = urllib.parse.urlencode({'q':query, 'hl':'ko', 'gl':'KR', 'ceid':'KR:ko'})
    url = 'https://news.google.com/rss/search?' + params
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as resp:
        root = ET.fromstring(resp.read())
    articles=[]
    for item in root.findall('./channel/item')[:limit]:
        title = html.unescape(item.findtext('title','')).strip()
        link = item.findtext('link','').strip()
        source = item.findtext('source','').strip()
        date = item.findtext('pubDate','').strip()
        if title and link.startswith('https://'):
            articles.append({'title':title, 'url':link, 'source':source, 'published':date})
    return articles

def main():
    now = datetime.now(KST)
    seen=set(); groups={}; errors={}
    for category, query in CATEGORIES.items():
        try:
            entries=fetch(query)
        except Exception as exc:
            errors[category]=str(exc)
            entries=[]
        groups[category]=[]
        for article in entries:
            normalized=re.sub(r'\W+','',article['title'].lower())
            if normalized in seen: continue
            seen.add(normalized)
            groups[category].append(article)
    payload={'updated_at':now.isoformat(timespec='seconds'), 'categories':groups, 'errors':errors}
    Path('docs').mkdir(exist_ok=True)
    Path('docs/news.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Collected:', {k:len(v) for k,v in groups.items()})
    if not any(groups.values()):
        raise RuntimeError('No news collected. Telegram send skipped.')
    token=os.environ.get('TELEGRAM_BOT_TOKEN','').strip()
    chat=os.environ.get('TELEGRAM_CHAT_ID','').strip()
    if token and chat:
        lines=[f'🗞️ My Daily News | {now:%Y-%m-%d} 08:00 KST','']
        for category, entries in groups.items():
            lines.append(f'【{category}】')
            for article in entries[:2]:
                lines.append('• '+article['title'][:110])
                lines.append(article['url'])
            lines.append('')
        message='\n'.join(lines)
        # Telegram sendMessage maximum text length: split by category for safety.
        for start in range(0,len(message),3500):
            body=urllib.parse.urlencode({'chat_id':chat,'text':message[start:start+3500]}).encode()
            request=urllib.request.Request(f'https://api.telegram.org/bot{token}/sendMessage',data=body)
            with urllib.request.urlopen(request,timeout=20) as response:
                response.read()
        print('Telegram sent')
    else:
        print('Telegram secrets absent: skipping send')

if __name__=='__main__': main()
