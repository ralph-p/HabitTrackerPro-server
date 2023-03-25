from datetime import datetime, timedelta

def get_token(request):
    if(request):
        headers = request.headers
        bearer = headers.get('Authorization')    # Bearer YourTokenHere
        token = bearer.split()[1]
        return token
    return ''

def convert_DTO_task_list(tasks):
    for task in tasks:
        task = convert_DTO_to_task(task)
        task.pop('task_note', None)
        task.pop('subtask', None)
        # del task['subtask']
    return tasks

def convert_DTO_to_task(task):
    if(task['task_note'] and task['subtask']):
        frequency = task['frequency']
        newest_note = max(task['task_note'], key=lambda x: x['inserted_at'])
        updated_at = datetime.fromisoformat(newest_note['inserted_at'])
        task['updated_at'] = updated_at.strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')

        time_in_frequency = 0
        if frequency == 0:
            # 0 for today
            today = datetime.utcnow().date()
            for note in task['task_note']:
                note_date = datetime.fromisoformat(note['inserted_at']).date()
                if note_date == today:
                    time_in_frequency += note['time']
        elif frequency == 1:
            # 1 for this week
            today = datetime.utcnow().date()
            week_start = today - timedelta(days=today.weekday())
            week_end = week_start + timedelta(days=6)
            for note in task['task_note']:
                note_date = datetime.fromisoformat(note['inserted_at']).date()
                if week_start <= note_date <= week_end:
                    time_in_frequency += note['time']
        elif frequency == 2:
            # 2 for this month
            today = datetime.utcnow().date()
            month_start = today.replace(day=1)
            month_end = month_start.replace(month=month_start.month+1) - timedelta(days=1)
            for note in task['task_note']:
                note_date = datetime.fromisoformat(note['inserted_at']).date()
                if month_start <= note_date <= month_end:
                    time_in_frequency += note['time']
                    
        task['amount_done'] = time_in_frequency
        task['num_subtask'] = len(task['subtask'])
    return task