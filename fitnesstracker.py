import hashlib
from datetime import datetime, timedelta
import matplotlib.pyplot as plt  # For plotting weight history

# Constants
GOAL_TYPES = ['Weight Loss', 'Muscle Gain', 'Maintenance']
ACHIEVEMENTS = {
    'First Workout': 'Complete your first workout',
    'Fitness Enthusiast': 'Complete 10 workouts',
    'Diet Champ': 'Track your diet for a week'
}

# Error handling utility
def input_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

# Reminder Scheduling
class Reminder:
    def __init__(self, message, remind_date):
        self.message = message
        self.remind_date = remind_date

    def __str__(self):
        return f"Reminder: {self.message} on {self.remind_date}"

class Workout:
    def __init__(self, name, duration, calories_burned, workout_type='General'):
        self.name = name
        self.duration = duration
        self.calories_burned = calories_burned
        self.type = workout_type

class Diet:
    def __init__(self, name, calories_consumed, proteins=0, carbs=0, fats=0):
        self.name = name
        self.calories_consumed = calories_consumed
        self.proteins = proteins
        self.carbs = carbs
        self.fats = fats

class User:
    def __init__(self, username, password, name, age, height, weight, goal):
        self.username = username
        self.password = hashlib.sha256(password.encode()).hexdigest()
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight
        self.goal = goal
        self.workouts = []
        self.diets = []
        self.achievements = []
        self.goal_plan = {"sub_goals": [], "deadline": None}
        self.reminders = []
        self.weight_history = [(datetime.now(), weight)]

    def update_weight(self, new_weight):
        self.weight_history.append((datetime.now(), new_weight))
        self.weight = new_weight
        return f"Weight updated to {new_weight}."

    def plot_weight_history(self):
        dates = [record[0] for record in self.weight_history]
        weights = [record[1] for record in self.weight_history]
        plt.plot(dates, weights, marker='o')
        plt.title(f"Weight History for {self.name}")
        plt.xlabel("Date")
        plt.ylabel("Weight (kg)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(True)
        plt.show()
    
    def add_reminder(self, message, remind_date):
        reminder = Reminder(message, remind_date)
        self.reminders.append(reminder)
        return f"Reminder set: {message} on {remind_date}"

    def add_workout(self, workout):
        self.workouts.append(workout)
        self.check_achievements()
        return f"Workout {workout.name} added."

    def add_diet(self, diet):
        self.diets.append(diet)
        self.check_achievements()
        return f"Diet {diet.name} added."

    def check_achievements(self):
        if len(self.workouts) == 1 and 'First Workout' not in self.achievements:
            self.achievements.append('First Workout')
        if len(self.workouts) >= 10 and 'Fitness Enthusiast' not in self.achievements:
            self.achievements.append('Fitness Enthusiast')
        if len(self.diets) >= 7 and 'Diet Champ' not in self.achievements:
            self.achievements.append('Diet Champ')

    def set_goal_deadline(self, days_from_now):
        self.goal_plan["deadline"] = datetime.now() + timedelta(days=days_from_now)

    def add_sub_goal(self, sub_goal):
        self.goal_plan["sub_goals"].append(sub_goal)

    def visualize_achievements(self):
        print("\nAchievement Summary for", self.name)
        for achievement in self.achievements:
            print(f"- {achievement}: {ACHIEVEMENTS[achievement]}")

class FitnessTracker:
    def __init__(self):
        self.users = []

    def register_user(self, username, password, name, age, height, weight, goal):
        if goal not in GOAL_TYPES:
            return "Invalid goal type."
        if self.find_user_by_username(username):
            return "Username already exists."
        user = User(username, password, name, age, height, weight, goal)
        self.users.append(user)
        return f"User {name} registered."

    def login(self, username, password):
        user = self.find_user_by_username(username)
        if user and user.password == hashlib.sha256(password.encode()).hexdigest():
            return f"Welcome back {user.name}!"
        return "Invalid login credentials."

    def find_user_by_username(self, username):
        return next((user for user in self.users if user.username == username), None)

    def get_user(self, username):
        return self.find_user_by_username(username)

    def list_users(self):
        return [user.name for user in self.users] if self.users else ["No users available"]

    def user_summary(self, username):
        user = self.get_user(username)
        if not user:
            return f"User {username} not found."
        return f"{user.name}: {len(user.workouts)} workouts, {len(user.diets)} diets recorded. Achievements: {', '.join(user.achievements) if user.achievements else 'None'}."

    def view_user_trends(self, username):
        user = self.get_user(username)
        if not user:
            return f"User {username} not found."
        total_burned = sum(workout.calories_burned for workout in user.workouts)
        total_consumed = sum(diet.calories_consumed for diet in user.diets)
        net_calories = total_consumed - total_burned
        return f"User {username} has a net calorie count of {net_calories}."

    def export_user_data(self, username):
        user = self.get_user(username)
        if not user:
            return f"User {username} not found."
        with open(f'{username}_data.csv', 'w', newline='') as csvfile:
            fieldnames = ['workout_name', 'duration', 'calories_burned', 'diet_name', 'calories_consumed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for workout in user.workouts:
                writer.writerow({'workout_name': workout.name, 'duration': workout.duration, 'calories_burned': workout.calories_burned})
            for diet in user.diets:
                writer.writerow({'diet_name': diet.name, 'calories_consumed': diet.calories_consumed})
        return f"Data for {user.name} exported."

    def switch_user(self, current_username, target_username):
        current_user = self.find_user_by_username(current_username)
        target_user = self.find_user_by_username(target_username)
        if not target_user:
            return f"User {target_username} not found."
        self.current_user = target_user
        return f"Switched to {target_user.name}. Please re-enter password for security."

    def list_user_achievements(self, username):
        user = self.get_user(username)
        if not user:
            return f"User {username} not found."
        user.visualize_achievements()
        return "Achievements displayed."

    def add_detailed_workout(self, username, workout_name, duration, calories_burned, workout_type):
        user = self.get_user(username)
        if not user:
            return f"User {username} not found."
        workout = Workout(workout_name, duration, calories_burned, workout_type)
        return user.add_workout(workout)

    def add_detailed_diet(self, username, diet_name, calories, proteins, carbs, fats):
        user = self.get_user(username)
        if not user:
            return f"User {username} not found."
        diet = Diet(diet_name, calories, proteins, carbs, fats)
        return user.add_diet(diet)

    def user_social_interaction(self, giver_username, receiver_username, note):
        giver = self.get_user(giver_username)
        receiver = self.get_user(receiver_username)
        if not receiver:
            return f"User {receiver_username} not found."
        if not giver:
            return f"User {giver_username} not recognized."
        return f"{giver.name} says to {receiver.name}: {note}"

    def set_reminder_for_user(self, username, message, date):
        user = self.get_user(username)
        if not user:
            return f"User {username} not found."
        return user.add_reminder(message, date)

    def show_all_reminders(self, username):
        user = self.get_user(username)
        if not user:
            return f"User {username} not found."
        if not user.reminders:
            return "No reminders set."
        return "\n".join(str(reminder) for reminder in user.reminders)

def main():
    tracker = FitnessTracker()

    while True:
        print("\n=== Fitness Tracker Management ===")
        print("1. Register")
        print("2. Login")
        print("3. List Users")
        print("4. Switch User")
        print("5. Add Detailed Workout for User")
        print("6. Add Detailed Diet for User")
        print("7. User Summary")
        print("8. View User Trends")
        print("9. Export User Data")
        print("10. Set User Goal Deadline")
        print("11. Add Sub-Goal to User")
        print("12. List User Achievements")
        print("13. Set Reminder for User")
        print("14. Show All Reminders for User")
        print("15. Social Note to Another User")
        print("16. Visualize Weight History")
        print("17. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            name = input("Enter user's name: ")
            age = int(input("Enter user's age: "))
            height = input_float("Enter user's height (in cm): ")
            weight = input_float("Enter user's weight (in kg): ")
            goal = input(f"Enter user's goal ({', '.join(GOAL_TYPES)}): ")
            print(tracker.register_user(username, password, name, age, height, weight, goal))

        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            print(tracker.login(username, password))

        elif choice == "3":
            users = tracker.list_users()
            for user in users:
                print(user)

        elif choice == "4":
            current_username = input("Enter current username: ")
            target_username = input("Enter target username: ")
            print(tracker.switch_user(current_username, target_username))

        elif choice == "5":
            username = input("Enter user's username: ")
            workout_name = input("Enter workout name: ")
            duration = input_float("Enter duration (in minutes): ")
            calories_burned = input_float("Enter calories burned: ")
            workout_type = input("Enter workout type (Cardio, Strength, etc.): ")
            print(tracker.add_detailed_workout(username, workout_name, duration, calories_burned, workout_type))

        elif choice == "6":
            username = input("Enter user's username: ")
            diet_name = input("Enter diet name: ")
            calories_consumed = input_float("Enter calories consumed: ")
            proteins = input_float("Enter proteins (in grams): ")
            carbs = input_float("Enter carbohydrates (in grams): ")
            fats = input_float("Enter fats (in grams): ")
            print(tracker.add_detailed_diet(username, diet_name, calories_consumed, proteins, carbs, fats))

        elif choice == "7":
            username = input("Enter user's username: ")
            print(tracker.user_summary(username))

        elif choice == "8":
            username = input("Enter user's username: ")
            print(tracker.view_user_trends(username))

        elif choice == "9":
            username = input("Enter user's username: ")
            print(tracker.export_user_data(username))

        elif choice == "10":
            username = input("Enter user's username: ")
            days = int(input("Enter number of days for the goal deadline: "))
            user = tracker.get_user(username)
            if user:
                user.set_goal_deadline(days)
                print(f"Deadline set for {user.name}'s goal.")

        elif choice == "11":
            username = input("Enter user's username: ")
            sub_goal = input("Describe the sub-goal: ")
            user = tracker.get_user(username)
            if user:
                user.add_sub_goal(sub_goal)
                print(f"Sub-goal '{sub_goal}' added for {user.name}.")

        elif choice == "12":
            username = input("Enter user's username: ")
            print(tracker.list_user_achievements(username))

        elif choice == "13":
            username = input("Enter user's username: ")
            message = input("Enter reminder message: ")
            remind_date = input("Enter reminder date (YYYY-MM-DD): ")
            print(tracker.set_reminder_for_user(username, message, remind_date))

        elif choice == "14":
            username = input("Enter user's username: ")
            print(tracker.show_all_reminders(username))

        elif choice == "15":
            giver_username = input("Enter your username: ")
            receiver_username = input("Enter receiver's username: ")
            note = input("Enter your message: ")
            print(tracker.user_social_interaction(giver_username, receiver_username, note))

        elif choice == "16":
            username = input("Enter user's username: ")
            user = tracker.get_user(username)
            if user:
                user.plot_weight_history()
            else:
                print("User not found.")

        elif choice == "17":
            print("Exiting the system.")
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()

