import nextcord
import sqlite3
import datetime
from nextcord.ext import commands

database = sqlite3.connect('sample_assignments.db')
cursor = database.cursor()
database.execute('CREATE TABLE IF NOT EXISTS Assignments (id INTEGER PRIMARY KEY, assignment_name VARCHAR, class VARCHAR, due_date VARCHAR, completion VARCHAR)')

class StoreData(commands.Cog):
    def __init__(self, client):
        self.client = client

    def add_helper(self):
        assignment = input("Input the name of the assignment here: ")
        course = input("Input the course associated with this assignment is for: ")
        while True:
            try:
                due_date = input("Input when this assignment is due (YYYY-MM-DD format): ")
                datetime.datetime(year=int(due_date[0:4]), month=int(due_date[5:7]), day=int(due_date[8:]))
                break
            except:
                print("Not a valid date.")
        return [assignment, course, due_date]

    def remove_helper(self):
        assignment_name = input("Input the name of the assignment to remove: ")
        course = input("Input the course associated with this assignment: ")
        return [assignment_name, course]

    def update_helper(self):
        assignment = input("Input the name of the assignment here: ")
        course = input("Input the course associated with this assignment is for: ")
        return [assignment, course]
    
    @nextcord.slash_command()
    async def add(self, interaction: nextcord.Interaction):
        query = "INSERT INTO Assignments(assignment_name, class, due_date, completion) VALUES (?,?,?,?)"
        data = self.add_helper()
        cursor.execute(query, (data[0], data[1], data[2], "Incomplete"))
        database.commit()
        print("Assignment added to database!")

    @nextcord.slash_command()
    async def remove(self, interaction: nextcord.Interaction):
        query = "DELETE FROM Assignments WHERE assignment_name = ? AND class = ?"
        remove = self.remove_helper()
        cursor.execute(query, (remove[0], remove[1]))
        database.commit()
        print("Assignment removed from database!")

    @nextcord.slash_command()
    async def view_all(self, interaction: nextcord.Interaction):
        query = "SELECT assignment_name, class, due_date, completion FROM Assignments"
        data = cursor.execute(query).fetchall()
        if not data:
            await interaction.send("Database is empty")
        else:
            assignments = '\n'.join((str(row[0]) + ' | ' + str(row[1]) + ' | ' + str(row[2]) + ' | ' + str(row[3])) for row in data)
            await interaction.send(assignments)
    
    @nextcord.slash_command()
    async def view_week(self, interaction: nextcord.Interaction):
        week_start = str(datetime.datetime.today().date())
        week_end = str(datetime.datetime.today().date()+datetime.timedelta(days=7))
        query = "SELECT assignment_name, class, due_date, completion FROM Assignments WHERE due_date >= '%s' AND due_date <= '%s';" %(week_start, week_end)
        data = cursor.execute(query).fetchall()
        if not data:
            await interaction.send("Database is empty")
        else:
            assignments = '\n'.join((str(row[0]) + ' | ' + str(row[1]) + ' | ' + str(row[2]) + ' | ' + str(row[3])) for row in data)
            await interaction.send(assignments)

    @nextcord.slash_command()
    async def update_completion(self, interaction: nextcord.Interaction):
        query = "UPDATE Assignments SET completion = 'Complete' WHERE assignment_name = ? AND class = ?"
        update = self.update_helper()
        cursor.execute(query, (update[0], update[1]))
        database.commit()
        await interaction.send(f"Assignment {update[0]} with course number {update[1]} has been updated!")
    
    @nextcord.slash_command()
    async def remove_many(self, interaction: nextcord.Interaction):
        current_day = str(datetime.datetime.today().date())
        query = "DELETE FROM Assignments WHERE due_date < '%s';" %(current_day)
        cursor.execute(query)
        database.commit()
        await interaction.send(f"Assignments before {current_day} have been removed!")

def setup(client):
    client.add_cog(StoreData(client))