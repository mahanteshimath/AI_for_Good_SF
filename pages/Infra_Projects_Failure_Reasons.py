import streamlit as st

# Apply Custom CSS
st.markdown("""
    <style>
        body {
            background-color: #f5f5f5;
            font-family: 'Arial', sans-serif;
            color: #333;
        }
        .main-title {
            color: #0D6EFD;
            font-size: 3rem;
            text-align: center;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .section-header {
            color: #1F618D;
            font-size: 2.4rem;
            font-weight: bold;
            border-bottom: 2px solid #1F618D;
            padding-bottom: 10px;
            margin-top: 30px;
            margin-bottom: 10px;
        }
        .markdown-text {
            font-size: 1.5rem;
            line-height: 1.6;
            font-weight: bold;
        }
        .footer {
            font-size: 0.9rem;
            color: #555;
            text-align: center;
            margin-top: 50px;
        }
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown('<div class="main-title">What\'s wrong with India\'s Infrastructure?!!!</div>', unsafe_allow_html=True)

# Introduction Section
st.markdown('<div class="section-header">Introduction</div>', unsafe_allow_html=True)
st.markdown("""
<div class="markdown-text">
Explore India's infrastructure, including its strengths and weaknesses. Learn about common challenges 
such as contractual issues, structural flaws, safety audits, and accountability gaps.
</div>
""", unsafe_allow_html=True)

# Reason 1: Contractual Reasons
st.markdown('<div class="section-header">Reason 1: Contractual Reasons</div>', unsafe_allow_html=True)
st.markdown("""

- **Overview**: Administrative lapses and technical inefficiencies often lead to delays and failures in infrastructure projects. 
- **Examples**:
  - *Morbi Bridge Collapse*: A result of poor contractor selection and oversight.
  - *Kolkata Flyover Incident*: Revealed gaps in procurement policies and contractor accountability.
- **Key References**:
  - [The Wire](https://thewire.in/government/administrative-lapses-and-technical-incompetence-behind-morbi-bridge-collapse-sit-says)
  - [The Guardian](https://www.theguardian.com/world/2022/nov/01/gujarat-bridge-collapse-anger-grows-in-india-over-cover-up-claims)

""")

# Reason 2: Design and Structural Flaws
st.markdown('<div class="section-header">Reason 2: Design and Structural Flaws</div>', unsafe_allow_html=True)
st.markdown("""
- **Overview**: Poor design standards and subpar construction materials often lead to failures.
- **Examples**:
  - *Pragati Maidan Tunnel*: Leakage and surface bumps despite repairs.
  - *Bihar Bridge Collapse*: Highlighted severe design and construction flaws.
- **Key References**:
  - [Economic Times](https://economictimes.indiatimes.com/news/india/bihar-rs-1700-cr-under-construction-bridge-collapsed-within-seconds)
  - [India Today](https://www.indiatoday.in/cities/delhi/story/pragati-maidan-tunnel-seepage-serious-design-flaws-delhi-pwd-notice-larsen-toubro-2498978-2024-02-07)
""")

# Reason 3: Safety Audits
st.markdown('<div class="section-header">Reason 3: Safety Audits</div>', unsafe_allow_html=True)
st.markdown("""
- **Overview**: Lack of routine and rigorous safety audits has resulted in preventable accidents.
- **Examples**:
  - *Mumbai CST Bridge Collapse*: Declared fit for use but failed shortly after.
  - Other fatal incidents demonstrate the urgent need for transparent audit practices.
- **Key References**:
  - [NDTV](https://www.ndtv.com/mumbai-news/3-arrested-in-less-than-a-month-after-mumbai-bridge-collapse-killed-6-2016849)
  - [Business Today](https://www.businesstoday.in/latest/economy-politics/story/mumbai-cst-bridge-collapse-audit-report-foot-over-bridge-bmc-mumbai-cst-bridge-collapse-structural-audit-report-deemed-foot-overbridge-fit-to-use-six-months-ago-178097-2019-03-15)

""")

# Reason 4: Accountability
st.markdown('<div class="section-header">Reason 4: Accountability</div>', unsafe_allow_html=True)
st.markdown("""

- **Overview**: Lack of accountability in governance and maintenance exacerbates infrastructure challenges.
- **Examples**:
  - *Morbi Bridge Incident*: Highlighted systemic corruption and governance failures.
  - *Delayed Accountability*: Maintenance neglect often leads to fatal outcomes.
- **Key References**:
  - [Times of India](https://timesofindia.indiatimes.com/city/ahmedabad/court-demands-accountability-for-maintenance-of-bridges/articleshow/98109045.cms)
  - [The Guardian](https://www.theguardian.com/world/2022/oct/31/indian-police-arrest-nine-people-after-footbridge-collapse-kills-at-least-134)

""")

# Conclusion
st.markdown('<div class="section-header">Conclusion</div>', unsafe_allow_html=True)
st.markdown("""
India’s infrastructure holds immense potential, but recurring issues in design, execution, and accountability hinder progress. 
Addressing these challenges with transparency, stricter audits, and improved governance can lead to safer and more reliable infrastructure.
""")

# Footer
st.markdown('<div class="footer">**Sources:** Compiled from trusted publications such as The Wire, NDTV, Business Today, and The Guardian.</div>', unsafe_allow_html=True)



st.markdown(
    '''
    <style>
    .streamlit-expanderHeader {
        background-color: blue;
        color: white; # Adjust this for expander header color
    }
    .streamlit-expanderContent {
        background-color: blue;
        color: white; # Expander content color
    }
    </style>
    ''',
    unsafe_allow_html=True
)

footer="""<style>

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: #2C1E5B;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with ❤️ by <a style='display: inline; text-align: center;' href="https://www.linkedin.com/in/mahantesh-hiremath/" target="_blank">MAHANTESH HIREMATH</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True) 