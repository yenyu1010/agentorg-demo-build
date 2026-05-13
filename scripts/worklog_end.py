import json, sys, datetime

fpath = sys.argv[1]
status = sys.argv[2]
summary = sys.argv[3]

with open(fpath, 'r', encoding='utf-8') as f:
    data = json.load(f)

data['end_time'] = datetime.datetime.now().isoformat()
data['status'] = status
data['output_summary'] = summary

# Calculate duration if start_time exists
if 'start_time' in data:
    try:
        start = datetime.datetime.fromisoformat(data['start_time'])
        end = datetime.datetime.fromisoformat(data['end_time'])
        duration_min = round((end - start).total_seconds() / 60, 1)
        data['duration_minutes'] = duration_min
    except:
        pass

with open(fpath, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Worklog closed: {fpath}")
print(f"Status: {status}")
if 'duration_minutes' in data:
    print(f"Duration: {data['duration_minutes']} minutes")
