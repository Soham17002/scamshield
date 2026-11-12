import re
from message_analyzer import analyze_message

def analyze_email(sender,subject,body):
    sender = sender if isinstance(sender, str) else ''
    subject = subject if isinstance(subject, str) else ''
    body = body if isinstance(body, str) else ''
    if not sender.strip() or not re.fullmatch(r'[^\s@]+@[^\s@.]+(?:\.[^\s@.]+)+', sender.strip()):
        return {'error':'Enter a valid sender email address.'}
    if len(subject)+len(body)>12000: return {'error':'Email content is too long (maximum 12,000 characters).'}
    if not subject.strip() and not body.strip(): return {'error':'Enter an email subject or body.'}
    base=analyze_message((subject+'\n'+body).strip() or 'Email with no content')
    if base.get('error'): base={'score':0,'level':'Low Risk','indicators':[],'recommendations':[],'summary':''}
    domain=sender.split('@')[-1].lower(); indicators=list(base['indicators']); score=base['score']
    if re.search(r'\d{4,}|[._-]{2,}',sender.split('@')[0]): score+=8; indicators.append('Sender name contains unusual number or punctuation patterns.')
    common_free={'gmail.com','outlook.com','yahoo.com','hotmail.com','icloud.com'}
    if domain in common_free: indicators.append('Sender uses a common consumer email provider; this alone is not suspicious.')
    score=min(100,score); level='High Risk' if score>=70 else 'Medium Risk' if score>=30 else 'Low Risk'
    return {'type':'Email','score':score,'level':level,'summary':f'Email content and sender-format screening found {len(indicators)} note(s).','indicators':indicators,'recommendations':['Check the sender address character by character.','Confirm payment or account requests through a known official channel.','Do not open unexpected attachments or provide credentials.'],'details':{'sender_domain':domain,'subject_length':len(subject),'body_length':len(body),'authentication':'SPF, DKIM and DMARC were not checked.'}}
