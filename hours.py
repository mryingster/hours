#!/usr/bin/python
import csv, platform, sys

def mPrint(*params):
    #Default Values
    style="\033[00"
    plain_text=""
    newline="\n"
    nospace=0
    style_text=""
    style_dict = {'-reset':'00',  '-bold':'01',    '-dim':'02',   '-under':'04',\
                  '-invert':'07', '-hidden':'08',  '-strike':'09',\
                  '-black':'30',  '-red':'31',     '-green':'32', '-yellow':'33',\
                  '-blue':'34',   '-magenta':'35', '-cyan':'36',  '-white':'37'}

    if params:
        for i in range(0, len(params)):
            if params[i] == "-nb":
                newline=""
            elif params[i] == "-ns":
                nospace=1
            elif params[i] == "-reset":
                style="\033[00"
            elif params[i] == "-w":
                main_log(plain_text)
            elif params[i] == "-bg":
                temp=1
            elif params[i-1] == "-bg":
                style=style+";4"+style_dict[params[i]][1]
            elif params[i] in style_dict:
                style=style+";"+style_dict[params[i]]
            else :
                plain_text=plain_text+str(params[i])
                style_text=style_text+style+"m"+str(params[i])+"\033[0m"
                if nospace==0:
                    plain_text=plain_text+" "
                    style_text=style_text+" "

    if platform.system() == "Linux" or platform.system() == "Darwin":
        sys.stdout.write(style_text+newline)
    else:
        sys.stdout.write(plain_text+newline)

def verifyFileExists(csvfilename, fields):
    try:
        with open(csvfilename): pass
    except IOError:
        print "Creating new file,", csvfilename
        with open(csvfilename, 'w') as csvfile:
            csvwriter = csv.DictWriter(csvfile, delimiter=',', fieldnames=fields)
            csvwriter.writerow(dict((fn,fn) for fn in fields)) #Write header row

def readCSV(csvfilename):
    dictarray = []
    with open(csvfilename, 'rb') as csvfile:
        csvdata = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in csvdata:
            dictarray.append(row)
        return dictarray

def writeCSV(csvfilename, dictarray, fields):
    with open(csvfilename, 'w') as csvfile:
        csvwriter = csv.DictWriter(csvfile, delimiter=',', fieldnames=fields)
        csvwriter.writerow(dict((fn,fn) for fn in fields)) #Write header row
        for row in dictarray:
            csvwriter.writerow(row)

def getTime():
    from datetime import datetime
    time = datetime.time(datetime.now())
    hours, minutes=time.hour, time.minute
    if minutes < 10: minutes='0'+str(minutes)
    if hours < 10: hours='0'+str(hours)
    return str(hours)+":"+str(minutes)

def getDate(separator='/'):
    from datetime import datetime
    date = datetime.date(datetime.now())
    return str(date.month)+separator+str(date.day)+separator+str(date.year)

def subtractTime(start, end):
    starthours, startminutes = start.split(":")
    endhours, endminutes = end.split(":")
    hours=int(endhours)-int(starthours)
    minutes=int(endminutes)-int(startminutes)
    while minutes < 0:
        hours-=1
        minutes+=60
    #Compensate for crossing over midnight
    if hours < 0 : hours = hours + 24
    #Use minimum time if less than minimum time
    minimumtime = 5
    if hours == 0 and minutes < minimumtime: minutes = minimumtime
    #Add leading 0 to numbers less than 10
    if minutes < 10: minutes = '0'+str(minutes)
    return str(hours)+":"+str(minutes)

def addTime(time1, time2):
    time1hours, time1minutes = time1.split(":")
    time2hours, time2minutes = time2.split(":")
    hours=int(time2hours)+int(time1hours)
    minutes=int(time2minutes)+int(time1minutes)
    while minutes > 59:
        hours += 1
        minutes -= 60
    if minutes < 10:
        minutes = "0"+str(minutes)
    return str(hours)+":"+str(minutes)


def multiplyTime(delta, rate):
    hours, minutes = delta.split(":")
    decimaltime=float(minutes)/60.0+float(hours)
    return convertMoney(decimaltime*rate)
    #return decimaltime*rate

def convertMoney(input):
    input=str(input)
    dollars, cents = input.split('.')
    #Add zero before digits lower than 10
    if int(cents) < 10 and not cents.startswith('0'): cents="0"+cents
    #Round to two points
    while int(cents) > 99: cents=str((int(cents)+05)/10)
    return dollars+"."+cents

