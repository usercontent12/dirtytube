def seconds_to_iso8601(duration):
    """
    Accepts:
    - int seconds
    - 'MM:SS'
    - 'HH:MM:SS'
    """
    if duration is None:
        return "PT0S"

    # If already an integer seconds
    if isinstance(duration, int):
        total_seconds = duration

    # If string like "5:20" or "01:12:45"
    elif isinstance(duration, str):
        parts = duration.split(":")
        parts = [int(p) for p in parts]  # convert to ints

        if len(parts) == 3:
            hours, minutes, seconds = parts
        elif len(parts) == 2:
            hours = 0
            minutes, seconds = parts
        else:
            raise ValueError(f"Invalid duration format: {duration}")

        total_seconds = hours * 3600 + minutes * 60 + seconds

    else:
        # fallback
        total_seconds = int(duration)

    # Build ISO8601
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    iso = "PT"
    if hours > 0:
        iso += f"{hours}H"
    if minutes > 0:
        iso += f"{minutes}M"
    if seconds > 0 or (hours == 0 and minutes == 0):
        iso += f"{seconds}S"

    return iso
