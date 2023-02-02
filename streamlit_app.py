import streamlit as st
import pandas as pd
import numpy as np
import pandas_datareader as pddata
import yfinance as yf
from formulas3 import *
from Formulas import *
from benfordslaw import benfordslaw
from prettytable import PrettyTable

st.title("Financial Forensics")
st.header("What is Financial Forensics?")
st.write("Forensic accounting, forensic accountancy or financial forensics is the specialty practice area of accounting that investigates whether firms engage in financial reporting misconduct.")

st.write('Here in this app we will try to look into some of the tools that are used by auditing firms to determine financial frauds')

companies = pd.read_csv("companylist.csv")
companies2 = companies.tail(-1) # removing the first row
companyTable = companies2['Symbol']
########################################################
st.write("### List of companies")
# Displaying the list of companies to select from
col1, col2, col3 = st.columns(3)
with col1:
    st.table(companyTable[0:17])
with col2:
    st.table(companyTable[17:34])
with col3:
    st.table(companyTable[34:50])
###################################################################
# take the input from user
#int_val = st.slider('Seconds', min_value=1, max_value=10, value=5, step=1) ----->> Slider
#int_val = st.number_input('Seconds', min_value=1, max_value=10, value=5, step=1)


userInput = st.number_input('Enter compnay choice', min_value=None, max_value=50)
companyChoice = userInput - 1
# Convert that input into companies ticker
companySymbols = companies2['Symbol'].tolist()
tickers = []
for symbol in companySymbols:
    symbol = symbol + ".NS"
    tickers.append(symbol)

tickerObject = yf.Ticker(tickers[companyChoice]) # Create ticker object of the selected company
#####################################################################################
forbiddenList = [5,6,10,12,14,15,16,20,24,29,33,34,36,37,38,39,41,45,46,47,48]
if userInput in forbiddenList:
    st.write("## Currently {}'s data is not accurately available from yfinance library".format(companySymbols[companyChoice]))
