from django.shortcuts import render, redirect
from django.contrib import messages
from .form import *
from operator import itemgetter


with open('media/hemle.csv') as hemle:
    hemle_file = hemle.readlines()

hem = []
for row in hemle_file:
    row = row.split(';')[:-1]
    # print(row)
    hem.append(row)


for i in range(len(hem)):

    if i == 0:
        change = hem[0][0]
        hem[0][0] = change[3:]

    else:
        for k in range(len(hem[i])):
             if k !=0:
                 hem[i][k] = int(hem[i][k])
# print(hem[1:-1])

with open('media/Mango.csv') as Man:
    mango_file = Man.readlines()
mango = []
for row in mango_file:
    row = row.split(';')
    mango.append(row)
# print(mango)

for i in range(len(mango)):
    if i==0:
        change = mango[0][0]
        mango[0][0] = change[3:]
    else:
        for k in range(len(mango[i])):
            if k!=0:
                mango[i][k] = int(mango[i][k])


# print(mango)

#pour Mango , liste = mango[1:] , pour hemle , liste = hem[1:-1]
def betterOptions2(liste,price, days, dataValue, callValue, smsValue):
    liste_local = liste
    options = []
    if (dataValue == 0 and callValue == 0 and smsValue == 0) or (price == 0 or days == 0):
        return []
    for i in liste_local:
        if i[-1] <= price:
            options.append(i)

    # print(options)
    data = []
    sms = []
    call = []
    for i in options:
        data.append(i[3])
        sms.append(i[1])
        call.append(i[2])
    max_data = max(data)
    min_data = min(data)
    max_sms = max(sms)
    min_sms = min(sms)
    max_call = max(call)
    min_call = min(call)

    for i in options:
#proceder de normalisation des donnees
        try:
            data_i = (i[3]-min_data)/(max_data-min_data)
            sms_i = (i[1]-min_sms)/(max_sms-min_sms)
            call_i = (i[2]-min_call)/(max_call-min_call)
            new = dataValue*data_i + sms_i*smsValue + call_i*callValue
            i.append(new)
        except ZeroDivisionError:
            return []

    # print('new options',options)

    resp = sorted(options, key=itemgetter(-1), reverse=True)
    # print('resp', resp)

    final =[]
    for i in resp:
        if dataValue != 0 and i[3] == 0:
            continue
        if smsValue !=0 and i[1] == 0:
            continue
        if callValue !=0 and i[2] == 0:
            continue
        final.append(i)
    print('finally', final)
    return final

def generateWS(liste):
    S = []

    for i in liste:
       wi = (i[5], i[-1])
       S.append(wi)
    return S

def BottomUpKnapsack(listeS,price):
    cache = [[0] * (price + 1) for i in range(len(listeS) + 1)]
    for i in range(1, len(listeS) + 1):

        for w in range(price + 1):

             if listeS[i - 1][0] > w:
                    cache[i][w] = cache[i - 1][w]
             else:

                    cache[i][w] = max(cache[i - 1][w], listeS[i - 1][1] + cache[i - 1][w - listeS[i - 1][0]])

    # print('cache',cache)

    return cache


#transforme la somme obtenu
def ObjectOfSum(listeS,value):
    response = []
    summ = 0
    for i in listeS:
        if summ+i[1] <= value:
            summ = summ+i[1]
            response.append(i)
    # print('response',response)
    return response




def BestOptions(listeS,price,options):
    listprices = []
    for i in listeS:
        listprices.append(i[0])
    cache = BottomUpKnapsack(listeS, price)
    resp = set()
    #recupere les sommes des valeurs des objets de listeS qui pour le poids entree par l'user
    #maximise la valeur
    # print(cache)
    for i in range(len(cache)):
        if cache[i][price] != 0:
            resp.add(cache[i][price])
    # print(resp)

    if len(resp) == 0:
        return []
    else:
        response = ObjectOfSum(listeS, max(resp))
        # print(response)
        enfin = []
        for i in response:

            for j in options:

                if i[0] == j[5] and i[1] == j[-1]:
                    enfin.append(j)
        # print('finalement', enfin)
        return enfin


# Create your views here.
def home(request):

    form = InputForm()
    if request.method == 'POST':

            days = request.POST['days']
            price = request.POST['price']
            smsvalue = request.POST['sms']
            callvalue = request.POST['call']
            datavalue = request.POST['data']
            # print('price', int(price))
            try:
                price1 = int(price)
                url = 'best/' + price + '/' + days + '/' + datavalue + '/' + smsvalue + '/' + callvalue
                return redirect(url)
            except:
                 print('error')
                 messages.error(request, ' price should not be a word ')

    contexte = {'form':form}
    return render(request, 'deals/index.html',contexte)



