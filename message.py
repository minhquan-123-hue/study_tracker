import json
#first version

def study_time():
    hours = int(input("how much hours you study today? "))

    return hours

def match_goal(hours):
    if hours >= 6:
        print("good , keep going")
    else:
        print("haizz, not good , need to improve")

def store_study_data(hours):
    with open("data.json" , "w") as file: # round 1 and 2
        json.dump(hours, file,indent = 4)


def main():
    hours = study_time()
    store_study_data(hours)
    match_goal(hours)

main()