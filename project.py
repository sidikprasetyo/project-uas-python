# Import library
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

# CSS
st.markdown(
    """
    <style>
        .sidebar-img {
            max-width: 175px;
            display: block;
            margin-left: 0px;
            margin-top: -75px;
            margin-bottom: 20px;
        }
        .sidebar .sidebar-content {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .title-sidebar {
            margin-top: -65px;
            margin-bottom: 50px;
        }
        div.stButton > button:first-child {
            padding: 5px 10px;
            text-align: left;
            text-decoration: none;
            display: inline-block;
            font-size: 15px;
            margin: 0px 0px;
            border-radius: 6px;
            width: 100%;
        }
    </style>
""",
    unsafe_allow_html=True
)

# Logo pada sidebar
st.sidebar.markdown(
    """
    <div style='display: flex; justify-content: center;'>
        <img class='sidebar-img' src='https://gss-technology.com/wp-content/uploads/2021/07/01-1-768x768.png' />
    </div>
    """,
    unsafe_allow_html=True
)

# Title pada sidebar
st.sidebar.markdown("<h1 class='title-sidebar' style='text-align: center;'>Project Python</h1>", unsafe_allow_html=True)

# Menu sidebar
if 'selected_option' not in st.session_state:
    st.session_state.selected_option = 'op1'

if st.sidebar.button('Dashboard', key='op1'):
    st.session_state.selected_option = 'op1'

if st.sidebar.button('Best Selling Manga', key='op2'):
    st.session_state.selected_option = 'op2'

if st.sidebar.button('Populasi Dunia', key='op3'):
    st.session_state.selected_option = 'op3'

if st.sidebar.button('Rice Production Indonesia', key='op4'):
    st.session_state.selected_option = 'op4'
    
# Garis dibawah menu sidebar
st.sidebar.markdown("<hr style='margin-top: 5px; margin-bottom: 5px;'>", unsafe_allow_html=True)

# Inti dari menu sidebar
if st.session_state.selected_option == 'op1':

    # Isi Menu Dashboard
    st.markdown("<h1 style='text-align: center;'>Project Ujian Akhir Semester Pemrograman Python</h1>", unsafe_allow_html=True)
    st.markdown("<h2>Anggota Kelompok</h2>", unsafe_allow_html=True)
    st.write('1. Azkha Brilliant Firdaus (210103126)\n2. Christian Imanuel Munaiseche (210103128)\n3. Sidik Prasetyo (210103142)\n4. Vincensius Gilang Pramudito (210103144)')

