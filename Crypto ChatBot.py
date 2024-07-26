import requests
import json
# stating our global functions that we call update thoughout the code

LCW_coin_name = ''

LCW_coin_percent_change_24_hours = 0

LCW_coin_price = 0

LCW_coin_price_change_24_hours = 0

CMC_coin_name = ''

CMC_coin_percent_change_24_hours = 0

CMC_coin_price = 0

CMC_coin_price_change_24_hours = 0

price_condition = 0

percent_condition = 0

def live_coin_watch_data_collection(coin):

    #call in a few of our global functions
    global LCW_coin_name, LCW_coin_percent_change_24_hours, LCW_coin_price, LCW_coin_price_change_24_hours

    url = "https://api.livecoinwatch.com/coins/single"
    #give our API a couple of parameters to follow to find the coin we want to check 
    payload = json.dumps({
      "currency": "USD",
      "code": coin,
      "meta": True
    })
    headers = {
      'content-type': 'application/json',
      'x-api-key': '1255339a-b646-4232-88aa-b4529dc242b6'
    }
    #set the response we get from the API to response
    response = requests.request("POST", url, headers=headers, data=payload)

    #use json to to sort thought the data the that API sends
    data = response.json()

    #Using the API documentation we can find certain data that we want to check
    #[0]
    LCW_coin_percent_change_24_hours = round((([data][0]["delta"]["day"]-1)*100),2) 
    #[1]
    LCW_coin_name = [data][0]["name"]
    #[2]
    LCW_coin_price = round([data][0]["rate"], 2)
    #[3]
    LCW_coin_price_change_24_hours = round(LCW_coin_percent_change_24_hours / 100 * LCW_coin_price,4)

    #return these values we just found and store them in our global functions
    return LCW_coin_percent_change_24_hours, LCW_coin_name, LCW_coin_price, LCW_coin_price_change_24_hours

def coin_market_cap_data_collection(coin):

    #call in a few of our global functions
    
    global CMC_coin_name, CMC_coin_percent_change_24_hours, CMC_coin_price, CMC_coin_price_change_24_hours

    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    #give our API a couple of parameters to follow to find the coin we want to check 

    headers = {
        "Accepts":"application/json",
        "X-CMC_PRO_API_KEY": coin_market_cap_api_key,
    }
    params = {"symbol": coin}

    #set the response we get from the API to response
    response = requests.get(url, headers=headers, params=params)

    #use json to to sort thought the data the that API sends
    data = response.json()

    #Using the API documentation we can find certain data that we want to check
    #[0]
    CMC_coin_percent_change_24_hours = round(data["data"][coin]["quote"]["USD"]["percent_change_24h"],2)
    #[1]
    CMC_coin_name = data["data"][coin]["name"]
    #[2]
    CMC_coin_price = round(data["data"][coin]["quote"]["USD"]["price"], 2)
    #[3]
    CMC_coin_price_change_24_hours = round(CMC_coin_percent_change_24_hours / 100 * CMC_coin_price,4)

    #return these values we just found and store them in our global functions
    return CMC_coin_percent_change_24_hours, CMC_coin_name, CMC_coin_price, CMC_coin_price_change_24_hours

# state the API key for the CMC API
coin_market_cap_api_key = "775ff4d9-647c-4d48-8628-c8ecc2f7cd58"

def prompts():
    #This functions runs when the user input 2 in user input
    #It gives them a couple symbols for them to use
    print(f"Here are some symbols of crypto's for you to check \n")
    print(f'BTC for Bitcoin \nETH for Ethereum \nBNB for BNB \nMKR for Maker \nXMR for Monero \nATOM for Cosmos \nLTC for Litecoin \nQNT for Quant \nAAVE for Aave')

def user_input():
    #Welcome the user and ask them if they know what Crypto they would like to check
    print(f'Hi\n')
    print("Welcome to Zac's Crypto Watch")
    #using input, so that the user has to type something before moving on
    symbol = input(f"Do you know the symbol of the crypto you would like to check?\n 1. Yes \n 2. No \n")
    #if they input 2 (No) we will run the prompts function above
    if (symbol == '2'):
        prompts()
    #setting coin (the crypto they would like to check) to whatever the user inputs.   
    coin = input(f'\nType the symbol of crypto you would like to check: ')

    #running the two API's using the users input (coin)
    live_coin_watch_data_collection(coin)

    coin_market_cap_data_collection(coin)

    #Giving the user data on the coin that they have just input and using
    #the global variables that are set in the API variables
    print(f'\nSure thing, here is all our relevant data on',LCW_coin_name,f':\n')
            
    print('Price of',LCW_coin_name,':')
    print(LCW_coin_price,'USD from Live Coin Watch') 
    print(CMC_coin_price,'USD from Coin Market Cap')
    print(f'\n')

    print('Percentage change of',LCW_coin_name,'in the past 24 hours:')
    print(LCW_coin_percent_change_24_hours,'% from Live Coin Watch') 
    print(CMC_coin_percent_change_24_hours,'% from Coin Market Cap')
    print(f'\n')

    print('Price change of',LCW_coin_name,'in the past 24 hours:')
    print(LCW_coin_price_change_24_hours,'USD from Live Coin Watch') #green writing
    print(CMC_coin_price_change_24_hours,'USD from Coin Market Cap')# red writing
    print(f'\n')

def twitter_data_price(LCW_coin_price, CMC_coin_price, LCW_coin_name):
    #bring in our price condition variable
    global price_condition
    #When the price from LCW is less than the price from CMC set price condition to 1
    if LCW_coin_price < CMC_coin_price:
        price_condition = 1
        return price_condition #return this value and store it in our global variable
           
    #Opposite happens when CMC's price is less than LCW's price
    else:
        price_condition = 2
        return price_condition
        

