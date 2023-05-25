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
                    case "delete":
                        if len(ops) < 3:
                            print("give name as parameter to delete a member")
                            return
                        members = open("members.json")
                        members = json.load(members)
                        name = ops[2].lower()
                        i = 0
                        for member in members:
                            if member["name"] == name:
                                calendar = calendarAPI.calendar()
                                calendar.id = member["calendarID"]
                                calendar.delete()
                                del members[i]
                                i -= 1
                            i += 1
                        with open("members.json", "w") as outfile:
                            outfile.write(json.dumps(members, indent=4))
                    case "add":
                        if len(ops) < 3:
                            print("give the name,phoneNumber,gmail of the member")
                            return
                        member = ops[2].split(",")
                        if len(member) < 3:
                            print("give the name,phoneNumber,gmail of the member")
                            return
                        members = open("members.json")
                        membersJson = json.load(members)
                        members.close()
                        calendar = calendarAPI.calendar()
                        calendar.create(member[0])
                        membersJson.append({"name":member[0].lower(), "phoneNumber":member[1], "calendarID":calendar.id, "gmail":member[2]})
                        with open("members.json", "w") as outfile:
                            outfile.write(json.dumps(membersJson, indent=4))
                        calendar.invite(member[2])
                    case "rename":
                        if len(ops) < 4:
                            print("give the name and the new name of the member.")
                            return
                        members = open("members.json")
                        members = json.load(members)
                        for member in controll.getMembers(ops[2]):
                            calendar = calendarAPI.calendar()
                            calendar.id = member["calendarID"]
                            calendar.rename(ops[3])
                            members.remove(member)
                            member["name"] = ops[3]
                            members.append(member)
                        controll.saveMembers(members)
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
    def getMember(name: str) -> dict:
        members = open("members.json")
        members = json.load(members)
        for member in members:
            if member["name"] == name:
                return member
        return None
    def saveMembers(members):
        with open("members.json", "w") as outfile:
            outfile.write(json.dumps(members, indent=4))
    def change(name: str, attr: list[str], save = True) -> dict:
        members = open("members.json")
        members = json.load(members)
        member = controll.getMember(name)
        members.remove(member)
        for change in attr:
            member[change.split("=")[0]] = change.split("=")[1]
        members.append(member)  
        if save:
            controll.saveMembers(members)

if __name__ == "__main__":
    while True:
        if console(input("besser als Telekom: ")):
            break