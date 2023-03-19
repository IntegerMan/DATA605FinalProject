import pandas as pd

def generate_merged_file_data(file_commits_path = 'FileCommits.csv', 
                              file_size_data_path='FileSizes.csv', 
                              output_file = 'MergedFileData.csv'):
    """
    Joins together file commit data and file size data into a single dataset and writes it to a CSV file
    """
    print('Loading file commit data from ' + file_commits_path)
    df_file_commits = pd.read_csv(file_commits_path)

    # Fix the junk column to be an ID
    df_file_commits.rename(columns={'Unnamed: 0': 'File_Commit_ID'}, inplace=True)

    # Because our test data was cloned to a temp directory as part of PyDriller, let's substitute it with the correct local path
    df_file_commits['relative_path'] = df_file_commits['new_path']

    # Replace NaN values with '' for readability
    df_file_commits.fillna('', inplace=True)

    print('Loading file size data from ' + file_size_data_path)
    df_files = pd.read_csv(file_size_data_path)

    # Pandas guesses at ID column names. Make the name make sense
    df_files.rename(columns={'Unnamed: 0': 'File_ID'}, inplace=True)

    # Replace '.' values (root directory) with '' instead
    df_files.replace({'path': {'.': ''}}, inplace=True)

    # These columns provide no additional information and muddy comparisons later
    df_files.drop(columns=['root', 'fullpath'], inplace=True) 

    # Create a new data frame by joining together the other two on their relative paths
    df_merged = pd.merge(df_file_commits, df_files, left_on='relative_path', right_on='relative_path')

    # Remove not needed and consolidate duplicated columns
    df_merged.drop(columns=['File_Commit_ID', 'File_ID', 'filename_x'], inplace=True)
    df_merged.rename(columns={'filename_y': 'filename'}, inplace=True)

    # Save the resulting dataset to disk
    df_merged.to_csv(output_file)
    print('Merged file data created in ' + output_file)


# Sample code to start working on propagating renames
# import pandas as pd

# df = pd.read_csv(file_commit_data_path)
# df.rename(columns={'Unnamed: 0': 'File_Commit_ID'}, inplace=True)

# df.sort_values(by=['author_date'], ascending=False, inplace=True)

# df_hasOld = df[~df['old_path'].isna()]
# df_changed = df_hasOld.loc[df['new_path'].ne(df['old_path'])]
# df_renames = df_changed.drop(columns=['message', 'File_Commit_ID', 'author_name', 'author_email', 'author_country', 'author_city', 'num_deletes', 'num_inserts', 'net_lines', 'project_name', 'project_path', 'filename'])
# df_renames.head()
# #df.to_csv(file_commits_file_path)

# def propagate_rename(row):
#     date = row['author_date']
#     file = row['new_path']
#     return row

# df = df.apply(propagate_rename, axis=1)
# df.head()