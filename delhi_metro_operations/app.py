import pandas as pd
import datetime as dt
import seaborn as sns
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt

# Streamlit Başlık ve Açıklamalar
st.title('Delhi Metro Operations Optimization')
st.write("""
    Bu uygulama, Delhi Metro rotalarının coğrafi yollarını ve sefer verilerini görselleştiren bir analiz sağlar.
    Ayrıca, veri setindeki farklı bölümleri inceleyebilir ve optimize edebilirsiniz.
""")

# Verileri yükleme
agency = pd.read_csv('delhi_metro_operations/agency.txt')
calendar = pd.read_csv('delhi_metro_operations/calendar.txt')
routes = pd.read_csv('delhi_metro_operations/routes.txt')
shapes = pd.read_csv('delhi_metro_operations/shapes.txt')
stop_times = pd.read_csv('delhi_metro_operations/stop_times.txt')
stops = pd.read_csv('delhi_metro_operations/stops.txt')
trips = pd.read_csv('delhi_metro_operations/trips.txt')

# Delhi Metro Rotalarının Coğrafi Yolları
st.subheader('Geographical Paths of Delhi Metro Routes')
fig, ax = plt.subplots(figsize=(10, 8))
sns.scatterplot(x='shape_pt_lon', y='shape_pt_lat', hue='shape_id', data=shapes, palette='viridis', s=10, legend=None, ax=ax)
ax.set_title('Geographical Paths of Delhi Metro Routes')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.grid(True)

# Grafiği Streamlit sayfasına yerleştir
st.pyplot(fig)

# trips ile calendar'ı birleştirerek gün bilgilerini ekleyin
trips_calendar = pd.merge(trips, calendar, on='service_id', how='left')

# Haftanın her günü için yapılan sefer sayısını hesapla
trip_counts = trips_calendar[['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']].sum()

# Etkileşimli bar grafiği oluştur
fig = px.bar(
    x=trip_counts.index,
    y=trip_counts.values,
    labels={'x': 'Day of the Week', 'y': 'Number of Trips'},
    title='Number of Trips per Day of the Week',
    color=trip_counts.index,
    color_discrete_sequence=px.colors.sequential.Plasma
)

# Grafiği Streamlit uygulamasına yerleştirin
st.title('Delhi Metro Operations')
st.write('Bu grafik, Delhi Metro seferlerinin haftalık dağılımını gösterir.')

# Etkileşimli grafiği Streamlit sayfasında göster
st.plotly_chart(fig)

# Görselleştirme: Durakların coğrafi dağılımını çizme
plt.figure(figsize=(10, 10))
sns.scatterplot(x='stop_lon', y='stop_lat', data=stops, color='red', s=50, marker='o')
plt.title('Geographical Distribution of Delhi Metro Stops')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True)

# Streamlit ile grafiği gösterme
st.title('Delhi Metro Stop Locations')
st.write('Bu grafik, Delhi Metro duraklarının coğrafi dağılımını göstermektedir.')

# Streamlit sayfasında görselleştirmeyi göster
st.pyplot(plt)

# Durakları, stop_times ve trips ile birleştirip, ardından routes ile birleştirerek her durağa ait rotaları ekliyoruz
stops_with_routes = pd.merge(pd.merge(stop_times, trips, on='trip_id'), routes, on='route_id')

# Her durakta kaç farklı rota geçtiğini sayıyoruz
stop_route_counts = stops_with_routes.groupby('stop_id')['route_id'].nunique().reset_index()
stop_route_counts = stop_route_counts.rename(columns={'route_id': 'number_of_routes'})

# Bu veriyi duraklar ile birleştirip, konumları ve isimleri alıyoruz
stop_route_counts = pd.merge(stop_route_counts, stops, on='stop_id')

# Rota sayısına göre durakların coğrafi dağılımını çizme
plt.figure(figsize=(10, 10))
sns.scatterplot(x='stop_lon', y='stop_lat', size='number_of_routes', hue='number_of_routes',
                sizes=(50, 500), alpha=0.5, palette='coolwarm', data=stop_route_counts)