def clockIsOpen(dictarray, verbose):
    if len(dictarray) > 0:
        if 'End' not in dictarray[-1] or dictarray[-1]['End'] == '':
            if verbose == 1: mPrint("Clock opened for", "-bold", "-cyan", dictarray[-1]['Client'], \
                                    "-reset", "with project", "-bold", "-cyan", dictarray[-1]['Project'], dictarray[-1]['Notes'], \
                                    "-reset", "since", "-bold", "-cyan", dictarray[-1]['Start'])
            return 1
    if verbose == 1: print "No clock is opened"
    return 0

def searchDict(dictarray):
    searchArray = []
    searchTerm = raw_input("Search Term: ")
    for dictionary in dictarray:
        for key in dictionary:
            if dictionary[key].lower().find(searchTerm.lower())>=0:
                searchArray.append(dictionary)
                #print "Found", searchterm, "in", dictionary
                break
    printPretty(searchArray)

def searchByMonth(dictarray):
    searchArray = []
    searchMonth, searchYear = 0, 0
    from datetime import datetime
    defaultMonth = datetime.date(datetime.now()).month
    defaultYear = datetime.date(datetime.now()).year

    while 1:
        searchMonth = raw_input("Select month (current is %s): " % defaultMonth)
        if searchMonth == "": searchMonth = str(defaultMonth)
        if int(searchMonth) < 1 or int(searchMonth) > 12:
            print "Invalid selection, %s" % searchMonth
        else: break

    while 1:
        searchYear = raw_input("Select year (current is %s): " % defaultYear)
        if searchYear == "": searchYear = str(defaultYear)
        if int(searchYear) < 1970 or int(searchYear) > defaultYear:
            print "Invalid selection, %s" % searchYear
        else: break

    for dictionary in dictarray:
        import re
        if re.compile('%s/.+/%s'%(searchMonth, searchYear)).match(dictionary['Date']):
            searchArray.append(dictionary)
    printPretty(searchArray)

def printPrettyHeader():
    #                           0    5    10   15   20   25   30   35   40   45   50   55   60   65   70   75   80   85   90   95  100  105  110  115  120  125
    #                           |----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
    mPrint("-bold", "-magenta", "            Start  End    Total      Sub    Multi")
    mPrint("-bold", "-magenta", "Date        Time   Time   Time  Rate Total  plier Total  Client      Project               Notes                 Inv. Paid")
    #                            06/08/2013  07:16  07:24  0:08  24   03.02  1.85  05.76  Client Name Project Name          Notes                 0
    #                            10        2 5    2 5    2 4   2 2 3  5    2 4   2 5    2 10        2 20                  2 20                  2 4 1  No

def printPretty(dictarray):
    printPrettyHeader()

    total=0.0
    totalInvoiceable=0.0
    totalTime='0:00'
    for i in dictarray:
        if 'End' not in i: continue #Skip non-completed rows...
        printPrettyLine(i)

        if i['Total'] != '':
            totalTime=addTime(totalTime, i['Total Time'])
            total+=float(i['Total'])
            if i['Invoice'] == '0':
                totalInvoiceable+=float(i['Total'])

    print ""
    print "\t       Total Time: %s"  %  totalTime
    print "\t            Total: $%s" %  total
    print "\tTotal Invoiceable: $%s" %  totalInvoiceable
    print ""

    askToSave(dictarray, totalTime, total, totalInvoiceable)

def printPrettyLine(line):
    print "%-10s  %-5s  %-5s  %-4s  %-2s   %-5s  %-4s  %-5s  %-10s  %-20s  %-20s  %-4s %s" %\
        (line['Date'], line['Start'], line['End'], line['Total Time'], line['Rate'], line['Sub Total'], line['Multiplier'], \
         line['Total'], line['Client'][0:10], line['Project'][0:20], line['Notes'][0:20], line['Invoice'], line['Paid'])

def askToSave(dictarray, totalTime, total, totalInvoiceable):
    if raw_input("Save to file? (y/n) ") == "y":
        #Check to see if invoicing a single client
        client=[]
        for i in dictarray:
            if i['Client'] not in client:
                client.append(i['Client'])
        if len(client) > 1:
            client=''
        else:
            client=client[0]+"_"

        defaultfilename = "Invoice_%s_%s%s.csv" % (getInvoiceNum(dictarray), client, getDate('-'))
        print "Please enter a filename (default is %s)" % defaultfilename
        filename=raw_input("> ")
        if filename == "" : filename=defaultfilename

        #Add rows for invoicing
        dictarray.append({})
        dictarray.append({'Multiplier':'Total Time:','Total':totalTime})
        dictarray.append({'Multiplier':'Total:','Total':total})
        dictarray.append({'Multiplier':'Total Invoiceable:','Total':totalInvoiceable})

        writeCSV(filename, dictarray, fields)

