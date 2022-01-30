import json
from urllib.request import urlopen
import numpy as np
import pandas as pd
import requests, re
from bs4 import BeautifulSoup as bs
import sys
import itertools


def Rule_num_one_ten_years_check(ticker, score):
    def ROIC_Check(ticker):
        score = 0
        sum = 0.0
        url = (f"https://stockanalysis.com/stocks/{ticker}/financials/ratios/")
        res = get_request(url)
        soup = bs(res.content, 'lxml')
        try:
            data = soup.find("span", text="Return on Capital (ROIC)").parent.parent.text
        except:
            print("cant find ROIC selector ")
        tenYROIC = data[24:84].split(sep='%')  # 24:82
        for i in range(len(tenYROIC) + 1):
            sum = sum + float(tenYROIC[i])
            if i == len(tenYROIC) - 1:
                average = sum / len(tenYROIC)
                if average >= 9:
                    score += 1
                    print(f"{ticker} has passed ROIC check with a 10 year average ROIC of {average}")
                    return score
                else:
                    print(f"{ticker} didnt pass ROIC check: {average}")
                    return score

    def ROIC_Check_old(ticker):
        score = 0
        sum = 0.0
        url = (f"https://stockanalysis.com/stocks/{ticker}/financials/ratios/")
        res = get_request(url)
        soup = bs(res.content, 'lxml')
        data = soup.find_all('tr')[17].text
        tenYROIC = data[25:78].split(sep='%')  # 24:82
        for i in range(len(tenYROIC) + 1):
            sum = sum + float(tenYROIC[i])
            if i == len(tenYROIC) - 1:
                average = sum / len(tenYROIC)
                if average >= 9:
                    score += 1
                    print(f"{ticker} has passed ROIC check with a 10 year average ROIC of {average}")
                    return score
                else:
                    print(f"{ticker} didnt pass ROIC check: {average}")
                    return score

    def get_request(url):
        res = requests.get(url)
        try:
            if res.status_code == 200:
                pass
        except:
            print(f"there was a problem downloading {url}")
        return res

    def Equity_growth_check(ticker):
        score = 0
        sum = 0.0
        url = (f"https://stockanalysis.com/stocks/{ticker}/financials/balance-sheet/")
        res = get_request(url)

        soup = bs(res.content, 'lxml')
        try:  # TODO validate with Muli that this is the relevant value
            # data = soup.find("span", text="Total Assets").parent.parent.text
            table = soup.find(lambda tag: tag.name == 'table' and tag.has_attr('id') and tag['id'] == "financial-table")
            rows = table.findAll(lambda tag: tag.name == 'tr')
            data = [r for r in rows if r.find("span", text="Total Assets")][0]
            data = data.findAll('td')
        except:
            print("cant find Total Assets")
        # data = soup.find_all('tr', class_='border-b-2 border')[2]
        pattern = (r'''(\d+,\d*,\d*,?\d*)''')
        allYequity = re.findall(pattern, str(data))

        for i, equity in enumerate(allYequity):
            allYequity[i] = allYequity[i].replace(',', '')
            allYequity[i] = float(allYequity[i])

        for i in range(len(allYequity) - 1):
            growth = ((allYequity[i] - allYequity[i + 1]) * 100 / allYequity[i + 1])
            sum = sum + growth
            print(f"sum: {sum}, growth: {growth}")
            if i == len(allYequity) - 2:  # 9 TODO ask Muli what he thinks about it
                average = sum / 9
                if average >= 9:
                    score += 1
                    print(f"{ticker} has passed equity growth check with a 10 year average equity growth of {average}")
                    return score
                else:
                    print(f"{ticker} didnt pass equity growth check: {average}")
                    return score

    def FCF_growth_Check(ticker):
        score = 0
        url = (f"https://stockanalysis.com/stocks/{ticker}/financials/cash-flow-statement/")
        res = requests.get(url)
        sum = 0.0
        try:
            if res.status_code == 200:
                pass
        except:
            print("there was a problem downloading")
        soup = bs(res.content, 'lxml')
        data = soup.find_all('tr', class_='tch tdent tsep')[0].text
        tenYFCF = data[21:82].split(sep='%')  # 21:82
        tenYFCF = tenYFCF[:10]
        for i in range(len(tenYFCF) + 1):
            sum = sum + float(tenYFCF[i])
            if i == len(tenYFCF) - 1:
                average = sum / 10
                if average >= 9:
                    score += 1
                    print(f"{ticker} has passed Free Cash Flow Growth check with a 10 year average of {average}")
                    return score
                else:
                    print(f"{ticker} didnt pass Free Cash Flow Growth check: {average}")
                    return score

    def Revenue_growth_Check(ticker):
        score = 0
        url = (f"https://stockanalysis.com/stocks/{ticker}/financials/")
        res = requests.get(url)
        sum = 0.0
        try:
            if res.status_code == 200:
                pass
        except:
            print("there was a problem downloading")
        soup = bs(res.content, 'lxml')
        data = soup.find_all('tr')[2].text
        tenYrevenue = data[14:82].split(sep='%')
        tenYrevenue = tenYrevenue[:10]
        for i in range(len(tenYrevenue) + 1):
            sum = sum + float(tenYrevenue[i])
            if i == len(tenYrevenue) - 1:
                average = sum / 10
                if average >= 9:
                    score += 1
                    print(f"{ticker} has passed Revenue Growth check with a 10 year average of {average}")
                    return score
                else:
                    print(f"{ticker} didnt pass Revenue growth check: {average}")
                    return score

    def EPS_growth_Check(ticker):
        score = 0
        url = (f"https://stockanalysis.com/stocks/{ticker}/financials/")
        res = requests.get(url)
        sum = 0.0
        try:
            if res.status_code == 200:
                pass
        except:
            print("there was a problem downloading")
        soup = bs(res.content, 'lxml')
        data = soup.find('tr', class_='tdent tch').text
        tenYEPS = data[10:87].split(sep='%')  # 10:87
        tenYEPS = tenYEPS[:10]
        for i in range(len(tenYEPS) + 1):
            sum = sum + float(tenYEPS[i])
            if i == len(tenYEPS) - 1:
                average = sum / 10
                if average >= 9:
                    score += 1
                    print(f"{ticker} has passed EPS Growth check with a 10 year average of {average}")
                    return score
                else:
                    print(f"{ticker} didnt pass EPS Growth check: {average}")
                    return score

    score1 = Equity_growth_check(ticker)
    score2 = ROIC_Check(ticker)
    score3 = FCF_growth_Check(ticker)
    score4 = Revenue_growth_Check(ticker)
    score5 = EPS_growth_Check(ticker)
    score = score + score1 + score2 + score3 + score4 + score5

    print(f'{ticker} got a score of: {score}/15 on the 10 year check.')
    return score


