#first version

def study_time():
    hours = int(input("how much hours you study today? "))

    return hours

def match_goal(hours):
    if hours >= 6:
        print("good , keep going")
    else:
        print("haizz, not good , need to improve")


def main():
    hours = study_time()
    match_goal(hours)

main()