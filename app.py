import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
from funnel_analyzer import FunnelAnalyzer
from data_generator import DataGenerator
from ai_insights import AIInsights

# Page configuration
st.set_page_config(
    page_title="Funnel Drop-Offs Analyzer - Trisha",
    page_icon="📊",
    layout="wide"
)

# Initialize components
@st.cache_resource
def initialize_components():
    data_gen = DataGenerator()
    analyzer = FunnelAnalyzer()
    ai_insights = AIInsights()
    return data_gen, analyzer, ai_insights

data_generator, funnel_analyzer, ai_insights = initialize_components()

# Main title and description
st.title("📊 Funnel Drop-Offs Analyzer - Trisha")
st.markdown("""
**Your AI-powered marketing analytics companion**

This tool helps marketing teams visualize conversion drop-offs from Google Ads traffic through funnel stages:
**Visitor → Lead → MQL → SQL**

- 🔍 Automatically identifies problematic drop-offs
- 📈 Generates actionable AI-powered recommendations
- 📊 Provides clear, color-coded visualizations
- 🚨 Sends alerts to your team channels
""")

# Sidebar configuration
st.sidebar.header("⚙️ Analysis Configuration")

# Data input method selector
data_input_method = st.sidebar.selectbox(
    "Data Input Method",
    ["Manual Entry", "CSV Upload", "API Integration", "Demo Data"],
    index=0,
    help="Choose how you want to input your funnel data"
)

st.sidebar.markdown("---")

# Initialize variables to avoid scope issues
manual_funnel_data = None
csv_funnel_data = None
api_funnel_data = None
time_period = "Last 30 Days"
traffic_source = ["Google Ads", "Facebook Ads"]

# Data input section based on selected method
if data_input_method == "Manual Entry":
    st.sidebar.subheader("📝 Enter Your Data")
    
    visitor_count = st.sidebar.number_input(
        "Visitors",
        min_value=1,
        value=1000,
        help="Total number of visitors"
    )
    
    lead_count = st.sidebar.number_input(
        "Leads",
        min_value=1,
        value=250,
        max_value=visitor_count,
        help="Number of leads generated"
    )
    
    mql_count = st.sidebar.number_input(
        "MQLs (Marketing Qualified Leads)",
        min_value=1,
        value=125,
        max_value=lead_count,
        help="Number of marketing qualified leads"
    )
    
    sql_count = st.sidebar.number_input(
        "SQLs (Sales Qualified Leads)",
        min_value=1,
        value=50,
        max_value=mql_count,
        help="Number of sales qualified leads"
    )
    
    # Store manual data
    manual_funnel_data = {
        'Visitor': visitor_count,
        'Lead': lead_count,
        'MQL': mql_count,
        'SQL': sql_count
    }

elif data_input_method == "CSV Upload":
    st.sidebar.subheader("📁 Upload CSV File")
    
    # Sample CSV template download
    sample_csv = """Stage,Count
Visitor,1000
Lead,250
MQL,125
SQL,50"""
    
    st.sidebar.download_button(
        label="📥 Download CSV Template",
        data=sample_csv,
        file_name="funnel_data_template.csv",
        mime="text/csv",
        help="Download this template to format your data correctly"
    )
    
    uploaded_file = st.sidebar.file_uploader(
        "Upload funnel data CSV",
        type=['csv'],
        help="CSV should have columns: Stage, Count"
    )
    
    if uploaded_file:
        try:
            csv_data = pd.read_csv(uploaded_file)
            if 'Stage' in csv_data.columns and 'Count' in csv_data.columns:
                csv_funnel_data = dict(zip(csv_data['Stage'], csv_data['Count']))
                st.sidebar.success("CSV uploaded successfully!")
                st.sidebar.write("Data preview:")
                st.sidebar.dataframe(csv_data)
            else:
                st.sidebar.error("CSV must have 'Stage' and 'Count' columns")
                csv_funnel_data = None
        except Exception as e:
            st.sidebar.error(f"Error reading CSV: {str(e)}")
            csv_funnel_data = None
    else:
        csv_funnel_data = None
        st.sidebar.info("Please upload a CSV file with your funnel data")

