import asyncio
from services.spbu_api import parse_spbu_url, get_schedule, format_schedule

url = "https://timetable.spbu.ru/AMCP/StudentGroupEvents/Primary/428711/2026-04-19"
parts = url.split("/")
print(parts)

async def main():
    url = "https://timetable.spbu.ru/AMCP/StudentGroupEvents/Primary/428711/2026-04-19"
    
    group_id = parse_spbu_url(url)
    print(f"group_id: {group_id}")
    
    data = await get_schedule(group_id)
    text = format_schedule(data)
    print(text)

asyncio.run(main())