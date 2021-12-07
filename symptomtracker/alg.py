from . import mongoform

def symptomAnalysis(symptom):
    #Input variables
    cold = symptom[3]
    jointPain = symptom[4]
    feelingWeek = symptom[5]
    lossOfAppt = symptom[6]
    abdominalPain = symptom[7]
    soreThroat = symptom[8]
    headache = symptom[9]
    temperature = symptom[10]
    temperature = 2*(temperature-35)
    dryCough = symptom[11]
    Dyspnea = symptom[12]
    nausea = symptom[13]
    vomiting = symptom[14]
    diarrhea = symptom[15]

    #output variables
    day0 = 0
    day1or2 = 0
    day3 = 0
    day4 = 0
    day5 = 0
    day6 = 0
    day7 = 0
    day8or9 = 0
    day10 = 0
    day11 = 0

    #conversions and adding weights
    if(cold<=1):#null
        weight = 1
        day0 += weight
    elif(cold<=6):#mild
        weight = (cold-1)/5
        day1or2 += weight
        day3 += weight
        day4 += weight
        day5 += weight
        day6 += weight
    else:#severe
        weight = (cold-6)/4
        day7 += weight
        day8or9 += weight
        day10 += weight
        day11 += weight
        
    if(jointPain<=1):#null
        weight = 1
        day0 += weight
        day1or2 += weight
        day3 += weight
    elif(jointPain<=4):#mild
        weight = (jointPain-1)/3
        day4 += weight
        day5 += weight
        day6 += weight
    elif(jointPain<=7):#painful
        weight = (jointPain-4)/3
        day7 += weight
        day8or9 += weight
        day10 += weight
        day11 += weight
    else:#severe
        weight = (jointPain-7)/3
        day11 += weight

    if(feelingWeek<=1):#null
        weight = 1
        day0 += weight
        day1or2 += weight
        day3 += weight
    elif(feelingWeek<=6):#occasional
        weight = (feelingWeek-1)/5
        day4 += weight
    else:#often
        weight = (feelingWeek-6)/4
        day5 += weight
        day6 += weight
        day7 += weight
        day8or9 += weight
        day10 += weight
        day11 += weight

    if(lossOfAppt<=1):#no
        weight = 1
        day0 += weight
        day1or2 += weight
        day3 += weight
        day4 += weight
        day5 += weight
        day6 += weight
        day7 += weight
        day8or9 += weight
    else:#yes
        weight = (lossOfAppt-1)/9
        day10 += weight
        day11 += weight

    if(abdominalPain<=1):#null
        weight = 1
        day0 += weight
        day1or2 += weight
        day3 += weight
        day4 += weight
        day5 += weight
        day6 += weight
        day7 += weight
        day8or9 += weight
    elif(abdominalPain<=4):#mild
        weight = (abdominalPain-1)/3
        day10 += weight
    elif(abdominalPain<=7):#painful
        weight = (abdominalPain-4)/3
        day10 += weight
        day11 += weight
    else:#severe
        weight = (abdominalPain-7)/3
        day11 += weight

    if(soreThroat<=1):
        weight = 1
        day0 += weight
    elif(soreThroat<=4):
        weight = (soreThroat-1)/3
        day1or2 += weight
        day3 += weight
    elif(soreThroat<=7):
        weight = (soreThroat-4)/3
        day3 += weight
        day4 += weight
        day5 += weight
        day6 += weight
    else:
        weight = (soreThroat-7)/3
        day7 += weight
        day8or9 += weight
        day10 += weight
        day11 += weight    

    if(headache<=1):
        weight = 1
        day0 += weight
        day1or2 += weight
        day3 += weight
        day4 += weight
    elif(headache<=4):
        weight = (headache-1)/3
        day5 += weight
        day6 += weight
    elif(headache<=7):
        weight = (headache-4)/3
        day6 += weight
        day7 += weight
        day8or9 += weight
        day10 += weight
        day11 += weight
    else:
        weight = (headache-7)/3
        day7 += weight
        day8or9 += weight
        day10 += weight
        day11 += weight

    if(temperature<=4):
        weight = 1
        day0 += weight
        day1or2 += weight
        day3 += weight
        day4 += weight
    elif(temperature<=6):
        weight = (temperature-4)/2
        day5 += weight
        day6 += weight
        day7 += weight
        day8or9 += weight
        day10 += weight
        day11 += weight
    else:
        weight = (temperature-6)/4
        day8or9 += weight
        day10 += weight
        day11 += weight
        
    if(dryCough<=1):
        weight = 1
        day0 += weight
        day1or2 += weight
        day3 += weight
        day4 += weight
    elif(dryCough<=4):
        weight = (dryCough-1)/3
        day5 += weight
        day6 += weight
    elif(dryCough<=7):
        weight = (dryCough-4)/3
        day7 += weight
    else:
        weight = (dryCough-7)/3
        day7 += weight
        day8or9 += weight
        day10 += weight
        day11 += weight

    if(Dyspnea<=1):
        weight = 1
        weight = 1
        day0 += weight
        day1or2 += weight
        day3 += weight
        day4 += weight
    elif(Dyspnea<=4):
        weight = (Dyspnea-1)/3
        day5 += weight
        day6 += weight
    elif(Dyspnea<=7):
        weight = (Dyspnea-4)/3
        day7 += weight
        day8or9 += weight
        day10 += weight
    else:
        weight = (Dyspnea-7)/3
        day8or9 += weight
        day10 += weight
        day11 += weight

    if(nausea<=1):
        weight = 1
        day0 += weight
        day1or2 += weight
        day3 += weight
        day4 += weight
    elif(nausea<=6):
        weight = (nausea-1)/5
        day3 += weight
        day4 += weight
        day5 += weight
        day6 += weight
    else:
        weight = (nausea-6)/4
        day7 += weight
        day8or9 += weight
        day10 += weight
        day11 += weight
        
        
    if(vomiting<=1):
        weight = 1
        day0 += weight
        day1or2 += weight
        day3 += weight
        day4 += weight
    elif(vomiting<=6):
        weight = (vomiting-1)/5
        day3 += weight
        day4 += weight
        day5 += weight
    else:
        weight = (vomiting-6)/4
        day6 += weight
        day7 += weight
        day8or9 += weight
        day10 += weight
        day11 += weight
        

    if(diarrhea<=1):
        weight = 1
        day0 += weight
        day1or2 += weight
        day3 += weight
        day4 += weight
    elif(diarrhea<=6):
        weight = (diarrhea-1)/5
        day3 += weight
        day4 += weight
        day5 += weight
        day6 += weight
    else:
        weight = (diarrhea-6)/4
        day7 += weight
        day8or9 += weight
        day10 += weight
        day11 += weight

    #final conversion 
    day0 /= 13
    day1or2 /= 13
    day3 /= 13
    day4 /= 13
    day5 /= 13
    day6 /= 13
    day7 /= 13
    day8or9 /= 13
    day10 /= 13
    day11 /= 13
           #0    1        2     3     4     5     6     7        8      9
    day = [day0, day1or2, day3, day4, day5, day6, day7, day8or9, day10, day11]

    maxday = max(day)
    if maxday == day1or2:
        day.append('1')
        day.append("Possibly affected and still on day 1 or 2")
    elif maxday == day3:
        day.append('3')
        day.append("Possibly affected and still on day 3")
    elif maxday == day4:
        day.append('4')
        day.append("Possibly affected and on day 4")
    elif maxday == day5:
        day.append('5')
        day.append("Possibly on day 5. Recomend to get a PCR/Antgen test done.")
    elif maxday == day6:
        day.append('6')
        day.append("Possibly on day 6. Recomend to get a PCR/Antgen test done.")
    elif maxday == day7:
        day.append('7')
        day.append("Possibly on day 5. Recomend to get a PCR/Antgen test done.")
    elif maxday == day8or9:
        day.append('8')
        day.append("Possibly on day 8 or 9. Recomend to get hospitalized.")
    elif maxday == day10:
        day.append('10')
        day.append("Possibly on day 10. Critical. Recomend to get hospitalized.")
    elif maxday == day11:
        day.append('11')
        day.append("Possibly on day 11. Critical. Recomend to get admitted to ICU.")
    elif maxday == day0:
        day.append('0')
        day.append("Does not seem to be affected by Covid 19")

    #Displaying results
    #print("Profile :", symptom)
    #print("Days :", day)

    #sending data to MongoDB
    db_err = mongoform.saveSymptoms(symptom, day)
    if db_err == 0:
        return 0
    else:
        return 1
