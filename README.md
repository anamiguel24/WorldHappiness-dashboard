# WorldHappiness-dashboard
This project is a dashboard created using the Plotly with Dash software, that visualizes data from the World Happiness Report dataset. The objective of this dashboard is to transform data into meaningful and interactive visualizations.

## Dataset

To conduct our project, we utilized various datasets and two different sources (Kaggle and World Happiness Report official website). We made some changes to the dataset, these changes are in the notebook in the pre-processing folder. The final dataset contains the variables presented in the following table.

|Variable|Type|Description|
|:----|:----|:----|
|Year|int64|Year|
|Country|object|Country’s name|
|CountryCode|object|ISO Alpha-3 Country Code|
|Continent|object|Continent the country belongs to|
|Happiness Rank|int64|Happiness Rank|
|Happiness Score|float64|Happiness Score on a scale from 0 to 10|
|Economy (GDP per capita)|float64|GDP per capita|
|Social Support|float64|National average of the binary responses (either 0 or 1) to the GWP question “If you were in trouble, do you have relatives or friends you can count on to help you whenever you need them, or not?”|
|Healthy Life Expectancy|float64|Healthy life expectancy at birth|
|Freedom|float64|National average of responses to the GWP question “Are you satisfied or dissatisfied with your freedom to choose what you do with your life?”|
|Generosity|float64|Residual of regressing national average of response to the GWP question “Have you donated money to a charity in the past month?” on GDP per capita|
|Government Trust|float64|National average of the survey responses to two questions in the GWP: “Is corruption widespread throughout the government or not” and “Is corruption widespread within businesses or not?”|

We planned to incorporate the countries’ flags into our dashboard, so we also downloaded a dataset from Kaggle consisting of four columns: name of the country, ISO Alpha-2 country code, ISO Alpha-3 country code and, lastly, an URL of the country’s flag.

## Visualization

The dashboard provides a variety of interactive visualizations, including:

- Visualization 1: Graph Map Choropleth 
- Visualization 2: Bar Chart of the Top 5 Countries
- Visualization 3: Bar Chart of the Bottom 5 Countries 
- Visualization 4: Bubble Chart
- Visualization 5: Radar Graph
- Visualizations 6 & 7: Line Chart with Ranking and Factor Evolution
- Visualization 8: Top 3 Countries by Factors

## Validation

Validation has been taken into consideration throughout the development of this dashboard. The data was carefully cleaned and processed to ensure accuracy, and the interactive features were thoroughly tested to ensure that they function as expected. To collect feedback on the usability of the dashboard and identify areas where improvements can be made, we used an observer's questionnaire based on tasks, the system usability scale (SUS) and, finally, Nielsen's 10 usability heuristics.
