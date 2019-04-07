if __name__ == "__main__":
    import pandas as pd
    import numpy as np

    whr2015 = pd.read_csv('2015.csv')
    whr2016 = pd.read_csv('2016.csv')
    whr2017 = pd.read_csv('2017.csv')

# Create years column in all data frames

    whr2015['year'] = 2015
    whr2016['year'] = 2016
    whr2017['year'] = 2017

# Homogenize column names across datasets

    for df in [whr2015, whr2016, whr2017]:
        parentheses = r"[()]"
        df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace(parentheses, '').str.replace('.', '_').str.replace('__', '_')

    column_name_map = {'economy_gdp_per_capita_':'economy_gdp_per_capita',
                      'health_life_expectancy_': 'health_life_expectancy',
                      'trust_government_corruption_': 'trust_government_corruption'}

    whr2017 = whr2017.rename(column_name_map, axis=1)

# Stack dataframes

    combined = pd.concat([whr2015, whr2016, whr2017], ignore_index=True, sort=False)

# Remove columns with missing data in two years

    combined.drop(['lower_confidence_interval', 'standard_error', 'upper_confidence_interval', 'whisker_high', 'whisker_low'], 
                  inplace=True,
                  axis=1
                 )

# Create df of countries and regions from 2015 and 2016 data sets

    combined_first_two_years = combined[(combined['year'] == 2015) | (combined['year'] == 2016)][['country', 'region']]

# Fill in region column for 2017

    combined = combined.merge(right=combined_first_two_years, how='left', on='country', suffixes=('_original', '_new'))

#Drop original regional column

    combined.drop('region_original', axis=1, inplace=True)

# Rename new region column

    combined.rename({'region_new':'region'}, axis=1,inplace=True)

# Drop duplicates created from merging

    combined.drop_duplicates(inplace=True)

    combined.loc[681,'country'] = 'Taiwan'
    combined.loc[681,'region'] = 'Eastern Asia'
    combined.loc[755,'country'] = 'Hong Kong'
    combined.loc[755,'region'] = 'Eastern Asia'

    combined.to_csv('years_combined.csv', index=False)
