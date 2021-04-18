del us-counties.csv
del king_latest.csv
curl https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv -o us-counties.csv
curl https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv -o us-states.csv
curl https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv -o us.csv
findstr /i King,Wash us-counties.csv > king_latest.csv
findstr /i Washington us-states.csv > washington_latest.csv
findstr /i Fulton,Geo us-counties.csv > fulton_latest.csv
findstr /i Georgia us-states.csv > georgia_latest.csv


