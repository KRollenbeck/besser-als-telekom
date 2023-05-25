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
                        if len(ops) == 3:
                            print(controll.show(ops[2]))
                            return
                        print(controll.show(ops[2], ops[3].split(",")))
                    case "list":
                        if len(ops) < 3:
                            for member in controll.loadMembers():
                                print(member)
                            return
                        for member in controll.list(ops[2].split(",")):
                            print(member)
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
    def loadMembers() -> list[dict]:
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
    def show(name: str, attr: list[str] = []) -> dict:
        member = controll.getMember(name)
        if member == None:
            return None
        if len(attr) == 0:
            return member
        memberOut = {}
        for arg in attr:
            memberOut[arg] = member[arg]
        return memberOut
    def list(attr: list[str] = []) -> list[dict]:
        members = controll.loadMembers()
        membersOut = []
        for member in members:
            memb = {"name": member["name"]}
            for arg in attr:
                memb[arg] = member[arg]
            membersOut.append(memb)
        return membersOut

if __name__ == "__main__":
    while True:
        if console(input("besser als Telekom: ")):
            break