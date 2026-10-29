
# STEP 7: Travel Budget Calculator Tool

def calculate_budget(days, people, daily_food, daily_travel,
                     hotel_per_night, activities_per_person):
    """Calculate the estimated cost of a trip."""

    if days < 1 or people < 1:
        raise ValueError("Days and people must be at least 1.")

    if min(daily_food, daily_travel, hotel_per_night,
           activities_per_person) < 0:
        raise ValueError("Expenses cannot be negative.")

    food_cost = days * people * daily_food
    local_travel_cost = days * people * daily_travel
    hotel_cost = max(0, days - 1) * hotel_per_night
    activity_cost = days * people * activities_per_person

    total_cost = (
        food_cost
        + local_travel_cost
        + hotel_cost
        + activity_cost
    )

    return {
        "food": food_cost,
        "local_travel": local_travel_cost,
        "hotel": hotel_cost,
        "activities": activity_cost,
        "total": total_cost
    }
