from rasa_sdk import Action
from rasa_sdk.events import SlotSet

class ActionFetchCalendarDeadline(Action):
    def name(self) -> str:
        return "action_fetch_calendar_deadline"

    async def run(self, dispatcher, tracker, domain):
        # Placeholder for fetching academic calendar deadline (e.g., via API or static data)
        # For now, using static response as no API is provided
        deadline = "Check the USIU website (www.usiu.ac.ke) for the current academic calendar deadlines."
        dispatcher.utter_message(text=f"The graduation application deadline is: {deadline}")
        return []