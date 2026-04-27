# Fully Automated Near Real-Time Global Weather Dashboard

📄 [Versão em português](README.md)

## Project Description
This project consists of building a complete weather data pipeline, from automated ingestion to final visualization in an interactive Power BI dashboard. Data is collected from external REST APIs, stored in a cloud database, and automatically updated throughout the day. The dashboard allows users to explore current, historical, and forecasted weather conditions for multiple cities around the world, providing near real-time data (with only a few hours delay at most). Beyond the technical aspects, the project also explores a unique visual identity inspired by the Frutiger Aero aesthetic, delivering a nostalgic, clean, and visually pleasing experience.

## 🎯 Objective
This is a personal project focused on improving data analytics skills, including:
- Building a complete end-to-end data pipeline
- Integrating multiple weather data sources
- Automating data ingestion and updates
- Developing an interactive and intuitive dashboard
- Applying best practices in data modeling and visualization
- Exploring UX/UI principles applied to dashboards

## Technologies Used
- Python
- Main libraries: meteostat, numpy, psycopg2, dotenv, requests
- Git & GitHub
- PostgreSQL (Neon - Cloud)
- OpenWeather API
- Meteostat API
- Prefect Cloud
- Power BI

## Project Architecture
The figure below illustrates the architecture behind this project:

![Pipeline](https://github.com/user-attachments/assets/622c01e0-2752-4dff-b708-0cd436411eeb)

## Data Pipeline (ETL)
### 🔹 Extraction
- Historical data collection using the Meteostat API
- Current (near real-time) data collection via OpenWeather API
- Forecast data collection for the next 5 days
- Multiple API requests executed for different global cities

### 🔹 Transformation
- Handling missing values
- Standardizing units and formats
- Converting timestamps to UTC
- Enriching data with additional attributes (e.g., weather_main, description, icon)

### 🔹 Loading
- Inserting data into PostgreSQL tables (Neon)
- Structuring data into multiple tables:
  - Historical data
  - Current data
  - Forecast data
- Ensuring data integrity and consistency
- Continuous updates via automation

## 🛢 Data Ingestion Strategy
- **Historical Data ([historical_ingestion.py](historical_ingestion.py))**  
Data from 10 cities across different countries, collected with daily granularity.

- **Current Data ([current_ingestion.py](current_ingestion.py))**
  - Runs automatically 4 times per day
  - 00:00, 06:00, 12:00, 18:00
  - Incremental database updates
 
- **Forecast Data ([forecast_ingestion.py](forecast_ingestion.py))**
  - Runs automatically once per day at 00:00
  - Incremental database updates
 
## Access the Dashboard
🔗 [Click here to access the Power BI dashboard](https://app.powerbi.com/view?r=eyJrIjoiMTM4NTYzYjMtZWIxMS00ZjYxLTkyMTItNmJlNjBkN2Y1NzZhIiwidCI6ImNmNzJlMmJkLTdhMmItNDc4My1iZGViLTM5ZDU3YjA3Zjc2ZiIsImMiOjR9)

## Interactive Dashboard
The dashboard was built in Power BI with a focus on clarity, interactivity, and user experience. On the sidebar, it includes the following filters: `City` (main filter, single selection), `Timestamp`, and `Weather Condition`. At the top, below the title, there are key KPI cards, all with explanatory tooltips for better user understanding, along with dynamic icons. On the top-right corner, there is a selector that allows `temperature unit switching`, enabling users to view the dashboard in either Celsius or Fahrenheit.

![Dashboard](https://github.com/user-attachments/assets/622848f5-9ede-4b43-863f-942777f2af85)

In the main section, there is a `tab-based navigation` (created using bookmarks), where each tab contains a different chart:
- `Line chart:` Temperature ([unit]) in [city] in the last [period] days
- `Line chart:` Temperature Forecast ([unit]) in [city] for the next 5 days
- `Bar chart:` Monthly Temperature Range (Min vs Max) in [city]
- `Bar chart:` Day vs Night Temperature ([unit]) in [city]

**Note:** Terms inside `[]` are dynamic placeholders that change based on the filters selected by the user.

Below this section, there is a donut chart titled "`Weather Condition Distribution in [city] (Top 5)`". Next to it, there is a section with an air humidity gauge (in %) and an atmospheric pressure gauge (in hPa), each accompanied by simple insight cards:
- `Air humidity:` dry, comfortable, humid, very humid
- `Atmospheric pressure:` unstable, stable

On the right side of the main section, there is a `city comparison section`, featuring an interactive toggle (built using bookmarks). It is disabled by default, but when activated, it reveals a second city filter and a comparison table showing attributes (such as temperature, feels like, humidity, etc.) between the main selected city and the comparison city.

## Selected Aesthetic: Frutiger Aero
The visual identity of this dashboard is strongly inspired by the Frutiger Aero aesthetic, a design style popular between the mid-2000s and early 2010s. This aesthetic is characterized by elements such as soft gradients, transparency, glossy surfaces, vibrant colors (especially blue and green tones), and nature/technology-inspired icons like sky, water, leaves, and light.

Often associated with interfaces like Windows Vista and Windows 7, Frutiger Aero conveyed a sense of optimistic futurism, cleanliness, and harmony between technology and nature.

This concept fits perfectly with the purpose of this project, which revolves around environmental and weather data. The combination of colors, visual elements, and effects aims not only to present information but also to create a more immersive, pleasant, and even nostalgic user experience.

## Color Palette
![Palette](https://github.com/user-attachments/assets/c947069c-e3eb-4aa9-8858-3e3910e77035)

## Automation (Prefect Cloud)
To keep the data always up to date, orchestration was implemented using Prefect Cloud to automatically run the ingestion scripts. The jobs created were:
- current_ingestion
- forecast_ingestion  

### Benefits:
- Fully automated cloud execution
- No dependency on local environment
- Scheduling via cron jobs
- Execution monitoring (logs and status)
- Pipeline scalability

## 🚀 Future Improvements
- Integration with more cities or regions
- Inclusion of higher granularity historical data (hourly)
- Implementation of weather alerts
- Creation of a custom API to serve the data
- Addition of interactive maps

## Learnings
- End-to-end data pipeline development
- Integration of multiple APIs
- Data modeling for analytics
- UX/UI applied to data visualization
- Best practices in automation and version control

## License
This project is licensed under the [MIT License](LICENSE).

## Tags
`#Prefect` `#API` `#PostgreSQL` `#Portfolio` `#Data` `#DataAnalytics` `#DataEngineering` `#DataVisualization` `#DataProject` `#Weather` `#pipeline` `#dashboard` `#cloud` `#datascience` `#dataengineering` `#datapipeline` `#etlprocess` `#datavisualization` `#automation` `#database` `#postgres` `#cloudcomputing` `#pythonproject` `#apiconsumption` `#realtime` `#datadriven` `#analytics` `#businessintelligence` `#cicd` `#clouddata` `#datastack` `#dataportfolio`