plt.title('Number of Routes per Metro Stop in Delhi')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend(title='Number of Routes')
plt.grid(True)

# Streamlit ile grafiği gösterme
st.title('Delhi Metro Stops and Routes')
st.write('Bu grafik, Delhi Metro duraklarında her bir duraktan geçen rota sayısını göstermektedir.')

# Streamlit sayfasında görselleştirmeyi göster
st.pyplot(plt)

# Streamlit başlık ve açıklamalar
st.title('Delhi Metro Trip Intervals Analysis')
st.write("""
Bu analizde, Delhi Metro'nun duraklarındaki trenlerin varış zamanları arasındaki farklar hesaplanarak, 
günün farklı saat dilimlerinde ortalama varış aralıkları belirlenmiştir. 
Aşağıdaki adımlar, zaman aralıklarının nasıl hesaplandığını ve analiz edildiğini göstermektedir.
""")

# 1. Adım: Varış Zamanlarını datetime.time formatına dönüştürme
# Bu adım, zaman verilerinin işlenebilmesi için doğru formata dönüştürülmesini sağlar
def convert_to_time(time_str):
    try:
        return dt.datetime.strptime(time_str, '%H:%M:%S').time()
    except ValueError:
        # Eğer saat 24:00:00 veya 25:00:00 gibi geçersiz bir zaman varsa, bunu düzeltmek için
        hour, minute, second = map(int, time_str.split(':'))
        return dt.time(hour % 24, minute, second)

stop_times['arrival_time_dt'] = stop_times['arrival_time'].apply(convert_to_time)
st.write("**1. Adım:** Varış zamanlarını zaman formatına dönüştürdük.")

# 2. Adım: Ardışık varış zamanları arasındaki farkları hesaplama
stop_times_sorted = stop_times.sort_values(by=['stop_id', 'arrival_time_dt'])
stop_times_sorted['next_arrival_time'] = stop_times_sorted.groupby('stop_id')['arrival_time_dt'].shift(-1)

# 3. Adım: İki zaman arasındaki farkı dakika cinsinden hesaplama
def time_difference(time1, time2):
    if pd.isna(time1) or pd.isna(time2):
        return None
    full_date_time1 = dt.datetime.combine(dt.date.today(), time1)
    full_date_time2 = dt.datetime.combine(dt.date.today(), time2)
    return (full_date_time2 - full_date_time1).seconds / 60

stop_times_sorted['interval_minutes'] = stop_times_sorted.apply(lambda row: time_difference(row['arrival_time_dt'], row['next_arrival_time']), axis=1)
st.write("**2. Adım:** Her durak için ardışık trenler arasındaki zaman farkını hesapladık.")

# 4. Adım: Zaman farklarındaki NaN değerlerini (son tren) kaldırma
stop_times_intervals = stop_times_sorted.dropna(subset=['interval_minutes'])

# 5. Adım: Günün saat dilimlerine göre ortalama interval hesaplama
def part_of_day(time):
    if time < dt.time(12, 0):
        return 'Morning'
    elif time < dt.time(17, 0):
        return 'Afternoon'
    else:
        return 'Evening'

stop_times_intervals['part_of_day'] = stop_times_intervals['arrival_time_dt'].apply(part_of_day)
average_intervals = stop_times_intervals.groupby('part_of_day')['interval_minutes'].mean().reset_index()
st.write("**3. Adım:** Günün farklı saat dilimlerinde (Sabah, Öğle, Akşam) ortalama varış aralıklarını hesapladık.")

# 6. Adım: Günün saat dilimlerine göre ortalama varış aralıklarını görselleştirme
plt.figure(figsize=(8, 6))
sns.barplot(x='part_of_day', y='interval_minutes', data=average_intervals, order=['Morning', 'Afternoon', 'Evening'], palette='mako')
plt.title('Average Interval Between Trips by Part of Day')
plt.xlabel('Part of Day')
plt.ylabel('Average Interval (minutes)')
plt.grid(True)

