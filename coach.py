import json

days = ("day1", "day2", "day3", "day4", "day5", "day6", "day7")
times =("morning", "lunch", "day", "evening", "exit")
sports = {"swimming", "cycling", "running"}
loads = ("easy", "medium", "hard")
answers = ("week", "workout", "exit")
replies_week = ("add", "remove", "exit")
replies_workout = ("edit", "remove", "exit")

def loadData():
    with open('main.json') as data_file:
        schedule = json.load(data_file)
    return schedule

def loadPredef():
    with open('main.json') as data_file:
        predata = json.load(data_file)
    preworkouts = predata["workouts"]
    return(preworkouts)

def editWeek(data):

    reply = "x"
    print("\nCurrent weeks in schedule :(" + (", ").join(data["schedule"].keys()) + ")")


    while (reply not in replies_week) or reply!="exit":
        count = 1
        for key in data["schedule"]:
            count = count + 1
        reply = str(input("What would you like to do with the weeks (" + (", ").join(replies_week) + "): "))
        if (reply not in replies_week):
            print("Invalid input, try again")

        if (reply == "add"):
            count = str(count)
            print("\nweek"+count, "has been added\n")
            data["schedule"]["week"+count] = { "day1": { "morning": -1, "lunch": -1, "day": -1, "evening": -1 }, "day2": { "morning": -1, "lunch": -1, "day": -1, "evening": -1 }, "day3": { "morning": -1, "lunch": -1, "day": -1, "evening": -1 }, "day4": { "morning": -1, "lunch": -1, "day": -1, "evening": -1 }, "day5": { "morning": -1, "lunch": -1, "day": -1, "evening": -1 }, "day6": { "morning": -1, "lunch": -1, "day": -1, "evening": -1 }, "day7": { "morning": -1, "lunch": -1, "day": -1, "evening": -1 } }

        if (reply == "remove"):
            count = int(count) - 1
            count = str(count)
            print("\nweek"+count, "has been removed\n")
            del data["schedule"]["week" + count]
        file = open("main.json", "w")
        file.write(json.dumps(data))
        file.close()

def editWorkout(data,preworkouts):
    week = "x"


    while week not in data["schedule"].keys():
        week = input(str("\nInput week (" + (", ").join(data["schedule"].keys()) + "): "))
        if week not in data["schedule"].keys():
            print("That does not exist, try again")
        else:
            day ="x"
            while day not in days:
                day = input(str("Input day (" + (", ").join(days) + "): "))
                if day not in days:
                    print("That does not exist, try again")

    week_schedule = data["schedule"][week][day]
    print("\nCurrently looking at workouts on",day, "in",week,"\n")
    for key in week_schedule:
        if week_schedule[key] == -1:
            print(key, ":", "no excerisize for this time of day")
        elif "predefinedworkout" in week_schedule[key].keys():
            print(key, ":", "predefined workout -",week_schedule[key]["predefinedworkout"])
        else:
            print(key, ":", week_schedule[key]["type"], "for", week_schedule[key]["minutes"], "minutes and",
                  week_schedule[key]["distance"], "kilometers, at a", week_schedule[key]["load"], "load")
    time = "x"
    while (time not in times) or time !="exit":
        time =input(str("\nInput time of day (" + (", ").join(times) + "): "))
        if time not in times and time!="exit":
            print("That does not exist, try again")
        elif time =="exit":
            continue
        else:
            if (week_schedule[time]==-1):
                print("No workout planned for",time)
            reply = "x"
            while (reply not in replies_workout):
                reply = str(input("\nChoose an option to perform on this workout (" + (", ").join(replies_workout) + "): "))
                if (reply not in replies_workout):
                    print("Invalid input, try again")

                elif(reply == "remove"):
                    if (week_schedule[time]==-1):
                        print("\nThe time:",time, "is already empty")
                    else:
                        data["schedule"][week][day][time]=-1
                        print("\nWorkout during", time, "on", day,"in",week,"has been removed")

                elif(reply == "edit"):
                    ask = "x"
                    workout = "x"
                    while (ask != "yes" and ask != "no"):
                        ask = str(input("\nWould you like to add a predefined workout? yes/no: "))
                        if (ask != "yes" and ask != "no"):
                            print("Invalid input, try again")

                    if (ask == "yes"):
                        while (workout not in preworkouts.keys()) or workout == "test":
                            workout = input(str("\nInput premade workout, except for 'test' (" + (", ").join(preworkouts.keys()) + "): "))
                            if workout == "test":
                                print("Cannot use test")
                            elif (workout not in preworkouts.keys()):
                                print("That does not exist, try again")
                            else:
                                data["schedule"][week][day][time] = {"predefinedworkout": workout}
                                print("\nPremade workout",workout,"has been placed during",time,"on", day,"in",week)

                    if (ask == "no"):
                        sport = "x"
                        load = "x"
                        while (sport not in sports):
                            sport = str(input("\nChoose sport type (" + (", ").join(sports) + "): "))
                            if (sport not in sports):
                                print("Invalid input, try again")

                        isMinutesSet = False
                        while (not isMinutesSet):
                            minutes = input("Input amount of time in minutes from 0 to 240: ")
                            try:
                                minutes = float(minutes)
                                if (minutes > 0 and minutes <= 240):
                                    isMinutesSet = True
                                else:
                                    print("Wrong Input: Please type a positive integer number above 0 and below 240")
                            except ValueError:
                                print("Wrong Input: Please input a number")

                        isDistanceSet = False
                        while (not isDistanceSet):
                            distance = input("Input the distance in kilometers from 0 to 200: ")
                            try:
                                distance = float(distance)
                                if (distance > 0 and distance <= 200):
                                    isDistanceSet = True
                                else:
                                    print("Wrong Input: Please type a positive integer number above 0 and below 200")
                            except ValueError:
                                print("Wrong Input: Please input a number")

                        while (load not in loads):
                            load = str(input("Choose load (" + (", ").join(loads) + "): "))
                            if (load not in loads):
                                print("Invalid input, try again")
                        data["schedule"][week][day][time] = {"type": sport, "minutes": minutes, "distance": distance, "load": load}
                        print("Workout created during",time,"on",day,"in",week, ":", data["schedule"][week][day][time]["type"], "for", data["schedule"][week][day][time]["minutes"], "minutes and",
                              data["schedule"][week][day][time]["distance"], "kilometers, at a", data["schedule"][week][day][time]["load"], "load")
                file = open("main.json", "w")
                file.write(json.dumps(data))
                file.close()

def main():
    answer = "x"
    while (answer not in answers) or answer !="exit":
        answer = str(input("\nCoach Menu | What would you like to edit in the schedule (" + (", ").join(answers) + "): "))
        if (answer not in answers):
            print("Invalid input, try again")
        elif (answer=="week"):
            data = loadData()
            editWeek(data)
        elif (answer=="workout"):
            data = loadData()
            preworkouts = loadPredef()
            editWorkout(data,preworkouts)

