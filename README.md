![Uploading image.png…]()


[TR]

# Delhi Metro Operations Optimization 🚇

## 📚 Genel Bakış

Bu Streamlit uygulaması, **Delhi Metro** verilerini görselleştirerek rotaların coğrafi yollarını, durakların dağılımını ve sefer yoğunluklarını analiz etmektedir. Uygulama, kullanıcıların metro sistemi hakkında daha iyi bir anlayış geliştirmelerine yardımcı olurken, aynı zamanda metronun çeşitli bölümleri ve çalışma saatleri hakkında da değerli bilgiler sunar.

## 🛠️ Kullanılan Kütüphaneler

- `pandas`: Veri işleme ve analizi için.
- `datetime`: Zaman hesaplamaları için.
- `seaborn`: Veri görselleştirmeleri için.
- `streamlit`: Etkileşimli web uygulaması için.
- `plotly`: Etkileşimli grafikler için.
- `matplotlib`: Veri görselleştirmeleri için.

## 🌍 Özellikler

- **Delhi Metro Rotalarının Coğrafi Yolları**: Metro rotalarının coğrafi yol haritalarını görselleştirir.
- **Sefer Dağılımı**: Haftanın her günü yapılan tren seferlerinin sayısını görselleştirir.
- **Duraklar ve Rotalar**: Her metro durağında kaç farklı rota geçtiğini gösterir.
- **Varış Zamanları Arasındaki Farklar**: Farklı zaman dilimlerinde ortalama varış aralıklarını hesaplar.
- **Zaman Dilimleri Analizi**: Delhi Metro'daki tren seferlerinin farklı zaman dilimlerine göre nasıl dağıldığını analiz eder.

## 🔧 Nasıl Kullanılır?

1. **Gerekli Veri Dosyalarını Yükleyin**: 
   - `agency.txt`, `calendar.txt`, `routes.txt`, `shapes.txt`, `stop_times.txt`, `stops.txt`, `trips.txt`
   
2. **Streamlit Uygulamasını Çalıştırın**:
   - Aşağıdaki komutla Streamlit uygulamasını başlatabilirsiniz:
     ```bash
     streamlit run app.py
     ```

3. **Veri İncelemesi ve Görselleştirme**:
   - **Geographical Paths of Delhi Metro Routes**: Metro rotalarının coğrafi yollarını keşfedin.
   - **Number of Trips per Day**: Haftanın her günü yapılan sefer sayısına bakın.
   - **Geographical Distribution of Metro Stops**: Metro duraklarının coğrafi dağılımını görün.
   - **Number of Routes per Metro Stop**: Her bir durakta kaç farklı rota geçtiğini inceleyin.
   - **Average Trip Intervals**: Günün farklı saat dilimlerinde ortalama varış aralıklarını analiz edin.
   - **Trips by Time Interval**: Delhi Metro seferlerinin günün saat dilimlerine göre dağılımını inceleyin.


## 📈 Ekstra Özellikler

- **Veri İleri Düzey Analizi**: Farklı günlerdeki ve saat dilimlerindeki sefer sıklıklarıyla ilgili daha derinlemesine analiz yapabilme.
- **Görselleştirme Özelleştirmeleri**: Seferlerin saat dilimlerine göre dağılımlarını ve varış aralıklarını özelleştirilmiş renk paletleri ve etkileşimli grafiklerle görselleştirebilirsiniz.

## 💻 Uygulama Nasıl Çalışır?

Uygulama, Delhi Metro'nun farklı veri setlerinden (`stop_times`, `trips`, `calendar` gibi) faydalanarak analizler gerçekleştirir. Bu analizler, metro operasyonlarının daha verimli bir şekilde optimize edilmesine yardımcı olabilir. Uygulama ayrıca kullanıcıların görselleştirmelerle bu verileri daha iyi anlamalarını sağlar.

