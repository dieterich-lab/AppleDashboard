

"""
# How long Patient had Apple Watch on hand
health_data = pd.read_csv('apple_health_modification.csv',low_memory=False)
Patient1 = health_data[health_data['@sourceName'] == 'Patient1']
Patient1 = Patient1.sort_values(by=['@startDate'])
Patient1['date'] = pd.to_datetime(Patient1['date'], format='%Y-%m-%d')
Patient1['@startDate'] = pd.to_datetime(Patient1['@startDate'])


data1 = Patient1.loc[(Patient1['@type'] == 'HKQuantityTypeIdentifierHeartRate')]
days = data1['date'].unique()

total_sec = np.vectorize(lambda x: x.total_seconds())
list1 =[]
for a in days:
    data2 = data1.loc[data1['date'] == a]
    N=len(data2)
    if N > 1:
        diff = total_sec(np.diff(data2['@startDate']))
        diff= np.insert(diff,0,0)
        list1 =[*list1, *diff]

        #get values smallet than 15 min
        diff_small_than_900 = filter(lambda x: x >= 900, diff)
        time = sum(diff_small_than_900 )
    elif N == 1:
        list1.append(0)
data1['diff']=list1
data1.to_csv('diff')

d = {'Date': days,'Time':time}
df = pd.DataFrame(d)

"""