def twitter_data_percent(LCW_coin_percent_change_24_hours, CMC_coin_percent_change_24_hours):
    #bring in our percent condition variable
    global percent_condition

    #Checking to see if the percent change is greater than 0
    if ((LCW_coin_percent_change_24_hours > 0.0) & (CMC_coin_percent_change_24_hours >0.0)): #is it positive

        #Checking to see if the percent from LCW is greater than CMC
        if LCW_coin_percent_change_24_hours > CMC_coin_percent_change_24_hours: #is LCW bigger
            percent_condition = 1
            return percent_condition

        #Checking to see if the percent from LCW is less than CMC
        elif LCW_coin_percent_change_24_hours < CMC_coin_percent_change_24_hours: #if CMC is bigger
            percent_condition = 2
            return percent_condition

    #Checking to see if the perchent change is less than 0
    elif ((LCW_coin_percent_change_24_hours < 0.0) & (CMC_coin_percent_change_24_hours < 0.0)): #is it negative

        #Checking to see if the percent from LCW is less than CMC
        if LCW_coin_percent_change_24_hours < CMC_coin_percent_change_24_hours: #is LCW smaller
            percent_condition = 3
            return percent_condition
        #Checking to see if the percent from LCW is greater than CMC
        elif LCW_coin_percent_change_24_hours > CMC_coin_percent_change_24_hours: #this runs if CMC is smaller
            percent_condition = 4
            return percent_condition



def alerting_user_of_twitter_post():

    #Print this when called upon to alert the user of a twitter post
    #based on the coin they are checking
    print('-----------------------------------------------------------')
    print('|                                                         |')
    print('|Hi,                                                      |')
    print("|Thank you for using Zac's Crypto Watch.                  |")                                                      
    print('|We have noticed that the coin that you have input        |')
    print('|has had some significant changes recently.               |')
    print('|                                                         |')
    print('|We are just letting you know that we are going to post   |')
    print('|this information on our Twitter so that other users like |')
    print('|yourself can receive free investment advice.             |')
    print('|                                                         |')
    print("|For investment advice, follow Zac's Crypto Watch.        |")
    print('|                                                         |')
    print('-----------------------------------------------------------')
    
def post_tweet():

    #bring in our price and percent coinditon variables
    global price_condition, percent_condition

    
    def twitter_post_price():

        #When price condtion is 1 print this
        if price_condition == 1:
            print('Price of', LCW_coin_name,'is',LCW_coin_price,'USD')
            print(f'\nPrice was collected from LiveCoinWatch \n')

        #When price condtion is 2 print this
        elif price_condition ==2:
            print('Price of', CMC_coin_name,'is',CMC_coin_price,'USD')
            print(f'\nPrice was collected from CoinMarketCap \n')
    def twitter_post_percent():

         #When percent condtion is 1 print this
        if percent_condition == 1:
            print(LCW_coin_name,'has risen by',LCW_coin_percent_change_24_hours,'% in the past 24 hours!')
            print('This is a',LCW_coin_price_change_24_hours,'USD increase!')
            print(f'\n this data was collected from LiveCoinWatch \n')
            print(f"\nFor those that previously invested things are looking good!\nSell when you are happy with profit. \n Folow Zac's Crypto Watch for more posts")

        #When percent condtion is 2 print this
        elif percent_condition == 2:
            print(CMC_coin_name,'has risen by',CMC_coin_percent_change_24_hours,'% in the past 24 hours!')
            print('This is a',CMC_coin_price_change_24_hours,'USD increase!')
            print(f'\nthis data was collected from CoinMarketCap \n')
            print(f"\nFor those that previously invested things are looking good!\nSell when you are happy with profit. \n Folow Zac's Crypto Watch for more posts")
                    
        #When percent condtion is 3 print this
        elif percent_condition == 3:
            print(LCW_coin_name,'has fallen by',LCW_coin_percent_change_24_hours,'% in the past 24 hours!')
            print('This is a',LCW_coin_price_change_24_hours,'USD drop!')
            print(f'\n this data was collected from LiveCoinWatch \n')
            print(f"\n this is a good time to invest. Buy low sell high. \n\nFollow Zac's Crypto Watch for more posts.")

        #When percent condtion is 4 print this
        elif percent_condition == 4:
            print(CMC_coin_name,'has fallen by',CMC_coin_percent_change_24_hours,'% in the past 24 hours!')
            print('This is a',CMC_coin_price_change_24_hours,'USD drop!')
            print(f'\n this data was collected from CoinMarketCap \n')
            print(f"\n this is a good time to invest. Buy low sell high. \n\nFollow Zac's Crypto Watch for more posts.")


    #Run the two twitter data functions for our if statement below
    twitter_data_price(LCW_coin_price, CMC_coin_price, LCW_coin_name)
    twitter_data_percent(LCW_coin_percent_change_24_hours, CMC_coin_percent_change_24_hours)

    #Using the information collected in the two above lines
    #Check to see if the two condtion variables are greater than 0
    if (price_condition > 0) & (percent_condition > 0):
        #Alert the user of a post
        alerting_user_of_twitter_post()

        print('-----------------------------------------------------------')
        #Run the two Twitter Post functions to print their data between our two seperation lines
        twitter_post_price()
        twitter_post_percent()
        print(f'-----------------------------------------------------------\n\n\n')


def main():
        while True:
            user_input()
            price_condition = twitter_data_price(LCW_coin_price, CMC_coin_price, LCW_coin_name)
            percent_condition = twitter_data_percent(LCW_coin_percent_change_24_hours, CMC_coin_percent_change_24_hours)
            post_tweet()
            
main()
