"""
CSS Styles
All custom CSS for the Streamlit application.
"""

import streamlit as st


def inject_custom_css():
    """Inject all custom CSS styles into the Streamlit app."""
    st.markdown(CSS_STYLES, unsafe_allow_html=True)


CSS_STYLES = """
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* Global Styles */
.stApp {
    font-family: 'Inter', sans-serif;
}

/* Animated Background */
.hero-section {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 20px;
    padding: 3rem 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.hero-section::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 50%);
    animation: rotate 20s linear infinite;
}

@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.hero-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    margin-bottom: 1rem;
    position: relative;
    z-index: 1;
    animation: fadeInUp 0.8s ease-out;
}

.hero-subtitle {
    color: #a0aec0;
    text-align: center;
    font-size: 1.2rem;
    font-weight: 400;
    position: relative;
    z-index: 1;
    animation: fadeInUp 0.8s ease-out 0.2s both;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Floating Blobs */
.blob {
    position: absolute;
    border-radius: 50%;
    filter: blur(40px);
    opacity: 0.3;
    animation: float 8s ease-in-out infinite;
}

.blob-1 {
    width: 200px;
    height: 200px;
    background: #667eea;
    top: 10%;
    right: 10%;
}

.blob-2 {
    width: 150px;
    height: 150px;
    background: #f093fb;
    bottom: 20%;
    left: 10%;
    animation-delay: -4s;
}

@keyframes float {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(5deg); }
}

/* Product Cards */
.product-card {
    background: linear-gradient(145deg, #1e1e2e, #252536);
    border: 1px solid rgba(102, 126, 234, 0.2);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.product-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
    transform: scaleX(0);
    transition: transform 0.3s ease;
}

.product-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(102, 126, 234, 0.2);
    border-color: rgba(102, 126, 234, 0.4);
}

.product-card:hover::before {
    transform: scaleX(1);
}

.product-emoji {
    font-size: 3rem;
    margin-bottom: 0.5rem;
}

.product-name {
    font-size: 1.3rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.3rem;
}

.product-category {
    display: inline-block;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.5rem;
}

.product-price {
    font-size: 1.5rem;
    font-weight: 800;
    color: #4ade80;
    margin: 0.5rem 0;
}

.product-rating {
    color: #fbbf24;
    font-size: 0.9rem;
}

.product-description {
    color: #94a3b8;
    font-size: 0.9rem;
    line-height: 1.5;
    margin: 0.5rem 0;
}

.product-specs {
    background: rgba(102, 126, 234, 0.1);
    border-radius: 8px;
    padding: 0.75rem;
    margin-top: 0.75rem;
}

.spec-item {
    color: #cbd5e1;
    font-size: 0.8rem;
    margin: 0.25rem 0;
}

/* Recommendation Card */
.recommendation-card {
    background: linear-gradient(145deg, #1a1a2e, #1e2235);
    border: 2px solid rgba(74, 222, 128, 0.3);
    border-radius: 20px;
    padding: 2rem;
    margin: 1rem 0;
    position: relative;
    overflow: hidden;
    animation: slideInRight 0.5s ease-out;
}

.recommendation-card::after {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle, rgba(74, 222, 128, 0.1) 0%, transparent 70%);
}

@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

.match-score {
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #4ade80 0%, #22d3ee 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.match-label {
    color: #94a3b8;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.reason-box {
    background: rgba(102, 126, 234, 0.1);
    border-left: 3px solid #667eea;
    padding: 1rem;
    border-radius: 0 8px 8px 0;
    margin-top: 1rem;
}

.reason-text {
    color: #e2e8f0;
    font-style: italic;
    line-height: 1.6;
}

/* Score Progress Bar */
.score-bar-container {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    height: 12px;
    overflow: hidden;
    margin: 0.5rem 0;
}

.score-bar {
    height: 100%;
    border-radius: 10px;
    background: linear-gradient(90deg, #667eea 0%, #4ade80 100%);
    transition: width 1s ease-out;
}

/* Skeleton Loading */
.skeleton-card {
    background: linear-gradient(145deg, #1e1e2e, #252536);
    border: 1px solid rgba(102, 126, 234, 0.2);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    animation: pulse 1.5s ease-in-out infinite;
}

.skeleton-header {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
}

.skeleton-circle {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: rgba(102, 126, 234, 0.2);
}

.skeleton-lines {
    flex: 1;
}

.skeleton-line {
    height: 12px;
    border-radius: 6px;
    background: rgba(102, 126, 234, 0.2);
    margin-bottom: 0.5rem;
}

.skeleton-title {
    width: 60%;
    height: 16px;
}

.skeleton-subtitle {
    width: 40%;
}

.skeleton-text {
    width: 100%;
}

.skeleton-text.short {
    width: 70%;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

/* Status Badge */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border-radius: 25px;
    font-size: 0.85rem;
    font-weight: 500;
}

.status-ai {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
    border: 1px solid rgba(102, 126, 234, 0.4);
    color: #a5b4fc;
}

.status-fallback {
    background: rgba(251, 191, 36, 0.2);
    border: 1px solid rgba(251, 191, 36, 0.4);
    color: #fbbf24;
}

/* Section Headers */
.section-header {
    font-size: 1.8rem;
    font-weight: 700;
    color: #ffffff;
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid rgba(102, 126, 234, 0.3);
}

/* Tab Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(30, 30, 46, 0.8);
    padding: 0.5rem;
    border-radius: 12px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 0.75rem 1.5rem;
    font-weight: 500;
}

/* Info Box */
.info-box {
    background: linear-gradient(145deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
    border: 1px solid rgba(102, 126, 234, 0.3);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
}

/* Message Boxes */
.message-box {
    padding: 1rem 1.5rem;
    border-radius: 12px;
    margin: 1rem 0;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.message-error {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    color: #fca5a5;
}

.message-success {
    background: rgba(74, 222, 128, 0.1);
    border: 1px solid rgba(74, 222, 128, 0.3);
    color: #86efac;
}

.message-warning {
    background: rgba(251, 191, 36, 0.1);
    border: 1px solid rgba(251, 191, 36, 0.3);
    color: #fde047;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Responsive */
@media (max-width: 768px) {
    .hero-title {
        font-size: 2rem;
    }
    .hero-subtitle {
        font-size: 1rem;
    }
    .recommendation-card {
        padding: 1rem;
    }
}
</style>
"""