elif data_input_method == "API Integration":
    st.sidebar.subheader("🔗 API Integration")
    
    api_platform = st.sidebar.selectbox(
        "Platform",
        ["Google Ads", "Facebook Ads", "HubSpot", "Salesforce", "Custom API"],
        help="Select your data source platform"
    )
    
    if api_platform == "Google Ads":
        st.sidebar.info("Google Ads integration requires API credentials")
        google_ads_customer_id = st.sidebar.text_input("Customer ID", placeholder="123-456-7890")
        
    elif api_platform == "HubSpot":
        st.sidebar.info("HubSpot integration requires API token")
        hubspot_token = st.sidebar.text_input("API Token", type="password")
        
    elif api_platform == "Salesforce":
        st.sidebar.info("Salesforce integration requires OAuth setup")
        sf_username = st.sidebar.text_input("Username")
        sf_password = st.sidebar.text_input("Password", type="password")
        
    elif api_platform == "Custom API":
        st.sidebar.info("Custom API integration")
        custom_api_url = st.sidebar.text_input("API Endpoint URL")
        custom_api_key = st.sidebar.text_input("API Key", type="password")
    
    st.sidebar.warning("API integrations require additional setup. Contact support for assistance.")
    api_funnel_data = None

else:  # Demo Data
    st.sidebar.subheader("🎯 Demo Configuration")
    
    # Time period selector
    time_period = st.sidebar.selectbox(
        "Analysis Period",
        ["Last 7 Days", "Last 30 Days", "Last 90 Days"],
        index=1
    )
    
    # Traffic source filter
    traffic_source = st.sidebar.multiselect(
        "Traffic Sources",
        ["Google Ads", "Facebook Ads", "Organic", "Direct", "Email"],
        default=["Google Ads", "Facebook Ads"]
    )

st.sidebar.markdown("---")

# Drop-off threshold slider
threshold = st.sidebar.slider(
    "Drop-off Alert Threshold (%)",
    min_value=30,
    max_value=40,
    value=35,
    step=1,
    help="Flag stages where conversion drops by more than this percentage"
)

st.sidebar.markdown("---")

# Run Analysis button
analyze_button_enabled = True
button_help = "Click to analyze your funnel data"

# Check if we have data to analyze
if data_input_method == "Manual Entry":
    funnel_data_ready = manual_funnel_data
elif data_input_method == "CSV Upload":
    funnel_data_ready = csv_funnel_data
    if not csv_funnel_data:
        analyze_button_enabled = False
        button_help = "Please upload a CSV file first"
elif data_input_method == "API Integration":
    funnel_data_ready = api_funnel_data
    analyze_button_enabled = False
    button_help = "API integration not yet implemented"
else:  # Demo Data
    funnel_data_ready = None

if st.sidebar.button("🚀 Run Analysis", type="primary", use_container_width=True, disabled=not analyze_button_enabled, help=button_help):
    with st.spinner("Analyzing funnel data..."):
        # Get funnel data based on input method
        if data_input_method == "Manual Entry":
            funnel_data = manual_funnel_data
        elif data_input_method == "CSV Upload":
            funnel_data = csv_funnel_data
        elif data_input_method == "Demo Data":
            # Generate mock data based on selections
            funnel_data = data_generator.generate_funnel_data(
                time_period=time_period,
                traffic_sources=traffic_source
            )
        else:
            st.error("Selected data input method not yet supported")
            funnel_data = None
        
        if funnel_data:
            # Store in session state
            st.session_state.funnel_data = funnel_data
            st.session_state.threshold = threshold
            st.session_state.analysis_complete = True
            st.session_state.timestamp = datetime.now()
            st.session_state.data_input_method = data_input_method

