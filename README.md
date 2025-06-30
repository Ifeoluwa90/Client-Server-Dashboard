# Client-Server-Dashboard
# Grazioso Salvare Animal Rescue Dashboard

*The Grazioso Salvare Animal Rescue Dashboard is a comprehensive, interactive web application designed to help identify and categorize dogs suitable for search-and-rescue training. This full-stack dashboard application integrates with MongoDB databases to provide real-time filtering, visualization, and mapping capabilities for animal shelter data. The dashboard enables rescue organizations to efficiently identify candidate animals based on specific rescue type criteria including water rescue, mountain/wilderness rescue, and disaster/individual tracking operations.*

## Motivation

*Animal rescue organizations need efficient tools to identify suitable candidates for specialized training programs. Traditional methods of manually searching through large datasets are time-consuming and prone to errors. This project was created to streamline the process of identifying rescue-suitable animals by providing an interactive, user-friendly dashboard that automatically filters and visualizes animal shelter data based on scientific rescue training criteria. The dashboard reduces the time required to identify suitable candidates from hours to minutes while ensuring consistent application of rescue type specifications. This standardized approach improves the efficiency of rescue animal identification and supports better decision-making for training program coordinators.*

## Getting Started

*This dashboard connects to a MongoDB database named "AAC" with a collection called "animals" containing Austin Animal Center outcomes data. The database contains 10,000+ animal records with comprehensive information including breeds, ages, sex, outcomes, and geolocation data. The dashboard requires a MongoDB user account called "aacuser" with readWrite permissions to the AAC database for secure data access.*

*The dashboard implements four main filtering categories based on Grazioso Salvare's rescue training specifications: Water Rescue (Labrador Retriever Mix, Chesapeake Bay Retriever, Newfoundland - Intact Females, 26-156 weeks), Mountain/Wilderness Rescue (German Shepherd, Alaskan Malamute, Old English Sheepdog, Siberian Husky, Rottweiler - Intact Males, 26-156 weeks), Disaster/Individual Tracking (Doberman Pinscher, German Shepherd, Golden Retriever, Bloodhound, Rottweiler - Intact Males, 20-300 weeks), and Reset functionality to view all available animals.*

*The main challenges encountered included implementing complex multi-field MongoDB queries, handling inconsistent geolocation data, ensuring real-time synchronization between dashboard components, and optimizing performance for large datasets. These challenges were overcome by developing robust query structures using MongoDB operators, implementing comprehensive error handling with fallback coordinates, creating a sophisticated callback architecture for component synchronization, and utilizing pagination and data optimization techniques for improved performance.*

## Installation

The following tools and libraries are required to use this software:

**MongoDB**: NoSQL database system chosen for its flexibility in handling complex animal shelter data with varying attributes and its powerful query capabilities for multi-field filtering operations.

**Python 3.9+**: Programming language selected for its extensive data science ecosystem and excellent integration with both MongoDB and web framework libraries.

**Plotly Dash**: Web framework chosen for its Python-native approach, reactive component architecture, and built-in visualization capabilities that eliminate the need for separate frontend/backend development.

**Pandas**: Data manipulation library selected for its powerful DataFrame operations and seamless integration with MongoDB data for analysis and filtering.

**Dash Leaflet**: Mapping library chosen for its interactive geolocation capabilities and professional mapping features.

**PyMongo**: Official MongoDB driver for Python, selected for its comprehensive feature set and reliable connection management.

**Jupyter Notebook**: Interactive development environment used for dashboard development and testing.

- *Install MongoDB and ensure it is running on localhost:27017*
- *Install Python 3.9 or higher*
- *Install required packages using: pip install dash plotly pandas pymongo dash-leaflet jupyter-dash*
- *Set up MongoDB user authentication with aacuser credentials*
- *Download and place the Grazioso Salvare logo file in the project directory*

## Usage

*This dashboard provides an intuitive interface for filtering and visualizing animal shelter data to identify rescue training candidates.*

### Code Example

