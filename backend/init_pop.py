import os
import django
import random

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")  # Replace with your project's settings
django.setup()

from api.models import NFLTeamStats  # Replace `my_app` with your Django app name

# Teams list for random selection
teams = [
    "ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE", "DAL", "DEN",
    "DET", "GB", "HOU", "IND", "JAX", "KC", "LV", "LAC", "LAR", "MIA",
    "MIN", "NE", "NO", "NYG", "NYJ", "PHI", "PIT", "SEA", "SF", "TB",
    "TEN", "WAS"
]

# Function to generate random data
def generate_random_data(num_records=10):
    data = []
    for _ in range(num_records):
        data.append(NFLTeamStats(
            team=random.choice(teams),
            season=random.randint(2000, 2024),
            week=random.randint(1, 17),
            total_snaps=random.randint(50, 80),
            yards_gained=round(random.uniform(200, 600), 1),
            touchdown=random.randint(0, 7),
            extra_point_attempt=random.randint(0, 7),
            field_goal_attempt=random.randint(0, 7),
            total_points=round(random.uniform(0, 50), 1),
            td_points=round(random.uniform(0, 42), 1),
            xp_points=round(random.uniform(0, 7), 1),
            fg_points=round(random.uniform(0, 15), 1),
            fumble=random.randint(0, 5),
            fumble_lost=random.randint(0, 3),
            shotgun=random.randint(10, 50),
            no_huddle=random.randint(0, 10),
            qb_dropback=random.randint(20, 40),
            pass_snaps_count=random.randint(30, 50),
            pass_snaps_pct=round(random.uniform(50, 80), 1),
            pass_attempts=random.randint(20, 50),
            complete_pass=random.randint(10, 40),
            incomplete_pass=random.randint(5, 20),
            air_yards=round(random.uniform(100, 400), 1),
            passing_yards=round(random.uniform(100, 500), 1),
            pass_td=random.randint(0, 5),
            interception=random.randint(0, 3),
            targets=random.randint(10, 50),
            receptions=random.randint(10, 50),
            receiving_yards=round(random.uniform(50, 300), 1),
            yards_after_catch=round(random.uniform(10, 150), 1),
            receiving_td=random.randint(0, 3),
            pass_fumble=random.randint(0, 2),
            pass_fumble_lost=random.randint(0, 2),
            rush_snaps_count=random.randint(10, 50),
            rush_snaps_pct=round(random.uniform(20, 50), 1),
            qb_scramble=random.randint(0, 5),
            rushing_yards=round(random.uniform(50, 300), 1),
            run_td=random.randint(0, 3),
            run_fumble=random.randint(0, 2),
            run_fumble_lost=random.randint(0, 2),
            home_wins=random.randint(0, 8),
            home_losses=random.randint(0, 8),
            home_ties=random.randint(0, 1),
            away_wins=random.randint(0, 8),
            away_losses=random.randint(0, 8),
            away_ties=random.randint(0, 1),
            wins=random.randint(0, 16),
            losses=random.randint(0, 16),
            ties=random.randint(0, 1),
            win_pct=round(random.uniform(0, 1), 3),
            record=f"{random.randint(0, 16)}-{random.randint(0, 16)}-{random.randint(0, 1)}",
            yps=round(random.uniform(4, 8), 2)
        ))
    return data

# Generate random data and insert it into the database
num_records = 10  # Adjust the number of records as needed
random_data = generate_random_data(num_records)
NFLTeamStats.objects.bulk_create(random_data)

print(f"Successfully inserted {num_records} random records into the NFLTeamStats model!")
