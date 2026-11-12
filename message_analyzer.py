import re
PATTERNS={
 'Urgent or threatening language':r'urgent|immediately|act now|within \d+ hours?|account.{0,20}(suspend|block|closed)|legal action|final warning',
 'OTP or password request':r'\b(otp|one.?time password|password|pin|cvv|passcode)\b',
 'Payment or money pressure':r'pay now|transfer (money|funds)|upi pin|collect request|payment pending|refund fee|processing fee',
 'Prize or reward bait':r'you (have )?won|lottery|prize|claim.{0,20}(reward|cash|gift)|free gift',
 'Suspicious link':r'https?://\S+|www\.\S+',
 'Impersonation language':r'bank support|customer care|verify your account|kyc update|income tax|parcel held|delivery failed'
}
def analyze_message(text):
    text=(text if isinstance(text, str) else '').strip()
    if len(text)<8: return {'error':'Paste a message with at least 8 characters.'}
    if len(text)>12000: return {'error':'Message is too long (maximum 12,000 characters).'}
    hits=[name for name,pat in PATTERNS.items() if re.search(pat,text,re.I)]
    score=min(100,len(hits)*17 + (12 if re.search(r'http[s]?://',text,re.I) else 0))
    level='High Risk' if score>=70 else 'Medium Risk' if score>=30 else 'Low Risk'
    return {'type':'Message','score':score,'level':level,'summary':f'Message screening detected {len(hits)} common scam signal(s).','indicators':hits,'recommendations':['Do not reply with passwords, OTPs, PINs or personal documents.','Do not open unexpected links or attachments.','Verify the request through the organisation’s official app or a known phone number.'],'details':{'character_count':len(text),'links_found':len(re.findall(r'https?://\S+',text,re.I)),'checks':'Pattern-based screening; not a trained classifier'}}
