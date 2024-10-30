
# **Global AQI Dashboard**

### **Overview**

The Global AQI Dashboard is an interactive data visualization tool designed to track and analyze air quality index (AQI) levels across various global cities. The dashboard leverages geolocation data to map AQI measurements, allowing stakeholders to monitor air quality trends, understand PM2.5 pollutant concentrations, and assess changes over time. This tool is valuable for organizations, environmental agencies, and public health professionals focused on pollution management and data-driven decision-making.

### **Features**

- **Donut Chart**: Visual color indicator displaying PM2.5 concentration levels.
- **Average PM2.5 Calculation**: Shows yearly and country-specific PM2.5 averages through dropdown navigation.
- **Dropdown Filters**: Select both country and year to filter data dynamically.
- **Interactive Map**: A map visualization using Plotly and Mapbox displays AQI levels across continents, with zoom capabilities for city-level details.
- **Consistent Color Mapping**: AQI levels are color-coded across all visualizations for immediate interpretation.
- **Dynamic Metrics**: Includes metrics like PM2.5 percentage change and yearly averages for each location, providing insights into pollution trends.

### **Technologies Used**

- **Python**: Main programming language for data processing and visualization.
- **Dash and Plotly**: For creating the interactive dashboard with a user-friendly interface.
- **Pandas**: Data manipulation and preprocessing.
- **Mapbox**: Provides geospatial rendering for the scatter map.

### **Project Structure**

```plaintext
Global-AQI-Dashboard/
|-- air-pollution.csv 
|-- air-population_extraction.csv         
|-- pages/
|   |-- Introduction.py           
|   |-- geospatial_analysis.py  
|-- main.py                    
|-- README.md                  
|-- requirements.txt
|-- utils.py          
```

### **Getting Started**

#### **Prerequisites**

- **Python**: Ensure Python 3.7 or above is installed.
- **Pip**: Ensure pip is installed for managing Python packages.

#### **Installation**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SmartDvi/Air_Pollution.git
   cd Air_pollution
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

#### **Run the Application**

To start the dashboard, execute the following command in your terminal:
```bash
python main.py
```

The dashboard will be available at `http://127.0.0.1:6070/`.

### **Usage**

1. **Navigating the Dashboard**: The dashboard has two main pages accessible through the navigation Sidebar:
   - **Overview**: Introduction to the project, purpose, and usage instructions.
   - **Map Visualization**: Displays AQI levels on a global map with zoom and filter options.
   - **Analytics**: Detailed charts and analyses on AQI trends and changes in PM2.5 levels over time.

2. **Filtering Data**: Use dropdowns to filter data by year or AQI level and explore trends within specific regions or cities.

3. **Interpreting Data**: Hover over points on the map for AQI level, PM2.5 concentration, and more. Color codes represent AQI levels, making it easy to identify regions with high pollution.

### **Customization**

- **Color Mapping**: To ensure visual consistency, color mappings are predefined for AQI levels in `main.py`. Adjust as needed to match your organization’s standards.
- **Map Centering and Zoom**: The map displays continents by default; adjust the `center` and `zoom` parameters in `map_visualization.py` for a global view or region-specific focus.

### **Contributing**

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit changes (`git commit -m 'Added new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

### **Contact**

For inquiries or feedback, reach out to:

- **Name**: Moritus Peters
- **Email**: petersmoritus@gmail.com
- **LinkedIn**: [Moritus Peters](http://www.linkedin.com/in/morituspeters)

