import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_DATA = {'all': 0,
              'jan': 1,
              'feb': 2,
              'mar': 3,
              'apr': 4,
              'may': 5,
              'jun': 6,
              'jul': 7,
              'aug': 8,
              'sep': 9,
              'oct': 10,
              'nov': 11,
              'dec': 12
               }
WEEK_DATA = { 'all': 'all',
              'mon': 'Monday',
              'tue': 'Tuesday',
              'wed': 'Wednesday',
              'thu': 'Thursday',
              'fri': 'Friday',
              'sat': 'Saturday',
              'sun': 'Sunday'
              }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #get user input for city (chicago, new york city, washington)
    print ("Please choose the city you would like to investigate? Enter 'c' for Chicago, 'n' for New York or 'w' for Washington: ")
    while True:
        city = str(input("--> ")).lower()
        if city == 'c' or city == 'n' or city == 'w':
            break
        else:
            print ("Options are 'c', 'n' or 'w': ")

    #change input to city name
    if city == 'c':
        city = "chicago"
    elif city == 'n':
        city = "new york city"
    elif city == 'w':
        city = "washington"
    else:
        print ('should not happen ;-)')

    #get user input for month (all, january, february, ... , june)
    print ("Please choose the month you are interested in? Enter 'all' for the whole year, 'jan' for january, 'feb', 'mar', ..., 'dec' for december: ")
    while True:
        month = str(input("--> ")).lower()
        if month == 'all' or month == 'jan' or month == 'feb' or month == 'mar' or month == 'apr' or month == 'may' or month == 'jun' or month == 'jul' or month == 'aug' or month == 'sep' or month == 'oct' or month == 'nov' or month == 'dec':
            break
        else:
            print ("Options are only 'all' or the first 3 letters of month: ")

    #get user input for day of week (all, monday, tuesday, ... sunday)
    print ("Please choose the day of week you are interested in? Enter 'all' for the whole week, 'mon' for monday, 'tue', ..., 'sun' for sunday: ")
    while True:
        day = str(input("--> ")).lower()
        if day == 'all' or day == 'mon' or day == 'tue' or day == 'wed' or day == 'thu' or day == 'fri'or day == 'sat'or day == 'sun':
            break
        else:
            print ("Options are only 'all' or the first 3 letters of day: ")

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    df['duration'] = df['End Time'] - df['Start Time']
    df['Trip'] = df['Start Station'] + " --> " + df['End Station']

    #filter month
    if month != 'all':
        df = df[df['month'] == MONTH_DATA[month]]

    #filter day of week
    if day != 'all':
        df = df[df['day_of_week'] == WEEK_DATA[day]]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    max_month = df['month'].mode()[0]
    for key, value in MONTH_DATA.items():
        if value == max_month:
            print ("The most common month (in your investigation interval) is:")
            print ("--> " + key.title())

    #display the most common day of week
    get_most_freq_of_column(df, 'day_of_week')

    #display the most common start hour
    get_most_freq_of_column(df, 'hour')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    get_most_freq_of_column(df, 'Start Station')

    #display most commonly used end station
    get_most_freq_of_column(df, 'End Station')

    #display most frequent combination of start station and end station trip
    get_most_freq_of_column(df, 'Trip')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    print ("The total travel time (in your investigation interval) is:")
    print ("--> " + str(df['duration'].sum()))

    #display mean travel time
    print ("The mean travel time (in your investigation interval) is:")
    print ("--> " + str(df['duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #display counts of user types
    print("Rentals per user type:")
    print("-->\n" + str(df['User Type'].value_counts()) + "\n")

    #skip following stats for washington
    if city == 'washington':
        return

    #display counts of gender (skip for washington)
    print("Rentals per gender:")
    print("-->\n" + str(df['Gender'].value_counts()) + "\n")

    #display earliest, most recent, and most common year of birth
    ## min (skip for washington)
    print ("The earliest year of birth (in your investigation interval) is:")
    print ("--> " + str(int(df['Birth Year'].min())))
    ## max (skip for washington)
    print ("The latest year of birth (in your investigation interval) is:")
    print ("--> " + str(int(df['Birth Year'].max())))
    ## most (skip for washington)
    #alternative: get_most_freq_of_column(df, 'Birth Year')
    print ("The most common birth year (in your investigation interval) is:")
    print ("--> " + str(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def get_most_freq_of_column(df,column):
    """Calcs the most freuent value in a column of a dataframe"""
    max_value = df[column].mode()[0]
    print ("The most common {} (in your investigation interval) is:".format(column))
    print ("--> " + str(max_value))

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        #Bypass for programming
        #df = load_data('new york city', 'all', 'all')

        #stat functions
        if not df.empty:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df, city)

            #raw data display
            raw_data_request = input('\nWould you like to see the raw data of your investigation? (5 lines)? Enter yes or no.\n')
            if raw_data_request.lower() == 'yes':
                print(df.head())
        else:
            print("\nThere are no data for your selection!")

        #restart programm
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
