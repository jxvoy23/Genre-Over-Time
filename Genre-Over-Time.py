import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

movies = pd.read_csv('/Users/j.xvoy/Downloads/title.basics.tsv.gz', sep='\t', low_memory=False)

movies = movies[['primaryTitle', 'startYear', 'genres']]

movies = movies[(movies['startYear'] != '\\N') & (movies['genres'] != '\\N')]

movies['startYear'] = pd.to_numeric(movies['startYear'], errors='coerce')

movies['genres'] = movies['genres'].str.split(',')

movies_exploded = movies.explode('genres') # one row per genre

movies_exploded['decade'] = (movies_exploded['startYear'] // 10) * 10

genre_counts = movies_exploded.groupby(['decade', 'genres']).size().reset_index(name='count')



plt.figure(figsize=(12, 6))
sns.lineplot(data=genre_counts, x='decade', y='count', hue='genres', marker='o')
plt.title('Movie Genre Popularity Over Time')
plt.xlabel('Decade')
plt.ylabel('Number of Movies')
plt.legend(title='Genre', bbox_to_anchor=(1.05, 1))
plt.show()

downloads_path = os.path.expanduser("~/Downloads/genre_counts.csv")
genre_counts.to_csv(downloads_path, index=False)

print(f"CSV file saved to: {downloads_path}")