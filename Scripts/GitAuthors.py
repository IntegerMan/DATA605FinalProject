import pandas as pd

def guess_city(row):
    """
    This code is awful, but guesses a city based on Time Zone. 
    I do this to support a requirement in the project to display data on a map. 
    The data is likely wrong, but it will illustrate that capability for my analysis project
    """
    tz = row['timezone_hours']
    if (tz == 10):
        row['city'] = 'Melbourne'
        row['country'] = 'Australia'
    elif (tz == 8):
        row['city'] = 'Beijing'
        row['country'] = 'China'
    elif (tz == 7):
        row['city'] = 'Bangkok'
        row['country'] = 'Thailand'
    elif (tz == 6):
        row['city'] = 'Dhakar'
        row['country'] = 'Senegal'
    elif (tz == 5):
        row['city'] = 'New Delhi'
        row['country'] = 'India'
    elif (tz == 4):
        row['city'] = 'Abu Dhabi'
        row['country'] = 'United Arab Emirates'
    elif (tz == 3):
        row['city'] = 'Moscow'
        row['country'] = 'Russia'
    elif (tz == 0):
        row['city'] = 'London'
        row['country'] = 'United Kingdom'
    elif (tz == -1):
        row['city'] = 'Praia'
        row['country'] = 'Cape Verde'
    elif (tz == -2):
        row['city'] = 'Nuuk'
        row['country'] = 'Greenland'
    elif (tz == -3):
        row['city'] = 'São Paulo'
        row['country'] = 'Brazil'
    elif (tz == -4):
        row['city'] = 'St. John\'s'
        row['country'] = 'Canada'
    elif (tz == -5):
        row['city'] = 'New York'
        row['state'] = 'NY'
        row['country'] = 'United States'
    elif (tz == -5.3):
        row['city'] = 'Indianapolis'
        row['state'] = 'IN'
        row['country'] = 'United States'
    elif (tz == -6):
        row['city'] = 'Chicago'
        row['state'] = 'IL'
        row['country'] = 'United States'
    elif (tz == -7):
        row['city'] = 'Phoenix'
        row['state'] = 'AZ'
        row['country'] = 'United States'
    elif (tz == -8):
        row['city'] = 'Redmond'
        row['state'] = 'WA'
        row['country'] = 'United States'
    elif (tz == -9):
        row['city'] = 'Anchorage'
        row['state'] = 'AK'
        row['country'] = 'United States'
    elif (tz == -13):
        row['city'] = 'Sydney'
        row['country'] = 'Australia'
    else:
        print('Unknown time zone: ' + tz)
        row['city'] = 'Unknown'
        row['state'] = 'Unknown'
        row['country'] = 'Unknown'
    
    return row


def identify_authors(commits_file_path='Commits.csv', output_file_path='Authors.csv'):
    """
    Builds a dataset of unique authors from all commits in the project
    """
    print('Reading commit data from ' + commits_file_path)
    df = pd.read_csv(commits_file_path)

    # Clean up our data frame to only have columns we care about
    df.rename(columns={'Unnamed: 0': 'ID'}, inplace=True)
    df.drop(columns=['ID','hash','message','author_date', 'committer_date', 'in_main', 'is_merge', 'num_deletes', 'num_inserts', 'net_lines', 'branches', 'files', 'num_files','dmm_unit_size', 'dmm_unit_complexity', 'dmm_unit_interfacing'], inplace=True)

    # Now let's create a set of names, E-Mails, and Time Zones, starting with just the authors
    df_authors = df.drop(columns=['committer_name', 'committer_email', 'committer_tz'])
    df_authors.rename(columns={'author_name': 'name', 'author_email': 'email', 'author_tz': 'timezone'}, inplace=True)

    # Now lets build a different dataset of just committers
    df_committers = df.drop(columns=['author_name', 'author_email', 'author_tz'])
    df_committers.rename(columns={'committer_name': 'name', 'committer_email': 'email', 'committer_tz': 'timezone'}, inplace=True)

    # Now lets merge those two together and drop duplicated rows
    df_unified = pd.concat([df_authors, df_committers])
    df_unified.drop_duplicates(inplace=True)

    # Time Zones in PyDriller are stored as seconds from epoch. Let's convert that to hours
    df_unified['timezone_hours'] = df_unified['timezone'] / (60 * 60)

    # Now let's make up a city for each time zone. This is just for my final project and should be removed afterwards
    df_unified = df_unified.apply(guess_city, axis=1)

    df_unified.to_csv(output_file_path)
    print('Saved author information to ' + output_file_path)
