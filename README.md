# Disney Baby
![The Most Trendy Baby Names Inspired by Disney characters in US History](http://i.imgur.com/YFjPNVV.png)

## Research Question
**Mass Media and Its influence on society**
Is there a relationship between Disney character’s Name and the frequency of babies’ names?

### The Topic of Visualization
The top trendy Disney character’s name used in babies’ name before and after the film was produced.

## Datasets

### Datasets  1: Disney Films & Characters Lists
##### Data Source
- Source: IMDb website
- Content:  A list “Walt Disney Animation Studios Feature Films” collected by IMDb users.
- Format: HTML

##### Data Collection
- Python package
  - Urllib2 & BeautifulSoup
- Parse HTML
  - Film Title/Url
  - Year
  - Rank
  - Character


### Datasets  2: The Number of Babies’ Name in US History
##### Data Source
- Source: The Social Security Administration
- Content: The numbers of given names in U.S. births (has SSN) 
  - 1923-2015
  - Privacy: 5+ occurrences
- Format: 
 - 93 files in txt format. ```name,sex,number```

##### Data Collection
- Direct download from SSA website
- Python: 
    - For loop to open the files
    - Get the required data
    - Save it as json


## Manipulation methods

**STEP 1.** Crawl_disney_char > json

``` javascript
[{"Year": "1937", "Character": "Doc", "Rank": "7.6", "Movie URL": "http://www.imdb.com/title/tt0029583/", "Title": "Snow White and the Seven Dwarfs"}]
```

**STEP 2.** Baby’s name & Disney Character > json

``` javascript
[{"Count": "71633", "Name": ["Mary", "F"], "Year": 1923}]
```

**STEP 3.** Find top N name in history by sum of name’s count > json

``` javascript
[{"Sum": 4531485, "Name": ["James", "M"]},  {"Sum": 3037975, "Name": ["Mary", "F"]}]
```

**STEP 4.** Generate “name counts” from 1923-2015 on number of occurrences in descending order for top N name > csv

``` 
Name, Gender, BornYear, Count
James,M,1923,50466
James,M,1924,52939
```

**STEP 5.** Generate “name_movie mapping” > csv 

``` 
Name,Movie Title,Year
Travis,The Princess and the Frog,2009
Louis,The Little Mermaid,1989
Louis,The Princess and the Frog,2009
``` 

**STEP 6.** Use “ploy.ly” python package to visualize a line chart for each top N name

## Data Visualization
![The Most Trendy Baby Names Inspired by Disney characters in US History](http://i.imgur.com/YFjPNVV.png)

##### Top 20 Disney Baby 
- X: year; Y: Counts of name
- Circle: The year of films released, hover to see the title of movie and its IMDb rank
- Color
    - Red: Female's Name
    - Blue: Male's Name

## Known Issues
- "5. Larry" circle has a bug of its position.
- Inconsistent data in IMDb user-generated character list.

## Next Step
Use popular film’s main characters to do further exploration.