def solutions(request,price,days,datavalue,callvalue,smsvalue):

    #premiere etape: trouver tous les forfaits possibles en ponderant nos solutions

    options_mango = betterOptions2(mango[1:], price, days, datavalue, callvalue, smsvalue)
    options_hemle = betterOptions2(hem[1:-1], price, days, datavalue, callvalue, smsvalue)

    if len(options_hemle) !=0:
    #Transformer les forfaits en liste de poids valeurs

        listeS_hemle = generateWS(options_hemle)



    #meilleurs solutions
    ## le premier que ca renvoie represente celui le plus proche de ce que l'on veut
    ## le reste , les forfaits a  compiler

        Best_hemle = BestOptions(listeS_hemle, price, options_hemle)

    else:
        Best_hemle = []

    if len(options_mango) !=0:
        listeS_mango = generateWS(options_mango)
        # print('news', listeS_mango)
        Best_mango = BestOptions(listeS_mango, price, options_mango)
    else:
        Best_mango = []

    print('best mango', Best_mango)
    print('best hemle', Best_hemle)

    # print (Best_mango[0][1])
    NameM=[]
    DataM=[]
    CallM = []
    SmsM = []
    PriceM=[]
    DayM=[]
    lenMango = len(Best_mango)
    for i in Best_mango:
        NameM.append(i[0]);
        DataM.append(i[3]);
        CallM.append(i[2]);
        SmsM.append(i[1]);
        DayM.append(i[4]);
        PriceM.append(i[5]);

    NameH = []
    DataH = []
    CallH = []
    SmsH = []
    PriceH=[]
    DayH = []
    lenHemle = len(Best_hemle)
    for i in Best_hemle:
        NameH.append(i[0]);
        DataH.append(i[3]);
        CallH.append(i[2]);
        SmsH.append(i[1]);
        DayH.append(i[4]);
        PriceH.append(i[5]);

    #Au niveau du front si la liste est vide , on lui dit qu'il n'ya pas de forfait disponible pour ca demande
    contexte = {'mango':Best_mango, 'hemle':Best_hemle,'price':price, 'NameH':NameH,
                'DataH':DataH,'SmsH':SmsH,'CallH':CallH,'NameM':NameM,
                'DataM':DataM,'SmsM':SmsM,'CallM':CallM,'DayM':DayM, 'PriceM':PriceM,
    'DayH': DayH, 'PriceH': PriceH,'hemle':lenHemle,'mango':lenHemle
    }
    #return ce que tu connais
    return render(request, 'deals/Best.html',contexte )


def list(request):
    with open('media/hemle.csv') as hemle:
        hemle_file = hemle.readlines()

    hem = []
    for row in hemle_file:
        row = row.split(';')[:-1]
        # print(row)
        hem.append(row)

    for i in range(len(hem)):

        if i == 0:
            change = hem[0][0]
            hem[0][0] = change[3:]

        else:
            for k in range(len(hem[i])):
                if k != 0:
                    hem[i][k] = int(hem[i][k])
    # print(hem[1:-1])

    with open('media/Mango.csv') as Man:
        mango_file = Man.readlines()
    mango = []
    for row in mango_file:
        row = row.split(';')
        mango.append(row)
    # print(mango)

    for i in range(len(mango)):
        if i == 0:
            change = mango[0][0]
            mango[0][0] = change[3:]
        else:
            for k in range(len(mango[i])):
                if k != 0:
                    mango[i][k] = int(mango[i][k])

    print('mango',mango)
    print('hemle', hem[0][1])

    NameM = []
    DataM = []
    CallM = []
    SmsM = []
    PriceM = []
    DayM = []
    for i in mango:
        NameM.append(i[0]);
        DataM.append(i[3]);
        CallM.append(i[2]);
        SmsM.append(i[1]);
        DayM.append(i[4]);
        PriceM.append(i[5]);

    NameH = []
    DataH = []
    CallH = []
    SmsH = []
    PriceH = []
    DayH = []
    for i in hem:
        if i !=[]:
            NameH.append(i[0]);
            DataH.append(i[3]);
            CallH.append(i[2]);
            SmsH.append(i[1]);
            DayH.append(i[4]);
            PriceH.append(i[5]);


    # Au niveau du front si la liste est vide , on lui dit qu'il n'ya pas de forfait disponible pour ca demande
    contexte = {'mango': mango, 'hemle': hem, 'NameH': NameH,
                'DataH': DataH, 'SmsH': SmsH, 'CallH': CallH, 'NameM': NameM,
                'DataM': DataM, 'SmsM': SmsM, 'CallM': CallM, 'DayM': DayM, 'PriceM': PriceM,
                'DayH': DayH, 'PriceH': PriceH,
                }


    return render(request, 'deals/list.html',contexte)

def about(request):
    return render(request, 'deals/about.html')





