import datetime as dt


def year(request):
    """Add current year to templates."""
    current_year = dt.date.today().year

    return {'year': current_year}
