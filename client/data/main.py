import file
import person
newPerson = person.Person("123456789", "TestUser")
newPerson.appendChat(True, "Hello, World!")
print(newPerson.getChat(0))