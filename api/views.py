from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view

from py2neo import Graph,Node,Relationship
import pandas as pd
# Create your views here.

@api_view(['POST'])
def postCheck(request):
    
    dbURL = "bolt://localhost:7687"
    keywordGraph = Graph(dbURL,auth=("neo4j", "password"))
    word = request.data["keyword"]
    df = keywordGraph.run("MATCH(k:KEYWORD{key:" + '"' + word + '"' + "}) -[r]-> (c:CASE)  RETURN c.number,c.date,c.url").to_data_frame()
    ans = []
    # # df2 = df.to_json(orient = 'records')
    # # print(type(df2))
    for i in range(0,len(df)):
        ans.append({"number":df["c.number"][i],"date":df["c.date"][i],"url":df["c.url"][i]})
    print(ans)
    # temp = [{"date":"30.11.2010","number":5},{"date":"06.05.2019","number":12}]
    return Response(ans)

@api_view(['POST'])
def postKeywords(request):
    
    dbURL = "bolt://localhost:7687"
    keywordGraph = Graph(dbURL,auth=("neo4j", "password"))
    statement = request.data["statement"]

    #extract words from statement having comma separated keywords
    words = []
    temp = ""
    for i in range(0,len(statement)):
        if statement[i] == ',':
            words.append(temp)
            temp = ""
        else:
            temp += statement[i]
    print('looking for knife',words)
    words.append(temp)
    
    #extract keywords from the words array
    keywords = ['murder', 'robbery', 'assault', 'theft', 'burglary', 'arson', 'fraud', 'embezzlement', 'forgery', 'extortion', 'kidnapping', 'stalking', 'harassment', 'manslaughter', 'homicide', 'drug', 'conspiracy', 'terrorism', 'rape', 'sexual', 'domestic voilence', 'vandalism', 'child abuse', 'abduction', 'racketeering', 'money laundering', 'smuggling', 'public corruption', 'bribery', 'perjury', 'obstruction', 'blackmail', 'espionage', 'cybercrime', 'identity theft', 'assassination', 'human trafficking', 'prostitution', 'imprisonment', 'trespassing', 'explosives', 'guns', 'weapons', 'armed', 'hijacking', 'carjacking', 'counterfeiting', 'bootlegging', 'hacking', 'ponzi', 'insider trading', 'insolvency', 'kickback', 'bank mortgage', 'copyright infringement', 'misappropriation', 'arrest', 'police brutality', 'testimony', 'drunk and drive', 'hit and run', 'contract', 'tort', 'liability', 'breach', 'defamation', 'injunction', 'remedy', 'compensation', 'arbitration', 'mediation', 'settlement', 'evidence deposition', 'interrogatory', 'pleading',   'frauds', 'fraudulent', 'conveyance', 'real estate', 'construction', 'intellectual property', 'trademark', 'patent infringement', 'trade secret', 'consumer protection', 'malpractice', 'personal injury', 'wrongful', 'death', 'discrimination', 'retaliation', 'whistleblower', 'non disclosure', 'shareholder', 'business dissolution', 'bankruptcy', 'debt collection', 'foreclosure', 'immigration', 'probate', 'divorce', 'child custody', 'alimony', 'adoption', 'surrogacy', 'property', 'easement', 'zoning', 'hoa', 'landlord tenant', 'eviction', 'internet', 'online defamation', 'cyberbullying', 'privacy violation', 'data breach', 'socialmedia fraud', 'maritime', 'aviation', 'insurance', 'reinsurance', 'recall franchise', 'accomplice', 'acquittal', 'aggravated assault', 'alibi', 'arraignment', 'bail', 'capital punishment', 'conviction', 'corpus delicti', 'criminal intent', 'double jeopardy', 'exculpatory evidence', 'extradition', 'felony', 'habeas corpus', 'indictment', 'infraction', 'insanity defense', 'jail', 'larceny', 'mistrial', 'probation', 'search warrant',  'subpoena', 'voir dire', 'wiretap', 'wrongful death', 'zero tolerance policy', 'premeditated', 'intentional', 'accidental',  'weapon', 'strangulation', 'asphyxiation', 'stabbing', 'shooting', 'poisoning', 'blunt force trauma', 'forensic evidence', 'autopsy', 'blood spatter', 'confession', 'premeditation', 'first-degree murder', 'second-degree murder', 'felony murder', 'attempted murder', 'self defense', 'justifiable homicide', 'mental illness', 'provocation', 'heat of passion', 'death penalty', 'life imprisonment']
    keyword_dict = {}
    extracted_keywords = []
    for i in keywords:
        keyword_dict[i] = True

    for i in words:
        if keyword_dict.get(i) is not None:
            extracted_keywords.append(i)
    # print(extracted_keywords)

    #extract cases corresponding to every extracted keyword
    # anstable = pd.DataFrame()
    # for word in extracted_keywords:
    #     temp = keywordGraph.run("MATCH(c:CASE) -[r]->(k:KEYWORD{key:" + '"' + word + '"' + "})  RETURN c.number").to_data_frame()
    #     anstable = anstable.append(temp,ignore_index = True)

    anstable = pd.DataFrame()
    for word in extracted_keywords:
        temp = keywordGraph.run("MATCH(c:CASE) -[r]->(k:KEYWORD{key:" + '"' + word + '"' + "})  RETURN c.number,c.date,c.url").to_data_frame()
        anstable = pd.concat([anstable, temp], ignore_index=True)

    # print(anstable)

    #calculate freq of cases occuring
    case_freq = {}
    cases = []
    date_dict = {}
    url_dict = {}
    for i in range(0,len(anstable)): 
        if case_freq.get(anstable["c.number"][i]) is None:
            case_freq[anstable["c.number"][i]] = 1
            date_dict[anstable["c.number"][i]] = anstable["c.date"][i]
            url_dict[anstable["c.number"][i]] = anstable["c.url"][i]
        else:
            case_freq[anstable["c.number"][i]] = case_freq[anstable["c.number"][i]] + 1
    cases=list(case_freq.items())
    # print(cases)

    #decreasingly sort cases based on their frequency of occuring and get top 3 cases
    cases.sort(key = lambda a:a[1])
    cases.reverse()
    cases_list = []
    for i in range(0,min(3,len(cases))):
        cases_list.append({"number":cases[i][0],"date":date_dict[cases[i][0]],"url":url_dict[cases[i][0]]})
    # print(cases_list)

    return Response(cases_list)

