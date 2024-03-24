# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 17:58:02 2024

@author: bwill
"""

import pandas as pd
import numpy as np
import time
import calendar as cal

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("What city would you like to research? (Select one of hte following:"+
                     " Chicago, New York City or Washington) \n" +
                     "Enter Here -->  ")
        # make entries case-insensitive and use small letters, as applied when assigning city names at lines 7-9
        city = city.lower()
        
        # invalid input handling for city
        if city not in ('new york city', 'chicago', 'washington'):
            print("Please enter a valid city.")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , December)
    while True:
        month = input("Which month would you like to analyze for " + city.title() + "?" + "\n"
                      "(Select a single month, January thru June or type none if you do not wish "+
                      "to specify a month.) \n" +
                      "Enter Here -->  ")        # make entries case-insensitive and use small letters
        month = month.lower()
        
        # invalid input handling for month
        if month not in ('january', 'february', 'march', 'april', 'may', 'june'):
            print("Please enter a valid month.")
            continue
        else:
            break

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Select which day of hte week you would like to analyze? \n" +
                    "You may select any day, Sunday through Saturday.\n" +
                    "Enter Here -->  ") 
        # make entries case-insensitive and use small letters
        day = day.lower()
        
        # Invalid input handling for month
        if day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                       'saturday', 'sunday', 'all'):
            print("Please enter a valid day.")
            continue
        else:
            break

    print('-'*40, '\n\n')
    print('You have made the following selections: \n\n' + 
          'City: ', '\t\t\t', city.title(), '\n' + 
          'In the Month of:',month.title(),'\n' +
          'For day:  ', '\t\t',  day.title(), '\n\n' + 
          'Please hold, this may take a few moments to retreive the data you requested..........') 
    print('-'*40)
    return city, month, day




def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Read the dataframe of the selected city, using the pandas package
    df = pd.read_csv(CITY_DATA[city])
    

    df.info()
    
    x = df.isnull().sum()
    print(x)
    
  #  df['Gender'] = df['Gender'].fillna('')
  #  df['Birth Year'] = df['Birth Year'].fillna('')
    #print(x)
 ##  df.groupby('Start Station')['Trip Duration'].describe()
    

 ##   boxplot = df.boxplot(column=['Trip Duration'], grid=True, color='black')
 ##   print(boxplot)

    
    print('Validating if data is available for', city.title(), '! \n\n') 
    print(df[['Start Time', 'Start Station', 'Trip Duration']].head(4))
   

    
    # Convert Start Time to a datetime for subsequent extraction of month and weekday (and later, hour)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Defind month and day of the week.
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday


    
    # Filter the dataset based on selections
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month = months.index(month) + 1
        df = df[df['Month'] == month]
    
    if day != 'all':
        days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        day = days.index(day) 
        df = df[df['Weekday'] == day]
    
    return df



def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Determine most common month
    ind_month = df['Month'].value_counts().idxmax()
    
    # Print full name of most common month
    if month != 'all':
        print(__'You have selected',month.title(),'. The most common '+
              'month for',city.title(),'is:  ', cal.month_name[ind_month], '\n\n'__)
    
    else:
        print('The most common month in ',city.title(),' is:  ', 
              cal.month_name[ind_month], '.\n\n')
  
   
    # Establish most common weekday
    ind_day = df['Weekday'].value_counts().idxmax()
    
    # Establish the  most common weekday
    if day != 'all':
        print('You have selected',day.title(),'. The most common '+
              'day of the week in',city.title(),'is:  ', cal.day_name[ind_day], '\n\n')    
    else:
        print('The most common day of the week is:  ', cal.day_name[ind_day], '\n\n')
    
        
    # display the most common start in hours. 
    df['Start Hour'] = df['Start Time'].dt.hour    
    
    # Set the most common start hour
    print('The most common start hour for your selected city', city.title(), 'on',  cal.day_name[ind_day],  'is:  ', 
          df['Start Hour'].value_counts().idxmax(), 'o\'clock.\n')
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


    time.sleep(10)



# DURATION STATISTICS

def duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    sum_sec = df['Trip Duration'].sum()
    
    print('The total travel time for your selection is:  ', sum_sec, 'seconds.\n\n')   
    
    # Establish total travel time to hours and cast data with zero decimal points
    sum_min = round(sum_sec / 60 ,0)
    
    # Establish total travel time
    print('The total travel time for your selection is:  ', sum_min, 'minutes.\n\n')

    # Calcluate the mean travel timef
    mean_sec = df['Trip Duration'].mean()
    
    # Establish total travel time to minutes and cast data with zero decimal points
    mean_min = round(mean_sec / 60  ,0)    
    
    # Establish total travel time to minutes and cast data with zero decimal points
    mean_h = round(mean_min / 60, 0)   
    
    # Display mean travel time in minutes if below one hour or in hours when the values are above 60 minutes.
    if mean_min < 60:
        print('The mean travel time for your selection when less than 60', mean_min, 'minutes.\n\n')
    else:
        mean_h = round(mean_min / 60 ,1)
        print('The mean travel time for your selection when less than 60 min', mean_h, 'hours.\n\n')
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


    time.sleep(10)

def user_stats(df, city):
    """Displays statistics on bikeshare users. Statistics will be calculated using NumPy."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # set new variable fordf for counts
    usertypes = df['User Type'].values
    
    # Count the occurences by the various user types
    subscriber  = (usertypes == 'Subscriber').sum()
    customer = (usertypes == 'Customer').sum()
    
    # Show count data by user type
    print('The number of subscribers in', city.title(), 'is:', subscriber,'\n')
    print('The number of customers in', city.title(), 'is:',customer,'\n')

    # Display counts of gender
    # Display earliest, most recent, and most common year of birth
    # gender and year of birth are missing from the Washington dataset
    if city.title() != 'Washington':
        
        # counts by gender
        gender = df['Gender'].values
        
        # Occurences by different user types
        male  = (gender == 'Male').sum()
        female = (gender == 'Female').sum()
        
        # Cast counts by Gender
        print('The number of male subscribers in', city.title(), 'is:',male,'\n')
        print('The number of female subscribers in', city.title(), 'is:',female,'\n')
        
        # year of birth
        # Set up the Valuesfor Birth Year
        birthyear = df['Birth Year'].values
        #df.dropna(subset=['Birth Year'])

        # Fine unique birth years and remove NaNs using the isnan method
        unique_birthyear = np.unique(birthyear[~np.isnan(birthyear)])
        
        # Latest birth year = highest / maximum number
        latest_birthyear = unique_birthyear.max()
        
        # Earliest birth year = lowest / minimum number
        earliest_birthyear = unique_birthyear.min()
        
        # Cast both the latest and earliest birth year
        print('The most recent birth year of users in', city.title(), 'is:',
              latest_birthyear ,'\n')
        print('The earliest birth year of users in', city.title(), 'is:',
              earliest_birthyear,'\n')   
        
        # Cast the most common birth year
        print('The most common birth year of users in', city.title(), 'is:', 
              df['Birth Year'].value_counts().idxmax(), '\n')
    
    else:
        # Since Washington does not have gender information.
        print('Uable to show gender and birth year for Washington as data is not available!')

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


    time.sleep(10)

    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most common start station for your selection is:  ', 
          df['Start Station'].value_counts().idxmax(), '.\n\n')

    # display most commonly used end station
    print('The most common end station for your selection is:  ', 
          df['End Station'].value_counts().idxmax(), '.\n\n')

    # display most frequent combination of start station and end station trip
    df['Station Combination'] = df['Start Station'] + ' (start) and ' + df['End Station']
    
    # Establihs most common station combination traveled between? 
    print('The most common station combination for your selection is: \n\n\n', 
         '* ', df['Station Combination'].value_counts().idxmax(), '\n')

    print('The Lease common station combination for your selection is: \n\n', 
          '* ', df['Station Combination'].value_counts().idxmin(), '\n')



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


    time.sleep(10)




# new function for raw data display    
def raw_data(df):
    """ Displays 4 lines of raw data at a time when yes is selected."""
    # define index i, start at line 1
    i = 1
    while True:
        rawdata = input('\nWould you like to see 4 lines of raw data? Enter yes or no.\n' +
        "Enter Here -->  ")
        if rawdata.lower() == 'yes':
            # print current 4 lines
            print(df[i:i+4])
            
            # increase index i by 4 to print next 4 lines in new execution
            i = i+4
            
        else:
            # break when no is selected
            break

        # Having to set changes to in arguments to allow functions to run properly
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, city, month, day)
        duration_stats(df)
        user_stats(df, city)
        station_stats(df)
 
      
 
        #Display raw data
        raw_data(df)
        
        
        restart = input('\nWould you like to restart? Enter yes or no.\n' +
        "Enter Here -->  ")
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
    
    
