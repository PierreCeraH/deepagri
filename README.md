# DeepAgri Project
Authors: [Pierre Cera-Huelva](https://github.com/PierreCeraH), [Wenfang Zhou](https://github.com/WenfangZh), [Constantin Talandier](https://github.com/Constantier), [Gaspar Dupas](https://github.com/Gaspar97)

## Project Description
Project in the context of a Paris LeWagon Data Science project (FT #802).

The aim of the project is to predict the production of soft wheat (used for bread) in Metropolitan France. The model will be aimed at predicting production at the mid-year harvest in early July based on data available at the start of March of the same year.

## Data Sourcing
This project exclusively used publicly-available data. Please contact the authors for more information on specific sources.

## Methodology
### Model
The project used a Linear Regression model. Other models, such as XGBoost Regressors and Dense NNs were also attempted, but underperformed compared to a standard linear regression, likely due to an insufficiently large dataset.

### Data
#### Scope
The project utilised data ranging from mid-2009 to February 2022 (inclusive).

#### Temporal Scale
The model was trained using features aggregated at a monthly level.

#### Geographical Scale
The model was trained on a per-department basis, using all of metropolitan France.
