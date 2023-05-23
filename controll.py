import json
import datetime
import calendarAPI

def main():
    while True:
        cmd = input("Besser als Telekom: ")
        ops = cmd.split(" ")
        match ops[0]:
            case "members":
                if len(ops) < 2:
                    print("operator expected")
                else:
                    match ops[1]:
                        case "change":
                            if len(ops) < 4:
                                print("give the name of the member and the changes")
                                continue
                            members = open("members.json")
                            members = json.load(members)
                            name = ops[2]
                            changes = ops[3].split(",")
                            for member in members:
                                if member["name"] == name:
                                    members.remove(member)
                                    for change in changes:
                                        member[change.split("=")[0]] = change.split("=")[1]
                                    members.append(member)
                            with open("members.json", "w") as outfile:
                                outfile.write(json.dumps(members, indent=4))
                        case "delete":
                            if len(ops) < 3:
                                print("give name as parameter to delete a member")
                                continue
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
                                continue
                            member = ops[2].split(",")
                            if len(member) < 3:
                                print("give the name,phoneNumber,gmail of the member")
                                continue
                            members = open("members.json")
                            membersJson = json.load(members)
                            members.close()
                            calendar = calendarAPI.calendar()
                            calendar.create(member[0])
                            membersJson.append({"name":member[0].lower(), "phoneNumber":member[1], "calendarID":calendar.id, "gmail":member[2]})
                            with open("members.json", "w") as outfile:
                                outfile.write(json.dumps(membersJson, indent=4))
                            calendar.invite(member[2])
                        case "show":
                            if len(ops) < 3:
                                print("give the name of the member you want to show")
                                continue
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
                                continue
                            name = ops[2]
                            for member in getMembers(name):
                                calendar = calendarAPI.calendar()
                                calendar.id = member["calendarID"]
                                print(calendar.nextAvailible(datetime.timedelta(days=1)))
                        case _:
                            print("operator \"" + ops[1] + "\" does not exist")
            case "break":
                break
            case _:
                print("command does not exist")

def getMembers(name):
    members = open("members.json")
    members = json.load(members)
    nameMembers = []
    for member in members:
        if member["name"] == name:
            nameMembers.append(member)
    return nameMembers

def saveMembers(members):
    with open("members.json", "w") as outfile:
        outfile.write(json.dumps(members, indent=4))

if __name__ == "__main__":
    main()