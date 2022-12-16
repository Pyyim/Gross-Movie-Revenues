import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.linear_model import Lasso, Ridge, LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
import pickle as pkl
from tqdm import tqdm
import time
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords

# uncomment if running for the first time
# import nltk
# nltk.download()

stopwords = stopwords.words('english')
pd.set_option('display.max_columns', None)

data = pd.read_csv('src/model/final_data.csv')

Y = data['1st_year_revenue']
X = data[['year', 'runtime']]

data.sort_values(by=['released'], inplace=True)
y = data['1st_year_revenue']
X = data.drop(columns=['title', '1st_year_revenue'], axis=1)
# X = data.drop(['gross'], axis=1)

# Shuffle to false to handle time data
X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size = 0.2)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, shuffle=False, test_size = 0.2)

categorical_cols = ['language', 'country', 'rating']

# Text Preprocessor
text_preprocesser = Pipeline(
    steps=[
        # Input tfidf parameters
        ('tfidf', TfidfVectorizer(stop_words = stopwords, strip_accents = 'unicode', min_df = .001, max_df = 0.7))
    ])

# Categorical Preprocessor
categorical_preprocessor = Pipeline(
    steps=[
        # Change to 'ignore' if error raised
        ("OHE", OneHotEncoder(handle_unknown='error', drop='first'))
    ])

#Combine preprocessors
#Commenting out TfidfVectorizer as it does not help the model
preprocessor = ColumnTransformer(
    transformers=[
#         ('text', text_preprocesser, 'plot'),
        ('category', categorical_preprocessor, categorical_cols)
    ])


rf_pipe = make_pipeline(
    preprocessor, 
    StandardScaler(with_mean=False), 
    RandomForestRegressor(random_state = 42)
)


rf_pipe = make_pipeline(
    preprocessor, 
    StandardScaler(with_mean=False), 
    RandomForestRegressor(max_depth = None, 
                          max_features = 'sqrt', 
                          n_estimators = 600, 
                          random_state = 42)
)
rf_pipe.fit(X_train, y_train)
filename= 'src/model/model.pkl'
pkl.dump(rf_pipe, open(filename, 'wb'))