@api_view(['POST'])
def postArticles(request):
    
    dbURL = "bolt://localhost:7687"
    keywordGraph = Graph(dbURL,auth=("neo4j", "password"))
    statement = request.data["statement"]

    #extract words from statement having comma separated keywords
    words = []
    temp = ""
    for i in range(0,len(statement)):
        if statement[i] == ',':
            words.append(temp)
            temp = ""
        else:
            temp += statement[i]
    words.append(temp)
    
    #extract keywords from the words array
    keywords = ['murder', 'robbery', 'assault', 'theft', 'burglary', 'arson', 'fraud', 'embezzlement', 'forgery', 'extortion', 'kidnapping', 'stalking', 'harassment', 'manslaughter', 'homicide', 'drug', 'conspiracy', 'terrorism', 'rape', 'sexual', 'domestic voilence', 'vandalism', 'child abuse', 'abduction', 'racketeering', 'money laundering', 'smuggling', 'public corruption', 'bribery', 'perjury', 'obstruction', 'blackmail', 'espionage', 'cybercrime', 'identity theft', 'assassination', 'human trafficking', 'prostitution', 'imprisonment', 'trespassing', 'explosives', 'guns', 'weapons', 'armed', 'hijacking', 'carjacking', 'counterfeiting', 'bootlegging', 'hacking', 'ponzi', 'insider trading', 'insolvency', 'kickback', 'bank mortgage', 'copyright infringement', 'misappropriation', 'arrest', 'police brutality', 'testimony', 'drunk and drive', 'hit and run', 'contract', 'tort', 'liability', 'breach', 'defamation', 'injunction', 'remedy', 'compensation', 'arbitration', 'mediation', 'settlement', 'evidence deposition', 'interrogatory', 'pleading',   'frauds', 'fraudulent', 'conveyance', 'real estate', 'construction', 'intellectual property', 'trademark', 'patent infringement', 'trade secret', 'consumer protection', 'malpractice', 'personal injury', 'wrongful', 'death', 'discrimination', 'retaliation', 'whistleblower', 'non disclosure', 'shareholder', 'business dissolution', 'bankruptcy', 'debt collection', 'foreclosure', 'immigration', 'probate', 'divorce', 'child custody', 'alimony', 'adoption', 'surrogacy', 'property', 'easement', 'zoning', 'hoa', 'landlord tenant', 'eviction', 'internet', 'online defamation', 'cyberbullying', 'privacy violation', 'data breach', 'socialmedia fraud', 'maritime', 'aviation', 'insurance', 'reinsurance', 'recall franchise', 'accomplice', 'acquittal', 'aggravated assault', 'alibi', 'arraignment', 'bail', 'capital punishment', 'conviction', 'corpus delicti', 'criminal intent', 'double jeopardy', 'exculpatory evidence', 'extradition', 'felony', 'habeas corpus', 'indictment', 'infraction', 'insanity defense', 'jail', 'larceny', 'mistrial', 'probation', 'search warrant',  'subpoena', 'voir dire', 'wiretap', 'wrongful death', 'zero tolerance policy', 'premeditated', 'intentional', 'accidental',  'weapon', 'strangulation', 'asphyxiation', 'stabbing', 'shooting', 'poisoning', 'blunt force trauma', 'forensic evidence', 'autopsy', 'blood spatter', 'confession', 'premeditation', 'first-degree murder', 'second-degree murder', 'felony murder', 'attempted murder', 'self defense', 'justifiable homicide', 'mental illness', 'provocation', 'heat of passion', 'death penalty', 'life imprisonment']
    keyword_dict = {}
    extracted_keywords = []
    for i in keywords:
        keyword_dict[i] = True

    for i in words:
        if keyword_dict.get(i) is not None:
            extracted_keywords.append(i)
    # print(extracted_keywords)

    #extract cases corresponding to every extracted keyword
    # anstable = pd.DataFrame()
    # for word in extracted_keywords:
    #     temp = keywordGraph.run("MATCH(c:CASE) -[r]->(k:KEYWORD{key:" + '"' + word + '"' + "})  RETURN c.number").to_data_frame()
    #     anstable = anstable.append(temp,ignore_index = True)

    anstable = pd.DataFrame()
    for word in extracted_keywords:
        temp = keywordGraph.run("MATCH(c:CASE) -[r]->(k:KEYWORD{key:" + '"' + word + '"' + "})  RETURN c.number,c.date,c.url").to_data_frame()
        anstable = pd.concat([anstable, temp], ignore_index=True)

    # print(anstable)

    #calculate freq of cases occuring
    case_freq = {}
    cases = []
    date_dict = {}
    url_dict={}
    for i in range(0,len(anstable)): 
        if case_freq.get(anstable["c.number"][i]) is None:
            case_freq[anstable["c.number"][i]] = 1
            date_dict[anstable["c.number"][i]] = anstable["c.date"][i]
            url_dict[anstable["c.number"][i]] = anstable["c.url"][i]
        else:
            case_freq[anstable["c.number"][i]] = case_freq[anstable["c.number"][i]] + 1
    cases=list(case_freq.items())
    # print(cases)

    #decreasingly sort cases based on their frequency of occuring and get top 3 cases
    cases.sort(key = lambda a:a[1])
    cases.reverse()
    cases_list = []
    for i in range(0,min(3,len(cases))):
        cases_list.append({"number":cases[i][0],"date":date_dict[cases[i][0]],"url":url_dict[cases[i][0]]})
    # print(cases_list)

    #articles graph
    graph = Graph(dbURL,name="articles", auth=("neo4j", "password"))

    #finding common cases which have same articles as the cases_list
    ans = pd.DataFrame()
    for i in range(len(cases_list)):
        temp = cases_list[i]["number"]
        print("temp",temp)
        # print(temp)
        resultTable = graph.run('''MATCH(c1:CASE{number:''' + str(temp) + '''}) -[r:ARTICLE_RELATED]->(a:ARTICLE) <-[r2:ARTICLE_RELATED]- (c2:CASE)
        RETURN c2.number,c2.date,c2.url,count(a) as x
        ORDER BY count(a) DESC''').to_data_frame()
        ans = pd.concat([ans,resultTable],ignore_index = True)
    # print(ans)

    #sorting by most commonly occuring
    result = ans.sort_values(by = 'x', ascending = False)
    result = result.reset_index(drop = True)

    #assigning dates and urls to case numbers
    for i in range(0,len(result)):
        date_dict[result['c2.number'][i]] = result['c2.date'][i]
        url_dict[result['c2.number'][i]] = result['c2.url'][i]
    
    #removing duplicates
    # final_ans = cases_list
    final_ans = []
    check_duplicate = {}
    for i in range(0,len(cases_list)):
        if check_duplicate.get(cases_list[i]["number"]) == None:
            check_duplicate[cases_list[i]["number"]] = 1

    count = len(final_ans)
    for i in range(0,len(result)):
        if count == 2:
            break
        if check_duplicate.get(result['c2.number'][i]) == None:
            check_duplicate[result['c2.number'][i]] = 1
            count = count + 1
            final_ans.append({"number":result['c2.number'][i],"date":date_dict[result['c2.number'][i]],"url":url_dict[result['c2.number'][i]]})
    print(final_ans)

    return Response(final_ans)

