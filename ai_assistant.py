import os

def ask_shield(prompt):
    key=os.getenv('GROQ_API_KEY')
    try:
        import streamlit as st
        key=key or st.secrets.get('GROQ_API_KEY','')
    except Exception: pass
    if not key:
        return ('**AI connection is not configured yet.** Add `GROQ_API_KEY` to your environment or Streamlit secrets to enable live responses.\n\nIn the meantime: never share an OTP, password, UPI PIN or recovery code. Verify suspicious requests using the organisation’s official app or a contact method you already trust.')
    try:
        from groq import Groq
        client=Groq(api_key=key)
        model=os.getenv('GROQ_MODEL','llama-3.3-70b-versatile')
        response=client.chat.completions.create(model=model,temperature=0.3,max_tokens=700,messages=[{'role':'system','content':'You are Shield AI, a careful cybersecurity education assistant. Do not ask for passwords, OTPs, PINs, API keys or secrets. Do not claim certainty without evidence. Clearly distinguish warning signs from verified facts. Keep answers practical.'},{'role':'user','content':prompt}])
        return response.choices[0].message.content
    except Exception as e:
        return f'**AI service unavailable.** Check your GROQ_API_KEY, model name and network connection.\n\nFallback safety advice: do not click unexpected links or share authentication codes. (Technical detail: {type(e).__name__})'
