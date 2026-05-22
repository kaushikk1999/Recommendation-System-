"""
UI Components
Reusable Streamlit UI components with custom styling.
"""

import streamlit as st
from typing import Optional

from app.api.schemas import RecommendationResponse, RecommendationItem
from app.data.products import get_product_by_id
from app.utils.helpers import has_given_feedback, record_feedback


def render_product_card(product: dict, compact: bool = False):
    """Render a product card with styling."""
    rating_stars = "⭐" * int(product["rating"]) + "☆" * (5 - int(product["rating"]))
    specs_html = "".join(
        f'<div class="spec-item">• <strong>{k}:</strong> {v}</div>'
        for k, v in product["specs"].items()
    )
    
    if compact:
        st.markdown(f"""
        <div class="product-card">
            <div style="display: flex; align-items: flex-start; gap: 1rem;">
                <div class="product-emoji">{product['emoji']}</div>
                <div style="flex: 1;">
                    <div class="product-name">{product['name']}</div>
                    <span class="product-category">{product['category']}</span>
                    <div class="product-price">${product['price']}</div>
                    <div class="product-rating">{rating_stars} ({product['rating']})</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="product-card">
            <div class="product-emoji">{product['emoji']}</div>
            <div class="product-name">{product['name']}</div>
            <span class="product-category">{product['category']}</span>
            <div class="product-price">${product['price']}</div>
            <div class="product-rating">{rating_stars} ({product['rating']})</div>
            <p class="product-description">{product['description']}</p>
            <div class="product-specs">
                {specs_html}
            </div>
            <p style="color: #94a3b8; font-size: 0.85rem; margin-top: 0.5rem;">
                <strong>Best for:</strong> {product['best_for']}
            </p>
        </div>
        """, unsafe_allow_html=True)


