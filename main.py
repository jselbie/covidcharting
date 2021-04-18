import os
import matplotlib.pyplot as plt
import datetime
import multiprocessing
from enum import Enum


class DataType(Enum):
    COUNTY = 1
    STATE = 2
    COUNTRY = 3

usa_dict = {}

def string_to_int(s, fallback=0):
    try:
        return int(s)
    except ValueError:
        return fallback
    return fallback

def plot(county, state, fignum=101):
    county_dict = usa_dict[state][county]
    dates = county_dict["dates"]
    cases = county_dict["cases"]
    deaths = county_dict["deaths"]
    dataType = county_dict["datatype"]
    isState = dataType==DataType.STATE
    isCountry = dataType==DataType.COUNTRY
    cases_rolling = [0]*len(cases)
    deaths_rolling = [0]*len(deaths)

    assert(len(cases)==len(deaths))

    for i in range(0, len(cases)):
        if (i <= 6):
            cases_rolling[i] = 0
            deaths_rolling[i] = 0
        else:
            cases_rolling[i] = cases[i] - cases[i-7]
            deaths_rolling[i] = deaths[i] - deaths[i-7]

    plt.figure(num=fignum, figsize=(22,6), dpi=100)
    # plt.figure(num=fignum, figsize=(11,6), dpi=100)
    plt.tick_params(axis="y", length=0)
    plt.xticks(rotation=45)
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.ylabel("Cases per week")


    max_cases_rolling = max(cases_rolling)
    max_cases_rolling_adjusted = (max_cases_rolling * 11) // 10
    if (max_cases_rolling_adjusted <= max_cases_rolling):
        max_cases_rolling_adjusted += 1

    plt.ylim(0, max_cases_rolling_adjusted)
    plt.grid(b=True, which="major", axis="y")

    title = "Covid-19 new cases per week: "+county+" County"+" "+state+ " (rolling 7 day summation)"
    if isState:
        title = "Covid-19 new cases per week: "+state+" State (rolling 7 day summation)"
    elif isCountry:
        title = "Covid-19 new cases per week: United States of America (rolling 7 day summation)"

    plt.title(title)

    # only the last thee months get plotted
    #if len(dates) > 90:
    #    dates = dates[-90:]
    #    cases_rolling = cases_rolling[-90:]

    plt.plot_date(dates, cases_rolling, xdate=True, fmt="b-", label="Infections")

    destdir = 'C:/Users/Jselbie/OneDrive/CovidCharts'
    os.chdir(destdir)

    sep = os.path.sep
    try:
        os.mkdir(state)
    except FileExistsError:
        pass
    filename = state + sep + county + ".png"
    if isState:
        filename = state + sep + "State of " + state + ".png"
    if isCountry:
        filename = "usa.png"

    plt.savefig(filename)

    plt.close()
    print("saved:", filename)



def plotState(state):
    state_dict = usa_dict[state]
    for county in state_dict:
        plot(county, state)


def plotSet(states, fignum):
    for state in states:
        state_dict = usa_dict[state]
    for county in state_dict:
        plot(county,state,fignum)

def plotAll():
    for state in usa_dict:
        for county in usa_dict[state]:
            plot(county, state)


def parse_csv(lines, dataType):

    minRowSize = 6 if dataType == DataType.COUNTY else (5 if dataType==DataType.STATE else 3)

    for line in lines:
        row = line.split(",")
        if len(row) < minRowSize or  row[0].lower()=="date":
            continue

        if dataType == DataType.COUNTY:
            date = row[0]
            county = row[1]
            state = row[2]
            cases = row[4]
            deaths = row[5]
        elif dataType == DataType.STATE:
            date = row[0]
            county = "ENTIRE STATE"
            state = row[1]
            cases = row[3]
            deaths = row[4]
        elif dataType == DataType.COUNTRY:
            date = row[0]
            county = "USA"
            state = "USA"
            cases = row[1]
            deaths = row[2]

        # parse date
        dy,dm,dd = date.split('-')
        d = datetime.datetime(int(dy),int(dm), int(dd))

        if not (state in usa_dict.keys()):
            usa_dict[state] = {}

        state_dict = usa_dict[state]

        if not (county in state_dict.keys()):
            state_dict[county] = {}
        
        county_dict = state_dict[county]

        if not ("dates" in county_dict):
            county_dict["dates"] = []
            county_dict["cases"] = []
            county_dict["deaths"] = []
            county_dict["datatype"] = dataType

        cases_int = string_to_int(cases, 0)
        deaths_int = string_to_int(deaths, 0)

        county_dict["dates"].append(d)
        county_dict["cases"].append(cases_int)
        county_dict["deaths"].append(deaths_int)



f=open("C:/users/jselbie/us-counties.csv")
lines = f.readlines()
f.close()
parse_csv(lines, DataType.COUNTY)

f=open("C:/users/jselbie/us-states.csv")
lines = f.readlines()
f.close()
parse_csv(lines, DataType.STATE)

f=open("C:/users/jselbie/us.csv")
lines = f.readlines()
f.close()
parse_csv(lines, DataType.COUNTRY)

print("done reading us.csv file")

plotAll()