@api_view(['POST'])
def postSections(request):
    
    dbURL = "bolt://localhost:7687"
    keywordGraph = Graph(dbURL,auth=("neo4j", "password"))
    statement = request.data["statement"]

    #extract words from statement having comma separated keywords
    words = []
    temp = ""
    for i in range(0,len(statement)):
        if statement[i] == ',':
            words.append(temp)
            temp = ""
        else:
            temp += statement[i]
    words.append(temp)
    
    #extract keywords from the words array
    keywords = ['murder', 'robbery', 'assault', 'theft', 'burglary', 'arson', 'fraud', 'embezzlement', 'forgery', 'extortion', 'kidnapping', 'stalking', 'harassment', 'manslaughter', 'homicide', 'drug', 'conspiracy', 'terrorism', 'rape', 'sexual', 'domestic voilence', 'vandalism', 'child abuse', 'abduction', 'racketeering', 'money laundering', 'smuggling', 'public corruption', 'bribery', 'perjury', 'obstruction', 'blackmail', 'espionage', 'cybercrime', 'identity theft', 'assassination', 'human trafficking', 'prostitution', 'imprisonment', 'trespassing', 'explosives', 'guns', 'weapons', 'armed', 'hijacking', 'carjacking', 'counterfeiting', 'bootlegging', 'hacking', 'ponzi', 'insider trading', 'insolvency', 'kickback', 'bank mortgage', 'copyright infringement', 'misappropriation', 'arrest', 'police brutality', 'testimony', 'drunk and drive', 'hit and run', 'contract', 'tort', 'liability', 'breach', 'defamation', 'injunction', 'remedy', 'compensation', 'arbitration', 'mediation', 'settlement', 'evidence deposition', 'interrogatory', 'pleading',   'frauds', 'fraudulent', 'conveyance', 'real estate', 'construction', 'intellectual property', 'trademark', 'patent infringement', 'trade secret', 'consumer protection', 'malpractice', 'personal injury', 'wrongful', 'death', 'discrimination', 'retaliation', 'whistleblower', 'non disclosure', 'shareholder', 'business dissolution', 'bankruptcy', 'debt collection', 'foreclosure', 'immigration', 'probate', 'divorce', 'child custody', 'alimony', 'adoption', 'surrogacy', 'property', 'easement', 'zoning', 'hoa', 'landlord tenant', 'eviction', 'internet', 'online defamation', 'cyberbullying', 'privacy violation', 'data breach', 'socialmedia fraud', 'maritime', 'aviation', 'insurance', 'reinsurance', 'recall franchise', 'accomplice', 'acquittal', 'aggravated assault', 'alibi', 'arraignment', 'bail', 'capital punishment', 'conviction', 'corpus delicti', 'criminal intent', 'double jeopardy', 'exculpatory evidence', 'extradition', 'felony', 'habeas corpus', 'indictment', 'infraction', 'insanity defense', 'jail', 'larceny', 'mistrial', 'probation', 'search warrant',  'subpoena', 'voir dire', 'wiretap', 'wrongful death', 'zero tolerance policy', 'premeditated', 'intentional', 'accidental',  'weapon', 'strangulation', 'asphyxiation', 'stabbing', 'shooting', 'poisoning', 'blunt force trauma', 'forensic evidence', 'autopsy', 'blood spatter', 'confession', 'premeditation', 'first-degree murder', 'second-degree murder', 'felony murder', 'attempted murder', 'self defense', 'justifiable homicide', 'mental illness', 'provocation', 'heat of passion', 'death penalty', 'life imprisonment']
    keyword_dict = {}
    extracted_keywords = []
    for i in keywords:
        keyword_dict[i] = True

    for i in words:
        if keyword_dict.get(i) is not None:
            extracted_keywords.append(i)
    # print(extracted_keywords)

    #extract cases corresponding to every extracted keyword
    # anstable = pd.DataFrame()
    # for word in extracted_keywords:
    #     temp = keywordGraph.run("MATCH(c:CASE) -[r]->(k:KEYWORD{key:" + '"' + word + '"' + "})  RETURN c.number").to_data_frame()
    #     anstable = anstable.append(temp,ignore_index = True)

    anstable = pd.DataFrame()
    for word in extracted_keywords:
        temp = keywordGraph.run("MATCH(c:CASE) -[r]->(k:KEYWORD{key:" + '"' + word + '"' + "})  RETURN c.number,c.date,c.url").to_data_frame()
        anstable = pd.concat([anstable, temp], ignore_index=True)

    # print(anstable)

    #calculate freq of cases occuring
    case_freq = {}
    cases = []
    date_dict = {}
    url_dict={}
    for i in range(0,len(anstable)): 
        if case_freq.get(anstable["c.number"][i]) is None:
            case_freq[anstable["c.number"][i]] = 1
            date_dict[anstable["c.number"][i]] = anstable["c.date"][i]
            url_dict[anstable["c.number"][i]] = anstable["c.url"][i]
        else:
            case_freq[anstable["c.number"][i]] = case_freq[anstable["c.number"][i]] + 1
    cases=list(case_freq.items())
    # print(cases)

    #decreasingly sort cases based on their frequency of occuring and get top 3 cases
    cases.sort(key = lambda a:a[1])
    cases.reverse()
    cases_list = []
    for i in range(0,min(3,len(cases))):
        cases_list.append({"number":cases[i][0],"date":date_dict[cases[i][0]],"url":url_dict[cases[i][0]]})
    # print(cases_list)

    #sections graph
    graph = Graph(dbURL,name="sections", auth=("neo4j", "password"))

    #finding common cases which have same sections as the cases_list
    ans = pd.DataFrame()
    for i in range(len(cases_list)):
        temp = cases_list[i]["number"]
        print("temp",temp)
        # print(temp)
        resultTable = graph.run('''MATCH(c1:CASE{number:''' + str(temp) + '''}) -[r:SECTION_RELATED]->(s:SECTION) <-[r2:SECTION_RELATED]- (c2:CASE)
        RETURN c2.number,c2.date,c2.url,count(s) as x
        ORDER BY count(s) DESC''').to_data_frame()
        ans = pd.concat([ans,resultTable],ignore_index = True)
    # print(ans)

    #sorting by most commonly occuring
    result = ans.sort_values(by = 'x', ascending = False)
    result = result.reset_index(drop = True)

    #assigning dates and urls to case numbers
    for i in range(0,len(result)):
        date_dict[result['c2.number'][i]] = result['c2.date'][i]
        url_dict[result['c2.number'][i]] = result['c2.url'][i]
    
    #removing duplicates
    # final_ans = cases_list
    final_ans = []
    check_duplicate = {}
    for i in range(0,len(cases_list)):
        if check_duplicate.get(cases_list[i]["number"]) == None:
            check_duplicate[cases_list[i]["number"]] = 1

    count = len(final_ans)
    for i in range(0,len(result)):
        if count == 3:
            break
        if check_duplicate.get(result['c2.number'][i]) == None:
            check_duplicate[result['c2.number'][i]] = 1
            count = count + 1
            final_ans.append({"number":result['c2.number'][i],"date":date_dict[result['c2.number'][i]],"url":url_dict[result['c2.number'][i]]})
    print(final_ans)
    return Response(final_ans)


