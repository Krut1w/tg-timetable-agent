import httpx
from datetime import datetime

def parse_spbu_url(url: str) -> int | None:
    parts = url.split("/")
    try:
        return int(parts[6])
    except (IndexError, ValueError):
        return None

async def get_schedule(group_id: int) ->dict | None:
    date = datetime.now().strftime("%Y-%m-%d")
    url = f"https://timetable.spbu.ru/api/v1/groups/{group_id}/events/{date}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return response.json()
    except Exception:
        return None

def format_schedule(data:dict) -> str:
    result = ""

    for day in data["Days"]:
        result += f"\n📅 {day['DayString']}\n"

        for event in day["DayStudyEvents"]:
            result += f"\n⏰ {event['TimeIntervalString']}\n"
            result += f"{event['Subject']}\n"
            result += f"📍 {event['LocationsDisplayText']}\n"
    return result