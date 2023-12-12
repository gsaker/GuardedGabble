import file
import person
# Create a new instance of the Person class with the given ID and name
newPerson = person.Person("123456789", "TestUser")
# Append chat messages to the person's chat history
newPerson.appendChat(True, "Hello, World!")
newPerson.appendChat(True, "It's Working!")
# Get all the chat messages for the person
print(newPerson.readJSON())
allChats = newPerson.getChats()
# This loop outputs each chat message in turn for the specified person
for item in range(len(allChats)):
    print(allChats[str(item)]["message"])