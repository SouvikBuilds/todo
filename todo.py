from pymongo import MongoClient
import datetime
import random
import string


MONGO_URL = "mongodb+srv://SouvikBuilds:souvik1234@cluster0.r5l5h1i.mongodb.net/TodoCollection?retryWrites=true&w=majority"
client = MongoClient(MONGO_URL)
db = client["TodoCollection"]
collection = db["user"]


class Details:
    @staticmethod
    def get_title():
        title = input("Enter Title Of Note: ").strip()
        if not title:
            raise ValueError("Title can't be empty.")
        if title.isdigit():
            raise ValueError("Title can't be digits only.")
        return title

    @staticmethod
    def get_description():
        description = input("Enter Description: ").strip()
        if not description:
            raise ValueError("Description can't be empty.")
        return description

    @staticmethod
    def get_status():
        status = input("Enter C for Complete and NC for Incomplete: ").strip().upper()
        if status not in ("C", "NC"):
            raise ValueError("Invalid status. Use 'C' or 'NC'.")
        print("✅" if status == "C" else "❌")
        return status

    @staticmethod
    def get_date():
        year = int(input("Enter Year: "))
        month = int(input("Enter Month: "))
        day = int(input("Enter Day: "))
        date = datetime.date(year, month, day)
        formatted_date = date.strftime("%d-%m-%Y")
        print(f"DateStamp: {formatted_date}")
        return formatted_date

    @staticmethod
    def get_id():
        prefix = "TAS"
        while True:
            suffix = ''.join(random.choices(string.ascii_uppercase, k=6))
            task_id = f"{prefix}{suffix}"
            if not collection.find_one({"task_id": task_id}):
                return task_id

class Management:
    @staticmethod
    def add_notes():
        n = int(input("Enter number of today's works: "))
        for _ in range(n):
            try:
                title = Details.get_title()
                description = Details.get_description()
                task_id = Details.get_id()
                datestamp = Details.get_date()
                status = Details.get_status()

                result = collection.insert_one({
                    "title": title,
                    "description": description,
                    "task_id": task_id,
                    "datestamp": datestamp,
                    "status": status
                })
                print(f"🟢 Task {task_id} added successfully.")
            except ValueError as e:
                print(f"❌ Error: {e}")

    @staticmethod
    def view_notes():
        tasks = collection.find()
        print("\n📋 All Tasks:")
        found = False
        for task in tasks:
            found = True
            print("-" * 40)
            print(f"🆔 Task ID: {task['task_id']}")
            print(f"📌 Title: {task['title']}")
            print(f"📝 Description: {task['description']}")
            print(f"📅 Date: {task['datestamp']}")
            print(f"✅ Status: {task['status']}")
        if not found:
            print("No tasks found.")

    @staticmethod
    def update_notes():
        task_id = input("Enter Task ID to update: ").strip().upper()
        if len(task_id) != 9:
            raise ValueError("Invalid Task ID length.")
        task = collection.find_one({"task_id": task_id})
        if task:
            print(f"🔄 Task Found: {task['title']} - {task['status']}")
            title = input("Enter new title (leave blank to skip): ").strip()
            description = input("Enter new description (leave blank to skip): ").strip()
            status = input("Enter updated status (C/NC) (leave blank to skip): ").strip().upper()

            updates = {}
            if title:
                updates["title"] = title
            if description:
                updates["description"] = description
            if status in ("C", "NC"):
                updates["status"] = status

            if updates:
                collection.update_one({"task_id": task_id}, {"$set": updates})
                print("✅ Task updated successfully.")
            else:
                print("⚠️ No updates provided.")
        else:
            print(f"❌ No task found with ID {task_id}")

    @staticmethod
    def delete_notes():
        task_id = input("Enter Task ID to delete: ").strip().upper()
        if len(task_id) != 9:
            raise ValueError("Invalid Task ID length.")
        result = collection.delete_one({"task_id": task_id})
        if result.deleted_count > 0:
            print(f"🗑️ Task {task_id} deleted successfully.")
        else:
            print(f"❌ No task found with ID {task_id}.")

    @staticmethod
    def exit_system():
        print("👋 Exiting system. Goodbye!")


class Menu:
    @staticmethod
    def show_menu():
        print("\n====== 🧠 TASK MANAGER MENU ======")
        options = {
            1: "Add Notes",
            2: "View Notes",
            3: "Update Notes",
            4: "Delete Notes",
            5: "Exit System"
        }
        for k, v in options.items():
            print(f"{k}. {v}")
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                Management.add_notes()
            elif choice == 2:
                Management.view_notes()
            elif choice == 3:
                Management.update_notes()
            elif choice == 4:
                Management.delete_notes()
            elif choice == 5:
                Management.exit_system()
                exit()
            else:
                print("❌ Invalid choice. Try again.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")


if __name__ == "__main__":
    while True:
        try:
            Menu.show_menu()
            cont = input("\n🔁 Enter 1 to continue or any key to exit: ").strip()
            if cont != "1":
                print("👋 Exiting. Thank you!")
                break
        except Exception as e:
            print(f"❌ Error: {e}")
