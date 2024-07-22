import pandas as pd

df = pd.read_csv("ospiti_puntate.csv")
df['Data'] = pd.to_datetime(df['Data'], dayfirst=True)
gender_names = pd.read_csv("names_with_genders.csv")

gender_dict = gender_names.set_index('name')['gender'].to_dict()

def get_gender_list(guest_list, gender_dict):
    names = [name.strip().split()[0].upper() for name in guest_list.split(',')]  # Extract first names
    genders = [gender_dict.get(name, 'Unknown') for name in names]  # Get genders
    return genders

df['GenderList'] = df['ListaOspiti'].apply(lambda x: get_gender_list(x, gender_dict))
df['FemalePercentage'] = df['GenderList'].apply(lambda x: x.count('F')/len(x) if len(x) > 0 else 'na')
df['ListaOspiti'] = df['ListaOspiti'].apply(lambda x : [item.strip() for item in x.split(',')])

each_show_mean = df[['Show','FemalePercentage']].groupby(by='Show').mean().reset_index().rename(columns={'FemalePercentage':'MeanFemalePercentage'}).sort_values(by='MeanFemalePercentage', ascending=True).reset_index()

def most_frequent_guest(df):
    general_presence_count = df.explode('ListaOspiti').groupby('ListaOspiti').agg({'Data':'count'}).reset_index().rename(columns={'Data':'Count'}).sort_values(by='Count', ascending=False)
    return general_presence_count

def most_frequent_guest_per_show(df):
    general_presence_count = df.explode('ListaOspiti').groupby(['Show','ListaOspiti']).agg({'Data':'count'}).reset_index().rename(columns={'Data':'Count'}).sort_values(by=['Show','Count'], ascending=False)
    return general_presence_count

def common_guests(df):
    data = most_frequent_guest_per_show(df)
    pl = set(data[data['Show']=='Propaganda Live'].ListaOspiti)
    oem = set(data[data['Show']=='Otto e Mezzo'].ListaOspiti)
    pp = set(data[data['Show']=='Piazza Pulita'].ListaOspiti)
    dm = set(data[data['Show']=='Di Martedi'].ListaOspiti)
    return pl.intersection(oem).intersection(pp).intersection(dm)


# Plain list of guests (overall) - Count of F percentage
def overall_plain_total_set(df):
    single_guest_overall_count = df.explode(['ListaOspiti','GenderList']).drop_duplicates(subset=['ListaOspiti']).groupby(by='GenderList').agg({'Data':'count'}).reset_index().rename(columns={'Data':'Count'})
    return single_guest_overall_count

def each_show_total_set_of_guests(df):
    single_guest_count_per_show = df.explode(['ListaOspiti','GenderList']).drop_duplicates(subset=['ListaOspiti']).groupby(by=['Show','GenderList']).agg({'Data':'count'}).reset_index().rename(columns={'Data':'Count'})
    return single_guest_count_per_show

most_frequent_guest(df).to_csv("results/general_guests_frequence.csv", index=False)
most_frequent_guest_per_show(df).to_csv("results/per_show_guests_frequence.csv", index=False)
with open('results/common_guests.txt', 'w') as file:
    file.write(str(common_guests(df)))