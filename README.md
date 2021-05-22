# Stock Trading Simulator

This project was created to simulate a trading environment and recreate the buying/selling experience of trading stocks in real life! Additionally, all the stock prices are real-time meaning the exact prices of all stocks are used in this web application. This project is merely a simulation, so you do not need to worry about putting your own money for investment! You will be provided with $10,000 (fake money, of course) at the start upon successful registration. After signing up, you can embark on your simulated trading journey! If you would like to view the various pages of the application and a more detailed explanation scroll down!

Real-time stock data provided by [iexcloud.io](url)!

This web app was created using HTML and CSS for the front-end. For the back-end, the python framework Flask was used along with SQLite to manage the databses storing all the user info.

<h1>Landing Page</h1>

<img width="1269" alt="Screen Shot 2021-05-22 at 12 24 09 PM" src="https://user-images.githubusercontent.com/64047718/119234272-ffbb7e00-bafa-11eb-8166-0deb05464efa.png">

Above is an image of the landing page of the web app. Here, users can log in, if they have already sign up. If they haven't signed up, they can click the "Register" button at the top right to get started!

<h1>Sign Up Page</h1>

<img width="1258" alt="Screen Shot 2021-05-22 at 12 43 00 PM" src="https://user-images.githubusercontent.com/64047718/119234310-47daa080-bafb-11eb-88d5-3e831966955f.png">

This is the sign up page for new users! Here, users are required to choose a username and password for their new account. 

<h1>Home Page</h1>

<img width="1265" alt="Screen Shot 2021-05-22 at 12 45 06 PM" src="https://user-images.githubusercontent.com/64047718/119234375-9425e080-bafb-11eb-98cd-0007caf468e9.png">

This is the home page of a new account! This is where the user's portfolio is shown in a table with 5 columns. The first column displays the symbol of the stock (AAPL for Apple, WMT for Walmart, etc). The next column displays the actual name of the company. The third column shows the number of stocks bought for that company. The next column shows the value of each stock at the current time (not the time of purchase). The last columns shows the total value of all the stocks from a certain company. This number is calculated buy multiplying the number of stocks (Column 3) by the value of one stock at the current time (Column 4). The row saying "CASH" is the number of money you have left after spending on stocks. At the bottom right of the table, the value of the Portfolio is displayed. This value represents the amount of money you would have if you were to sell all your stocks at that time. As said before, all users start off with $10,000 to begin their trading journey. Currently the user has not invested in anything yet which is why their total is still $10,000. Below is what the home page may look like for a user that has already invested!

<img width="1265" alt="Screen Shot 2021-05-22 at 1 12 07 PM" src="https://user-images.githubusercontent.com/64047718/119235210-5aef6f80-baff-11eb-89b1-c4596cf43594.png">

As you can see above, the portfolio shows all the different stocks the user has bought. In this case, the user has bought 16 Apple shares with a value of $125.43	each and 3 Walmart shares for $141.75	each. The user had started with $10,000 and over time, the price of the stocks increased a bit so the user's portfolio value is now at $10,087.86. After buying all the Apple and Walmart stocks, the user has $7,655.73 in cash. Remember, the user has not sold their stocks yet which is why their "CASH" value is less. If they choose to sell a stock, the money would be added to their "CASH". 

<h1>Quoting</h1>

<img width="1259" alt="Screen Shot 2021-05-22 at 2 01 04 PM" src="https://user-images.githubusercontent.com/64047718/119236590-41055b00-bb06-11eb-902f-97831a77eb94.png">

When you click the "Quote" button at the top of the screen, you will be prompted to this page. Here, you can quote a stock! By quoting a stock, you recieve information about that stock regarding its current price. In the text box, you will nbe prompted to type a valid stock symbol (not the compoany name) and upon clicking the "Submit" button, the quote will appear! Below is an image of what appears when typing "AAPL" to get the quote of an Apple stock.

<img width="1277" alt="Screen Shot 2021-05-22 at 2 04 56 PM" src="https://user-images.githubusercontent.com/64047718/119236670-b96c1c00-bb06-11eb-9d82-bd5887912317.png">

<h1>Buying</h1>

<img width="1268" alt="Screen Shot 2021-05-22 at 2 06 17 PM" src="https://user-images.githubusercontent.com/64047718/119237217-b6265f80-bb09-11eb-9e13-89245b9e9cb5.png">

After quoting a certain stock and you decide to buy it, you can click on the "Buy" button at the top to purchase any amount of stocks. Two fields will appear as shown above, "Symbol" and "Shares". In the "Symbol" field you type the symbol of the stock company. In the "Shares" field, you type the number of that stock you will be buying. The web app makes sure to handle errors like an invalid stock symbol or an invalid number of stocks. Additionally, the system checks to make sure the user has the sufficient amount of money to maker their purcahse. If they do not, an error message is displayed notifying the user that they have an insufficient amount of money.

<img width="1273" alt="Screen Shot 2021-05-22 at 2 23 47 PM" src="https://user-images.githubusercontent.com/64047718/119237136-621b7b00-bb09-11eb-9b1b-b27828adc471.png">

After making the purchase, the user is redirected back to the home page where there portfolio is displayed. The table is updated to reflect the changes made from the new purchase. Above is an image of how a portfolio may look on a new account after a user makes their first purchase of 2 Apple stocks.

<h1>Selling</h1>

<img width="1269" alt="Screen Shot 2021-05-22 at 2 28 42 PM" src="https://user-images.githubusercontent.com/64047718/119237380-7dd35100-bb0a-11eb-9128-99059b957a61.png">

Previously, we went over how to buy a stock. Now its time to sell! To sell a stock, the user can click the "Sell" button at the top of the page. Above is what the page will look after arriving. The drop-down menu contains a list of choices for the stock to sell. The list is determined by the different types of stocks the user has purchased and has in their portfolio. The "Shares" field accepts an integer that represents the number of stocks to be sold. To check for errors, the web app makes sure the user is entering a valid number of stocks to be sold. Similar to buying a stock, after selling, the user is brought back to the homepage where the changes are accurately reflected in the table. 

<h1>History</h1>

<img width="1273" alt="Screen Shot 2021-05-22 at 2 21 46 PM" src="https://user-images.githubusercontent.com/64047718/119237463-eb7f7d00-bb0a-11eb-955d-de453ce22fd7.png">

To allow users to track all their trades, the "History" page contains the timestamps of all the user's actions. Every time the user buys or sells, the action is timestamped. If the user made a purchase, the number is a positive number, but if the user sold their stocks, it is represented by a negative number. The third column, "Price" shows the price at which the stock was sold or bought at. The oldest actions are listed at the top while the most recent are at the bottom. 

<h1>Change Password</h1>

<img width="1278" alt="Screen Shot 2021-05-22 at 2 39 44 PM" src="https://user-images.githubusercontent.com/64047718/119237588-9bed8100-bb0b-11eb-9f61-3beaf60bbd46.png">

When clicking "Change Password" at the top, the user is prompted to this page. Here, the user can type the new password they wish to have and click "Change" to change it. 

Finally, to log out, the user clicks the "Log Out" button at the top right of the app. They will be redirected back to the log in page.