@api_view(['POST'])
def postOnlySections(request):

    dbURL = "bolt://localhost:7687"
    sectionsGraph = Graph(dbURL,name="sections",auth=("neo4j", "password"))
    statement = request.data["statement"]

    #extract words from statement having comma separated keywords
    words = []
    temp = ""
    for i in range(0,len(statement)):
        if statement[i] == ',':
            words.append(temp)
            temp = ""
        else:
            temp += statement[i]
    words.append(temp)
    
    #extract sections from the words array
    sections = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "29A", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "52A", "53", "53A", "54", "55", "55A", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", "91", "92", "93", "94", "95", "96", "97", "98", "99", "100", "101", "102", "103", "104", "105", "106", "107", "108", "108A", "109", "110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120", "120A", "120B", "121", "121A", "122", "123", "124", "124A", "125", "126", "127", "128", "129", "130", "131", "132", "133", "134", "135", "136", "137", "138", "138A", "139", "140", "141", "142", "143", "144", "145", "146", "147", "148", "149", "150", "151", "152", "153", "153A", "153AA", "153B", "154", "155", "156", "157", "158", "159", "160", "161", "162", "163", "164", "165", "165A", "166", "166A", "166B", "167", "168", "169", "170", "171", "171A", "171B", "171C", "171D", "171E", "171F", "171G", "171H", "171I", "172", "173", "174", "174A", "175", "176", "177", "178", "179", "180", "181", "182", "183", "184", "185", "186", "187", "188", "189", "190", "191", "192", "193", "194", "195", "195A", "196","197","198","199","200", "201", "202", "203", "204", "205", 
            "206", "207", "208", "209", "210", "211", "212", "213", "214", "215", "216", "216A", "216B", "217", "218", "219", "220", "221", "222", "223", "224", "225", "225A", "225B", "226", "227", "228", "228A", "229", "229A", "230", "231", "232", "233", "234", "235", "236", "237", "238", "239", "240", "241", "242", "243", "244", "245", "246", "247", "248", "249", "250", "251", "252", "253", "254", "255", "256", "257", "258", "259", "260", "261", "262", "263", "263A", "264", "265", "266", "267", "268", "269", "270", "271", "272", "273", "274", "275", "276", "277", "278", "279", "280", "281", "282", "283", "284", "285", "286", "287", "288", "289", "290", "291", "292", "293", "294", "294A", "295", "295A", "296", "297", "298", "299", "300", "301", "302", "303", "304", "304A", "304B", "305", "306", "307", "308", "309", "310", "311", "312", "313", "314", "315", "316", "317", "318", "319", "320", "321", "322", "323", "324", "325", "326", "326A", "326B", "327", "328", "329", "330", "331", "332", "333", "334", "335", "336", "337", "338", "339", "340", "341", "342", "343", "344", "345", "346", "347", "348", "349", "350", "351", "352", "353", "354", "354A", "354B", "354C", "354D", "355", "356", "357", "358", "359", "360", "361", "362", "363", "363A", "364", "364A", "365", "366", "366A", "366B", "367", "368", "369", "370", "370A", "371", "372", "373", "374", "375", "376", "376A", "376AB", "376B", "376C", "376D", "376DA", "376DB", "376E", "377", "378", "379", "380", "381", "382", "383", "384", "385", "386", "387", "388", "389", "390",
            "391", "392", "393", "394", "395", "396", "397", "398", "399", "400", "401", "402", "403", 
            "404", "405", "406", "407", "408", "409", "410", "411", "412", "413", "414", "415", "416", "417", "418", "419", "420", "421", "422", "423", "424", "425", "426", "427", "428", "429", "430", "431", "432", "433", "434", "435", "436", "437", "438", "439", "440", "441", "442", "443", "444", "445", "446", "447", "448", "449", "450", "451", "452", "453", "454", "455", "456", "457", "458", "459", "460", "461", "462", "463", "464", "465", "466", "467", "468", "469", "470", "471", "472", "473", "474", "475", "476", "477", "477A", "478", "479", "480", 
            "481", "482", "483", "484", "485", "486", "487", "488", "489", 
            "489A", "489B", "489C", "489D", "489E", "490", "491", "492", "493", "494", "495", "496", "497", "498", "498A", "499", "500", "501", "502","503", "504", "505","506", "507", "508", "509", "510","511"]
    sections_dict = {}
    extracted_sections = []
    for i in sections:
        sections_dict[i] = True

    for i in words:
        if sections_dict.get(i) is not None:
            extracted_sections.append(i)
    # print(extracted_keywords)

    #extract cases corresponding to every extracted keyword
    # anstable = pd.DataFrame()
    # for word in extracted_keywords:
    #     temp = keywordGraph.run("MATCH(c:CASE) -[r]->(k:KEYWORD{key:" + '"' + word + '"' + "})  RETURN c.number").to_data_frame()
    #     anstable = anstable.append(temp,ignore_index = True)

    anstable = pd.DataFrame()
    for word in extracted_sections:
        temp = sectionsGraph.run("MATCH(c:CASE) -[r]->(s:SECTION{number:" + '"' + word + '"' + "})  RETURN c.number,c.date,c.url").to_data_frame()
        anstable = pd.concat([anstable, temp], ignore_index=True)

    # print(anstable)

    #calculate freq of cases occuring
    case_freq = {}
    cases = []
    date_dict = {}
    url_dict = {}
    for i in range(0,len(anstable)): 
        if case_freq.get(anstable["c.number"][i]) is None:
            case_freq[anstable["c.number"][i]] = 1
            date_dict[anstable["c.number"][i]] = anstable["c.date"][i]
            url_dict[anstable["c.number"][i]] = anstable["c.url"][i]
        else:
            case_freq[anstable["c.number"][i]] = case_freq[anstable["c.number"][i]] + 1
    cases=list(case_freq.items())
    # print(cases)

    #decreasingly sort cases based on their frequency of occuring and get top 3 cases
    cases.sort(key = lambda a:a[1])
    cases.reverse()
    cases_list = []
    for i in range(0,min(3,len(cases))):
        cases_list.append({"number":cases[i][0],"date":date_dict[cases[i][0]],"url":url_dict[cases[i][0]]})
    # print(cases_list)

    return Response(cases_list)