# Streamlit görselleştirmeyi sayfada gösterme
st.pyplot(plt)

# Grafik açıklaması
st.write("""
Grafikte, Delhi Metro'nun sabah, öğle ve akşam saat dilimlerinde ortalama varış aralıkları gösterilmektedir. 
Bu sayede, her bir saat dilimindeki tren yoğunluğu ve aralıklarının anlaşılması hedeflenmiştir. 
Veriler, trenler arasındaki ortalama süreyi ve günün farklı saatlerindeki hareketliliği gösterir.
""")

# Streamlit başlık ve açıklamalar
st.title('Delhi Metro Trip Count by Time Interval')
st.write("""
Bu analizde, Delhi Metro'sundaki tren seferlerinin zaman dilimlerine göre nasıl dağıldığını inceleyeceğiz.
Zaman dilimleri: 
- **Early Morning**: 00:00 - 06:00
- **Morning Peak**: 06:00 - 10:00
- **Midday**: 10:00 - 16:00
- **Evening Peak**: 16:00 - 20:00
- **Late Evening**: 20:00 - 00:00
Aşağıdaki grafik, her zaman diliminde kaç sefer yapıldığını göstermektedir.
""")

# 1. Adım: Zaman dilimlerini sınıflandırmak
# Bu fonksiyon, her bir trenin varış saatine göre zaman dilimlerini belirler.
def classify_time_interval(time):
    if time < dt.time(6, 0):
        return 'Early Morning'
    elif time < dt.time(10, 0):
        return 'Morning Peak'
    elif time < dt.time(16, 0):
        return 'Midday'
    elif time < dt.time(20, 0):
        return 'Evening Peak'
    else:
        return 'Late Evening'

# Zaman dilimi sınıflandırmasını her varış zamanı için uygula
stop_times['time_interval'] = stop_times['arrival_time_dt'].apply(classify_time_interval)
st.write("**1. Adım:** Her varış zamanına göre zaman dilimi sınıflandırmasını yaptık.")

# 2. Adım: Zaman dilimlerine göre tren seferlerinin sayısını hesaplamak
# Bu adım, her zaman dilimindeki benzersiz seferlerin sayısını hesaplar
trips_per_interval = stop_times.groupby('time_interval')['trip_id'].nunique().reset_index()
trips_per_interval = trips_per_interval.rename(columns={'trip_id': 'number_of_trips'})
st.write("**2. Adım:** Her zaman diliminde yapılan tren seferlerinin sayısını hesapladık.")

# 3. Adım: Zaman dilimlerini sıralamak
# Zaman dilimlerini mantıklı bir sıralama için kategorik olarak sıralıyoruz
ordered_intervals = ['Early Morning', 'Morning Peak', 'Midday', 'Evening Peak', 'Late Evening']
trips_per_interval['time_interval'] = pd.Categorical(trips_per_interval['time_interval'], categories=ordered_intervals, ordered=True)
trips_per_interval = trips_per_interval.sort_values('time_interval')
st.write("**3. Adım:** Zaman dilimlerini doğru sırayla sıraladık.")

# 4. Adım: Zaman dilimlerine göre tren seferlerinin sayısını görselleştirme
plt.figure(figsize=(10, 6))
sns.barplot(x='time_interval', y='number_of_trips', data=trips_per_interval, palette='Set2')
plt.title('Number of Trips per Time Interval')
plt.xlabel('Time Interval')
plt.ylabel('Number of Trips')

# Grafik üstüne açıklama ekleme
for p in plt.gca().patches:
    plt.gca().annotate(f'{p.get_height():,.0f}',
                       (p.get_x() + p.get_width() / 2., p.get_height()),
                       ha='center', va='center',
                       fontsize=12, color='black',
                       xytext=(0, 8), textcoords='offset points')

plt.grid(True)

# Streamlit görselleştirmeyi sayfada gösterme
st.pyplot(plt)

