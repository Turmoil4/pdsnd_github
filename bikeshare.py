#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 20:33:13 2020

@author: williamrobinson
"""

# Import the required functions for the project
import time
import pandas as pd


# As files are on local PC, I have opened each file and loaded into Pandas
chi = open('./chicago.csv','r')
#chi= open('/Users/williamrobinson/Documents/Education/Udacity_Degree/Python_Dev/Project2/chicago.csv','r')
chi_data=pd.read_csv(chi)
chi.close()

nyc=open('./new_york_city.csv','r')
#nyc= open('/Users/williamrobinson/Documents/Education/Udacity_Degree/Python_Dev/Project2/new_york_city.csv','r')
nyc_data=pd.read_csv(nyc)
nyc.close()

wdc=open('./washington.csv','r')
#wdc= open('/Users/williamrobinson/Documents/Education/Udacity_Degree/Python_Dev/Project2/washington.csv','r')
wdc_data=pd.read_csv(wdc)
wdc.close()

# Created dictionaries that are then correlated to User Inputs
CITY_DATA = { 'chi': chi_data,'nyc': nyc_data,'dc': wdc_data}
citynames = {'chi': "Chicago",'nyc': "New York City",'dc': "Washington, DC"}

cal_months={'0':'ALL','1':'January','2':'February','3':'March','4':'April',
            '5':'May','6':'June'}

#Data does not include data past June
#,'7':'July','8':'August','9':'September','10':'October','11':'November','12':'December'}
cal_days={'0':'ALL','1':'Monday','2':'Tuesday','3':'Wednesday','4':'Thursday',
         '5':'Friday','6':'Saturday','7':'Sunday'}


# The getuserdata function requests information from the users:
def getuserdata():
    
    # This variable will be used to insure that we have valid inputs from user
    valid_city=0
    valid_month=0
    valid_day=0
    print("-"*100)
    print("Calling the getuserdata function.\n")
    print('Hello! Let\'s explore some US bikeshare data!')
    print("-"*100)

# Created 3 while loops to account fro invalid inputs.
# Ask user for select city.

    while valid_city<1:
        usercity = input("Choosing ONLY from (CHI, NYC, DC), Input your selected city: \n")
        if usercity.lower() in CITY_DATA:
            valid_city+=1
        else:
            valid_city=0

# get user input for month (all, january, february, ... , june)

    while valid_month<2:
        usermonth=input("Use ONLY numbers 1-6 (Jan-Jun) for selected month, where 0=ALL Months: \n")
        if usermonth in cal_months:
            valid_month+=2
        else:
            valid_month=0

# get user input for day of week (all, monday, tuesday, ... sunday)

    while valid_day<3:
        userday=input("Use ONLY numbers 1-7 (Mon-Sun) for selected day, where 0=ALL Days: \n") 
        if userday in cal_days:
            valid_day+=3
        else:
            valid_day=0

# converts user input for city into lower case for future calls
    city=usercity.lower()
    print("-"*100)
    
    return(city,usermonth,userday)

"""First, use the provided city to create the intial dataframe.In order to 
filter the resulting pandas dataframe, we converted the user inputs to 
intergers.  This is because the dataframe columns for month and day_of_week 
are integers.  Then Filter Working Database(wrk_df) by user inputted month 
(int_mon) and day(int_day)to create new dataframe."""

def create_df(city,usermonth,userday):
    print("Calling the create_df function.\n")
    start_time=time.time()
    wrk_df = CITY_DATA.get(city)
    int_mon = int(usermonth)
    int_day = int(userday)

#Convert Start Time column to datetime
    wrk_df['Start Time']=pd.to_datetime(wrk_df['Start Time'])

#Extract month, day of week, and hour from Start Time to create new columns
    wrk_df['month'] = wrk_df['Start Time'].dt.month
    wrk_df['day_of_week'] = wrk_df['Start Time'].dt.weekday+1
    wrk_df['hour']=wrk_df['Start Time'].dt.hour
    
#Add column that combines start/end stations for trip popular trips
    wrk_df['Trip']=wrk_df['Start Station'].str.cat(wrk_df['End Station'],sep=" to ")

#Filter by user selected month and day
    if int_mon!=0:
        wrk_df=wrk_df[wrk_df['month']==int_mon]
        
    if int_day!=0:
        wrk_df=wrk_df[wrk_df['day_of_week']==int_day]
        
#Script testing print(wrk_df.iloc[0:15,2:5])
#Script testing print(list(wrk_df))
    print("\n**This function took %s seconds.**" % round((time.time() - start_time),5))
    print("-"*100)
    return(wrk_df,int_mon,int_day)

"""The usrprint function prints out the user inputs.Data noted by USR is 
the converted user inputs as we simplified user inputs.  These are used 
to clear print statements of user inputs"""

def usrprint(city,usermonth,userday):
    
    print("Calling the usrprint function.\n")
    start_time=time.time()
    
    cityname=citynames[city]
    usr_month=cal_months.get(usermonth)
    usr_day=cal_days.get(userday)
    
    print("\nYour selected city is: {}\n".format(cityname))
    print("Your selected month is: {}\n".format(usr_month))
    print("Your selected day is: {}\n".format(usr_day))
    print("\n**This function took %s seconds.**" % round((time.time() - start_time),5))
    print("-"*100)
    
    return(cityname,usr_month,usr_day)

"""This pop_travel_time function calculates the frequent times of travel.  
Keep in mind that if the user has selected ALL months, then common month is 
excluded.  Likewise, if user selects ALL days, the common days is excluded."""

def pop_travel_time(wrk_df,int_mon,int_day,usr_month,usr_day,cityname):
    
    #Most Popular Month
    start_time=time.time()
    print('\nCalculating The Most Frequent Times of Travel in {}\n'.format(cityname))

    if int_mon==0:
        pop_month=str(wrk_df['month'].mode()[0])
        print("1. The most popular month for bike usage is {}".format(cal_months.get(pop_month)))
    else:
        print("1. Popular Month is ONLY VALID if user selects ALL months!")
    
    #Most Popular Day
    if int_day==0:
        pop_day=str(wrk_df['day_of_week'].mode()[0])
        print("2. The most popular day for bike usage in the month of {} is {}".format(usr_month,cal_days.get(pop_day)))
    else:
        print("2. Popular Day is ONLY VALID if user selects ALL days!")     

    #Most Popular Hour
    pop_hour=wrk_df['hour'].mode()[0]
    print("3. The most popular hour for bike usage is {} for the month of {} and includes {} days!".format(pop_hour,usr_month,usr_day))
    
    print("\n**This function took %s seconds.**" % round((time.time() - start_time),5))
    print("-"*100)

"""This pop_station function determines the most used stations and trips"""

def pop_stations(wrk_df,cityname):
    start_time=time.time()
    print('\nCalculating The Most Frequently used stations and trips between stations in {}\n'.format(cityname))

    # display most commonly used start station
    pop_start_station = wrk_df['Start Station'].mode(dropna=True)[0]

    # display most commonly used end station
    pop_end_station = wrk_df['End Station'].mode(dropna=True)[0]

    """display most frequent combination of start station and end station trip
    This refers to the concatenated column (TRIP) that combines start/end 
    stations."""

    pop_trip = wrk_df['Trip'].mode(dropna=True)[0]

    #Print results
    print("4. The most popular starting station for customers is {}!".format(pop_start_station))
    print("5. The most popular end station for customers is {}!".format(pop_end_station))
    print("6. The most popular trips for customers is {}!".format(pop_trip))
    
    print("\n**This function took %s seconds.**" % round((time.time() - start_time),5))
    print("-"*100)
    
"""This trip_duration function calculates and displays statistics on the 
total and average trip duration"""

def trip_duration(wrk_df,cityname):
    start_time=time.time()
    print('\nCalculating the average and total travel times in {}\n'.format(cityname))

    # display total travel time
    total_time=round(sum(wrk_df['Trip Duration'])/360,2)
    
    # display mean travel time
    mean_time= round(wrk_df['Trip Duration'].mean(skipna=True,numeric_only=None)/360,2)
    
    #print results
    print("7. The TOTAL trip time is {} hours!".format(total_time))
    print("8. The MEAN trip time is {} hours!\n".format(mean_time))
    
    print("\n**This function took %s seconds.**" % round((time.time() - start_time),5))
    print("-"*100)

"""The user_info function calculates and displays statistics on 
bikeshare users."""

def userinfo(wrk_df,city,cityname):
    start_time=time.time()
    print('\nCalculating the user statistics in {}\n'.format(cityname))
    
    # Display counts of user types
    usercount = wrk_df.groupby(['User Type'])['Trip Duration'].count()
    print("9. The below table proviudes the total rentals by the type of user.\n")
    print(usercount)
    print("\n")
    
    """As DC does not have gender or birth year columns, we cannot calculate 
    stats related to these columns."""
    if(city=='dc'):
        print("10. Because Washington, DC does not offer Gender and Birth Year, we will not provide these stats")
        print("\n")
    else:
        # Display counts of gender
        gendercount=wrk_df.groupby(['Gender'])['Trip Duration'].count()
        print("10.  The below table provides the total rentals by the user gender.\n")
        print(gendercount)
        print("\n")
    
        """Display earliest (min-oldest), most recent(max-recent), and most 
        common year(mode-common) of birth"""
        common_yr=int(wrk_df['Birth Year'].mode(dropna=True)[0])
        recent_yr=int(wrk_df['Birth Year'].max())
        oldest_yr=int(wrk_df['Birth Year'].min())
        
        print("11. Most users were born in {}.".format(common_yr))
        print("12. The youngest users were born in {}.".format(recent_yr))
        print("13. The oldest user was born in {}.".format(oldest_yr))
    
    print("\n**This function took %s seconds.**" % round((time.time() - start_time),5))
    print("-"*100)
    
"""The view raw data allows the user to view raw data.  For presentation 
purposes, I limited the raw data to only 6 columns"""
def view_raw_data(wrk_df):
    rowstart=-5
    rowend=0
    validresp=0

    """This while loop accomplishes a few things: 1. It makes sure that the 
    user inputs the proper vaue of (yes/no). 2. It advances the rows to be shown"""
    while validresp==0 and rowend!="end":
        viewdata = input("Would you like to see more raw data (5 rows)? Enter yes or no)? \n").lower()
        if viewdata=="yes":
            validresp=0
            rowstart+=5
            rowend+=5
            print("\n")
            print("-"*100)
            print(wrk_df.iloc[rowstart:rowend,1:])
            print("\n")
            print("-"*100)
        elif viewdata=="no":
            validresp=0
            rowend="end"
        else:
            print("Check your responses!  Only yes or no are valid.")
            validresp=0

"""The main function pulls everything together.  It loops as long as the user
wishes to restart."""              
def main():
    while True:
        city,usermonth,userday = getuserdata()
        wrk_df,int_mon,int_day = create_df(city, usermonth, userday)
        cityname,usr_month,usr_day = usrprint(city,usermonth,userday)
        pop_travel_time(wrk_df,int_mon,int_day,usr_month,usr_day,cityname)
        pop_stations(wrk_df,cityname)
        trip_duration(wrk_df,cityname)
        userinfo(wrk_df,city,cityname)
        view_raw_data(wrk_df)
        
        #Does user wish to restart the program
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
# Simple primary code
main()
        