@api_view(['POST'])
def postOnlyArticles(request):

    dbURL = "bolt://localhost:7687"
    articlesGraph = Graph(dbURL,name="articles",auth=("neo4j", "password"))
    statement = request.data["statement"]

    #extract words from statement having comma separated keywords
    words = []
    temp = ""
    for i in range(0,len(statement)):
        if statement[i] == ',':
            words.append(temp)
            temp = ""
        else:
            temp += statement[i]
    words.append(temp)
    
    #extract articles from the words array
    articles = ["1", "2", "2A", "3", "4", "5", "6", "7", "8", "9", "10","11", "12", "13", "14", "15", "16", "17", "18", "19", "20","21", "21A", "22", "23", "24", "25", "26", "27", "28", "29",
        "30", "31", "31A", "31B", "31C", "31D", "32", "32A", "33", "34", "35", "36", "37", "38",
        "39", "39A", "40", "41", "42", "43", "43A", "44", "45", "46", "47",
        "48", "48A", "49", "50", "51", "51A", "52", "53", "54", "55", "56",
        "57", "58", "59", "60", "61", "62", "63", "64", "65", "66",
        "67", "68", "69", "70", "71", "72", "73", "74", "75", "76",
        "77", "78", "79", "80", "81", "82", "83", "84", "85", "86",
        "87", "88", "89", "90", "91", "92", "93", "94", "95", "96",
        "97", "98", "99", "100", "101", "102", "103", "104", "105", "106",
        "107", "108", "109", "110", "111", "112", "113", "114", "115", "116",
        "117", "118", "119", "120", "121", "122", "123", "124", "125", "126",
        "127", "128", "129", "130", "131", "131A", "132", "133", "134", "134A", "135", "136",
        "137", "138", "139", "139A", "140", "141", "142", "143", "144", "144A", "145", "146",
        "147", "148", "149", "150", "151", "152", "153", "154", "155", "156",
        "157", "158", "159", "160", "161", "162", "163", "164", "165", "166",
        "167", "168", "169", "170", "171", "172", "173", "174", "175", "176",
        "177", "178", "179", "180", "181", "182", "183", "184", "185", "186",
        "187", "188", "189", "190", "191", "192", "193", "194", "195", "196",
        "197","198","199","200", "201", "202", "203", "204", "205", "206",
        "207", "208", "209", "210", "211", "212", "213", "214", "215", "216",
        "217", "218", "219", "220", "221", "222", "223", "224", "224A", "225", "226", "226A",
        "227", "228", "228A", "229", "230", "231", "232", "233", "233A", "234", "235", "236",
        "237", "238", "239", "239A", "239AA", "239AB", "240", "241", "242", "243", "243A", "243B", "243C", "243D", "243E", "243F", "243G", "243H", "243I", "243J", "243K", "243L", "243M", "243N", "243O", "243P", "243Q", "243R", "243S", "243T", "243U", "243V", "243W", "243X", "243Y", "243Z", "243ZA", "243ZB", "243ZC", "243ZD", "243ZE", "243ZF", "243ZG", "243ZH", "243ZI", "243ZJ", "243ZK", "243ZL", "243ZM", "243ZN", "243ZO", "243ZP", "243ZQ", "243ZR", "243ZS", "243ZT", "244", "244A", "245", "246",
        "247", "248", "249", "250", "251", "252", "253", "253", "254", "255", "256", "257", "257A", "258", "258A", "259", "260", "261", "262",
        "263", "264", "265", "266", "267", "268", "268A", "269", "270", "271", "272",
        "273", "274", "275", "276", "277", "278", "279", "280", "281", "282",
        "283", "284", "285", "286", "287", "288", "289", "290", "290A", "291", "292",
        "293", "294", "295", "296", "297", "298", "299", "300", "300A", "301", "302",
        "303", "304", "305", "306", "307", "308", "309", "310", "311", "312", "312A",
        "313", "314", "315", "316", "317", "318", "319", "320", "321", "322",
        "323", "323A", "323B", "324", "325", "326", "327", "328", "329", "329A", "330", "331", "332",
        "333", "334", "335", "336", "337", "338", "338A", "339", "340", "341", "342",
        "343", "344", "345", "346", "347", "348", "349", "350", "350A", "350B", "351", "352",
        "353", "354", "355", "356", "357", "358", "359","359A","360","361", "361A", "361B", "362",
        "363", "363A", "364", "365", "366", "367", "368", "369", "370", "371", "371A", "371B", "371C", "371D", "371E", "371F", "371G", "371H", "371-I", "371J", "372", "372A",
        "373", "374", "375", "376", "377", "378", "378A", "379", "380", "381", "382",
        "383", "384", "385", "386", "387", "388", "389", "390", "391", "392",
        "393", "394","394A","395"]
    articles_dict = {}
    extracted_articles = []
    for i in articles:
        articles_dict[i] = True

    for i in words:
        if articles_dict.get(i) is not None:
            extracted_articles.append(i)
    # print(extracted_keywords)

    #extract cases corresponding to every extracted keyword
    # anstable = pd.DataFrame()
    # for word in extracted_keywords:
    #     temp = keywordGraph.run("MATCH(c:CASE) -[r]->(k:KEYWORD{key:" + '"' + word + '"' + "})  RETURN c.number").to_data_frame()
    #     anstable = anstable.append(temp,ignore_index = True)

    anstable = pd.DataFrame()
    for word in extracted_articles:
        temp = articlesGraph.run("MATCH(c:CASE) -[r]->(a:ARTICLE{number:" + '"' + word + '"' + "})  RETURN c.number,c.date,c.url").to_data_frame()
        anstable = pd.concat([anstable, temp], ignore_index=True)

    # print(anstable)

    #calculate freq of cases occuring
    case_freq = {}
    cases = []
    date_dict = {}
    url_dict = {}
    for i in range(0,len(anstable)): 
        if case_freq.get(anstable["c.number"][i]) is None:
            case_freq[anstable["c.number"][i]] = 1
            date_dict[anstable["c.number"][i]] = anstable["c.date"][i]
            url_dict[anstable["c.number"][i]] = anstable["c.url"][i]
        else:
            case_freq[anstable["c.number"][i]] = case_freq[anstable["c.number"][i]] + 1
    cases=list(case_freq.items())
    # print(cases)

    #decreasingly sort cases based on their frequency of occuring and get top 3 cases
    cases.sort(key = lambda a:a[1])
    cases.reverse()
    cases_list = []
    for i in range(0,min(3,len(cases))):
        cases_list.append({"number":cases[i][0],"date":date_dict[cases[i][0]],"url":url_dict[cases[i][0]]})
    # print(cases_list)

    return Response(cases_list)