def render_recommendation_card(rec: RecommendationItem, product: dict, index: int):
    """Render a recommendation result card with feedback buttons."""
    score = rec.match_score
    reason = rec.reason
    rating_stars = "⭐" * int(product["rating"]) + "☆" * (5 - int(product["rating"]))
    specs_html = " • ".join(f"{k}: {v}" for k, v in list(product["specs"].items())[:3])
    
    st.markdown(f"""
    <div class="recommendation-card" style="animation-delay: {index * 0.1}s;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem;">
            <div style="flex: 1; min-width: 200px;">
                <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                    <span style="font-size: 3rem;">{product['emoji']}</span>
                    <div>
                        <div class="product-name" style="font-size: 1.5rem;">{product['name']}</div>
                        <span class="product-category">{product['category']}</span>
                    </div>
                </div>
                <div class="product-price" style="font-size: 2rem;">${product['price']}</div>
                <div class="product-rating" style="font-size: 1rem;">{rating_stars} ({product['rating']})</div>
                <p class="product-description">{product['description']}</p>
                <p style="color: #94a3b8; font-size: 0.85rem;">{specs_html}</p>
            </div>
            <div style="text-align: center; min-width: 120px;">
                <div class="match-label">Match Score</div>
                <div class="match-score">{score}%</div>
                <div class="score-bar-container">
                    <div class="score-bar" style="width: {score}%;"></div>
                </div>
            </div>
        </div>
        <div class="reason-box">
            <p class="reason-text">💡 {reason}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feedback buttons
    if not has_given_feedback(rec.product_id):
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("👍 Helpful", key=f"up_{rec.product_id}_{index}"):
                record_feedback(rec.product_id, "positive")
                st.success("Thanks for the feedback!")
                st.rerun()
        with col2:
            if st.button("👎 Not helpful", key=f"down_{rec.product_id}_{index}"):
                record_feedback(rec.product_id, "negative")
                st.info("Thanks for the feedback!")
                st.rerun()
    else:
        st.markdown("<small style='color: #64748b;'>✓ Feedback recorded</small>", unsafe_allow_html=True)


def render_skeleton_cards(count: int = 3):
    """Render loading skeleton cards."""
    for i in range(count):
        st.markdown(f"""
        <div class="skeleton-card" style="animation-delay: {i * 0.1}s;">
            <div class="skeleton-header">
                <div class="skeleton-circle"></div>
                <div class="skeleton-lines">
                    <div class="skeleton-line skeleton-title"></div>
                    <div class="skeleton-line skeleton-subtitle"></div>
                </div>
            </div>
            <div class="skeleton-line skeleton-text"></div>
            <div class="skeleton-line skeleton-text short"></div>
        </div>
        """, unsafe_allow_html=True)


def render_hero_section():
    """Render the animated hero section."""
    st.markdown("""
    <div class="hero-section">
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
        <h1 class="hero-title">🛍️ AI Product Recommendation Studio</h1>
        <p class="hero-subtitle">
            Find the perfect product using natural-language preferences powered by Ollama AI
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_example_chips() -> Optional[str]:
    """
    Render clickable example query chips.
    Returns the selected example if clicked, None otherwise.
    """
    st.markdown("""
    <div style="text-align: center; margin: 1rem 0;">
        <span style="color: #94a3b8; font-size: 0.9rem;">Try these examples:</span>
    </div>
    """, unsafe_allow_html=True)
    
    examples = [
        "Phone under $500",
        "Laptop for students",
        "Headphones with long battery life",
        "Best smartwatch for fitness",
        "Budget tablet for kids",
        "Gaming laptop under $1000"
    ]
    
    selected = None
    cols = st.columns(3)
    for i, example in enumerate(examples):
        with cols[i % 3]:
            if st.button(f"💡 {example}", key=f"example_{i}", use_container_width=True):
                selected = example
    
    return selected


def render_source_badge(source: str):
    """Render the recommendation source badge."""
    if source == "ai":
        st.markdown("""
        <div class="status-badge status-ai">
            <span>🤖</span>
            <span>Powered by Ollama AI</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-badge status-fallback">
            <span>⚡</span>
            <span>Smart Fallback Engine</span>
        </div>
        """, unsafe_allow_html=True)


def render_warning_message(message: str):
    """Render a warning message box."""
    st.markdown(f"""
    <div class="message-box message-warning">
        <span>⚠️</span>
        <span>{message}</span>
    </div>
    """, unsafe_allow_html=True)


def render_error_message(message: str):
    """Render an error message box."""
    st.markdown(f"""
    <div class="message-box message-error">
        <span>❌</span>
        <span>{message}</span>
    </div>
    """, unsafe_allow_html=True)


def render_success_message(message: str):
    """Render a success message box."""
    st.markdown(f"""
    <div class="message-box message-success">
        <span>✅</span>
        <span>{message}</span>
    </div>
    """, unsafe_allow_html=True)


def render_info_box(content: str):
    """Render an info box."""
    st.markdown(f"""
    <div class="info-box">
        <p style="color: #e2e8f0; margin: 0;">{content}</p>
    </div>
    """, unsafe_allow_html=True)


def render_api_status(is_configured: bool):
    """Render API configuration status."""
    if is_configured:
        st.markdown("""
        <div class="message-box message-success">
            <span>✅</span>
            <span><strong>API Connected:</strong> Ollama API key is configured. AI recommendations are active.</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="message-box message-warning">
            <span>⚠️</span>
            <span><strong>API Not Configured:</strong> Using smart fallback engine. Add OLLAMA_API_KEY to enable AI recommendations.</span>
        </div>
        """, unsafe_allow_html=True)


def render_search_history(history: list[dict]):
    """Render the search history sidebar."""
    if not history:
        st.markdown("<p style='color: #64748b; font-size: 0.9rem;'>No searches yet</p>", unsafe_allow_html=True)
        return
    
    for entry in history[:5]:
        source_icon = "🤖" if entry["source"] == "ai" else "⚡"
        st.markdown(f"""
        <div style="padding: 0.5rem; background: rgba(102, 126, 234, 0.1); border-radius: 8px; margin-bottom: 0.5rem;">
            <div style="color: #e2e8f0; font-size: 0.85rem;">{source_icon} {entry['query'][:30]}...</div>
            <div style="color: #64748b; font-size: 0.75rem;">{entry['results_count']} results</div>
        </div>
        """, unsafe_allow_html=True)


def render_rate_limit_status(status: dict):
    """Render rate limit status."""
    used = status["requests_used"]
    limit = status["requests_limit"]
    remaining = status["requests_remaining"]
    
    if remaining > 5:
        color = "#4ade80"
    elif remaining > 2:
        color = "#fbbf24"
    else:
        color = "#ef4444"
    
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 0.5rem;">
        <div style="flex: 1; background: rgba(255,255,255,0.1); border-radius: 4px; height: 8px; overflow: hidden;">
            <div style="width: {(used/limit)*100}%; height: 100%; background: {color};"></div>
        </div>
        <span style="color: {color}; font-size: 0.8rem;">{remaining}/{limit}</span>
    </div>
    """, unsafe_allow_html=True)
