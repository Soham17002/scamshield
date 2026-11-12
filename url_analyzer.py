import re, ipaddress
from urllib.parse import urlparse

SHORTENERS={'bit.ly','tinyurl.com','t.co','goo.gl','ow.ly','is.gd','buff.ly','cutt.ly'}
KEYWORDS={'login','verify','secure','account','update','bank','wallet','password','otp','payment','gift','free','claim','refund','support'}

def analyze_url(value):
    value=(value if isinstance(value, str) else '').strip()
    if not value: return {'error':'Please enter a URL.'}
    if len(value)>2048: return {'error':'URL is too long (maximum 2,048 characters).'}
    if any(ch.isspace() for ch in value): return {'error':'URL cannot contain spaces.'}
    if re.match(r'^[a-z][a-z0-9+.-]*://', value, re.I) and not re.match(r'^https?://', value, re.I):
        return {'error':'Only HTTP and HTTPS website URLs are supported.'}
    candidate=value if re.match(r'^https?://',value,re.I) else 'http://'+value
    try:
        p=urlparse(candidate); host=p.hostname
        port=p.port  # Accessing .port validates its syntax and legal range.
        if not host or '.' not in host: return {'error':'Enter a valid website address, such as example.com.'}
    except (ValueError, TypeError): return {'error':'The URL contains an invalid hostname or port.'}
    except Exception: return {'error':'Could not parse this URL.'}
    points=0; indicators=[]; low=host.lower()
    if p.username is not None or p.password is not None:
        points+=15; indicators.append('The URL contains embedded username or password information.')
    try: ipaddress.ip_address(host); points+=30; indicators.append('The address uses a raw IP address instead of a domain name.')
    except ValueError: pass
    if p.scheme!='https': points+=12; indicators.append('The URL does not use HTTPS.')
    if len(value)>100: points+=8; indicators.append('The URL is unusually long.')
    if low.count('.')>=3: points+=10; indicators.append('The hostname contains several subdomain levels.')
    if '@' in p.netloc: points+=18; indicators.append('The URL contains an @ symbol in its authority section.')
    if '-' in low: points+=5; indicators.append('The domain contains hyphens; inspect spelling carefully.')
    if host.lower() in SHORTENERS: points+=15; indicators.append('The domain is a known URL-shortening service, so the destination is obscured.')
    hits=sorted(k for k in KEYWORDS if k in (low+p.path+p.query).lower())
    if hits: points+=min(25,5*len(hits)); indicators.append('Security-sensitive or incentive keywords appear: '+', '.join(hits)+'.')
    if re.search(r'%[0-9a-f]{2}',value,re.I): points+=5; indicators.append('The URL contains encoded characters.')
    score=min(100,points); level='High Risk' if score>=70 else 'Medium Risk' if score>=30 else 'Low Risk'
    return {'type':'URL','score':score,'level':level,'summary':f'URL pattern analysis found {len(indicators)} warning indicator(s).','indicators':indicators,'recommendations':['Do not enter passwords, OTPs or payment details unless you independently verify the site.','Open the organisation through its official app or a manually typed trusted address.','If this link arrived unexpectedly, verify it with the sender using another channel.'],'details':{'hostname':host,'scheme':p.scheme,'url_length':len(value),'subdomain_count':max(0,len(host.split('.'))-2),'https':p.scheme=='https','heuristic_version':'1.0'}}
