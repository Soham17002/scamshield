from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from database import init_db, add_scan, get_scans, delete_scan, clear_scans, stats
from url_analyzer import analyze_url
from message_analyzer import analyze_message
from email_analyzer import analyze_email
from ai_assistant import ask_shield

BASE_DIR = Path(__file__).resolve().parent
LOGO_MARK = BASE_DIR / 'screenshots' / 'scamshield-mark.png'

st.set_page_config(page_title='SCAMSHIELD | Cybersecurity Intelligence', page_icon=str(LOGO_MARK), layout='wide', initial_sidebar_state='expanded')
init_db()

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root { --bg:#080d18; --panel:#111b2e; --muted:#94a3b8; --green:#00d68f; --cyan:#38bdf8; }
html, body, [class*="css"] {font-family:Inter,sans-serif;}
.stApp {background:radial-gradient(ellipse at 75% 0%,rgba(0,214,143,.09),transparent 34%),#080d18;color:#f8fafc;}
section[data-testid="stSidebar"] {background:linear-gradient(180deg,#091321 0%,#080f1c 100%);border-right:1px solid rgba(148,163,184,.13)}
/* Sidebar navigation: restrained inactive state and a clear emerald active state. */
section[data-testid="stSidebar"] div.stButton > button {
    min-height:44px;
    height:44px;
    justify-content:flex-start;
    text-align:left;
    padding:0 14px;
    margin:3px 0;
    border-radius:11px;
    background:transparent !important;
    color:#a9b8ca !important;
    border:1px solid transparent !important;
    box-shadow:none !important;
    font-size:.91rem;
    font-weight:550;
    transition:background .18s ease,border-color .18s ease,color .18s ease,transform .18s ease;
}
section[data-testid="stSidebar"] div.stButton > button:hover {
    background:rgba(56,189,248,.08) !important;
    color:#f8fafc !important;
    border-color:rgba(56,189,248,.18) !important;
    transform:translateX(2px);
}
section[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
    background:linear-gradient(100deg,rgba(0,214,143,.20),rgba(0,214,143,.08)) !important;
    color:#54f2bf !important;
    border:1px solid rgba(0,214,143,.30) !important;
    box-shadow:inset 3px 0 0 #00d68f,0 5px 18px rgba(0,0,0,.12) !important;
    font-weight:700;
}
section[data-testid="stSidebar"] div.stButton > button[kind="primary"]:hover {
    background:rgba(0,214,143,.22) !important;
    color:#8fffd5 !important;
}
section[data-testid="stSidebar"] div.stButton > button [data-testid="stIconMaterial"] {
    color:inherit !important;
    font-size:19px !important;
}
.block-container {padding-top:1.5rem;padding-bottom:2rem;max-width:1500px}
@keyframes ss-fade-up {from{opacity:0;transform:translateY(9px)}to{opacity:1;transform:translateY(0)}}
@keyframes ss-scan {0%{background-position:0% 50%}100%{background-position:200% 50%}}
.main .block-container {animation:ss-fade-up .35s ease both}
.panel,.hero,div[data-testid="stMetric"] {animation:ss-fade-up .4s ease both}
.stButton>button:focus-visible,input:focus-visible,textarea:focus-visible {outline:2px solid #38bdf8!important;outline-offset:2px!important}
div[data-testid="stProgress"] > div > div {background:linear-gradient(90deg,#00b982,#38bdf8,#00b982);background-size:200% 100%;animation:ss-scan 3s linear infinite}
@media (max-width:760px) {
 .block-container {padding:1rem .8rem 1.5rem}
 .hero {padding:24px 18px}
 .hero h1 {font-size:2rem}
 .panel {padding:15px}
 section[data-testid="stSidebar"] div.stButton > button {min-height:42px;height:42px}
}
@media (prefers-reduced-motion: reduce) {
 *,*::before,*::after {animation-duration:.01ms!important;animation-iteration-count:1!important;scroll-behavior:auto!important;transition-duration:.01ms!important}
}
div[data-testid="stMetric"] {background:linear-gradient(145deg,#142139,#0e1728);border:1px solid #26364d;padding:17px;border-radius:15px;box-shadow:0 8px 28px #0002}
div[data-testid="stMetricLabel"] p {color:#94a3b8!important}
div[data-testid="stMetricValue"] {color:#f8fafc!important}
.stButton>button {border-radius:10px;border:1px solid #24536a;background:linear-gradient(100deg,#00bd83,#00d6a0);color:#04131a;font-weight:700;min-height:42px;transition:.2s}
.stButton>button:hover {transform:translateY(-2px);box-shadow:0 8px 24px #00d68f33;border-color:#00e6a0}
.stTextInput input,.stTextArea textarea,.stSelectbox div[data-baseweb="select"] {background:#0d1728!important;color:#f8fafc!important;border-color:#31445d!important;border-radius:10px!important}
div[data-testid="stTabs"] button {color:#a9b8ca}
hr {border-color:#26364d}
.hero {padding:35px 32px;border:1px solid #164b50;border-radius:22px;background:radial-gradient(circle at 78% 50%,#064d494d,transparent 33%),linear-gradient(120deg,#0c1b2b,#081321);margin-bottom:22px;position:relative;overflow:hidden}
.hero h1 {font-size:clamp(2.2rem,4vw,3.5rem);line-height:1.08;margin:12px 0;color:#f8fafc;font-weight:800;max-width:680px}
.hero p {color:#b6c5d6;max-width:650px;font-size:1.02rem}
.pill {display:inline-block;background:#003d36;color:#4cf4c0;padding:6px 12px;border-radius:30px;font-size:.78rem;font-weight:700}
.panel {background:linear-gradient(145deg,#121e31,#0d1727);border:1px solid #26364d;border-radius:16px;padding:20px;margin-bottom:14px}
.small-muted {color:#94a3b8;font-size:.88rem}.glow {color:#00e5a0}.risk-high {color:#ff7777}.risk-medium {color:#ffc65b}.risk-low {color:#36e8b0}
div[data-testid="stDataFrame"] {border:1px solid #26364d;border-radius:12px;overflow:hidden}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

PAGES = ['Overview','URL Scanner','Message Scanner','Email Scanner','Shield AI','Scan History','Analytics','Threat Intelligence','Learn & Awareness','Settings']
if 'page' not in st.session_state: st.session_state.page='Overview'
if 'theme' not in st.session_state: st.session_state.theme='Dark'

with st.sidebar:
    logo_col, brand_col = st.columns([0.9, 3.4], vertical_alignment='center', gap='small')
    with logo_col:
        st.image(str(LOGO_MARK), width=52)
    with brand_col:
        st.markdown("<div style='font-size:21px;font-weight:850;letter-spacing:-.6px;color:#f8fafc;line-height:1.1'>SCAM<span style='color:#00d68f'>SHIELD</span></div><div style='font-size:10px;letter-spacing:1.1px;color:#94a3b8;margin-top:5px'>AI-POWERED SECURITY CENTER</div>", unsafe_allow_html=True)
    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
    nav_icons = {
        'Overview': ':material/dashboard:',
        'URL Scanner': ':material/link:',
        'Message Scanner': ':material/mark_email_unread:',
        'Email Scanner': ':material/mail:',
        'Shield AI': ':material/auto_awesome:',
        'Scan History': ':material/history:',
        'Analytics': ':material/monitoring:',
        'Threat Intelligence': ':material/gpp_maybe:',
        'Learn & Awareness': ':material/school:',
        'Settings': ':material/settings:',
    }
    for p in PAGES:
        active = st.session_state.page == p
        if st.button(
            p,
            key='nav_' + p,
            icon=nav_icons[p],
            type='primary' if active else 'secondary',
            use_container_width=True,
        ):
            st.session_state.page = p
            st.rerun()
    st.markdown('---')
    st.toggle('Reduce motion', key='reduce_motion', help='Turn off decorative movement and transitions.')
    st.markdown("<div class='small-muted'>SCAMSHIELD v1.1 · Local prototype<br>Built for safer digital habits</div>",unsafe_allow_html=True)
    if st.session_state.get('reduce_motion'):
        st.markdown("<style>*,*::before,*::after{animation:none!important;transition:none!important}</style>",unsafe_allow_html=True)

page=st.session_state.page

def heading(title, subtitle=''):
    st.markdown(f'<h1 style="font-size:2rem;margin-bottom:3px">{title}</h1><p class="small-muted">{subtitle}</p>',unsafe_allow_html=True)

def save_result(kind, source, result):
    add_scan(kind, source, result['score'], result['level'], result['summary'], result.get('indicators',[]))
    st.session_state.last_result=result

def result_view(r):
    color={'High Risk':'#ef4444','Medium Risk':'#f59e0b','Low Risk':'#00d68f'}.get(r['level'],'#38bdf8')
    st.markdown(f"<div class='panel' style='border-color:{color}66'><div style='color:{color};font-weight:800;font-size:1.1rem'>● {r['level']} · Risk score {r['score']}/100</div><h3>{r['summary']}</h3><div class='small-muted'>Heuristic assessment only — this is an estimate, not a guarantee of safety.</div></div>",unsafe_allow_html=True)
    st.progress(max(0,min(100,int(r.get('score',0))))/100, text=f"Estimated risk score: {r.get('score',0)}/100")
    a,b=st.columns(2)
    with a:
        st.markdown('**Detected indicators**')
        for x in r.get('indicators',[]): st.markdown(f'- ⚠️ {x}')
        if not r.get('indicators'): st.success('No obvious warning indicators were found by these checks.')
    with b:
        st.markdown('**Recommended actions**')
        for x in r.get('recommendations',[]): st.markdown(f'- {x}')
    if r.get('details'):
        with st.expander('Technical details'): st.json(r['details'])

if page=='Overview':
    st.markdown("<div class='hero'><span class='pill'>✦ AI-POWERED CYBERSECURITY</span><h1>Stay One Step Ahead<br>of Digital Scams.</h1><p>AI-assisted security checks that help you identify suspicious URLs, phishing messages, and scam emails before they become a problem.</p></div>",unsafe_allow_html=True)
    s=stats(); cols=st.columns(4)
    for c,(label,val,delta) in zip(cols,[('Total Scans',s['total'],'Saved in this browser session database'),('High Risk',s['high'],'Scans flagged high risk'),('Medium Risk',s['medium'],'Scans needing caution'),('Low Risk',s['low'],'Lower-risk results')]):
        c.metric(label,val,help=delta)
    l,r=st.columns([1.15,1])
    with l:
        st.markdown('<div class="panel"><h3>Quick security scan</h3><p class="small-muted">Choose a scanner to inspect a suspicious item.</p></div>',unsafe_allow_html=True)
        x,y,z=st.columns(3)
        for c,p in zip([x,y,z],['URL Scanner','Message Scanner','Email Scanner']):
            if c.button(p, use_container_width=True): st.session_state.page=p; st.rerun()
    with r:
        st.markdown('<div class="panel"><h3>Security reminder</h3><p>Never share OTPs, passwords, UPI PINs or recovery codes. Open your bank or service through its official app instead of links in unexpected messages.</p></div>',unsafe_allow_html=True)
    scans=get_scans(8)
    st.subheader('Recent scans')
    if scans: st.dataframe(pd.DataFrame(scans)[['created_at','scan_type','input_summary','risk_score','result']],use_container_width=True,hide_index=True)
    else: st.info('Your scan activity will appear here after your first scan.')

elif page=='URL Scanner':
    heading('URL Scanner','Inspect a website address without opening it. SCAMSHIELD never visits submitted links.')
    if st.button('Load safe test example',icon=':material/science:'):
        st.session_state['url_field']='https://example.com'
    url=st.text_input('Website URL',key='url_field',placeholder='https://example.com',help='Paste a URL or enter a domain. The scanner analyses its text only.')
    c1,c2=st.columns([1,4])
    if c1.button('Clear URL',icon=':material/backspace:'):
        st.session_state['url_field']=''
        st.session_state.pop('last_result',None)
        st.rerun()
    if c2.button('Scan URL',type='primary',icon=':material/travel_explore:',use_container_width=True):
        with st.spinner('Inspecting URL patterns…'):
            r=analyze_url(url)
        if r.get('error'): st.error(r['error'])
        else: save_result('URL',url,r)
    if st.session_state.get('last_result') and st.session_state.last_result.get('type')=='URL':
        result_view(st.session_state.last_result)
    st.markdown('<div class="panel"><h3>How it works</h3><p class="small-muted">Enter URL → inspect domain structure and warning patterns → review an explainable risk estimate. SCAMSHIELD never visits the submitted address.</p></div>',unsafe_allow_html=True)

elif page=='Message Scanner':
    heading('Message Scanner','Check SMS, chat messages and social media DMs for common scam signals.')
    example_message='URGENT: Your bank account will be blocked today. Verify your details at http://example.test and share your OTP.'
    c1,c2=st.columns(2)
    if c1.button('Load example message',icon=':material/science:'):
        st.session_state['message_field']=example_message
    if c2.button('Clear message',icon=':material/backspace:'):
        st.session_state['message_field']=''
        st.session_state.pop('last_result',None)
    with st.form('msg_form'):
        msg=st.text_area('Paste message',height=190,key='message_field',placeholder='Paste the suspicious message here…',max_chars=12000)
        st.caption(f'{len(msg)} / 12,000 characters')
        scan=st.form_submit_button('Scan Message',type='primary',icon=':material/shield:')
    if scan:
        with st.spinner('Checking message signals…'):
            r=analyze_message(msg)
        if r.get('error'): st.error(r['error'])
        else: save_result('Message',msg,r)
    if st.session_state.get('last_result') and st.session_state.last_result.get('type')=='Message':
        result_view(st.session_state.last_result)

elif page=='Email Scanner':
    heading('Email Scanner','Review sender details, subject and body for phishing indicators.')
    c1,c2=st.columns(2)
    if c1.button('Load example email',icon=':material/science:'):
        st.session_state['sender_field']='security-alert@example.test'
        st.session_state['subject_field']='Urgent: verify your account'
        st.session_state['email_body_field']='Your account will be suspended. Verify your details at https://example.test and provide your OTP.'
    if c2.button('Clear email',icon=':material/backspace:'):
        for key in ('sender_field','subject_field','email_body_field'):
            st.session_state[key]=''
        st.session_state.pop('last_result',None)
    with st.form('email_form'):
        sender=st.text_input('Sender email address',key='sender_field',placeholder='security@example.com')
        subject=st.text_input('Email subject',key='subject_field')
        body=st.text_area('Email body',height=180,key='email_body_field',max_chars=12000)
        st.caption(f'{len(subject)+len(body)} / 12,000 subject + body characters')
        scan=st.form_submit_button('Analyse Email',type='primary',icon=':material/mark_email_read:')
    if scan:
        with st.spinner('Reviewing email indicators…'):
            r=analyze_email(sender,subject,body)
        if r.get('error'): st.error(r['error'])
        else: save_result('Email',f'{sender} | {subject} | {body}',r)
    if st.session_state.get('last_result') and st.session_state.last_result.get('type')=='Email':
        result_view(st.session_state.last_result)

elif page=='Shield AI':
    heading('Shield AI','Ask questions about suspicious messages, links and safer online behaviour.')
    if 'chat' not in st.session_state: st.session_state.chat=[]
    for role,content in st.session_state.chat:
        with st.chat_message(role): st.markdown(content)
    prompt=st.chat_input('Ask Shield AI about cybersecurity…')
    if prompt:
        st.session_state.chat.append(('user',prompt))
        with st.chat_message('user'): st.markdown(prompt)
        with st.chat_message('assistant'):
            with st.spinner('Shield AI is thinking…'):
                answer=ask_shield(prompt)
            st.markdown(answer)
        st.session_state.chat.append(('assistant',answer))
    if st.button('Clear conversation',icon=':material/delete_sweep:'):
        st.session_state.chat=[]
        st.rerun()

elif page=='Scan History':
    heading('Scan History','Review, filter, export or delete locally saved scan records.')
    scans=get_scans(500)
    if scans:
        df=pd.DataFrame(scans)
        search=st.text_input('Search history',placeholder='Search type, date or input summary…')
        f1,f2=st.columns(2)
        types=f1.multiselect('Scan type',sorted(df.scan_type.unique()),default=sorted(df.scan_type.unique()))
        levels=f2.multiselect('Risk level',sorted(df.result.unique()),default=sorted(df.result.unique()))
        filtered=df[df.scan_type.isin(types)&df.result.isin(levels)].copy()
        if search.strip():
            mask=filtered.astype(str).apply(lambda col: col.str.contains(search.strip(),case=False,na=False)).any(axis=1)
            filtered=filtered[mask]
        filtered=filtered.sort_values('created_at',ascending=False)
        st.dataframe(filtered[['id','created_at','scan_type','input_summary','risk_score','result']],use_container_width=True,hide_index=True)
        st.download_button('Export filtered CSV',filtered.to_csv(index=False).encode(),file_name='scamshield_scan_history.csv',mime='text/csv',icon=':material/download:')
        ids=filtered.id.tolist()
        if ids:
            selected=st.selectbox('Select record to delete',ids,format_func=lambda i:f'#{i} · '+str(df.loc[df.id==i,'input_summary'].iloc[0])[:55])
            if st.button('Delete selected record',icon=':material/delete:'):
                delete_scan(selected); st.success('Record deleted.'); st.rerun()
        if st.button('Clear all scan history',icon=':material/delete_sweep:'): st.session_state.confirm_clear=True
        if st.session_state.get('confirm_clear'):
            st.warning('This permanently deletes all locally stored scan records.')
            a,b=st.columns(2)
            if a.button('Confirm delete all'): clear_scans(); st.session_state.confirm_clear=False; st.rerun()
            if b.button('Cancel'): st.session_state.confirm_clear=False; st.rerun()
    else: st.info('No scan records yet. Run a scan to populate your history.')

elif page=='Analytics':
    heading('Security Analytics','Insights based on your saved scan history. No fabricated activity is shown.')
    scans=get_scans(1000)
    if scans:
        df=pd.DataFrame(scans); a,b=st.columns(2)
        with a:
            fig=px.pie(df,names='result',hole=.65,title='Risk distribution',color='result',color_discrete_map={'Low Risk':'#00d68f','Medium Risk':'#f59e0b','High Risk':'#ef4444'}); fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',font_color='#e2e8f0',transition_duration=450); st.plotly_chart(fig,use_container_width=True)
        with b:
            bytype=df.groupby('scan_type').size().reset_index(name='scans'); fig=px.bar(bytype,x='scan_type',y='scans',title='Scans by type',color_discrete_sequence=['#00d68f']); fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font_color='#e2e8f0',transition_duration=450); st.plotly_chart(fig,use_container_width=True)
        df['day']=pd.to_datetime(df.created_at).dt.date; daily=df.groupby('day').size().reset_index(name='scans'); fig=px.line(daily,x='day',y='scans',markers=True,title='Scan activity'); fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font_color='#e2e8f0',transition_duration=450); st.plotly_chart(fig,use_container_width=True)
    else: st.info('Analytics will appear after you complete scans. Charts are generated from stored records only.')

elif page=='Threat Intelligence':
    heading('Threat Intelligence','Educational indicators and scam patterns. This page does not claim to provide a live threat feed.')
    topics=[('Lookalike domains','Attackers register domains that resemble banks, delivery companies or popular platforms. Check the exact spelling and registered domain.'),('Urgency and pressure','Messages that threaten account closure, legal action or immediate loss try to rush you into unsafe actions.'),('Credential harvesting','Unexpected pages asking for passwords, OTPs, card PINs or recovery codes are dangerous warning signs.'),('UPI collect requests','Never approve an unexpected collect request or enter your UPI PIN to receive money.'),('Shortened links','Short links hide their destination. Verify the destination through a trusted channel before interacting.')]
    for title,body in topics:
        with st.expander(title): st.write(body)
    st.caption('External live threat feeds are not connected in this build. Content above is general cybersecurity education.')

elif page=='Learn & Awareness':
    heading('Learn Cybersecurity','Short practical guides to safer digital habits.')
    guides=[('What is phishing?','Phishing is a deceptive attempt to make you reveal information or click a harmful link. Verify requests independently and inspect the sender and domain.'),('UPI & payment scams','A UPI PIN authorises a payment; it is not required to receive money. Reject unexpected collect requests and verify beneficiaries.'),('Email security','Check the full sender address, unexpected attachments, links and unusual payment instructions. Confirm sensitive requests using a known contact method.'),('Password security','Use unique passwords, a password manager and multi-factor authentication. Never reuse your banking password.'),('Social engineering','Scammers exploit trust, fear, urgency and authority. Pause and verify before sending money or sharing information.'),('Safe browsing','Keep software updated, use official app stores, check domain spelling and avoid entering credentials after following unsolicited links.')]
    cols=st.columns(2)
    for i,(title,body) in enumerate(guides):
        with cols[i%2]:
            with st.expander('📘 '+title): st.write(body)

elif page=='Settings':
    heading('Settings','Manage local data and optional AI configuration.')
    st.markdown('<div class="panel"><h3>AI configuration</h3>Set GROQ_API_KEY as an environment variable or Streamlit secret. The key is read only by the backend and must never be placed in frontend code.</div>',unsafe_allow_html=True)
    st.code('GROQ_API_KEY=your_key_here\nGROQ_MODEL=llama-3.3-70b-versatile',language='bash')
    st.markdown('**Data & privacy**')
    st.write('Scan history is stored in a local SQLite database. Message and email contents are reduced to short summaries before storage.')
    if st.button('Delete all local scan data'): st.session_state.confirm_settings=True
    if st.session_state.get('confirm_settings'):
        st.warning('This action cannot be undone.')
        a,b=st.columns(2)
        if a.button('Yes, permanently delete data',type='primary',icon=':material/delete_forever:'):
            clear_scans(); st.session_state.confirm_settings=False; st.success('Local scan history deleted.'); st.rerun()
        if b.button('Cancel'):
            st.session_state.confirm_settings=False
            st.rerun()
    st.markdown('**About SCAMSHIELD**')
    st.write('A student cybersecurity project prototype. Risk results are heuristic estimates and should not be treated as verified threat intelligence.')

st.markdown('<hr><div class="small-muted" style="text-align:center">SCAMSHIELD · Stay alert. Verify independently. Stay safe.</div>',unsafe_allow_html=True)
