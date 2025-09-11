from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from typing import Dict, Any, List
import icalendar
import pytz

class CalendarIntegration:
    def __init__(self):
        self.google_service = None
        self.outlook_service = None
        
    async def sync_to_google_calendar(
        self, 
        credentials: Credentials,
        project_data: Dict[str, Any]
    ) -> List[str]:
        """Sync project tasks to Google Calendar"""
        
        service = build('calendar', 'v3', credentials=credentials)
        
        # Create a project calendar
        calendar = {
            'summary': f"AgentPlanner: {project_data['description'][:50]}",
            'description': project_data['description'],
            'timeZone': 'America/New_York'
        }
        
        created_calendar = service.calendars().insert(body=calendar).execute()
        calendar_id = created_calendar['id']
        
        # Add tasks as events
        event_ids = []
        start_date = datetime.now()
        
        for task in project_data['tasks']:
            event = {
                'summary': f"[{task['category'].upper()}] {task['name']}",
                'description': self._create_event_description(task),
                'start': {
                    'date': (start_date + timedelta(days=task.get('start_day', 0))).isoformat()[:10]
                },
                'end': {
                    'date': (start_date + timedelta(
                        days=task.get('start_day', 0) + task['duration']
                    )).isoformat()[:10]
                },
                'colorId': self._get_color_id(task['complexity']),
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                        {'method': 'popup', 'minutes': 60},  # 1 hour before
                    ],
                },
            }
            
            # Add milestones as separate events
            if task.get('is_milestone'):
                event['transparency'] = 'transparent'
                event['colorId'] = '11'  # Red for milestones
            
            created_event = service.events().insert(
                calendarId=calendar_id,
                body=event
            ).execute()
            
            event_ids.append(created_event['id'])
        
        return {
            'calendar_id': calendar_id,
            'calendar_link': created_calendar['htmlLink'],
            'events_created': event_ids
        }
    
    async def generate_ics_file(self, project_data: Dict[str, Any]) -> bytes:
        """Generate ICS file for universal calendar import"""
        
        cal = icalendar.Calendar()
        cal.add('prodid', '-//AgentPlanner//AI Project Planning//EN')
        cal.add('version', '2.0')
        cal.add('calscale', 'GREGORIAN')
        cal.add('method', 'PUBLISH')
        cal.add('x-wr-calname', f"AgentPlanner: {project_data['description'][:50]}")
        cal.add('x-wr-timezone', 'UTC')
        
        start_date = datetime.now(pytz.UTC)
        
        for task in project_data['tasks']:
            event = icalendar.Event()
            event.add('summary', f"[{task['category'].upper()}] {task['name']}")
            event.add('description', self._create_event_description(task))
            event.add('dtstart', start_date + timedelta(days=task.get('start_day', 0)))
            event.add('dtend', start_date + timedelta(
                days=task.get('start_day', 0) + task['duration']
            ))
            event.add('dtstamp', datetime.now(pytz.UTC))
            event.add('uid', f"{task['id']}@agentplanner.ai")
            
            # Add categories
            event.add('categories', [task['category'], task['complexity']])
            
            # Add alarm/reminder
            alarm = icalendar.Alarm()
            alarm.add('action', 'DISPLAY')
            alarm.add('description', f"Task starting: {task['name']}")
            alarm.add('trigger', timedelta(hours=-1))
            event.add_component(alarm)
            
            cal.add_component(event)
        
        # Add milestones
        for milestone in project_data.get('milestones', []):
            event = icalendar.Event()
            event.add('summary', f"🎯 MILESTONE: {milestone['name']}")
            event.add('description', milestone['description'])
            event.add('dtstart', start_date + timedelta(days=milestone['target_date']))
            event.add('dtend', start_date + timedelta(days=milestone['target_date']))
            event.add('priority', 1)
            cal.add_component(event)
        
        return cal.to_ical()
    
    def _create_event_description(self, task: Dict) -> str:
        return f"""
Task: {task['name']}
Description: {task['description']}
Category: {task['category']}
Complexity: {task['complexity']}
Duration: {task['duration']} days
Dependencies: {', '.join(task.get('dependencies', []))}

Resources Required:
{task.get('resources', {}).get('required_roles', 'TBD')}

Estimated Cost: ${task.get('estimated_cost', 'TBD')}
"""