import streamlit as st
import pandas as pd
import preprocessor,help
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')


df = preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")


# Set a transparent image URL
image_url = "https://upload.wikimedia.org/wikipedia/commons/5/5c/Olympic_rings_without_rims.svg"

# Sidebar image
st.sidebar.markdown(
    f"""
    <div style="text-align: center;">
        <img src="{image_url}" style="max-width: 100%; height: auto;">
    </div>
    """,
    unsafe_allow_html=True,
)


user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal_Tally")
    years,country = help.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select country",country)

    medal_tally = help.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall' :
        st.title("Medal Tally in  " + str(selected_year))
    if selected_year == 'Overall' and selected_country != 'Overall' :
        st.title("Overall Performance of  " + selected_country)
    if selected_year != 'Overall' and selected_country != 'Overall' :
        st.title(selected_country + " Performance in " + str(selected_year)+ " Olympics")
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)


    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time= help.participating_regions_over_time(df)
    fig = px.line(nations_over_time, x="Edition", y="No of Countries")
    st.title('Participating Nations Over The Years ')
    st.plotly_chart(fig)

    events_over_time= help.events_happen_over_time(df)
    fig = px.line(events_over_time, x="Edition", y="Events")
    st.title('Events Over The Years ')
    st.plotly_chart(fig)


    athletes_over_time= help.athlete_part_over_time(df)
    fig = px.line(athletes_over_time, x="Edition", y="Athletes")
    st.title('Athletes Over The Years ')
    st.plotly_chart(fig)

    st.title("No. of Events over time(Every Sport)")
    fig,ax = plt.subplots(figsize=(30,30))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)


    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = help.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    # Get country medal data
    country_df = help.yearwise_medal_tally(df, selected_country)

    # Check if the country has won any medals
    if country_df['Medal'].sum() == 0:
        st.title(f"{selected_country} has not won any medals in the Olympics.")
    else:
        # Medal tally over the years
        fig = px.line(country_df, x="Year", y="Medal")
        st.title(selected_country + " Medal Tally over the years")
        st.plotly_chart(fig)

        # Heatmap for country performance in sports
        st.title(selected_country + " excels in the following sports")
        pt = help.country_event_heatmap(df, selected_country)
        
        # Check if there are any events for heatmap
        if pt.empty:
            st.write(f"No performance data available for {selected_country}.")
        else:
            fig, ax = plt.subplots(figsize=(20, 20))
            ax = sns.heatmap(pt, annot=True)
            st.pyplot(fig)

        # Top 10 athletes
        st.title("Top 10 athletes of " + selected_country)
        top10_df = help.most_successful_countrywise(df, selected_country)

        if top10_df.empty:
            st.write(f"No top athlete data available for {selected_country}.")
        else:
            st.table(top10_df)

if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')


    # Title
    st.title('Height vs Weight Analysis')

    # Select a sport from the dropdown
    selected_sport = st.selectbox('Select a Sport', sport_list)

    # Get the filtered DataFrame for the selected sport
    temp_df = help.weight_v_height(df, selected_sport)

    # Drop rows with missing values in 'Height' or 'Weight'
    temp_df = temp_df.dropna(subset=['Height', 'Weight'])

    # Create the scatter plot
    fig, ax = plt.subplots(figsize=(12, 8))
    ax = sns.scatterplot(
    x='Weight', 
    y='Height', 
    hue='Medal', 
    style='Sex', 
    data=temp_df, 
    s=60,
    palette='viridis'
    )

    # Plot title and labels
    ax.set_title(f'Height vs Weight Analysis for {selected_sport}', fontsize=16)
    ax.set_xlabel('Weight (kg)', fontsize=12)
    ax.set_ylabel('Height (cm)', fontsize=12)
    ax.legend(title='Medal')

    # Display the plot in Streamlit
    st.pyplot(fig)



    st.title("Men Vs Women Participation Over the Years")
    final = help.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)


    




