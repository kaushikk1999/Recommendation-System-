"""
AI Product Recommendation Studio
A production-ready product recommendation system powered by Ollama AI.

Features:
- AI-powered recommendations via Ollama API
- Smart fallback engine when AI unavailable
- Rate limiting and caching
- Input validation and sanitization
- User feedback collection
- Search history tracking
- Analytics events
"""

import sys
import os
import logging

# Add app directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s'
)
logger = logging.getLogger(__name__)

# Import application modules
from app.config import is_api_configured, API_CONFIG
from app.api.schemas import UserQuery, RecommendationResponse
from app.services.recommender import get_recommendations, get_recommendation_stats
from app.data.products import get_all_products, get_product_by_id, get_all_categories
from app.utils.helpers import (
    init_session_state,
    check_rate_limit,
    get_rate_limit_status,
    add_to_search_history,
    get_search_history,
    track_event,
    get_health_status,
    validate_query,
    sanitize_query,
    get_analytics_summary,
)
from app.ui.styles import inject_custom_css
from app.ui.components import (
    render_hero_section,
    render_example_chips,
    render_product_card,
    render_recommendation_card,
    render_source_badge,
    render_warning_message,
    render_error_message,
    render_info_box,
    render_api_status,
    render_search_history,
    render_rate_limit_status,
    render_skeleton_cards,
)


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    st.set_page_config(
        page_title="AI Product Recommendations",
        page_icon="🛍️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Inject custom CSS
    inject_custom_css()
    
    # Initialize session state
    init_session_state()
    
    # Render hero section
    render_hero_section()
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🤖 AI Recommender", 
        "📦 Product Catalog", 
        "ℹ️ How It Works",
        "⚙️ API Status"
    ])
    
    # ===== TAB 1: AI RECOMMENDER =====
    with tab1:
        st.markdown('<h2 class="section-header">Get Personalized Recommendations</h2>', unsafe_allow_html=True)
        
        # Example chips
        selected_example = render_example_chips()
        if selected_example:
            st.session_state.query_input = selected_example
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Input section
        col1, col2 = st.columns([3, 1])
        
        with col1:
            user_query = st.text_input(
                "What are you looking for?",
                value=st.session_state.get("query_input", ""),
                placeholder="E.g., I need a lightweight laptop for school under $600",
                key="main_query_input"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            recommend_clicked = st.button(
                "🚀 Get Recommendations",
                type="primary",
                use_container_width=True
            )
        
        # Optional filters in expander
        products = get_all_products()
        categories = get_all_categories()
        
        with st.expander("🎯 Optional Filters"):
            filter_cols = st.columns(2)
            with filter_cols[0]:
                category_filter = st.selectbox(
                    "Category",
                    ["All Categories"] + categories,
                    key="category_filter"
                )
            with filter_cols[1]:
                max_budget = st.slider(
                    "Max Budget ($)",
                    min_value=0,
                    max_value=1500,
                    value=1500,
                    step=50,
                    key="budget_filter"
                )
        
        # Process recommendations
        if recommend_clicked and user_query.strip():
            # Validate input
            is_valid, error_msg = validate_query(user_query)
            if not is_valid:
                render_error_message(error_msg)
            else:
                # Check rate limit
                allowed, rate_msg = check_rate_limit()
                if not allowed:
                    render_warning_message(rate_msg)
                else:
                    # Sanitize query
                    clean_query = sanitize_query(user_query)
                    
                    # Create validated query object
                    query_obj = UserQuery(
                        text=clean_query,
                        category_filter=category_filter if category_filter != "All Categories" else None,
                        max_budget=max_budget if max_budget < 1500 else None
                    )
                    
                    with st.spinner("🔮 AI is analyzing your preferences..."):
                        # Track event
                        track_event("recommendation_request", {
                            "query_length": len(clean_query),
                            "has_category_filter": category_filter != "All Categories",
                            "has_budget_filter": max_budget < 1500
                        })
                        
                        # Get recommendations
                        results = get_recommendations(query_obj)
                        st.session_state.recommendations = results
                        
                        # Add to search history
                        add_to_search_history(
                            clean_query,
                            results.source,
                            len(results.recommendations)
                        )
        
        # Display results
        if st.session_state.get("recommendations"):
            results: RecommendationResponse = st.session_state.recommendations
            
            # Source indicator
            render_source_badge(results.source)
            
            # Warning message if any
            if results.warning:
                render_warning_message(results.warning)
            
            # Summary
            if results.summary:
                render_info_box(results.summary)
            
            # Recommendation cards
            st.markdown('<h3 style="color: #ffffff; margin-top: 2rem;">🎯 Top Recommendations</h3>', unsafe_allow_html=True)
            
            for i, rec in enumerate(results.recommendations):
                product = get_product_by_id(rec.product_id)
                if product:
                    render_recommendation_card(rec, product, i)
                else:
                    st.warning(f"Product ID '{rec.product_id}' not found in catalog")
        
        elif recommend_clicked:
            render_error_message("Please enter your preferences to get recommendations.")
    
    # ===== TAB 2: PRODUCT CATALOG =====
    with tab2:
        st.markdown('<h2 class="section-header">Complete Product Catalog</h2>', unsafe_allow_html=True)
        
        # Category filter
        all_categories = ["All"] + categories
        selected_cat = st.selectbox("Filter by Category", all_categories, key="catalog_filter")
        
        # Filter products
        all_products = get_all_products()
        filtered = all_products if selected_cat == "All" else [p for p in all_products if p["category"] == selected_cat]
        
        st.markdown(f"<p style='color: #94a3b8;'>Showing {len(filtered)} products</p>", unsafe_allow_html=True)
        
        # Display in columns
        cols = st.columns(3)
        for i, product in enumerate(filtered):
            with cols[i % 3]:
                render_product_card(product)
    
    # ===== TAB 3: HOW IT WORKS =====
    with tab3:
        st.markdown('<h2 class="section-header">How It Works</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
            <h3 style="color: #a5b4fc; margin-top: 0;">🔮 AI-Powered Recommendations</h3>
            <p style="color: #e2e8f0;">
                This system uses the Ollama AI API with Gemma model to understand your 
                natural language preferences and match them with products from our catalog.
            </p>
            
            <h4 style="color: #a5b4fc; margin-top: 1.5rem;">📝 How to Use</h4>
            <ol style="color: #cbd5e1;">
                <li>Describe what you're looking for in plain English</li>
                <li>Optionally apply category and budget filters</li>
                <li>Click "Get Recommendations" to receive AI-curated suggestions</li>
                <li>Each recommendation includes a match score and reasoning</li>
            </ol>
            
            <h4 style="color: #a5b4fc; margin-top: 1.5rem;">⚡ Smart Fallback Engine</h4>
            <p style="color: #e2e8f0;">
                If the AI API is unavailable, the system automatically switches to a deterministic 
                recommendation engine that uses keyword matching, budget analysis, and rating-based 
                ranking to find the best products for you.
            </p>
            
            <h4 style="color: #a5b4fc; margin-top: 1.5rem;">🔒 Privacy & Security</h4>
            <p style="color: #e2e8f0;">
                Your preferences are processed securely and not stored. The API key is managed 
                through secure environment variables and never exposed in the application.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Stats
        stats = get_recommendation_stats()
        st.markdown(f"""
        <div class="info-box">
            <h4 style="color: #a5b4fc; margin-top: 0;">📊 System Stats</h4>
            <p style="color: #e2e8f0;">
                <strong>Products in catalog:</strong> {stats['total_products']}<br>
                <strong>Categories:</strong> {stats['categories']}<br>
                <strong>AI Available:</strong> {'✅ Yes' if stats['ai_available'] else '❌ No (using fallback)'}<br>
                <strong>Cache TTL:</strong> {stats['cache_ttl_seconds']} seconds
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # ===== TAB 4: API STATUS =====
    with tab4:
        st.markdown('<h2 class="section-header">API Configuration Status</h2>', unsafe_allow_html=True)
        
        render_api_status(is_api_configured())
        
        st.markdown(f"""
        <div class="info-box">
            <h4 style="color: #a5b4fc; margin-top: 0;">🔧 Configuration</h4>
            <p style="color: #e2e8f0;">
                <strong>API Provider:</strong> <code>Ollama</code><br>
                <strong>Model:</strong> <code>{API_CONFIG.model}</code><br>
                <strong>Timeout:</strong> {API_CONFIG.timeout} seconds
            </p>
            
            <h4 style="color: #a5b4fc; margin-top: 1.5rem;">📋 Setup Instructions</h4>
            <p style="color: #e2e8f0;">To enable AI recommendations:</p>
            <ol style="color: #cbd5e1;">
                <li>Get your API key from <a href="https://ollama.com" style="color: #a5b4fc;">Ollama</a></li>
                <li>Create <code>.streamlit/secrets.toml</code> file</li>
                <li>Add: <code>OLLAMA_API_KEY = "your-api-key"</code></li>
                <li>Restart the application</li>
            </ol>
            
            <p style="color: #94a3b8; font-size: 0.85rem; margin-top: 1rem;">
                For Streamlit Community Cloud deployment, add the secret in the app settings dashboard.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Rate limit status
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<h4 style="color: #a5b4fc;">📈 Rate Limit Status</h4>', unsafe_allow_html=True)
        rate_status = get_rate_limit_status()
        render_rate_limit_status(rate_status)
        
        # Search history
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<h4 style="color: #a5b4fc;">🕐 Recent Searches</h4>', unsafe_allow_html=True)
        history = get_search_history()
        render_search_history(history)
        
        # Health check
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🧪 Run Health Check", type="secondary"):
            health = get_health_status()
            st.json(health.model_dump())
    
    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 2rem; margin-top: 3rem; border-top: 1px solid rgba(102, 126, 234, 0.2);">
        <p style="color: #64748b; font-size: 0.85rem;">
            Built with ❤️ using Streamlit • Powered by Ollama AI
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