else:
    #st.write(tickerObject.info)
    ##########################################################################################
    #get necessary Data
    incomeStatement = tickerObject.financials
    balanceSheet = tickerObject.balancesheet
    cashFlow = tickerObject.cashflow
    #Clean the data
    # Cashflow
    cashFlow = cashFlow[cashFlow.columns[0:len(incomeStatement.columns)]]
    cashFlow.columns = ['2022', '2021','2020','2019']
    cashFlow.dropna()
    #income statement
    incomeStatement = incomeStatement[incomeStatement.columns[0:len(incomeStatement.columns)]]
    incomeStatement.columns = ['2022', '2021','2020','2019']
    incomeStatement = incomeStatement.fillna(0).astype(float)
    #balance sheet
    balanceSheet = balanceSheet[balanceSheet.columns[0:len(incomeStatement.columns)]]
    balanceSheet.columns = ['2022', '2021','2020','2019']
    balanceSheet = balanceSheet.fillna(0).astype(float)
    #################################################################################################
    # Zscore
    x1 = balanceSheet.loc["Working Capital"] / balanceSheet.loc["Total Assets"]

    x2 = balanceSheet.loc["Retained Earnings"] / balanceSheet.loc["Total Assets"]

    x3 = incomeStatement.loc["EBIT"] / balanceSheet.loc["Total Assets"]

    x4 = int(pddata.get_quote_yahoo(tickers[companyChoice])['marketCap'])/ balanceSheet.loc["Current Liabilities"]

    x5 = incomeStatement.loc["Total Revenue"] / balanceSheet.loc["Total Assets"]
    
    
    ########################################################################################################
    #beneish m score
    # COGS = Revenue  - GrossProfit
    cogs22 = incomeStatement.at['Total Revenue', '2022'] - \
        incomeStatement.at['Gross Profit', '2022']
    cogs21 = incomeStatement.at['Total Revenue', '2021'] - \
        incomeStatement.at['Gross Profit', '2021']
    cogs20 = incomeStatement.at['Total Revenue', '2020'] - \
        incomeStatement.at['Gross Profit', '2020']
    cogs19 = incomeStatement.at['Total Revenue', '2019'] - \
        incomeStatement.at['Gross Profit', '2019']
    
    incomeStatement.loc['Cost of Goods Sold'] = [cogs22, cogs21,cogs20,cogs19]

    if('Long Term Debt' not in balanceSheet.index):
        ld22 = balanceSheet.at['Total Liab', "2022"] - \
            balanceSheet.at['Total Current Liabilities', "2022"] - \
            balanceSheet.at['Other Liab', "2022"]
        ld21 = balanceSheet.at['Total Liab', "2021"] - \
            balanceSheet.at['Total Current Liabilities', "2021"] - \
            balanceSheet.at['Other Liab', "2021"]
        ld20 = balanceSheet.at['Total Liab', "2020"] - \
            balanceSheet.at['Total Current Liabilities', "2020"] - \
            balanceSheet.at['Other Liab', "2020"]
        ld19 = balanceSheet.at['Total Liab', "2019"] - \
            balanceSheet.at['Total Current Liabilities', "2019"] - \
            balanceSheet.at['Other Liab', "2019"]
            
        balanceSheet.loc['Long Term Debt'] = [ld22, ld21, ld20, ld19]

    if('Long Term Investments' not in balanceSheet.index):
        li22 = balanceSheet.at['Common Stock', "2022"] + \
            balanceSheet.at['Cash And Cash Equivalents', "2022"]
        li21 = balanceSheet.at['Common Stock', "2021"] - \
            balanceSheet.at['Cash And Cash Equivalents', "2021"]
        li20 = balanceSheet.at['Common Stock', "2020"] - \
            balanceSheet.at['Cash And Cash Equivalents', "2020"]
        li19 = balanceSheet.at['Common Stock', "2019"] - \
            balanceSheet.at['Cash And Cash Equivalents', "2019"]
            
        balanceSheet.loc['Long Term Investments'] = [li22, li21, li20, li19]
    

    df = incomeStatement.loc[["Total Revenue",
                            "Cost of Goods Sold", "Selling General And Administration", "Net Income"]]

    df2 = balanceSheet.loc[["Gross Accounts Receivable",
                        "Current Assets", "Gross PPE", "Long Term Investments", "Total Assets", "Current Liabilities", "Long Term Debt"]]

    df3 = cashFlow.loc[["Depreciation",
                    "Operating Cash Flow"]]

    data = pd.concat([df, df2, df3])

    data.index = ["Revenue", "Cost of Goods Sold", "Selling, General & Admin.Expense", "Depreciation", "Net Income from Continuing Operations", "Accounts Receivables",
                  "Current Assets", "Property, Plant & Equipment", "Securities", "Total Assets", "Current Liabilities", "Total Long-term Debt", "Cash Flow from Operations"]

    ##########################################################################################
    dsri = [DSRI(data,2022),DSRI(data,2021),DSRI(data,2020)]
    gmi = [GMI(data,2022),GMI(data,2021),GMI(data,2020)]
    aqi = [AQI(data,2022),AQI(data,2021),AQI(data,2020)]
    sgi = [SGI(data,2022),SGI(data,2021),SGI(data,2020)]
    depi = [DEPI(data,2022),DEPI(data,2021),DEPI(data,2020)]
    sgai = [SGAI(data,2022),SGAI(data,2021),SGAI(data,2020)]
    lvgi = [LVGI(data,2022),LVGI(data,2021),LVGI(data,2020)]
    tata = [TATA(data,2022),TATA(data,2021),TATA(data,2020)]
    m_score = [BeneishMScore(dsri[0], gmi[0], aqi[0], sgi[0], depi[0], sgai[0], lvgi[0], tata[0]),BeneishMScore(dsri[1], gmi[1], aqi[1], sgi[1], depi[1], sgai[1], lvgi[1], tata[1]),
          BeneishMScore(dsri[2], gmi[2], aqi[2], sgi[2], depi[2], sgai[2], lvgi[2], tata[2])]

    ################################################################################################
    # table for ratios
    data = [dsri,gmi,aqi,sgi,depi,sgai,lvgi,tata]
    index =[
            "Day Sales in Receivables Index(DSRI)",
            "Gross Margin Index(GMI)",
            "Asset Quality Index(AQI)",
            "Sales Growth Index(SGI)",
            "Depreciation Index(DEPI)",
            "Selling, General, & Admin. Expenses Index(SGAI)",
            "Leverage Index(LVGI)",
            "Total Accruals to Total Assets(TATA)"
        ]
    columns = ['2022', '2021', '2020']
    ratios = pd.DataFrame(data,index,columns)

    mScore = [m_score]
    indexForTable = "Benish M score for {}".format(companySymbols[companyChoice])
    dict1 = {"Benish M score for {}".format(companySymbols[companyChoice]): m_score}
    mScoreTable = pd.DataFrame(dict1).T # For transpose
    mScoreTable.columns = ['2022','2021','2020']
    st.write("### Beneish M score")
    st.table(mScoreTable)
    ###################################################################################################
    #Altman Z Score
    st.write("### Altman Z score")
    # Formula is written above m score

    z = (1.2 * x1) + (1.4 * x2) + (3.3 * x3) + (0.6 * x4) + (x5)

    altmanZScoreTable = pd.DataFrame(z).T
    altmanZScoreTable.index = ['AltmanZScore for {}'.format(companySymbols[companyChoice])]
    st.table(altmanZScoreTable)
    ###############################################################################################
    # Beneford law
    yearChoice = st.text_input("Enter a year",value = '2022')
    digitChoice = st.number_input("Enter a digit position",min_value = 1, max_value = 2, step=1)
    ### Function To calculate Beneford law
    def calcBL(yearChoice,digitChoice):
        if digitChoice==1:
            bl = benfordslaw(alpha=0.05)
        else:
            bl = benfordslaw(alpha=0.05,pos=digitChoice)
        result = bl.fit(tickerObject.balancesheet[['{}'.format(yearChoice)+'-03-31']])
        
        figure = bl.plot()
        st.write("### The beneford law test for {}st digit is ".format(digitChoice))
        st.pyplot(figure[0])
        
    calcBL(yearChoice,digitChoice)
     


    ##################################################################################################
    # Probability of Fraud
    coeff1 = balanceSheet.loc['Inventory']/balanceSheet.loc['Total Assets']
    coeff2 = incomeStatement.loc['Total Revenue']/balanceSheet.loc['Gross PPE']
    coeff3 = (balanceSheet.loc['Total Assets']+balanceSheet.loc['Stockholders Equity'])/balanceSheet.loc['Total Assets']
    coeff4 = balanceSheet.loc['Current Assets']/balanceSheet.loc['Current Liabilities']

    exponent = 2.7**(5.768-4.236*coeff1-0.0259*coeff2-4.766*coeff3-1.936*coeff4)
    P =(1-(1/(1+exponent)))*100 
    PTranspose = P.T
    pTable = pd.DataFrame(PTranspose)
    pTable.columns = ['Probability Percentage for {}'.format(companySymbols[companyChoice])]
    st.write("### The probability of fraud is: ")
    st.table(pTable)

    ####################################################################################################
    ## Tablute the scores ################
    # Zscore tabulated
    ### Zcore test tabluated
    entry12 = []
    for zvalues in z:
        print(zvalues)
        i = 0
        if zvalues>=3:
            entry12value = "NO"
            safeYears = z.index[i]
            entry12.append(entry12value)
        elif zvalues>=1.8 and zvalues<3: 
            entry12value ="PROBABLY"
            safeYears = z.index[i]
            entry12.append(entry12value)
        else:
            entry12value = "YES"
            safeYears = z.index[i]
            entry12.append(entry12value)
        i = i + 1
    
    print(entry12)
    

    # m score tabulated
    entry11 = []
    for mvalues in m_score:
        print(m_score)
        i = 0
        if mvalues<-2.22:
            entry11value = "NO"
        
            entry11.append(entry11value)
        elif mvalues>=-2.22 and mvalues<-1.78: 
            entry11value ="PROBABLY"
        
            entry11.append(entry11value)
        else:
            entry11value = "YES"

            entry11.append(entry11value)
        i = i + 1
    
    entry11.append("insuff data for 2019")    
    print(entry11)
    print(entry12)


    # benefordslaw tabulated



    # prob % tabulated
    prob = pTable.squeeze()
    entry14 = []
    for pvalues in prob:
        print(prob)
        i = 0
        if pvalues<50:
            entry14value = "NO"
        
            entry14.append(entry14value)
    
        else:
            entry14value = "YES"
       
            entry14.append(entry14value)
        i = i + 1
    ######################################
    #Pretty table
    
    table1 = PrettyTable()
    table1.field_names = ["Year", "BeneishMscore", "AltmanZscore", "FraudProbability"]
    table1.title = "Tabulated Test Result for {} ".format(companySymbols[companyChoice])
    table1.add_row(['2022',entry11[0],entry12[0],entry14[0]])
    table1.add_row(['2021',entry11[1],entry12[1],entry14[1]])
    table1.add_row(['2020',entry11[2],entry12[2],entry14[2]])
    table1.add_row(['2019',entry11[3],entry12[3],entry14[3]])
    while True:
        with open('test.csv', 'w', newline='') as f_output:
            f_output.write(table1.get_csv_string())
        table1DF = pd.read_csv('test.csv')
        
        st.table(table1DF)
        break
    
    





