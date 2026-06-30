
import json
from datetime import datetime
from .database.db_setup import create_tables
from .database.db_operations import (
    get_or_create_user,
    save_study_plan,
    get_study_plan,
    get_all_plans,
    mark_task_complete,
    get_progress,
    save_message,
    get_conversation_history
)

class PersistentMemory:
    """
    Purani SharedMemory = RAM mein sab kuch
    Nayi PersistentMemory = Database mein sab kuch

    Fark:
    Purani → Restart karo → Gone
    Nayi   → Restart karo → Sab safe!
    """

    def __init__(self, session_id="default"):
        self.session_id = session_id
        # Database tables banao agar nahi hain
        create_tables()
        # User register karo
        get_or_create_user(session_id)
        print(f"✅ PersistentMemory ready for session: {session_id[:8]}")

    def save_plan(self, topic, plan_data):
        """Plan database mein save karo."""
        save_study_plan(self.session_id, topic, plan_data)

    def get_plan(self, topic):
        """Database se plan nikalo."""
        return get_study_plan(self.session_id, topic)

    def mark_complete(self, topic, task):
        """Task complete karo."""
        mark_task_complete(self.session_id, topic, task)

    def get_progress_summary(self, topic):
        """Progress nikalo."""
        return get_progress(self.session_id, topic)

    def get_today_task(self, topic):
        """Aaj ka task nikalo."""
        plan = self.get_plan(topic)
        if not plan:
            return None
        start  = datetime.fromisoformat(plan["start_date"])
        day_no = (datetime.now() - start).days + 1
        for entry in plan.get("schedule", []):
            if entry.get("day") == day_no:
                return entry.get("task")
        return None

    def save_conversation(self, role, message, agent=""):
        """Message save karo."""
        save_message(self.session_id, role, message, agent)

    def get_history(self, limit=10):
        """Conversation history nikalo."""
        return get_conversation_history(self.session_id, limit)

    def log(self, agent, action, detail=""):
        """Simple log — agent ka kaam record karo."""
        print(f"[{agent}] {action} — {detail}")

    @property
    def study_plans(self):
        """Backward compatibility ke liye."""
        plans = get_all_plans(self.session_id)
        result = {}
        for p in plans:
            full = self.get_plan(p["topic"])
            if full:
                result[p["topic"]] = full
        return result
