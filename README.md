# Overview
Realtime Risk Compliance Monitoring is a system that alerts stakeholders by summarizing government policy changes. This helps stakeholders make informed decisions regarding their market products. The system scrapes policy data from multiple countries, processes it using AI, and delivers summarized insights via email notifications.
# Features
1) Web Scraping: Extracts policy updates from four countries (USA, India, Bangladesh, Pakistan) using beautifulsoup.

2) Data Storage: Stores scraped data in an Elasticsearch container running on Docker.

3) AI-Powered Summarization: Utilizes an AI model to summarize policy changes.

4) Automated Email Alerts: Sends summarized updates to stakeholders via email.

5) Data Visualization: Displays policy trends and summaries in Kibana.

# Tech Stack
1) Python (Backend and AI processing)

2) Beautifulsoup(Web scraping)

3) Elasticsearch (Data storage and retrieval)

4) Docker (Containerization of Elasticsearch)

5) AI model (Summarization)

6) Kibana (Data visualization)

7) SMTP (Email notifications)

# Project Flow
1) Web Scraping

Beautifulsoup extracts policy changes from government websites of the USA, India, Bangladesh, and Pakistan. 

2) Data Storage

The scraped data is stored in an Elasticsearch instance running in a Docker container.

3) Summarization

The stored data is processed using the AI model to generate concise summaries.

4) Email Notifications

Summarized insights are sent to stakeholders via email, enabling timely decision-making.

5) Data Visualization

Kibana is used to visualize trends and insights from the policy data.

# Future Enhancements
1) Integrate real-time monitoring with streaming data pipelines.

2) Expand support for more countries and policy sources.

3) Implement advanced NLP techniques for improved summarization.

# Screenshots

![image](https://github.com/user-attachments/assets/c46d789f-9aff-4a62-909a-fb996b6d34eb)

![image](https://github.com/user-attachments/assets/d236e85f-f8e9-48d2-8894-7c59537e3a94)

![image](https://github.com/user-attachments/assets/e6320d93-e72c-42fa-9edd-73779d8010af) 

![image](https://github.com/user-attachments/assets/f5608679-2920-4ad4-926b-d97bc40373b5)