elif st.session_state.selected_option == 'op2':

    # Isi Menu Best Selling Manga
    st.sidebar.markdown('### Best Selling Manga')

    # Menu dropdown
    option_bar = st.sidebar.selectbox('Pilih Opsi',('Data Frame', 'Visualisasi'), index=0 if 'should_default_op2' not in st.session_state else 1)

    if 'should_default_op2' not in st.session_state:
        st.session_state.should_default_op2 = True

    # Membaca dataset CSV
    df1 = pd.read_csv('best-selling-manga.csv')

    if option_bar == 'Data Frame':
        st.session_state.should_default_op2 = False
        # Menampilkan data frame dari dataset
        st.markdown("<h2 align='center'>Data Frame Dataset Best Selling Manga</h2>", unsafe_allow_html=True)
        st.dataframe(df1)

        # Menampilkan ringkasan dataset
        st.markdown("<h2 align='center'>Ringkasan Dataset Best Selling Manga</h2>", unsafe_allow_html=True)
        st.dataframe(df1.describe())

    elif option_bar == 'Visualisasi':
        st.markdown("<h2 align='center'>Visualisasi Dataset Best Selling Manga</h2>", unsafe_allow_html=True)

        # Menghitung jumlah manga series berdasarkan publisher
        publisher_manga_series = df1.groupby('Publisher')['Manga series'].count().reset_index()

        # Menampilkan bar chart publisher dan jumlah manga series
        fig1 = px.bar(publisher_manga_series, x='Publisher', y='Manga series', title="Manga Series by Publisher", range_y=[0, max(publisher_manga_series['Manga series']) * 1.2] ,text='Manga series')

        # Menampilkan chart di Streamlit
        st.plotly_chart(fig1, use_container_width=True)

        # menampilkan total jumlah manga series dan jumlah publisher
        total_manga = publisher_manga_series['Manga series'].sum()
        total_publisher = publisher_manga_series.shape[0]
        col1, col2 = st.columns([1, 1])
        with col1:
            st.write("Jumlah Manga Series")
            st.write(f"{total_manga}")

        with col2:
            st.write("Jumlah Publisher")
            st.write(f"{total_publisher}")


        # Menghitung jumlah author berdasarkan demographic
        author_demographic = df1.groupby('Demographic')['Author(s)'].count().reset_index()

        # Menampilkan pie chart demographic dan jumlah author
        fig2 = px.pie(author_demographic, values='Author(s)', names='Demographic', title='Persentase Author per Demographic')

        # Menampilkan chart di Streamlit
        st.plotly_chart(fig2, use_container_width=True)


        # Membuat grafik scatter plot
        fig3 = px.scatter(df1, x='No. of collected volumes', y='Approximate sales in million(s)', color='Demographic',
                        title='Collected Volumes and Approximate Sales by Demographic',
                        labels={'No. of collected volumes': 'Number of Collected Volumes', 'Approximate sales in million(s)': 'Approximate Sales in million'})

        # Menampilkan grafik di Streamlit
        st.plotly_chart(fig3, use_container_width=True)


        # Membuat grafik rata-rata penjualan berdasarkan publisher
        fig4 = go.Figure()

        publishers = df1['Publisher'].unique()

        for publisher in publishers:
            df_temp = df1[df1['Publisher'] == publisher]
            fig4.add_trace(go.Scatter(x=df_temp.index, y=df_temp['Average sales per volume in million(s)'],
                                    mode='lines', name=publisher))

        # Menambahkan judul dan label sumbu
        fig4.update_layout(title='Average Sales per Volume by Publisher',
                        xaxis_title='Index',
                        yaxis_title='Average Sales per Volume in million')

        # Menampilkan stacked line chart di Streamlit
        st.plotly_chart(fig4, use_container_width=True)

        # Membuat box plot
        fig5 = px.box(df1, x='Demographic', y='Average sales per volume in million(s)', 
                    title='Average Sales per Volume berdasarkan Demographic',
                    labels={'Average sales per volume in million(s)': 'Average Sales per Volume'})

        # Menampilkan box plot di Streamlit
        st.plotly_chart(fig5, use_container_width=True)

