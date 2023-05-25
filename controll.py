import json
import datetime
import calendarAPI

def console(input) -> bool:
    ops = input.split(" ")
    match ops[0]:
        case "members":
            if len(ops) < 2:
                print("operator expected")
            else:
                match ops[1]:
                    case "change":
                        if len(ops) < 4:
                            print("give the name of the member and the changes")
                            return
                        controll.change(ops[2], ops[3].split(","),True)
                    case "remove":
                        if len(ops) < 3:
                            print("give name as parameter to delete a member")
                            return
                        controll.remove(ops[2])
                    case "add":
                        if len(ops) < 3:
                            print("give the name,phoneNumber,gmail of the member")
                            return
                        member = ops[2].split(",")
                        if len(member) < 2:
                            print("give the name,phoneNumber")
                            return
                        if len(member) == 2:
                            controll.add(member[0], member[1])
                        else:
                            controll.add(member[0], member[1], member[2])
                    case "rename":
                        if len(ops) < 4:
                            print("give the name and the new name of the member.")
                            return
                        controll.rename(ops[2], ops[3])
                    case "show":
                        if len(ops) < 3:
                            print("give the name of the member you want to show")
                            return
                        members = open("members.json")
                        members = json.load(members)
                        name = ops[2]
                        for member in members:
                            if member["name"] == name:
                                if len(ops) < 4:
                                    print(member)
                                else:
                                    instances = ops[3].split(",")
                                    memberDict = {}
                                    for instance in instances:
                                        memberDict[instance] = member[instance]
                                    print(memberDict)
                    case "list":
                        members = open("members.json")
                        members = json.load(members)
                        for member in members:
                            if len(ops) < 3:
                                print(member["name"])
                            else:
                                memberDict = {}
                                instances = ["name"] + ops[2].split(",")
                                for instance in instances:
                                    memberDict[instance] = member[instance]
                                print(memberDict)
                    case "availible":
                        if len(ops) < 3:
                            members = calendarAPI.memberCalendars()
                            members.load()
                            print(members.availibility())
                    case "nextAvailible":
                        if (len(ops) < 3):
                            cal = calendarAPI.memberCalendars()
                            cal.load()
                            print(cal.nextAvailible())
                            return
                        name = ops[2]
                        for member in controll.getMembers(name):
                            calendar = calendarAPI.calendar()
                            calendar.id = member["calendarID"]
                            print(calendar.nextAvailible(datetime.timedelta(days=1)))
                    case _:
                        print("operator \"" + ops[1] + "\" does not exist")
        case "break":
            return True
        case _:
            print("command does not exist")


class controll:
    def loadMembers() -> dict:
        return json.load(open("members.json"))
    def getMember(name: str) -> dict:
        members = controll.loadMembers()
        for member in members:
            if member["name"] == name:
                return member
        return None
    def saveMembers(members: dict):
        with open("members.json", "w") as outfile:
            outfile.write(json.dumps(members, indent=4))
    def change(name: str, attr: list[str], save = True) -> dict:
        members = controll.loadMembers()
        member = controll.getMember(name)
        members.remove(member)
        for change in attr:
            member[change.split("=")[0]] = change.split("=")[1]
        members.append(member)  
        if save:
            controll.saveMembers(members)
    def remove(name: str):
        members = controll.loadMembers()
        member = controll.getMember(name)
        calendar = calendarAPI.calendar()
        calendar.id = member["calendarID"]
        calendar.delete()
        if member != None:
            members.remove(member)
        controll.saveMembers(members)
    def add(name: str, phoneNumber: str, gmail: str = None, invite=True) -> dict:
        if controll.getMember(name) == None:
            member = {"name": name, "phoneNumber": phoneNumber, "gmail": None}
            calendar = calendarAPI.calendar()
            calendar.create(name)
            member["calendarID"] = calendar.id
            if gmail != None:
                member["gmail"] = gmail
                if invite:
                    calendar.invite(gmail)
            members  = controll.loadMembers()
            members.append(member)
            controll.saveMembers(members)
            return member
        else:
            return None
    def rename(name: str, newName: str) -> dict:
        if controll.getMember(newName) == None:
            member = controll.getMember(name)
            calendar = calendarAPI.calendar()
            calendar.id = member["calendarID"]
            calendar.rename(newName)
            return controll.change(name, ["name=" + newName])
        return None

if __name__ == "__main__":
    while True:
        if console(input("besser als Telekom: ")):
            break