##### **İletişim**
Herhangi bir sorunuz veya geri bildiriminiz için aşağıdaki kanallardan ulaşabilirsiniz:
- **Email:** [furkansukan10@gmail.com](furkansukan10@gmail.com)
- **LinkedIn:** [LinkedIn Profile](https://www.linkedin.com/in/furkansukan/)
- **Kaggle:** [Kaggle Profile](https://www.kaggle.com/furkansukan)
- **Website:** [Project Website](https://customersegmentation-furkansukan.streamlit.app/)
---


[EN]

# Delhi Metro Operations Optimization 🚇

## Overview 🌍
This Streamlit application provides a comprehensive analysis of the Delhi Metro operations, including geographical route visualizations, trip distributions, and operational optimizations. It allows users to explore various metro data and gain insights into the operations throughout different time intervals of the day.

---

## Features ⚙️
1. **Geographical Paths of Delhi Metro Routes** 🌏  
   Visualize the geographical paths of Delhi Metro routes, showcasing the metro's shape and the routes it takes across the city.

2. **Trips Distribution Analysis** 📊  
   Discover the number of trips made on each day of the week, helping to identify peak operational periods.

3. **Metro Stop Locations** 📍  
   View the distribution of metro stops across Delhi and understand how routes connect to each stop.

4. **Route Distribution per Stop** 🚉  
   Explore how many different routes pass through each metro stop to assess station traffic.

5. **Trip Intervals Analysis** ⏱  
   Analyze the arrival intervals between trains at various stops, segmented by different times of the day.

6. **Trip Count by Time Interval** ⏳  
   View how trips are distributed across different time intervals of the day: Early Morning, Morning Peak, Midday, Evening Peak, and Late Evening.

---

## Setup and Installation 📥
To run this application, ensure you have the following Python libraries installed:
- **Pandas** for data manipulation
- **Seaborn** for statistical data visualization
- **Streamlit** for building the interactive web app
- **Plotly** for interactive charts
- **Matplotlib** for static plots

You can install the necessary packages using:
```bash
pip install pandas seaborn streamlit plotly matplotlib
```

---

## Data Files 📂
The application relies on the following input data files:
- **agency.txt**  
- **calendar.txt**  
- **routes.txt**  
- **shapes.txt**  
- **stop_times.txt**  
- **stops.txt**  
- **trips.txt**  

Make sure these files are located in your working directory.

---

## How it Works 🔧

### 1. **Geographical Paths Visualization** 🌍
This section visualizes the geographical paths of the metro routes using latitude and longitude coordinates from the `shapes.txt` file.

### 2. **Trips Distribution** 📊
The number of trips made for each day of the week is calculated by merging the `trips.txt` and `calendar.txt` data. The result is displayed through an interactive bar chart.

### 3. **Stop Locations** 📍
The `stops.txt` data is used to plot the geographical locations of metro stops across Delhi.

### 4. **Route Distribution per Stop** 🚉
Using the `stop_times.txt` and `trips.txt` data, we calculate how many routes pass through each stop and visualize the distribution using a scatter plot.

### 5. **Trip Intervals Analysis** ⏱
We calculate the average time intervals between train arrivals at different stops. These intervals are categorized into parts of the day (Morning, Afternoon, Evening) and visualized via a bar chart.

### 6. **Trip Count by Time Interval** ⏳
We classify the trips into specific time intervals (Early Morning, Morning Peak, Midday, Evening Peak, Late Evening) and visualize the number of trips within each interval.

---

## Try It Out 🖥️
To launch the app locally:
```bash
streamlit run app.py
```

---

##### **Contact**
Feel free to reach out for questions or feedback via:
- **Email:** [furkansukan10@gmail.com](furkansukan10@gmail.com)
- **LinkedIn:** [LinkedIn Profile](https://www.linkedin.com/in/furkansukan/)
- **Kaggle:** [Kaggle Profile](https://www.kaggle.com/furkansukan)
- **Website:** [Project Website](https://customersegmentation-furkansukan.streamlit.app/)

--- 

---

