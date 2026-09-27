def build_trip_prompt(destination: str, preferences: str = "") -> str:
    return f"Create a practical trip plan for {destination}. Preferences: {preferences}".strip()