elif st.session_state.selected_option == 'op3':

    # Isi menu Populasi Dunia
    st.sidebar.markdown('### Populasi Dunia')

    # Menu dropdown
    option_bar = st.sidebar.selectbox('Pilih Opsi',('Data Frame', 'Visualisasi'), index=0 if 'should_default_op3' not in st.session_state else 1)

    if 'should_default_op3' not in st.session_state:
        st.session_state.should_default_op3 = True

    # Membaca dataset CSV
    df2 = pd.read_csv('Dataset_populasi_dunia.csv')

    if option_bar == 'Data Frame':
        st.session_state.should_default_op3 = False

        # Menampilkan data frame dari dataset
        st.markdown("<h2 align='center'>Data Frame Dataset Populasi Dunia</h2>", unsafe_allow_html=True)
        st.dataframe(df2)

        # Menampilkan ringkasan dataset
        st.markdown("<h2 align='center'>Ringkasan Dataset Populasi Dunia</h2>", unsafe_allow_html=True)
        st.dataframe(df2.describe())

    elif option_bar == 'Visualisasi':
        st.markdown("<h2 align='center'>Visualisasi Dataset Populasi Dunia</h2>", unsafe_allow_html=True)

        # Membuat peta choropleth
        fig6 = px.choropleth(df2, locations='Country Name', locationmode='country names', color='Population',
                            title='Choropleth Map of Population by Country',
                            color_continuous_scale=px.colors.sequential.Plasma)

        # Menampilkan peta choropleth di Streamlit
        st.plotly_chart(fig6, use_container_width=True)


        # Membuat area chart land area vs. water area
        fig7 = go.Figure()

        fig7.add_trace(go.Scatter(x=df2['Country Name'], y=df2['Land Area'], mode='lines', name='Land Area'))
        fig7.add_trace(go.Scatter(x=df2['Country Name'], y=df2['Water Area'], mode='lines', name='Water Area'))

        # Update layout
        fig7.update_layout(title='Comparison Land Area and Water Area by Country', xaxis_title='Country Name', yaxis_title='Area')

        # Menampilkan area chart di Streamlit
        st.plotly_chart(fig7, use_container_width=True)


        # Membuat histogram laju kelahiran dan kematian
        st.write("<h3>Distribution of Birth Rate and Death Rate</h3>", unsafe_allow_html=True)

        # Membersihkan DataFrame dari nilai yang hilang
        df2 = df2.dropna()

        # Membuat histogram distribusi laju kelahiran (birth rate) dan laju kematian (death rate)
        fig8 = ff.create_distplot([df2['Birth Rate'], df2['Death Rate']], ['Birth Rate', 'Death Rate'],  bin_size=2)

        # Menampilkan histogram di Streamlit
        st.plotly_chart(fig8, use_container_width=True)

elif st.session_state.selected_option == 'op4':

    # Isi menu Rice Production Indonesia
    st.sidebar.markdown('### Rice Production Indonesia')

    # Menu dropdown
    option_bar = st.sidebar.selectbox('Pilih Opsi',('Data Frame', 'Visualisasi'), index=0 if 'should_default_op4' not in st.session_state else 1)

    if 'should_default_op4' not in st.session_state:
        st.session_state.should_default_op4 = True

    # Membaca dataset CSV
    df3 = pd.read_csv('Rice Production Indonesia 2020-2022.csv')

    if option_bar == 'Data Frame':
        st.session_state.should_default_op4 = False
        # Menampilkan data frame dari dataset
        st.markdown("<h2 align='center'>Data Frame Rice Production Indonesia 2020-2022</h2>", unsafe_allow_html=True)
        st.dataframe(df3)

        # Menampilkan ringkasan dataset
        st.markdown("<h2 align='center'>Ringkasan Dataset Rice Production Indonesia 2020-2022</h2>", unsafe_allow_html=True)
        st.dataframe(df3.describe())

    elif option_bar == 'Visualisasi':
        st.markdown("<h2 align='center'>Visualisasi Dataset Rice Production Indonesia 2020-2022</h2>", unsafe_allow_html=True)
        # Membuat time series line chart produksi berdasarkan tahun
        fig9 = px.line(df3, x='Year', y='Production.(ton)', color='Provinsi', title='Production Over Time by Province',
                    labels={'Year': 'Year', 'Production.(ton)': 'Production'})

        # Membuat time series line chart produktivitas berdasarkan tahun
        fig10 = px.line(df3, x='Year', y='Productivity(kw/ha)', color='Provinsi', title='Productivity Over Time by Province',
                    labels={'Year': 'Year', 'Productivity(kw/ha)': 'Productivity'})

        # Menampilkan time series line chart di Streamlit
        st.plotly_chart(fig9, use_container_width=True)
        st.plotly_chart(fig10, use_container_width=True)


        # Membuat scatter plot hubungan antara yield area dan produksi pertanian
        fig11 = px.scatter(df3, x='Yield.Areal(ha)', y='Production.(ton)', color='Provinsi', title='Yield Area vs. Production by Province',
                        labels={'Yield.Areal(ha)': 'Yield Area (ha)', 'Production.(ton)': 'Production (ton)'})

        # Menampilkan scatter plot di Streamlit
        st.plotly_chart(fig11, use_container_width=True)