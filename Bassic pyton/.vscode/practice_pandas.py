# #pandas is mainly divided into two parts: Series and DataFrame. 
# # A Series is a one-dimensional labeled array capable of holding any data type, 
# # while a DataFrame is a two-dimensional labeled data structure with columns of potentially different types.

# #Series using list
from matplotlib.pyplot import plot
from pandas import *
# countrys = ['USA', 'Canada', 'Germany', 'UK', 'France']
# print(Series(countrys))

# runs=[100, 200, 300, 400, 500]
# print(Series(runs))

# #custom index
# marks=[90, 80, 70, 60, 50]
# Subjects=['Maths', 'Science', 'English', 'History', 'Geography']
# print(Series(marks, index=Subjects))

# #setting name
# print(Series(marks, index=Subjects, name="Student Marks"))

# #series using dictionary
marks={
    'Maths': 90,
    'Science': 80,
    'English': 70,
    'History': 60,
    'Geography': 50
}
marks_series=Series(marks, name="Student ke Marks")
marks_series

# #Sreies attribute
# a=marks_series.size
# print("Size of series:", a)
# b=marks_series.dtype
# print("Data type of series:", b)
# c=marks_series.name
# print("Name of series:", c)
# d=marks_series.is_unique
# print("Is series unique:", d)
# e=marks_series.index
# print("Index of series:", e)
# f=marks_series.values
# print("Values of series:", f)

#Series methods
from pandas import read_csv


# ab=read_csv("C:\\Users\\asus\\OneDrive\\Desktop\\Python_project\\Bassic pyton\\.vscode\\city_loc.csv")
# print(type(ab))
#to convert dataframe to series we can use squeeze() method
from numpy import *
city=read_csv("C:\\Users\\asus\\OneDrive\\Desktop\\Python_project\\Bassic pyton\\.vscode\\city_loc.csv").squeeze("columns")
# print(city)     #squeeze can't convert this into sequence as their are more than 1 columns
# print(city.head()) #top 5
# print(city.tail()) #bottom 5
#print(city.sample(5)) #random 5
#print(city.count())
#print(city.sort_values(by='Year', ascending=False).head().values[0])
#sort is temporary change
#when inplace = true is used then permenent change
#print(city.sort_values(by='Year', ascending=False, inplace=True))
#print(city.sort_index(ascending=True).head().values[0])
# print(city['latitude'].mean()) 
# print(city['latitude'].median())
# print(city['latitude'].mode())
# print(city['latitude'].std())
# print(city['latitude'].var())
# print(city['latitude'].min())
# print(city['latitude'].max())
# print(city['latitude'].sum())
# print(city['latitude'].product())
#print(city['latitude'].describe())

#INDEXING AND SLICING
#print(city['latitude'][0]) #indexing
#indexing in -1 only works for string
#print(city['latitude'][0:4]) #slicing
#print(city['latitude'][-4:]) #negative slicing

#Editing series
# marks_series["Maths"]=100
# print(marks_series)
# marks_series["SST"]=90
# print(marks_series)
# #Editing can be done through slicing
# marks_series[0:3]=100, 200, 300
# print(marks_series)

# #series with python fuctionality(len/sum/min/max/dir/type)
# print(len(marks_series))
# print(dict(marks_series))
# print(sum(marks_series))
# print(min(marks_series))
# #membership operator 
# print("Maths" in marks_series)  #default it works on indexes
# print(50 in marks_series.values)  #.values to check in values
# for i in marks_series:
#     print(i)  #it will print values of series
# for i in marks_series.index:
#     print(i)  #it will print index of series
# print(marks_series > 60)  #it will return boolean series
# print(100- marks_series)  #it will return series with values subtracted from 100

#Boolean indexing and filtering
# print(city[city['latitude'] > 50].size)  #it will return series with values greater than 30
# print(marks_series[marks_series > 60].size)  #it will return series with values greater than 60

#Graph plotting 
# from matplotlib import pyplot as plt
# plt.plot(city['latitude'], city['longitude'])
# plt.xlabel('Latitude')
# plt.ylabel('Longitude')
# plt.title('City Locations')
# plt.grid(True)
# plt.show()


## Data Frame ##
movies = read_csv(r"C:\Users\asus\OneDrive\Desktop\Python_project\Bassic pyton\.vscode\movies.csv")
ipl = read_csv(r"C:\Users\asus\OneDrive\Desktop\Python_project\Bassic pyton\.vscode\ipl-matches - ipl-matches.csv")

#dataframe using list 
# student_data=[
#     [100,80,10],
#     [90,70,7],
#     [120,100,14],
#     [80,50,2]
# ]
# ds=DataFrame(student_data,columns=['iq','marks','package'])
# print(ds)

#dataframe using dictionary
# student_dict={
#     'iq':[100,90,120,80],
#     'marks':[80,70,100,50],
#     'package':[10,7,14,2]
# }
# ds=DataFrame(student_dict)
# print(ds)

#Dataframe Attributes and Methods
# print(movies.shape)
# print(ipl.shape)
# print(movies.dtypes)
# print(ipl.dtypes)
# print(movies.index)
# print(movies.columns)
# print(movies.values)
# print(movies.head())
# print(movies.tail())
# print(movies.sample(5))
# print(movies.info())
# print(movies.describe())
# print(movies.isnull().sum())
# print(movies.count())
print(movies.duplicated().sum())
#print(movies.drop_duplicates())
#print(movies.rename(columns={'Title':'Movie Title'}))