# Grafik açıklaması
st.write("""
Grafikte, Delhi Metro'sundaki tren seferlerinin günün farklı saat dilimlerinde nasıl dağıldığı gösterilmektedir. 
**Sabah yoğunluğu** en fazla seferin yapıldığı zaman dilimidir. **Gece** ise daha az sayıda seferin yapıldığı bir dilimdir.
""")

# Streamlit başlık ve açıklamalar
st.title('Delhi Metro Trip Count Optimization by Time Interval')
st.write("""
Bu analizde, Delhi Metro'daki tren seferlerinin zaman dilimlerine göre nasıl optimize edileceğini göreceğiz.
Zaman dilimlerini optimize ederek, her bir dilimde daha verimli bir sefer planı oluşturacağız.
""")

# 1. Adım: Zaman dilimlerini sınıflandırmak
def classify_time_interval(time):
    if time < dt.time(6, 0):
        return 'Early Morning'
    elif time < dt.time(10, 0):
        return 'Morning Peak'
    elif time < dt.time(16, 0):
        return 'Midday'
    elif time < dt.time(20, 0):
        return 'Evening Peak'
    else:
        return 'Late Evening'

# Zaman dilimi sınıflandırmasını her varış zamanı için uygula
stop_times['time_interval'] = stop_times['arrival_time_dt'].apply(classify_time_interval)
st.write("**1. Adım:** Zaman dilimlerini sınıflandırdık.")

# 2. Adım: Zaman dilimlerine göre tren seferlerinin sayısını hesaplamak
trips_per_interval = stop_times.groupby('time_interval')['trip_id'].nunique().reset_index()
trips_per_interval = trips_per_interval.rename(columns={'trip_id': 'number_of_trips'})
st.write("**2. Adım:** Zaman dilimlerine göre tren seferlerinin sayısını hesapladık.")

# 3. Adım: Zaman dilimlerinde yapılan sefer sayısını optimize etmek
adjustment_factors = {'Morning Peak': 1.20, 'Evening Peak': 1.20, 'Midday': 0.90, 'Early Morning': 1.0, 'Late Evening': 0.90}

# Ayarlamaları uygulamak
adjusted_trips_per_interval = trips_per_interval.copy()
adjusted_trips_per_interval['adjusted_number_of_trips'] = adjusted_trips_per_interval.apply(
    lambda row: int(row['number_of_trips'] * adjustment_factors[row['time_interval']]), axis=1)
st.write("**3. Adım:** Zaman dilimlerine göre yapılan sefer sayılarının optimizasyonunu gerçekleştirdik.")

# 4. Adım: Orijinal ve optimize edilmiş sefer sayılarının karşılaştırılması
plt.figure(figsize=(12, 6))
bar_width = 0.35
r1 = range(len(adjusted_trips_per_interval))
r2 = [x + bar_width for x in r1]

plt.bar(r1, adjusted_trips_per_interval['number_of_trips'], color='blue', width=bar_width, edgecolor='grey', label='Original')
plt.bar(r2, adjusted_trips_per_interval['adjusted_number_of_trips'], color='cyan', width=bar_width, edgecolor='grey', label='Adjusted')

plt.xlabel('Time Interval', fontweight='bold')
plt.ylabel('Number of Trips', fontweight='bold')
plt.xticks([r + bar_width/2 for r in range(len(adjusted_trips_per_interval))], adjusted_trips_per_interval['time_interval'])
plt.title('Original vs Adjusted Number of Trips per Time Interval')
plt.legend()

# Grafik gösterimi
st.pyplot(plt)

# Grafik açıklaması
st.write("""
Grafikte, orijinal tren sefer sayıları ile optimizasyon sonrası tren sefer sayıları karşılaştırılmaktadır. 
**Morning Peak** ve **Evening Peak** saatlerinde sefer sayıları %20 artırıldı. **Midday** ve **Late Evening** saatlerinde ise %10 azaltma yapıldı.
Bu optimizasyon, tren yoğunluğunun doğru zaman dilimlerinde daha verimli dağıtılmasını sağlamaktadır.
""")