def get_financail_summery(stock):
    def get_jsonparsed_data(url):
        response = urlopen(url)
        data = response.read().decode("utf-8")
        return json.loads(data)

    five_years_finance = {}
    financial_ratios = {}
    year_ratios = {}
    score2 = 0
    years = [2020, 2019, 2018, 2017, 2016]

    api_keys = ['be9ce7f88fa812f27c5d903501f91791', '25ceb4c7e21615e4e20ca185ba6febdf',
                'ffabfbd36dabd4019b84799661cd5af7', 'd402eacea21db4e50182b821dbb2708b',
                '9eaca11372e3d4b58cf50c8fee829daf', '9e9cacaedd6feb1b8c87c3958e08cad0',
                '907f9f4407208d0ce576ad152bbe7622', '9efd9e334bbc5f7a980d11b51643cd24',
                'caaf9d2b550c7b829b1fc3708c989342']

    error = {
        'Error Message': 'Limit Reach . Please upgrade your plan or visit our documentation for more details at https://financialmodelingprep.com/developer/docs/pricing '}

    for i in range(1, len(api_keys) + 1):
        url = (f"https://financialmodelingprep.com/api/v3/income-statement/{stock}?apikey={api_keys[i - 1]}")
        income_statement = get_jsonparsed_data(url)
        url2 = (f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{stock}?apikey={api_keys[i - 1]}")
        balance_sheet = get_jsonparsed_data(url2)
        url3 = (f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{stock}?apikey={api_keys[i - 1]}")
        cash_flow = get_jsonparsed_data(url3)
        url4 = (
            f"https://financialmodelingprep.com/api/v3/historical-discounted-cash-flow/{stock}?apikey={api_keys[i - 1]}")
        DCF = get_jsonparsed_data(url4)
        url5 = (f"https://financialmodelingprep.com/api/v3/profile/{stock}?apikey={api_keys[i - 1]}")
        MC = get_jsonparsed_data(url5)
        url6 = (f"https://financialmodelingprep.com/api/v3/financial-growth/{stock}?apikey={api_keys[i - 1]}")
        growth = get_jsonparsed_data(url6)
        if DCF == error or MC == error or growth == error or income_statement == error or balance_sheet == error or cash_flow == error:
            print(f"api key number {i} passed its limit.")
        elif DCF == [] or MC == [] or growth == [] or income_statement == [] or balance_sheet == [] or cash_flow == []:
            print(f"There is a problem with the data base on {stock}")
            break
        elif i != 1:
            print(f"Im using the {i} api key")
            break
        else:
            break
    for i in range(0, 5):
        finance = {}
        ## income statement summery
        finance['Net_Income'] = income_statement[i]['netIncome']

        finance['Ebitda'] = income_statement[i]['ebitda']
        finance["Depreciation_And_Amortization"] = income_statement[i]["depreciationAndAmortization"]
        finance["Profit_to_work_with"] = finance["Ebitda"] - finance["Depreciation_And_Amortization"]
        finance["cost_Of_Revenue"] = income_statement[i]['costOfRevenue']
        finance["Revenue"] = income_statement[i]['revenue']

        ##balance sheet statement
        finance["Equity"] = balance_sheet[i]['totalStockholdersEquity']
        finance["Assets"] = balance_sheet[i]['totalAssets']
        finance["Liabilities"] = balance_sheet[i]['totalDebt']
        finance["Current_assets"] = balance_sheet[i]['totalCurrentAssets']
        finance["Current_Liabilities"] = balance_sheet[i]['totalCurrentLiabilities']

        ## cash flow statement
        finance["Free_Cash_Flow"] = cash_flow[i]['freeCashFlow']
        finance["Operating_Cash_Flow"] = cash_flow[i]['operatingCashFlow']
        finance["Dividends"] = cash_flow[i]['dividendsPaid']

        ##DCF
        finance['DCF'] = DCF[0]['historicalDCF'][i]['DCF']
        finance['DCf_date'] = DCF[0]['historicalDCF'][i]['date']

        ##market cap
        if i == 0:
            finance['Market_Cap'] = MC[0]['mktCap']
        else:
            finance['Market_Cap'] = "*"

        if i == 4:
            finance['*'] = 'AVERAGE GROWTH:'
        else:
            finance['*'] = '*'

        ##growth
        finance['EPS_growth'] = (growth[i]['epsgrowth']) * 100
        finance['Revenue_Growth'] = (growth[i]['revenueGrowth']) * 100
        finance['FreeCashFlow_Growth'] = (growth[i]['freeCashFlowGrowth']) * 100

        finance['**'] = '*'

        five_years_finance.update({years[i]: finance})

    df = pd.DataFrame(five_years_finance)

    for i in range(0, 4):
        year_ratios['equity_growth'] = ((((five_years_finance[(years[i])]['Equity']) - (
            five_years_finance[(years[i + 1])]['Equity'])) * 100) / (five_years_finance[(years[i + 1])]['Equity']))
        # year_ratios['gross_profit_growth'] = ((((((five_years_finance[(years[i])]['cost_Of_Revenue']) / (five_years_finance[(years[i])]['Revenue'])) - ((five_years_finance[(years[i + 1])]['cost_Of_Revenue']) / (five_years_finance[(years[i + 1])]['Revenue'])))) / ((five_years_finance[(years[i + 1])]['cost_Of_Revenue']) / (five_years_finance[(years[i + 1])]['Revenue']))) * 100)
        year_ratios['Net_Income_growth'] = ((((five_years_finance[(years[i])]['Net_Income']) - (
            five_years_finance[(years[i + 1])]['Net_Income'])) * 100) / (
                                                five_years_finance[(years[i + 1])]['Net_Income']))
        year_ratios['ROIC'] = (100 * (((five_years_finance[(years[i])]['Profit_to_work_with']) - (
            five_years_finance[(years[i])]['Dividends'])) / ((five_years_finance[(years[i])]['Liabilities']) + (
            five_years_finance[(years[i])]['Equity']))))
        year_ratios['ROE'] = ((five_years_finance[(years[i])]['Profit_to_work_with']) / (
            five_years_finance[(years[i + 1])]['Equity']) * 100)
        year_ratios['profit_margin'] = ((five_years_finance[(years[i])]['Profit_to_work_with']) / (
            five_years_finance[(years[i])]['Revenue']) * 100)
        year_ratios['current_ratio'] = ((five_years_finance[(years[i])]['Current_assets']) / (
            five_years_finance[(years[i])]['Current_Liabilities']))
        year_ratios['financial_margin'] = (
                (five_years_finance[(years[i])]['Liabilities']) / (five_years_finance[(years[i])]['Equity']))
        if i == 0:
            year_ratios['PE_Ratio'] = (
                    (five_years_finance[(years[i])]['Market_Cap']) / (five_years_finance[(years[i])]['Net_Income']))
        financial_ratios.update({years[i]: year_ratios})
        year_ratios = {}
        if i == 3:
            financial_ratios.update({2016: np.nan})

    df_financial_ratios = pd.DataFrame(financial_ratios)

    df_financial_ratios['Averages'] = np.nan

    for row in range(0, len(df_financial_ratios)):
        sum = 0.0
        for column in range(0, 5):
            if column != 4:
                sum = sum + float(df_financial_ratios.iloc[row, column])
            else:
                df_financial_ratios.iloc[row, 5] = sum / 4

    df['Averages'] = np.nan

    df_full = pd.concat([df, df_financial_ratios], axis='rows')

    for row in range(18, 21):
        if df_full.iloc[row, 0] == 'EPS_growth' or 'Revenue_Growth' or 'FreeCashFlow_Growth':
            sum = 0.0
            for column in range(0, 6):
                if column < 5:
                    sum = sum + float(df_full.iloc[row, column])
                else:
                    df_full.iloc[row, column] = sum / 5

    #### rule number one testing
    score = 0
    if df_full.loc['ROIC', 'Averages'] >= 9:
        score += 1
        if df_full.loc['equity_growth', 'Averages'] >= 9:
            score += 1
            if df_full.loc['ROIC', 2020] >= 9:
                score += 1
                if df_full.loc['equity_growth', 2020] >= 9:
                    score += 1
                    if score == 4:
                        if df_full.loc['EPS_growth', 'Averages'] >= 9:
                            score += 1
                        if df_full.loc['Revenue_Growth', 'Averages'] >= 9:
                            score += 1
                        if df_full.loc['FreeCashFlow_Growth', 'Averages'] >= 9:
                            score += 1
                        if score == 7:
                            if df_full.loc['EPS_growth', 2020] >= 9:
                                score += 1
                            if df_full.loc['Revenue_Growth', 2020] >= 9:
                                score += 1
                            if df_full.loc['FreeCashFlow_Growth', 2020] >= 9:
                                score += 1
                            if score >= 8:
                                df_full.loc['Net_Income', 'Averages'] = ("score = " + str(score))
                                df_full.to_excel(
                                    f'{stock}_financial_statement.xlsx')
                                print(f"{stock} passed rule number one test for 5 years data with the score- {score}. "
                                      "chacking 10 years data...")
                                score = Rule_num_one_ten_years_check(stock, score)
    # df_full.loc['Net_Income', 'Averages'] = ("score = " + str(score))
    # df_full.to_excel(f'score_{score}_{stock}_financial_statement.xlsx')
    print(f"{stock} got a score of {score}")
    if score == 7:
        answer = input("do you still want to make an excel file?")
        if answer == 'yes':
            df_full.loc['Net_Income', 'Averages'] = ("score = " + str(score))
            df_full.to_excel(f'{stock}_financial_statement.xlsx')
    # answer = input("do you want to check another stock? ")
    # if answer == 'yes' or ' ':
    #     get_financail_summery()

    # return print(f"{stock} got a score of {score}")


if __name__ == "__main__":
    print("hi")
    if len(sys.argv) > 1:
        stock = sys.argv[1]
    else:
        stock = input("Please enter a symbol for a 'rule number one' test: ").upper()

    get_financail_summery(stock)