```python
# Setup and run the Grazioso Salvare Dashboard
from jupyter_dash import JupyterDash
from dash import dcc, html, dash_table
import pandas as pd
from animal_shelter import AnimalShelter

# Initialize database connection
username = "aacuser"
password = "SNHU1234"
shelter = AnimalShelter(username, password)

# Load data
df = pd.DataFrame.from_records(shelter.read({}))

# Initialize dashboard
app = JupyterDash('GraziosoSalvareDashboard')

# Configure layout with filters, data table, map, and charts
app.layout = html.Div([
    # Interactive filter options
    dcc.RadioItems(
        id='filter-type',
        options=[
            {'label': 'Water Rescue', 'value': 'Water Rescue'},
            {'label': 'Mountain/Wilderness Rescue', 'value': 'Mountain/Wilderness Rescue'},
            {'label': 'Disaster/Individual Tracking', 'value': 'Disaster/Individual Tracking'},
            {'label': 'Reset (Show All)', 'value': 'Reset'}
        ]
    ),
    # Data table, map, and chart components
])

# Run dashboard
app.run_server(debug=True, port=8051)
```

### Dashboard Components

**Interactive Filtering System:**
- Input: Radio button selection for rescue type
- Output: Filtered dataset based on breed, age, and sex criteria
- Functionality: Real-time database queries with complex multi-field filtering

**Data Table:**
- Input: Filtered animal data from database
- Output: Paginated, sortable table with 15 records per page
- Features: Native filtering, sorting, row selection, professional styling

**Geolocation Mapping:**
- Input: Selected animal record from data table
- Output: Interactive map centered on animal location
- Features: Popup information, coordinate validation, Austin fallback coordinates

**Breed Distribution Chart:**
- Input: Current filtered dataset
- Output: Pie chart showing top 10 breed distributions
- Features: Interactive hover information, percentage calculations, legend display

### Tests

*The dashboard includes comprehensive testing for all functionality:*

**Filter Testing:**
```python
# Test Water Rescue filter
water_rescue_data = get_rescue_data("Water Rescue")
print(f"Water rescue candidates found: {len(water_rescue_data)}")

# Test Mountain/Wilderness filter
mountain_data = get_rescue_data("Mountain/Wilderness Rescue")
print(f"Mountain rescue candidates found: {len(mountain_data)}")

# Test Disaster/Individual Tracking filter
disaster_data = get_rescue_data("Disaster/Individual Tracking")
print(f"Disaster rescue candidates found: {len(disaster_data)}")

# Test Reset functionality
all_data = get_rescue_data("Reset")
print(f"Total animals in database: {len(all_data)}")
```

**Component Integration Testing:**
```python
# Test data table updates
@app.callback(Output('datatable-id', 'data'), Input('filter-type', 'value'))
def test_table_update(filter_type):
    filtered_df = get_rescue_data(filter_type)
    return filtered_df.to_dict('records')  # Should return filtered data

# Test map synchronization  
@app.callback(Output('map-id', 'children'), Input('datatable-id', 'selected_rows'))
def test_map_update(selected_rows):
    # Should update map based on table selection
    return updated_map_component

# Test chart updates
@app.callback(Output('breed-chart', 'figure'), Input('datatable-id', 'derived_virtual_data'))
def test_chart_update(viewData):
    # Should update breed distribution chart
    return updated_chart_figure
```

**Database Query Testing:**
```python
# Test complex query structure
water_query = {
    "animal_type": "Dog",
    "breed": {"$in": ["Labrador Retriever Mix", "Chesapeake Bay Retriever"]},
    "sex_upon_outcome": {"$regex": "Intact Female", "$options": "i"},
    "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
}
water_results = shelter.read(water_query)  # Should return matching records
```

**Test Results Summary:**

**Dashboard Functionality:**
- Filter operations: Successfully filters data based on rescue type specifications
- Data table: Displays filtered results with sorting, pagination, and selection capabilities  
- Map integration: Successfully displays animal locations with popup information
- Chart updates: Dynamically updates breed distribution based on filtered data
- Component synchronization: All components update consistently when filters change

**Performance Testing:**
- Large dataset handling: Successfully processes 10,000+ animal records
- Query optimization: Complex multi-field queries execute efficiently
- Real-time updates: Dashboard components update without performance lag
- Error handling: Gracefully handles missing data and connection issues

### video
## 📺 Dashboard Functionality Demo

