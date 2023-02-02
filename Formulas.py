def DSRI(df,year):
    if year == 2022:
        return (df.at["Accounts Receivables", "2022"] / df.at["Revenue", "2022"]) / (df.at["Accounts Receivables", "2021"] / df.at["Revenue", "2021"])
    elif year == 2021:
        return (df.at["Accounts Receivables", "2021"] / df.at["Revenue", "2021"]) / (df.at["Accounts Receivables", "2020"] / df.at["Revenue", "2020"])
    elif year == 2020:
        return (df.at["Accounts Receivables", "2020"] / df.at["Revenue", "2020"]) / (df.at["Accounts Receivables", "2019"] / df.at["Revenue", "2019"])

def GMI(df,year):
    if year == 2022:
        return ((df.at["Revenue", "2021"] - df.at["Cost of Goods Sold", "2021"])/df.at["Revenue", "2021"]) / ((df.at["Revenue", "2022"] - df.at["Cost of Goods Sold", "2022"])/df.at["Revenue", "2022"])
    elif year == 2021:
        return ((df.at["Revenue", "2020"] - df.at["Cost of Goods Sold", "2020"])/df.at["Revenue", "2020"]) / ((df.at["Revenue", "2021"] - df.at["Cost of Goods Sold", "2021"])/df.at["Revenue", "2021"])
    elif year == 2020:
        return ((df.at["Revenue", "2019"] - df.at["Cost of Goods Sold", "2019"])/df.at["Revenue", "2019"]) / ((df.at["Revenue", "2020"] - df.at["Cost of Goods Sold", "2020"])/df.at["Revenue", "2020"])

def AQI(df,year):
    if year == 2022:
        AQI_t1 = (1 - (df.at["Current Assets", "2022"] +
            df.at["Property, Plant & Equipment", "2022"]+df.at["Securities", "2022"])) / df.at["Total Assets", "2022"]
        AQI_t2 = (1 - (df.at["Current Assets", "2021"] +
            df.at["Property, Plant & Equipment", "2021"]+df.at["Securities", "2021"])) / df.at["Total Assets", "2021"]
        return AQI_t1 / AQI_t2
    elif year == 2021:
        AQI_t1 = (1 - (df.at["Current Assets", "2021"] +
            df.at["Property, Plant & Equipment", "2021"]+df.at["Securities", "2021"])) / df.at["Total Assets", "2021"]
        AQI_t2 = (1 - (df.at["Current Assets", "2020"] +
            df.at["Property, Plant & Equipment", "2020"]+df.at["Securities", "2020"])) / df.at["Total Assets", "2020"]
        return AQI_t1 / AQI_t2

    elif year == 2020:
        AQI_t1 = (1 - (df.at["Current Assets", "2020"] +
            df.at["Property, Plant & Equipment", "2020"]+df.at["Securities", "2020"])) / df.at["Total Assets", "2020"]
        AQI_t2 = (1 - (df.at["Current Assets", "2019"] +
            df.at["Property, Plant & Equipment", "2019"]+df.at["Securities", "2019"])) / df.at["Total Assets", "2019"]
        return AQI_t1 / AQI_t2

def SGI(df,year):
    if year == 2022:
        return (df.at["Revenue", "2022"] / df.at["Revenue", "2021"])
    elif year == 2021:
        return (df.at["Revenue", "2021"] / df.at["Revenue", "2020"])
    elif year == 2020:
        return (df.at["Revenue", "2020"] / df.at["Revenue", "2019"])

def DEPI(df,year):
    if year == 2022:
        DEPI_t1 = (df.at["Depreciation", "2021"] / (df.at["Depreciation",
               "2021"] + df.at["Property, Plant & Equipment", "2021"]))
        DEPI_t2 = (df.at["Depreciation", "2022"] / (df.at["Depreciation",
               "2022"] + df.at["Property, Plant & Equipment", "2022"]))
        return DEPI_t1 / DEPI_t2
    elif year == 2021:
        DEPI_t1 = (df.at["Depreciation", "2020"] / (df.at["Depreciation",
               "2020"] + df.at["Property, Plant & Equipment", "2020"]))
        DEPI_t2 = (df.at["Depreciation", "2021"] / (df.at["Depreciation",
               "2021"] + df.at["Property, Plant & Equipment", "2021"]))
        return DEPI_t1 / DEPI_t2

    elif year == 2020:
        DEPI_t1 = (df.at["Depreciation", "2019"] / (df.at["Depreciation",
               "2019"] + df.at["Property, Plant & Equipment", "2019"]))
        DEPI_t2 = (df.at["Depreciation", "2020"] / (df.at["Depreciation",
               "2020"] + df.at["Property, Plant & Equipment", "2020"]))
        return DEPI_t1 / DEPI_t2

def SGAI(df,year):
    if year == 2022:
        return (df.at["Selling, General & Admin.Expense", "2022"] / df.at["Revenue", "2022"]) / (df.at["Selling, General & Admin.Expense", "2021"] / df.at["Revenue", "2021"])

    elif year == 2021:
        return (df.at["Selling, General & Admin.Expense", "2021"] / df.at["Revenue", "2021"]) / (df.at["Selling, General & Admin.Expense", "2020"] / df.at["Revenue", "2020"])

    elif year == 2020:
        return (df.at["Selling, General & Admin.Expense", "2020"] / df.at["Revenue", "2020"]) / (df.at["Selling, General & Admin.Expense", "2019"] / df.at["Revenue", "2019"])


def TATA(df,year):
    if year == 2022:
        return (df.at["Net Income from Continuing Operations", "2022"] - df.at["Cash Flow from Operations", "2022"]) / df.at["Total Assets", "2022"]
    elif year == 2021:
        return (df.at["Net Income from Continuing Operations", "2021"] - df.at["Cash Flow from Operations", "2021"]) / df.at["Total Assets", "2021"]

    elif year == 2020:
        return (df.at["Net Income from Continuing Operations", "2020"] - df.at["Cash Flow from Operations", "2020"]) / df.at["Total Assets", "2020"]

def LVGI(df,year):
    if year == 2022:
        return ((df.at["Current Liabilities", "2022"] + df.at["Total Long-term Debt", "2022"]) / df.at["Total Assets", "2022"]) / ((df.at["Current Liabilities", "2021"] + df.at["Total Long-term Debt", "2021"]) / df.at["Total Assets", "2021"])

    elif year == 2021:
        return ((df.at["Current Liabilities", "2021"] + df.at["Total Long-term Debt", "2021"]) / df.at["Total Assets", "2021"]) / ((df.at["Current Liabilities", "2020"] + df.at["Total Long-term Debt", "2020"]) / df.at["Total Assets", "2020"])

    elif year == 2020:
        return ((df.at["Current Liabilities", "2020"] + df.at["Total Long-term Debt", "2020"]) / df.at["Total Assets", "2020"]) / ((df.at["Current Liabilities", "2019"] + df.at["Total Long-term Debt", "2019"]) / df.at["Total Assets", "2019"])


def BeneishMScore(dsri, gmi, aqi, sgi, depi, sgai, lvgi, tata):
    return -4.84+0.92*dsri+0.528*gmi+0.404*aqi+0.892*sgi+0.115*depi-0.172*sgai+4.679*tata-0.327*lvgi

########################################################################################################
# Altman Z score




#########################################################################################################
#Beneford law






############################################################################################################
# probability of fraud