# Check if analysis has been run
if hasattr(st.session_state, 'analysis_complete') and st.session_state.analysis_complete:
    funnel_data = st.session_state.funnel_data
    threshold = st.session_state.threshold
    
    # Analyze the funnel
    analysis_results = funnel_analyzer.analyze_funnel(funnel_data, threshold)
    
    # Display timestamp
    st.success(f"✅ Analysis completed at {st.session_state.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Main dashboard
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Funnel Performance Overview")
        
        # Funnel visualization
        fig_funnel = go.Figure()
        
        stages = list(funnel_data.keys())
        values = list(funnel_data.values())
        colors = []
        
        for i, stage in enumerate(stages):
            if stage in analysis_results['problematic_stages']:
                colors.append('#FF6B6B')  # Red for problematic stages
            else:
                colors.append('#4ECDC4')  # Teal for healthy stages
        
        fig_funnel.add_trace(go.Funnel(
            y=stages,
            x=values,
            textinfo="value+percent initial",
            marker=dict(color=colors),
            hovertemplate='<b>%{y}</b><br>Count: %{x}<br>Conversion: %{percentInitial}<extra></extra>'
        ))
        
        fig_funnel.update_layout(
            title="Conversion Funnel with Drop-off Highlights",
            height=500,
            showlegend=False
        )
        
        st.plotly_chart(fig_funnel, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Key Metrics")
        
        # Overall conversion rate
        overall_conversion = (values[-1] / values[0]) * 100
        st.metric(
            "Overall Conversion Rate",
            f"{overall_conversion:.1f}%",
            delta=f"{overall_conversion - 10:.1f}%" if overall_conversion > 10 else f"{overall_conversion - 10:.1f}%"
        )
        
        # Total visitors
        st.metric("Total Visitors", f"{values[0]:,}")
        
        # Final conversions
        st.metric("Final Conversions (SQL)", f"{values[-1]:,}")
        
        # Problematic stages count
        problematic_count = len(analysis_results['problematic_stages'])
        st.metric(
            "Problematic Stages",
            problematic_count,
            delta=f"-{problematic_count}" if problematic_count > 0 else "0"
        )
    
    # Detailed analysis table
    st.subheader("📊 Stage-by-Stage Analysis")
    
    # Create detailed DataFrame
    detailed_df = pd.DataFrame(analysis_results['stage_analysis'])
    
    # Color code problematic rows
    def color_problematic_rows(row):
        if row['Stage'] in analysis_results['problematic_stages']:
            return ['background-color: #FFE5E5'] * len(row)
        return [''] * len(row)
    
    styled_df = detailed_df.style.apply(color_problematic_rows, axis=1)
    st.dataframe(styled_df, use_container_width=True)
    
    # Conversion rate chart
    st.subheader("📉 Conversion Rate by Stage")
    
    conversion_df = pd.DataFrame({
        'Stage': stages[1:],  # Skip first stage as it's the baseline
        'Conversion Rate': [analysis_results['stage_analysis'][i]['Conversion Rate (%)'] for i in range(1, len(stages))]
    })
    
    fig_conversion = px.bar(
        conversion_df,
        x='Stage',
        y='Conversion Rate',
        title="Conversion Rates Between Stages",
        color='Conversion Rate',
        color_continuous_scale=['#FF6B6B', '#FFE66D', '#4ECDC4']
    )
    
    fig_conversion.update_layout(height=400)
    st.plotly_chart(fig_conversion, use_container_width=True)
    
    # AI-powered insights
    st.subheader("🤖 AI-Powered Insights & Recommendations")
    
    with st.spinner("Generating AI insights..."):
        insights = ai_insights.generate_insights(analysis_results, funnel_data)
        
        if insights:
            # Display insights in expandable sections
            with st.expander("🔍 Funnel Analysis Summary", expanded=True):
                st.write(insights.get('summary', 'No summary available'))
            
            with st.expander("💡 Actionable Recommendations", expanded=True):
                recommendations = insights.get('recommendations', [])
                if recommendations:
                    for i, rec in enumerate(recommendations, 1):
                        st.write(f"**{i}.** {rec}")
                else:
                    st.write("No specific recommendations available")
            
            with st.expander("📈 Optimization Priorities", expanded=True):
                priorities = insights.get('priorities', [])
                if priorities:
                    for priority in priorities:
                        st.write(f"• {priority}")
                else:
                    st.write("No specific priorities identified")
        else:
            st.error("Unable to generate AI insights. Please check your OpenAI API key.")
    
    # Mock integrations section
    st.subheader("📱 Team Notifications")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💬 Slack Alert Preview")
        slack_message = f"""
🚨 **Funnel Drop-off Alert**
        
**Analysis Period:** {time_period}
**Problematic Stages:** {len(analysis_results['problematic_stages'])}
**Overall Conversion:** {overall_conversion:.1f}%

**Issues Found:**
{chr(10).join([f"• {stage}" for stage in analysis_results['problematic_stages']])}

**Next Steps:** Review AI recommendations in Trisha dashboard
        """
        st.code(slack_message, language="markdown")
    
    with col2:
        st.markdown("### 📋 Notion Report Preview")
        notion_content = f"""
# Funnel Analysis Report - {datetime.now().strftime('%Y-%m-%d')}

## Executive Summary
- **Total Visitors:** {values[0]:,}
- **Final Conversions:** {values[-1]:,}
- **Overall Rate:** {overall_conversion:.1f}%
- **Issues:** {len(analysis_results['problematic_stages'])} problematic stages

## Key Findings
{chr(10).join([f"- {stage} needs attention" for stage in analysis_results['problematic_stages']])}

## Status: {'🔴 Needs Attention' if problematic_count > 0 else '🟢 Healthy'}
        """
        st.code(notion_content, language="markdown")
    
    # Export functionality
    st.subheader("📥 Export Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Export detailed data as CSV
        csv_data = pd.DataFrame(analysis_results['stage_analysis']).to_csv(index=False)
        st.download_button(
            label="Download CSV Report",
            data=csv_data,
            file_name=f"funnel_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Export insights as JSON
        json_data = json.dumps(insights, indent=2) if insights else json.dumps({"error": "No insights available"}, indent=2)
        st.download_button(
            label="Download JSON Insights",
            data=json_data,
            file_name=f"funnel_insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    with col3:
        # Export summary report
        summary_report = f"""
Funnel Analysis Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Configuration:
- Threshold: {threshold}%
- Period: {time_period}
- Sources: {', '.join(traffic_source)}

Results:
- Total Visitors: {values[0]:,}
- Final Conversions: {values[-1]:,}
- Overall Conversion Rate: {overall_conversion:.1f}%
- Problematic Stages: {len(analysis_results['problematic_stages'])}

Stage Details:
{chr(10).join([f"- {stage['Stage']}: {stage['Count']:,} ({stage['Conversion Rate (%)']:.1f}%)" for stage in analysis_results['stage_analysis']])}

Issues:
{chr(10).join([f"- {stage}" for stage in analysis_results['problematic_stages']])}
        """
        st.download_button(
            label="Download Summary Report",
            data=summary_report,
            file_name=f"funnel_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

else:
    # Initial state - show data input instructions
    st.info("👆 Choose your data input method in the sidebar and click **'Run Analysis'** to get started!")
    
    # Show data input options
    st.subheader("📊 How to Input Your Data")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        **📝 Manual Entry**
        - Enter your funnel numbers directly
        - Perfect for quick analysis
        - Visitors → Leads → MQLs → SQLs
        """)
    
    with col2:
        st.markdown("""
        **📁 CSV Upload**
        - Upload your data from Excel/Google Sheets
        - Download the CSV template
        - Bulk data import
        """)
    
    with col3:
        st.markdown("""
        **🔗 API Integration**
        - Connect to your CRM/Ad platforms
        - Google Ads, HubSpot, Salesforce
        - Real-time data sync
        """)
    
    with col4:
        st.markdown("""
        **🎯 Demo Data**
        - Test with sample data
        - See all features in action
        - Perfect for evaluation
        """)
    
    st.markdown("---")
    
    # Show sample funnel visualization
    st.subheader("📊 Sample Funnel Visualization")
    
    sample_data = {
        'Visitor': 1000,
        'Lead': 500,
        'MQL': 250,
        'SQL': 100
    }
    
    stages = list(sample_data.keys())
    values = list(sample_data.values())
    
    fig_sample = go.Figure()
    fig_sample.add_trace(go.Funnel(
        y=stages,
        x=values,
        textinfo="value+percent initial",
        marker=dict(color=['#4ECDC4', '#4ECDC4', '#FFE66D', '#FF6B6B'])
    ))
    
    fig_sample.update_layout(
        title="Sample Funnel Analysis (Demo Data)",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_sample, use_container_width=True)
    
    # Feature highlights
    st.subheader("🌟 Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📈 Smart Analytics**
        - Automatic drop-off detection
        - Customizable thresholds
        - Multi-source analysis
        - Historical comparisons
        """)
    
    with col2:
        st.markdown("""
        **🤖 AI Insights**
        - GPT-4 powered recommendations
        - Actionable next steps
        - Priority optimization areas
        - Performance predictions
        """)
    
    with col3:
        st.markdown("""
        **📱 Team Integration**
        - Slack notifications
        - Notion reports
        - CSV/JSON exports
        - Real-time alerts
        """)

# Footer
st.markdown("---")
st.markdown("*Built with ❤️ for marketing teams. Powered by Streamlit & OpenAI.*")
