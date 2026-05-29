CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
.main .block-container { padding: 1rem 2rem; max-width: 1400px; }
[data-testid="stSidebar"] { display: none !important; }
.top-banner {
    background: linear-gradient(135deg, #00c9a7, #00d4aa, #45e0c0);
    border-radius: 18px; padding: 1.5rem 2.5rem; margin-bottom: 1.5rem;
    display: flex; justify-content: space-between; align-items: center;
    box-shadow: 0 8px 32px rgba(0,201,167,0.25);
}
.top-banner h2 { color: #0a0e17; margin: 0; font-weight: 700; font-size: 1.6rem; }
.mongo-badge {
    background: rgba(255,255,255,0.85); color: #0a0e17; padding: 6px 18px;
    border-radius: 20px; font-size: 0.85rem; font-weight: 600;
}
.stat-card {
    background: linear-gradient(135deg, #111827, #1a2332);
    border: 1px solid rgba(0,201,167,0.15); border-radius: 14px;
    padding: 1.2rem 0.8rem; text-align: center;
    border-bottom: 3px solid #00c9a7;
    transition: transform 0.3s, box-shadow 0.3s;
}
.stat-card:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0,201,167,0.2); }
.stat-number {
    font-size: 2.2rem; font-weight: 700; color: #00c9a7;
}
.stat-label {
    color: #6b7b8d; font-size: 0.75rem; text-transform: uppercase;
    letter-spacing: 1.5px; margin-top: 4px;
}
.success-toast { padding: 1rem; border-radius: 10px; background: linear-gradient(135deg, #00b894, #00cec9);
    color: white; font-weight: 500; animation: slideIn 0.5s ease; }
.error-toast { padding: 1rem; border-radius: 10px; background: linear-gradient(135deg, #e17055, #d63031);
    color: white; font-weight: 500; animation: slideIn 0.5s ease; }
.info-box {
    background: rgba(0,201,167,0.08); border: 1px solid rgba(0,201,167,0.25);
    border-radius: 12px; padding: 1.2rem; margin: 1rem 0;
}
.acid-card {
    background: linear-gradient(135deg, #111827, #1a2332);
    border: 1px solid rgba(0,201,167,0.15); border-radius: 14px;
    padding: 1.5rem; text-align: center;
}
.acid-letter {
    width: 50px; height: 50px; border-radius: 50%; display: inline-flex;
    align-items: center; justify-content: center; font-size: 1.4rem;
    font-weight: 700; color: #00c9a7;
    background: rgba(0,201,167,0.15); margin-bottom: 8px;
}
.lock-card {
    background: rgba(255,107,107,0.08); border: 1px solid rgba(255,107,107,0.25);
    border-radius: 12px; padding: 1rem; margin: 0.5rem 0;
}
@keyframes slideIn { from { transform: translateX(100px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] { border-radius: 8px; padding: 8px 16px; font-weight: 500; }
div[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }
</style>
"""