def getInvoiceNum(dictarray):
    InvoiceNum = 0
    for i in dictarray:
        if int(i['Invoice']) > InvoiceNum:
            InvoiceNum = int(i['Invoice'])
    return InvoiceNum

def invoiceHours(dictarray):
    # Ask which client to invoice, 'a' for all
    InvoiceNum = str(getInvoiceNum(dictarray)+1)
    client = userInput("Select a client to invoice ('a' for all)", getClients(dictarray))
    if client == '': client = 'a'

    # Copy uninvoiced lines to new array, print uninvoiced lines
    invoicableArray=[]
    for i in dictarray:
        if i['Invoice'] == '0' and 'End' in i:
            if client == 'a' or client == i['Client']:
                invoicableArray.append(i)
    for j in invoicableArray:
        j.update({'Invoice':str(InvoiceNum)})
    printPretty(invoicableArray)

    # Mark lines as invoiced after exporting file, return array
    if raw_input('Mark lines as invoiced? (y/n): ') != 'y':
        for i in dictarray:
            if i['Invoice'] == InvoiceNum and 'End' in i:
                if client == 'a' or client == i['Client']:
                    i.update({'Invoice':'0'})

    return dictarray

def getClients(dictarray):
    clients=[]
    for i in dictarray:
        if not i['Client'] in clients:
            clients.append(i['Client'])
    return clients

def getProjects(dictarray, client):
    projects=[]
    for i in dictarray:
        if i['Client'] == client:
            if not i['Project'] in projects:
                projects.append(i['Project'])
    return projects

def getNotes(dictarray, client, project):
    notes=[]
    for i in dictarray:
        if i['Client'] == client:
            if i['Project'] == project:
                if not i['Notes'] in notes:
                    notes.append(i['Notes'])
    return notes

def userInput(message, commands):
    import readline
    import rlcompleter
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
    def complete(text, state):
        for cmd in commands:
            if cmd.startswith(text):
                if not state:
                    return cmd
                else:
                    state -= 1
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)
    return raw_input('Enter %s: ' % message)

def startEntry(dictarray, quick):
    #creat new row
    newrow={}

    client=userInput("Client", getClients(dictarray))
    project=userInput("Project", getProjects(dictarray, client))
    notes=userInput("Notes", getNotes(dictarray, client, project))
    rate="0"

    #See if hours has been defined for this client
    if quick == 1:
        for old in range(len(dictarray)-1, -1, -1):
            if dictarray[old]['Client'] == client:
                rate=dictarray[old]['Rate']
                break

    if rate == "0":
        rate=raw_input("Rate: ")

    newrow.update({'Date':getDate()})
    newrow.update({'Start':getTime()})
    newrow.update({'Rate':rate})
    newrow.update({'Client':client})
    newrow.update({'Project':project})
    newrow.update({'Notes':notes})
    newrow.update({'Invoice':'0'})
    newrow.update({'Paid':'No'})

    return newrow

def calculateEntry(start, end, rate, multiplier):
    appendrow={}
    appendrow.update({'End':end})
    appendrow.update({'Total Time':subtractTime(start, appendrow['End'])})
    appendrow.update({'Sub Total':multiplyTime(appendrow['Total Time'], float(rate))})
    appendrow.update({'Multiplier':multiplier})
    appendrow.update({'Total':convertMoney(float(appendrow['Sub Total'])*float(multiplier))})
    return appendrow

def recalculateArray(dictarray):
    for row in dictarray:
        row.update(calculateEntry(row['Start'],row['End'],row['Rate'],row['Multiplier']))
    return dictarray

def resortArray(dictarray):
    import datetime
    resortedarray=sorted(dictarray, key=lambda row: datetime.datetime.strptime(row["Date"], "%m/%d/%Y"))
    return resortedarray

def closeEntry(dictarray, quick):
    print "Closing Entry..."
    appendrow={}
    if quick == 1:
        if 'Multiplier' not in dictarray[-1] or dictarray[-1]['Multiplier'] == '': multiplier = "1.0"
    else:
        multiplier=raw_input("Multiplier (default is 1.0): ")
        if multiplier == "" : multiplier = "1.0"
    start=dictarray[-1]['Start']
    rate=dictarray[-1]['Rate']
    end=getTime()
    appendrow.update(calculateEntry(start, end, rate, multiplier))
    return appendrow

def editEntry(dictarray, fields, line):
    appendrow={}
    for field in fields:
        if field in ['Total Time','Sub Total','Total']: continue #skip calculated fields
        print "Enter new value for", field, "(current value:", dictarray[line][field]+")"
        input=raw_input("> ")
        if input!='':
            appendrow.update({field:input})
        else:
            appendrow.update({field:dictarray[line][field]})

    #Recalculate values if clock is closed
    if appendrow['End'] != '':
        if appendrow['Multiplier'] == "" : appendrow.update({'Multiplier':"1.0"}) #Make it default value if unspecified
        appendrow.update(calculateEntry(appendrow['Start'], appendrow['End'], appendrow['Rate'], appendrow['Multiplier']))
    printPretty([appendrow])
    return appendrow

