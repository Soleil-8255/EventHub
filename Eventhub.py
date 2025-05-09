from datetime import datetime  

class EventHub:
    def __init__(self):
        self.events = {}  
        self.attendees = {}

        with open("events.txt", "a") as file:
            file.close()
        
        self.read_events()
  

    def store_events(self):
        with open("events.txt", "w") as file:
            for name, details in self.events.items():
                attendees_str = ",".join(self.attendees.get(name, []))  
                file.write(f"{name} | {details['date']} | {details['time']} | {details['location']} | {details['description']} | {attendees_str}\n")

    def read_events(self):
        with open("events.txt", "r") as file:
            for line in file:
                parts = line.strip().split(" | ")
                name, date, time, location, description = parts[:5]  
                attendees = parts[5].split(",") if len(parts) > 5 else []  
                self.events[name] = {"date": date, "time": time, "location": location, "description": description}
                self.attendees[name] = attendees  

    def conflict(self, date, time, location, exclude=None):
        for event, details in self.events.items():
            if event != exclude and details["date"] == date and details["time"] == time and details["location"] == location:
                return True
        return False


 
    def add_event(self):
        while True:
            name = input("Enter event name (Required, or type 'exit' to cancel): ").strip()
            if name.lower() == "exit":
                print("❌ Event creation canceled.")
                return
            if name:  
                break
            print("Error: Event name cannot be empty. Please enter a valid name.")

        while True:
            date = input("Enter event date (YYYY-MM-DD, Required, or type 'exit' to cancel): ").strip()
            if date.lower() == "exit":
                print("❌ Event creation canceled.")
                return
            try:
                datetime.strptime(date, "%Y-%m-%d") 
                break
            except ValueError:
                print("Error: Invalid date format. Please use 'YYYY-MM-DD'.")

        while True:
            time = input("Enter event time (e.g., 7:00AM-10:00PM, Required, or type 'exit' to cancel): ").strip()
            if time.lower() == "exit":
                print("❌ Event creation canceled.")
                return
            try:
                start, end = time.split("-")
                datetime.strptime(start.strip(), "%I:%M%p") 
                datetime.strptime(end.strip(), "%I:%M%p")
                break
            except (ValueError, IndexError):
                print("Error: Invalid time format. Please use '7:00AM-10:00PM'.")

        location = input("Enter event location (Required, or type 'exit' to cancel): ").strip()
        if location.lower() == "exit":
            print("❌ Event creation canceled.")
            return
        while not location:  
            print("Error: Event location cannot be empty. Please enter a valid location.")
            location = input("Enter event location (Required): ").strip()

        description = input("Enter event description (Optional, or type 'exit' to cancel): ").strip()
        if description.lower() == "exit":
            print("❌ Event creation canceled.")
            return

        if self.conflict(date, time, location):
            print("Error: Time and location conflict with another event.")
            return
        
        self.events[name] = {
            "date": date,
            "time": time,
            "location": location,
            "description": description
        }
        self.attendees[name] = []

        print(f"✔ Event '{name}' added successfully!")
        self.store_events()


    def update_event(self):
        name = input("Enter event name to update: ").strip()
        if name not in self.events:
            print("Event not found.")
            return

        print("1. Name\n2. Date\n3. Time\n4. Location\n5. Description")
        choice = input("Enter choice: ").strip()
    
        fields = ["name", "date", "time", "location", "description"]
        if choice == "1":
            new_name = input("Enter new event name: ").strip()
            if new_name in self.events:
                print("Error: Event name already exists.")
                return
            self.events[new_name] = self.events.pop(name)
            self.attendees[new_name] = self.attendees.pop(name)
        else:
            field = fields[int(choice) - 1]
            new_value = input(f"Enter new {field}: ").strip()

            temp = self.events[name].copy()
            temp[field] = new_value

            if self.conflict(temp["date"], temp["time"], temp["location"], exclude=name):
                print("Error: Time and location conflict with another event.")
                return
        
            self.events[name][field] = new_value

        print("✔ Event updated successfully!")
        self.store_events()

    def delete_event(self): 
        if not self.events:
            print("No events available to delete.")
            return

        while True:
            name = input("Enter the event name to delete (or 'exit' to cancel): ").strip()
            if name.lower() == "exit":
                print("❌ Event deletion canceled.")
                return
            if name in self.events:
                del self.events[name]
                del self.attendees[name]
                print(f"✔ Event '{name}' deleted successfully!")
                self.store_events()
                return 
            print("Error: Event not found. Try again.")

            
    def register_attendee(self):
        if not self.events:
            print("No events available to register for.")
            return

        while True:
            name = input("Enter the event name to register for (or 'exit' to cancel): ").strip()
            if name.lower() == "exit":
                print("❌ Registration canceled.")
                return
            if name in self.events:
                break
            print("Error: Event not found. Try again.")

        attendee_names = input("Enter attendee name (comma-separated): ").strip()
        if attendee_names:
            attendees = [attendee.strip() for attendee in attendee_names.split(",") if attendee.strip()]
            if attendees:
                self.attendees[name].extend(attendees)
                print(f"{', '.join(attendees)} registered successfully for '{name}'!")
                self.store_events()
                return
        print("Error: Attendee names cannot be empty. Try again.")
        

    def manage_attendees(self):
        name = input("Enter the event name to manage attendees: ").strip()
        if name not in self.attendees:
            print("Error: Event not found.")
            return
        
        print("1. Update Attendee Name")
        print("2. Delete Attendee")
        choice = input("Enter your choice (1-2): ").strip()
        
        if choice == "1":
            self.update_attendee(name)
        elif choice == "2":
            self.delete_attendee(name)
        else:
            print("Error: Invalid choice.")



    def update_attendee(self, event_name):
        print("Current Attendees:", ", ".join(self.attendees[event_name]) if self.attendees[event_name] else "None")
        
        old_name = input("Enter the attendee name to update: ").strip()
        if old_name not in self.attendees[event_name]:
            print("Error: Attendee not found.")
            return

        new_name = input("Enter the new name: ").strip()
        if new_name:
            idx = self.attendees[event_name].index(old_name)
            self.attendees[event_name][idx] = new_name
            print(f"✔ Attendee '{old_name}' updated to '{new_name}'!")
            self.store_events()
        else:
            print("Error: New name cannot be empty.")


    def delete_attendee(self, event_name):
        print("Current Attendees:", ", ".join(self.attendees[event_name]) if self.attendees[event_name] else "None")
        
        name = input("Enter the attendee name to delete: ").strip()
        if name in self.attendees[event_name]:
            self.attendees[event_name].remove(name)
            print(f"✔ Attendee '{name}' removed!")
            self.store_events()
        else:
            print("Error: Attendee not found.")




    def print_schedule(self):       
        if not self.events:
            print("No events available.")
            return

        print("\n Event Schedule:")
        for name, details in self.events.items():
            print("=" * 40)
            print(f"Name: {name}")
            print(f"Date: {details['date']}")
            print(f"Time: {details['time']}")
            print(f"Location: {details['location']}")
            print(f"Description: {details.get('description', 'N/A')}")
            
            attendees = self.attendees.get(name, [])
            if attendees:
                print("Attendees:")
                for attendee in attendees:
                    print(f"   - {attendee}")  
            else:
                print("Attendees: None")

        print("=" * 40)


    def main_menu(self):       
        while True:
            print("\n" + "=" * 50)
            print("✨EVENTHUB - EVENT MANAGEMENT SYSTEM✨ ".center(50))
            print("=" * 50)

            print("    1 - Add Event")
            print("    2 - Update Event")
            print("    3 - Delete Event")
            print("    4 - Register Attendee")
            print("    5 - Manage Attendees")
            print("    6 - Print Event Schedule")
            print("    7 - Exit")

            print("-" * 50)
            choice = input("Enter your choice: ").strip()
            print("-" * 50)  

            if choice == "1":
                self.add_event()
            elif choice == "2":
                self.update_event()
            elif choice == "3":
                self.delete_event()
            elif choice == "4":
                self.register_attendee()
            elif choice == "5":
                self.manage_attendees()
            elif choice == "6":
                self.print_schedule()
            elif choice == "7":
                print("\n" + "_" * 50)
                print(" Exiting EventHub... Goodbye! ".center(50))
                print("_" * 50 + "\n")
                input("\nPress Enter to exit...")
                break
            else:
                print("Error: Invalid choice. Try again.")


hub = EventHub()
hub.main_menu()
