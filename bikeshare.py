import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Define accepatble values for each user input
valid_cities_inputs = ['chicago', 'washington', 'new york city']
valid_months_inputs = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
valid_days_inputs = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_user_input(value_name, valid_values):
    """
    Asks user to specify a valid value for a specific input

    Args:
        (str) value_name - the value user should enter
        (str) valid_values - valid values that the use should enter one of them
    Returns:
        df - the valid value user enter
    """
    # we used while to keep taking value from user till a valid one is entered
    while( True ):
        value = input(f'Please enter the {value_name} you want to search in:').lower()
        if value in valid_values:
            return value
        print(f'Invalid {value_name}, please try again!')

        
def format_and_display_duration(duration_in_seconds, duration_name):
    """
    Convert durations in seconds to hours, minutes, and seconds, and display it in a clear way

    Args:
        (float) duration_in_seconds - the duration we wnat to format and display in seconds
    Returns:
        void - no vlue to return
    """
    # 1.first of all we want to extract hours, minutes, seconds
    # 1.1.divide duration_in_seconds by 60 to convert seconds to minutes, and keep the reminder as seconds
    minutes, seconds = divmod(duration_in_seconds, 60)
    # 1.2.divide minutes by 60 to convert minutes to hours, and keep the reminder as minutes
    hours, minutes = divmod(minutes, 60)
    # 1.3.divide hours by 24 to convert hours to days, and keep the reminder as hours
    days, hours = divmod(hours, 24)
    
    # 2.display the duration in a clear way
    # 2.1.find the final duration text
    final_duration_text = ''
    for unit_duration in [[days, 'days'], [hours, 'hours'], [minutes, 'minutes']]:
        if unit_duration[0] > 0:
            final_duration_text += f'{unit_duration[0]} {unit_duration[1]}, '
    final_duration_text += f'and {seconds} seconds'
    # 2.2.display the the duration
    print(f'The {duration_name} is {final_duration_text}.')
    
        
        
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    city = get_user_input('city', valid_cities_inputs)

    # get user input for month (all, january, ... , june)
    month = get_user_input('month', valid_months_inputs)
    
    # get user input for day of week (all, monday, ... sunday)
    day = get_user_input('day', valid_days_inputs)

    # print separator and return user inputs
    print('-'*50)
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

    # read the file of the city we're seaching in, and put it in a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # solve quality and tidness issues 
    # change start time and end time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # extract some useful fields form start time field
    df['start_time_month'] = df['Start Time'].dt.month
    df['start_time_day_name'] = df['Start Time'].dt.weekday_name
    df['start_time_hour'] = df['Start Time'].dt.hour
    
    # combine start and end stations IDs
    df['from_to_stations'] = 'From ' + df['Start Station'] + " to " +  df['End Station']
    
    # filter by month, if month not equal to 'all'
    if month != 'all':
        df = df[df['start_time_month'] == valid_months_inputs.index(month)]
        
    # filter by day, if day not equal to 'all'
    if day != 'all':
        df = df[df['start_time_day_name'] == day.title()]
    
    # return the cleaned datafrom
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month if the dataframe contains data for all months
    try:
        if month == 'all':
            most_common_month = valid_months_inputs[df['start_time_month'].mode()[0]]
            print(f'The most common month is {most_common_month}')
        else:
            print(f'There is no most common month, as you asked to get data for only one month.')
    except:
        print('An error happened, while getting and displaying the most common month.')

    # display the most common day of week
    try:
        if day == 'all':
            most_common_day_name = df['start_time_day_name'].mode()[0]
            print(f'The most common day name is {most_common_day_name}')
        else:
            print(f'There is no most common day, as you asked to get data for only one day.')
    except:
        print('An error happened, while getting and displaying the most common day.')

    # display the most common start hour
    try:
        most_common_start_hour = df['start_time_hour'].mode()[0]
        print(f'The most common start hour is {most_common_start_hour}:00')
    except:
        print('An error happened, while getting and displaying the most common start hour.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    try:
        most_common_start_station = df['Start Station'].mode()[0]
        print(f'The most commonly used start station is {most_common_start_station}')
    except:
        print('An error happened, while getting and displaying the most commonly used start station.')

    # display most commonly used end station
    try:
        most_common_end_station = df['End Station'].mode()[0]
        print(f'The most commonly used end station is {most_common_end_station}')
    except:
        print('An error happened, while getting and displaying the most commonly used end station.')

    # display most frequent combination of start station and end station trip
    try:
        most_common_from_to_stations = df['from_to_stations'].mode()[0]
        print(f'The most frequent combination of start station and end station trip is {most_common_from_to_stations}')
    except:
        print('An error happened, while getting and displaying the most frequent combination of start station and end station trip.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # calculate and display total travel time
    try:
        total_travel_time = df['Trip Duration'].sum()
        format_and_display_duration(total_travel_time, 'total travel time')
    except:
        print('An error happened, while getting and displaying the total travel time.')

    # calculate and display mean travel time
    try:
        mean_travel_time = df['Trip Duration'].mean()
        format_and_display_duration(mean_travel_time, 'mean travel time')
    except:
        print('An error happened, while getting and displaying the mean travel time.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
        user_types_counts = df['User Type'].value_counts()
        print(f'The user types counts are:\n {user_types_counts}')
    except:
        print('An error happened, while getting and displaying the counts of user types.')
    
    # Display counts of gender, gender not exist for all cities, so will check if it exist beofre getting counts
    try:
        if 'Gender' in df.columns:
            gender_counts = df['Gender'].value_counts()
            print(f'The gender counts are:\n {gender_counts}')
        else:
            print(f'The dataset of the city {city} does not have gender data, so we do not have gender counts to display.')
    except:
        print('An error happened, while getting and displaying the counts of gender.')

    # Display earliest, most recent, and most common year of birth
    # Note: year of birth not exist for all cities, so will check if it exist beofre getting earliest, most recent, and most common
    try:
        if 'Birth Year' in df.columns:
            # Display earliest year of birth
            earliest_birth_year = df['Birth Year'].min()
            print(f'The earliest year of birth is: {earliest_birth_year}')
            # Display most recent year of birth
            most_recent_birth_year = df['Birth Year'].max()
            print(f'The most recent year of birth is: {most_recent_birth_year}')
            # Display most common year of birth
            most_common_birth_year = df['Birth Year'].mode()
            print(f'The most common year of birth is: {most_common_birth_year}')
        else:
            print(f'The dataset of the city {city} does not have birth year data, so we have nothing to to display.')
    except:
        print('An error happened, while getting and displaying the earliest, most recent, and most common year of birth.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def display_raw_data(df):
    """Displays raw data 5 by 5, till we reach to the end of the df, or till the user want to stop."""
    
    # put the initail data for start row, and end row
    start_row_index = 0
    end_row_index = 5
    
    # get the length of the dataframe 
    dataframe_length = df.shape[0]
    
    # keep getting 5 by 5 till we reach to the end of the df, or till the user want to stop.
    while True:
        # check if the user would like to see next 5 lines, if no break.
        user_input = input('Would you like to see the next 5 lines of raw data?\n[yes or no]:').lower()
        if user_input == 'no':
            break
        # if start out of boundery: break 
        if start_row_index >= dataframe_length:
            print('There is no more rows to display')
            break;
        # if end index greater than df length, put it as df length
        if end_row_index > dataframe_length:
            end_row_index = dataframe_length
        # print the 5 rows
        print(df.iloc[start_row_index:end_row_index])
        # update the start, end indexes
        start_row_index += 5
        end_row_index += 5
    

def main():
    while True:
        # this try/except to handel error that we can't continue in this iteration.
        # will also add many internal try to handel failing in doing partial parts
        try: 
            city, month, day = get_filters()
            df = load_data(city, month, day)
        
            time_stats(df, month, day)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df, city)
            
            display_raw_data(df)

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
               break
        except:
            print('An error happened, please try again!')


if __name__ == "__main__":
	main()
