"""
Constants and Configuration Values
"""

# MVP Country List (20-30 countries)
MVP_COUNTRIES = [
    # Developed Markets
    'USA',  # United States
    'GBR',  # United Kingdom
    'DEU',  # Germany
    'FRA',  # France
    'JPN',  # Japan
    'CAN',  # Canada
    'AUS',  # Australia
    'KOR',  # South Korea

    # Emerging Markets - Asia
    'CHN',  # China
    'IND',  # India
    'IDN',  # Indonesia
    'THA',  # Thailand
    'VNM',  # Vietnam
    'MYS',  # Malaysia
    'PHL',  # Philippines

    # Emerging Markets - Latin America
    'BRA',  # Brazil
    'MEX',  # Mexico
    'CHL',  # Chile
    'COL',  # Colombia
    'ARG',  # Argentina

    # Emerging Markets - Europe/Middle East/Africa
    'TUR',  # Turkey
    'POL',  # Poland
    'ZAF',  # South Africa
    'SAU',  # Saudi Arabia
    'ARE',  # UAE

    # Frontier Markets
    'EGY',  # Egypt
    'NGA',  # Nigeria
    'KEN',  # Kenya
]

# Indicator Definitions
INDICATORS = {
    # External Sector Momentum (25%)
    'fx_momentum': {
        'name': 'FX Momentum',
        'pillar': 'external_sector',
        'weight': 0.40,
        'source': 'IMF',
        'calculation': 'pct_change_6m',
        'frequency': 'monthly'
    },
    'fx_reserves_change': {
        'name': 'FX Reserves Change',
        'pillar': 'external_sector',
        'weight': 0.30,
        'source': 'IMF',
        'calculation': 'pct_change_6m',
        'frequency': 'monthly'
    },
    'export_growth_momentum': {
        'name': 'Export Growth Momentum',
        'pillar': 'external_sector',
        'weight': 0.30,
        'source': 'World Bank',
        'calculation': 'yoy_acceleration',
        'frequency': 'quarterly'
    },

    # Inflation & Price Momentum (20%)
    'cpi_acceleration': {
        'name': 'CPI YoY Acceleration',
        'pillar': 'inflation',
        'weight': 0.70,
        'source': 'IMF',
        'calculation': 'yoy_acceleration',
        'frequency': 'monthly'
    },
    'core_cpi_acceleration': {
        'name': 'Core CPI Acceleration',
        'pillar': 'inflation',
        'weight': 0.30,
        'source': 'OECD',
        'calculation': 'yoy_acceleration',
        'frequency': 'monthly'
    },

    # Real Activity Momentum (20%)
    'industrial_production_acceleration': {
        'name': 'Industrial Production YoY Acceleration',
        'pillar': 'real_activity',
        'weight': 0.60,
        'source': 'OECD',
        'calculation': 'yoy_acceleration',
        'frequency': 'monthly'
    },
    'pmi': {
        'name': 'Manufacturing PMI',
        'pillar': 'real_activity',
        'weight': 0.40,
        'source': 'OECD',
        'calculation': 'raw_value',  # PMI is already a diffusion index
        'frequency': 'monthly'
    },

    # Monetary & Financial Conditions (20%)
    'policy_rate_change': {
        'name': 'Policy Rate Change',
        'pillar': 'monetary_financial',
        'weight': 0.40,
        'source': 'IMF',
        'calculation': 'absolute_change_12m',
        'frequency': 'monthly'
    },
    'balance_sheet_growth': {
        'name': 'Central Bank Balance Sheet Growth',
        'pillar': 'monetary_financial',
        'weight': 0.30,
        'source': 'IMF',
        'calculation': 'pct_change_12m',
        'frequency': 'monthly'
    },
    'credit_growth': {
        'name': 'Private Sector Credit Growth YoY',
        'pillar': 'monetary_financial',
        'weight': 0.30,
        'source': 'BIS',
        'calculation': 'yoy',
        'frequency': 'quarterly'
    },

    # Structural / Capacity Score (15%)
    'education_index': {
        'name': 'Education / Human Capital Index',
        'pillar': 'structural',
        'weight': 0.40,
        'source': 'UNDP',
        'calculation': 'raw_value',
        'frequency': 'annual'
    },
    'industry_composition': {
        'name': 'Industrial Value Added (% of GDP)',
        'pillar': 'structural',
        'weight': 0.40,
        'source': 'World Bank',
        'calculation': 'raw_value',
        'frequency': 'annual'
    },
    'diversification': {
        'name': 'Export Diversification Index',
        'pillar': 'structural',
        'weight': 0.20,
        'source': 'World Bank',
        'calculation': 'raw_value',
        'frequency': 'annual'
    },
}

# Country coordinates for map visualization (sample - should be expanded)
COUNTRY_COORDINATES = {
    'USA': (37.09, -95.71),
    'GBR': (55.38, -3.44),
    'DEU': (51.17, 10.45),
    'FRA': (46.23, 2.21),
    'JPN': (36.20, 138.25),
    'CAN': (56.13, -106.35),
    'AUS': (-25.27, 133.78),
    'KOR': (35.91, 127.77),
    'CHN': (35.86, 104.20),
    'IND': (20.59, 78.96),
    'IDN': (-0.79, 113.92),
    'THA': (15.87, 100.99),
    'VNM': (14.06, 108.28),
    'MYS': (4.21, 101.98),
    'PHL': (12.88, 121.77),
    'BRA': (-14.24, -51.93),
    'MEX': (23.63, -102.55),
    'CHL': (-35.68, -71.54),
    'COL': (4.57, -74.30),
    'ARG': (-38.42, -63.62),
    'TUR': (38.96, 35.24),
    'POL': (51.92, 19.15),
    'ZAF': (-30.56, 22.94),
    'SAU': (23.89, 45.08),
    'ARE': (23.42, 53.85),
    'EGY': (26.82, 30.80),
    'NGA': (9.08, 8.68),
    'KEN': (-0.02, 37.91),
}
