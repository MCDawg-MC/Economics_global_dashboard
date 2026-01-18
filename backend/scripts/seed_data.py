"""
Seed initial data to database
Populates countries and indicator definitions
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine, Base
from app.models import Country, Indicator
from app.utils.constants import MVP_COUNTRIES, INDICATORS, COUNTRY_COORDINATES


def seed_countries(db: Session):
    """
    Seed country data

    Args:
        db: Database session
    """
    print("Seeding countries...")

    country_names = {
        'USA': 'United States',
        'GBR': 'United Kingdom',
        'DEU': 'Germany',
        'FRA': 'France',
        'JPN': 'Japan',
        'CAN': 'Canada',
        'AUS': 'Australia',
        'KOR': 'South Korea',
        'CHN': 'China',
        'IND': 'India',
        'IDN': 'Indonesia',
        'THA': 'Thailand',
        'VNM': 'Vietnam',
        'MYS': 'Malaysia',
        'PHL': 'Philippines',
        'BRA': 'Brazil',
        'MEX': 'Mexico',
        'CHL': 'Chile',
        'COL': 'Colombia',
        'ARG': 'Argentina',
        'TUR': 'Turkey',
        'POL': 'Poland',
        'ZAF': 'South Africa',
        'SAU': 'Saudi Arabia',
        'ARE': 'United Arab Emirates',
        'EGY': 'Egypt',
        'NGA': 'Nigeria',
        'KEN': 'Kenya',
    }

    for country_code in MVP_COUNTRIES:
        # Check if country already exists
        existing = db.query(Country).filter(Country.code == country_code).first()
        if existing:
            print(f"  {country_code} already exists, skipping...")
            continue

        # Get coordinates
        coords = COUNTRY_COORDINATES.get(country_code, (None, None))

        # Create country
        country = Country(
            code=country_code,
            name=country_names.get(country_code, country_code),
            latitude=coords[0],
            longitude=coords[1],
            is_active=True
        )

        db.add(country)
        print(f"  Added {country_code} - {country.name}")

    db.commit()
    print(f"Seeded {len(MVP_COUNTRIES)} countries")


def seed_indicators(db: Session):
    """
    Seed indicator definitions

    Args:
        db: Database session
    """
    print("\nSeeding indicators...")

    for code, info in INDICATORS.items():
        # Check if indicator already exists
        existing = db.query(Indicator).filter(Indicator.code == code).first()
        if existing:
            print(f"  {code} already exists, skipping...")
            continue

        # Create indicator
        indicator = Indicator(
            code=code,
            name=info['name'],
            pillar=info['pillar'],
            weight_in_pillar=info['weight'],
            source=info['source'],
            calculation_method=info['calculation'],
            frequency=info['frequency']
        )

        db.add(indicator)
        print(f"  Added {code} - {info['name']}")

    db.commit()
    print(f"Seeded {len(INDICATORS)} indicators")


def main():
    """Main seeding function"""
    print("Starting database seeding...")

    # Create tables
    print("\nCreating tables...")
    Base.metadata.create_all(bind=engine)

    # Create session
    db = SessionLocal()

    try:
        # Seed data
        seed_countries(db)
        seed_indicators(db)

        print("\nDatabase seeding completed successfully!")

    except Exception as e:
        print(f"\nError during seeding: {e}")
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