def selectEntryToEdit(dictarray, fields):
    printPrettyHeader()
    for i in range(len(dictarray)):
        print i,
        printPrettyLine(dictarray[i])

    default=len(dictarray)-1

    while 1:
        selection=raw_input("Select line to edit (default is %i): " % default)
        if selection == "":
            selection=default
            break
        selection=int(selection)
        if selection < 0 or selection > default:
            print "Invalid selection"
        else:
            break

    dictarray[selection].update(editEntry(dictarray, fields, selection))
    return dictarray

def printOutstanding(dictarray):
    temparray=[]
    for i in dictarray:
        if i['Paid'] == 'No':
            temparray.append(i)
    printPretty(temparray)
    return

def markInvoicesPaid(dictarray):
    uninvoiced=[]
    for i in dictarray:
        if i['Paid'] == 'No' and i['Invoice'] not in uninvoiced:
            uninvoiced.append(i['Invoice'])

    mPrint("-bold", "Outstanding Invoices")
    for i in uninvoiced:
        print i

    selection=raw_input("Select invoice to mark as paid (default is %s): " % uninvoiced[-1])
    if selection == "" : selection = uninvoiced[-1]

    for i in dictarray:
        if i['Invoice'] == selection:
            i.update({'Paid':'Yes'})

    return dictarray

def additionalCommands():
    mPrint("-bold", "-yellow", "\nAdditional Commands:")
    mPrint("-bold", " e)", "-reset", "Edit an entry")
    mPrint("-bold", " a)", "-reset", "Print all hours")
    mPrint("-bold", " m)", "-reset", "Print hours by month")
    mPrint("-bold", " s)", "-reset", "Search")
    mPrint("-bold", " u)", "-reset", "Update hours from CSV file")
    mPrint("-bold", " r)", "-reset", "Re-calculate and re-sortCSV File")
    print ""
    return

def main(csvfilename, dictarray, fields):
    #Main loop
    while 1:
        print ""
        clockIsOpen(dictarray, 1)
        mPrint("-bold", "-yellow", "\nPlease select option:")
        mPrint("-bold", " n)", "-reset", "Start New clock")
        mPrint("-bold", " c)", "-reset", "Close clock")
        mPrint("-bold", " i)", "-reset", "Show uninvoiced hours")
        mPrint("-bold", " o)", "-reset", "Show outstanding invoices")
        mPrint("-bold", " p)", "-reset", "Mark invoices number as paid")
        mPrint("-bold", " ?)", "-reset", "Additional commands")
        mPrint("-bold", " q)", "-reset", "Quit")
        print ""
        Selection=raw_input("> ").lower()

        if Selection == "q":
            quit()
        elif Selection == "n":
            if clockIsOpen(dictarray, 0): dictarray[-1].update(closeEntry(dictarray, 1))
            dictarray.append(startEntry(dictarray, 1))
        elif Selection == "c":
            if clockIsOpen(dictarray, 0): dictarray[-1].update(closeEntry(dictarray, 0))
            else: print "No clock to close"
        elif Selection == "e":
            dictarray = selectEntryToEdit(dictarray, fields)
        elif Selection == "i":
            dictarray=invoiceHours(dictarray)
        elif Selection == "a":
            printPretty(dictarray)
        elif Selection == "s":
            searchDict(dictarray)
        elif Selection == "m":
            searchByMonth(dictarray)
        elif Selection == "p":
            dictarray = markInvoicesPaid(dictarray)
        elif Selection == "o":
            printOutstanding(dictarray)
        elif Selection == "?":
            additionalCommands()
        elif Selection == "r":
            dictarray = recalculateArray(dictarray)
            dictarray = resortArray(dictarray)
        elif Selection == "u":
            dictarray = readCSV(csvfilename)
        else:
            print "Unknown selection..."
        #After each command, write to file...
        writeCSV(csvfilename, dictarray, fields)

#Variables
csvfilename='hours.csv'
fields=['Date', 'Start', 'End', 'Total Time', 'Rate', 'Sub Total', 'Multiplier', 'Total', 'Client', 'Project', 'Notes', 'Invoice', 'Paid']
verifyFileExists(csvfilename, fields)

#Import hours from file
dictarray = readCSV(csvfilename)

#Write backup file before making changes
writeCSV(csvfilename+"~", dictarray, fields)

#Start main program
main(csvfilename, dictarray, fields)
