# Funnel Drop-Offs Analyzer - Trisha

## Overview

A Streamlit-based marketing analytics tool that helps teams visualize and optimize conversion funnels from Google Ads traffic. The application analyzes visitor progression through four key stages: Visitor → Lead → MQL → SQL, providing AI-powered insights and recommendations for improving conversion rates.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit for web interface
- **Visualization**: Plotly for interactive charts and graphs
- **Data Processing**: Pandas for data manipulation
- **Caching**: Streamlit's @st.cache_resource decorator for component initialization

### Backend Architecture
- **Modular Design**: Separate classes for different functionalities
- **Data Generation**: Synthetic data generation for testing and demonstration
- **Analysis Engine**: Funnel analysis with configurable thresholds
- **AI Integration**: OpenAI GPT-4o integration for insights generation

### Data Storage
- **In-Memory Processing**: Data is generated and processed in memory
- **No Persistent Storage**: Current implementation uses synthetic data without database persistence

## Key Components

### 1. FunnelAnalyzer (`funnel_analyzer.py`)
- **Purpose**: Core analysis engine for funnel conversion rates
- **Functionality**: Calculates conversion rates, identifies drop-offs, categorizes stage health
- **Key Features**: 
  - Configurable drop-off thresholds (30-40%)
  - Stage-by-stage analysis with health indicators
  - Problematic stage identification

### 2. DataGenerator (`data_generator.py`)
- **Purpose**: Generates realistic funnel data for analysis
- **Functionality**: Creates synthetic data based on traffic sources and time periods
- **Key Features**:
  - Multiple traffic source support (Google Ads, Facebook Ads, Organic, Direct, Email)
  - Time period multipliers for different analysis windows
  - Realistic conversion rate simulation

### 3. AIInsights (`ai_insights.py`)
- **Purpose**: Generates AI-powered recommendations using OpenAI GPT-4o
- **Functionality**: Analyzes funnel data and provides actionable insights
- **Key Features**:
  - Executive summary generation
  - Actionable recommendations
  - Priority-based optimization suggestions
  - JSON-structured output for easy parsing

### 4. Streamlit App (`app.py`)
- **Purpose**: Main user interface and application orchestration
- **Functionality**: Provides interactive dashboard with visualizations
- **Key Features**:
  - Wide layout configuration
  - Sidebar controls for analysis parameters
  - Real-time visualization updates
  - Component caching for performance

## Data Flow

1. **Configuration**: User sets analysis parameters (time period, traffic sources, thresholds)
2. **Data Generation**: DataGenerator creates synthetic funnel data based on parameters
3. **Analysis**: FunnelAnalyzer processes data to identify drop-offs and conversion rates
4. **Visualization**: Plotly generates interactive charts and graphs
5. **AI Insights**: AIInsights generates recommendations based on analysis results
6. **Display**: Streamlit renders the complete dashboard with insights

## External Dependencies

### Required Libraries
- `streamlit`: Web application framework
- `pandas`: Data manipulation and analysis
- `plotly`: Interactive visualization library
- `openai`: AI insights generation
- `datetime`: Date/time handling

### API Integrations
- **OpenAI GPT-4o**: For generating AI-powered insights and recommendations
- **Authentication**: Uses OPENAI_API_KEY environment variable

## Deployment Strategy

### Current Setup
- **Platform**: Designed for Replit deployment
- **Configuration**: Streamlit app with page configuration optimized for wide layout
- **Environment**: Requires OPENAI_API_KEY environment variable
- **Dependencies**: Standard Python packages installable via pip

### Scalability Considerations
- **Caching**: Implements Streamlit caching for component initialization
- **Modular Architecture**: Separate classes allow for easy testing and maintenance
- **API Management**: Graceful handling of missing API keys

## User Preferences

Preferred communication style: Simple, everyday language.

## Changelog

Changelog:
- July 04, 2025. Initial setup