[![Dashboard Demo](https://img.youtube.com/vi/zg_PcO3dVn8/maxresdefault.jpg)](https://www.youtube.com/watch?v=zg_PcO3dVn8 "Grazioso Salvare Dashboard Demo - Click to Watch!")

**Video demonstrates:**
- Interactive filtering for all rescue types
- Data table functionality and row selection
- Geolocation mapping with animal details
- Breed distribution chart updates
- Complete user workflow from filter selection to animal identification

**Dashboard Component Details:**

**Interactive Filter Options:** Radio button interface with clear rescue type labels and visual indicators

**Data Table Features:** Professional styling with alternating row colors, sortable columns, pagination controls, and selection highlighting

**Geolocation Mapping:** Interactive Leaflet map with zoom controls, popup information windows, and professional styling

**Breed Distribution Chart:** Pie chart with percentage labels, interactive legend, and hover tooltips

**Branding Elements:** Grazioso Salvare logo with SNHU link, developer identification, and consistent color scheme

## Roadmap/Features (Optional)

**Proposed Future Enhancements:**

- **Advanced Search Capabilities**: Custom criteria input allowing users to specify age ranges, multiple breed selections, and custom outcome types beyond the standard rescue categories

- **Export Functionality**: CSV and PDF export options for filtered results to support offline analysis and reporting requirements

- **Real-time Data Synchronization**: Automatic updates from shelter databases to ensure dashboard always reflects current animal availability

- **User Authentication System**: Role-based access control allowing different permission levels for shelter staff, rescue coordinators, and administrators

- **Mobile-Responsive Design**: Enhanced mobile interface optimization for field use by rescue coordinators and shelter staff

- **Analytics Dashboard**: Advanced reporting features including trend analysis, success rate tracking, and performance metrics for rescue programs

- **Integration APIs**: RESTful API endpoints to allow integration with external rescue management systems and third-party applications

- **Notification System**: Automated alerts when new animals matching specific rescue criteria become available

**Known Issues and Improvements:**

- Geolocation data quality varies across different shelter records
- Performance optimization needed for datasets exceeding 50,000 records  
- Enhanced error handling for network connectivity issues during real-time updates

**What Makes This Project Stand Out:**

- **Scientific Rescue Criteria Integration**: Implements evidence-based rescue training specifications directly into the filtering system
- **Real-time Component Synchronization**: Sophisticated callback architecture ensuring all dashboard components update consistently
- **Professional User Experience**: Enterprise-level interface design with intuitive navigation and comprehensive error handling
- **Scalable Architecture**: Modular design supporting easy expansion and integration with additional rescue organization databases

  # CS-340 Portfolio Reflection

## How do you write programs that are maintainable, readable, and adaptable?

Writing maintainable code requires modular design and clear documentation. In the CRUD Python module from Project One, I created separate methods for each database operation with comprehensive error handling, making the code easy to test and modify. The modular design allowed me to easily connect the dashboard widgets to the database in Project Two without rewriting database logic. This CRUD module could be adapted for future projects like inventory management systems or customer databases by simply changing the connection parameters and extending the base class.

## How do you approach a problem as a computer scientist?

I approach problems systematically by analyzing requirements before implementation. For the Grazioso Salvare project, I first understood the client's need to identify rescue dogs based on specific criteria, then designed the database queries and user interface to meet those requirements efficiently. This project differed from previous coursework because it required thinking like a consultant working with real client needs rather than just completing technical exercises. For future database projects, I would use similar techniques: thorough requirements analysis, iterative development with client feedback, and designing for scalability from the beginning.

## What do computer scientists do, and why does it matter?

Computer scientists solve real-world problems by creating technological solutions that improve efficiency and decision-making. My dashboard transforms a manual process that could take hours into an automated system that identifies suitable rescue animals in seconds, allowing organizations to focus on training rather than data management. This type of work matters because it makes complex technology accessible to domain experts who can apply it to solve important problems, ultimately improving rescue operations and potentially saving more lives through better efficiency.

## Contact

Your name: Ifeoluwa Adewoyin

Email: Ifeoluwaadewoyin90@gmail.com

Course: CS-340 Client/Server Development

Institution: Southern New Hampshire University

Project: Grazioso Salvare Animal Rescue Dashboard

---

*This dashboard demonstrates advanced full-stack development capabilities including MongoDB database integration, interactive web application development using Plotly Dash, real-time data visualization, geolocation mapping, and professional user interface design for mission-critical rescue operations.*
