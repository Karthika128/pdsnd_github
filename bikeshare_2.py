import time
import pandas as pd
import numpy as np

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
        try:
            city= str(input("Enter the city name from the list (chicago, new york city ,washington): ")).lower()
            print(city)
        except:
            print("Not a valid city. Enter a city name as shown in the list.")
        else:
            if city in CITY_DATA:
                break
            else:
                print("Not a valid city. Enter a city name as shown in the list.")

    # get user input for month (all, january, february, ... , june)
    months=['all', 'january', 'february','march','april','may','june']
    while True:
        try:
            month=str(input("Enter the month from the list (all, january, february, march, april, may, june): ")).lower()
            print(month)
        except:
            print("Not a valid month. Enter a month as shown in the list.")
        else:
            if month in months:
                break
            else:
                print("Not a valid month. Enter a month as shown in the list.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days=['all', 'monday', 'tuesday','wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        try:
            day= str(input("Enter the day of week from the list (all, monday, tuesday,wednesday, thursday, friday, saturday, sunday): "))
            print(day)
        except:
            #checking if it is not a valid day 
            print("Not a valid day. Enter a day as shown in the list.")
        else:
            if day in days:
                break
            else:
                print("Not a valid day. Enter a day as shown in the list.")

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
    df=pd.read_csv(city.replace(' ','_')+'.csv')
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
   # providing user an option to see raw data 5 lines at a time
    linecount=5
    while True:
        try:
            rawdata = str(input("Do you want to see next 5 lines of filtered raw data?: Enter yes or no.\n"))
            print(rawdata)
        except:
            print("Not a valid input!")
        else:
            if rawdata.lower() == 'no':
                break
            elif rawdata.lower() == 'yes':
                print(df.head(linecount))
                linecount+=5
            else:
               print('Not a valid input!')

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("Most common month is: ", df['month'].mode()[0])

    # display the most common day of week
    print("Most common day of week is: ", df['day_of_week'].mode()[0])

    # display the most common start hour
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    print('Most common Start Hour is: ', df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most common start station is: ', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most common end station is: ', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['startendpointcombo']=df['Start Station']+ ' '+ df['End Station']
    print('Most frequent combination of start station and end station is: ',df['startendpointcombo'].mode()[0])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time is: ', df['Trip Duration'].sum())

    # display mean travel time
    print('Mean travel time is: ', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The counts of user types is:\n',df['User Type'].value_counts())

    #check to see if 'Gender' column exists in the dataframe, as washington city data doesnot have Gender data
    if 'Gender' in df.columns:
        # Display counts of gender
        print('The counts of gender is:\n',df['Gender'].value_counts())

    #check to see if 'Birth Year' column exists in the dataframe, as washington city data doesnot have Birth Year data
    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        print('The most earliest year of birth is: ',int(df['Birth Year'].min()))
        print('The most recent year of birth is: ',int(df['Birth Year'].max()))
        print('The most common year of birth is: ',int(df['Birth Year'].mode()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
           break

if __name__ == "__main__":
	main()
