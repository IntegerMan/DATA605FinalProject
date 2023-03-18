# Analyzing Source Code
Project by Matt Eland (@IntegerMan)

## File Analysis Workflow

1. Clone your repository locally using `git clone` or a Git tool such as GitKraken or GitHub Desktop.
2. Install all requirements needed:
   1. Pandas
   2. PyDriller
   3. os
3. Open `PullData.ipynb`
4. Set `repository_path` equal to the local file path of your git repository. You do not need to specify `.git`, just the local folder. For example: `repository_path = 'C:\\dev\\VisualizingCode'`
5. Run all cells in `PullData.ipynb` this will generate:
   1. `Commits.csv` containing all git commits
   2. `FileCommits.csv` which breaks down commits at a one row per file per commit level
   3. `Authors.csv` containing information on each unique developer in your project.
   4. `FileSizes.csv` containing file statistics for all source files in the current version of your project
   5. `MergedFileData.csv` which joins together `FileCommits.csv` and `FileSizes.csv`

The data should now be ready to import into Tableau, Power BI, or another tool. You can also analyze the data in Python or another programming language