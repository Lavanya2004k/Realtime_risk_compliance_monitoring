# Realtime_risk_compliance_monitoring

The main aim of the project is to alert the stake holder by sending the summarized data in which it contains the changes of the decisions taken by the government. This can help the stake holders to take decisions for their products which are in the market.

# Steps that were followed to create the project  

1) Web scraped the data from four countries: USA,INDIA,BANGLADESH and PAKISTAN
   I have used selenium to webscrape my data from these four countries. Selenium scrapes the data which is there inside the page of login. So, rather than using beautifulsoup I have used selenium to do this.
2) The scrapped data gets stored in elastic search where I have created a container in the docker at a port address.
3) The data gets fetched from elastic search and will be summarized using a AI model(Llama).
4) The summarized data will be sent to the stake holders email as points.
5) The plots of the news data are shown in Kibana.
