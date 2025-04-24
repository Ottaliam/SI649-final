import altair as alt
import pandas as pd

# Configure Altair to save as PNG (requires selenium and chrome/chromedriver)
# alt.renderers.enable('png')
alt.data_transformers.disable_max_rows()

# Read the data
data = pd.read_csv("dataset.csv")

# Process the release year
data['release_year'] = data['release_date'].str.split('-').str[0].astype(int)
data = data[data['release_year'] != 0]

# Define chart dimensions for consistency
chart_width = 800
chart_height = 500

# Create and save charts for each year
for year in range(2000, 2021):
    chart = alt.Chart(data).transform_filter(
        alt.datum.release_year == year
    ).transform_aggregate(
        count='count()',
        groupby=['track_genre']
    ).transform_window(
        rank='rank(count)',
        sort=[alt.SortField('count', order='descending')]
    ).transform_filter(
        alt.datum.rank <= 10
    ).mark_bar().encode(
        y=alt.Y("track_genre:N", sort="-x"),
        x=alt.X("count:Q"),
        color=alt.Color("track_genre:N", scale=alt.Scale(scheme="dark2"))
    ).properties(
        width=chart_width,
        height=chart_height,
    )
    
    # Save the chart as PNG
    chart.save(f"../../public/chart_{year}.png")