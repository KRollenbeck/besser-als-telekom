from __future__ import print_function

import datetime
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class calendar:
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None
    def nextAvailible(self, timeDelta):
        self.connect()
        now = datetime.datetime.utcnow().isoformat() + "Z"
        end = (datetime.datetime.utcnow() + timeDelta).isoformat() + "Z"
        query = self.service.freebusy().query(body={"timeMin":now, "timeMax":end, "items":[{"id":self.id}]}).execute()
        busy = query.get("calendars").get(self.id).get("busy")
        if len(busy) == 0:
            return None
        return busy[0]["start"]
    def connect(self):
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
        self.service = build('calendar', 'v3', credentials=self.creds)
    def availible(self) -> bool:
        self.connect()
        now = datetime.datetime.utcnow().isoformat()
        now = now[0:len(now) - 7] + "Z"
        # now = "2023-05-17T05:52:14Z"
        nextDay = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).date().isoformat() + "T00:00:00Z"
        try:
            available = self.service.freebusy().query(body={"timeMin":now, "timeMax":nextDay, "items":[{"id":self.id}]}).execute()
            # print("query:", available)
            busy = available.get("calendars").get(self.id).get("busy")
            if (len(busy) == 0):
                return False
            elif (available.get("timeMin")[0:len(available.get("timeMin")) - 5] + "Z" != busy[0].get("start")):
                return False
            return True
        except HttpError as error:
            print('An error occurred: %s' % error)
        return None
    def create(self, name):
        self.connect()
        calendar = {"summary": name, "timeZone": "UTC+02:00"}
        newCalendar = self.service.calendars().insert(body=calendar).execute()
        self.id = newCalendar["id"]
    def delete(self):
        self.connect()
        self.service.calendars().delete(calendarId=self.id).execute()
    def invite(self, ruleID):
        self.connect()
        rule = {
            'scope': {
                'type': 'user',
                'value': ruleID,
            },
            'role': 'reader'
        }
        created_rule = self.service.acl().insert(calendarId=self.id, body=rule).execute()
        print (created_rule['id'])
class memberCalendars:
    def load(self):
        self.members = []
        members = open("members.json")
        members = json.load(members)
        for member in members:
            cal = calendar()
            cal.id = member["calendarID"]
            cal.name = member["name"]
            self.members.append(cal)
    def availibility(self):
        availible = []
        for member in self.members:
            if member.availible():
                availible.append(member.name)
        return availible
    def nextAvailible(self):
        members = open("members.json")
        members = json.load(members)
        i = 0
        for member in self.members:
            members[i]["nextAvailible"] = member.nextAvailible(datetime.timedelta(days=1))
            i += 1
        nextAvailible = {"name":None,"nextAvailible":None}
        for member in members:
            if member["nextAvailible"] != None:
                if nextAvailible["nextAvailible"] == None:
                    nextAvailible["nextAvailible"] = member["nextAvailible"]
                    nextAvailible["name"] = member["name"]
                    continue
                if (datetime.datetime.fromisoformat(member["nextAvailible"]) - datetime.datetime.fromisoformat(nextAvailible["nextAvailible"]) < datetime.timedelta(days=0)):
                    nextAvailible["name"] = member["name"]
                    nextAvailible["nextAvailible"] = member["nextAvailible"]
        return nextAvailible
