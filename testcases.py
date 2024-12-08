import unittest
from datetime import datetime
from fitnesstracker import FitnessTracker, Workout, Diet

class TestFitnessTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = FitnessTracker()
        self.tracker.register_user("jdoe", "password123", "John Doe", 30, 175, 70, "Weight Loss")

    def test_register_user(self):
        result = self.tracker.register_user("jsmith", "secret456", "Jane Smith", 28, 160, 55, "Muscle Gain")
        self.assertIn("registered", result)

    def test_login_user(self):
        result = self.tracker.login("jdoe", "password123")
        self.assertIn("Welcome back John Doe", result)

    def test_invalid_login(self):
        result = self.tracker.login("jdoe", "wrongpassword")
        self.assertIn("Invalid login credentials", result)

    def test_duplicate_user_registration(self):
        result = self.tracker.register_user("jdoe", "newpass789", "John Doe", 30, 175, 70, "Weight Loss")
        self.assertIn("already exists", result)

    def test_add_detailed_workout(self):
        self.tracker.login("jdoe", "password123")
        user = self.tracker.get_user("jdoe")
        if user:
            result = self.tracker.add_detailed_workout("jdoe", "Yoga Session", 60, 200, "Flexibility")
            self.assertIn("Workout Yoga Session added", result)

    def test_detailed_diet_entry(self):
        self.tracker.login("jdoe", "password123")
        result = self.tracker.add_detailed_diet("jdoe", "Protein Shake", 300, 30, 10, 5)
        self.assertIn("Diet Protein Shake added", result)

    def test_set_goal_deadline(self):
        user = self.tracker.get_user("jdoe")
        if user:
            user.set_goal_deadline(30)
            self.assertIsNotNone(user.goal_plan["deadline"])

    def test_add_sub_goal(self):
        user = self.tracker.get_user("jdoe")
        if user:
            user.add_sub_goal("Run 5km")
            self.assertIn("Run 5km", user.goal_plan["sub_goals"])

    def test_list_user_achievements(self):
        user = self.tracker.get_user("jdoe")
        if user:
            user.add_workout(Workout("Morning Run", 30, 300))
            result = self.tracker.list_user_achievements("jdoe")
            self.assertIn("Achievements displayed", result)

    def test_set_reminder(self):
        user = self.tracker.get_user("jdoe")
        if user:
            result = self.tracker.set_reminder_for_user("jdoe", "Work out!", "2023-11-05")
            self.assertIn("Reminder set", result)

    def test_show_reminders(self):
        self.tracker.set_reminder_for_user("jdoe", "Work out!", "2023-11-05")
        reminders = self.tracker.show_all_reminders("jdoe")
        self.assertIn("Reminder: Work out!", reminders)

    def test_social_interaction(self):
        self.tracker.register_user("jsmith", "password456", "Jane Smith", 28, 160, 55, "Muscle Gain")
        result = self.tracker.user_social_interaction("jdoe", "jsmith", "Keep pushing forward!")
        self.assertIn("says to Jane Smith", result)

    def test_weight_history_updates(self):
        user = self.tracker.get_user("jdoe")
        if user:
            user.update_weight(72)
            self.assertEqual(user.weight, 72)
            self.assertGreater(len(user.weight_history), 1)

    def test_plot_weight_history(self):
        user = self.tracker.get_user("jdoe")
        if user:
            user.update_weight(73)
            try:
                user.plot_weight_history()
                success = True
            except Exception as e:
                success = False
            self.assertTrue(success)

if __name__ == '__main__':
    unittest.main()