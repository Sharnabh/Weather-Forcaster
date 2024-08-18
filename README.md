# Weather-Forcaster
### Project Report: Weather Forecaster Application
***Code by Sharnabh Banerjee***

---

#### **1. Project Overview**

The Weather Forecaster Application is a Python-based desktop application that provides weather information for any specified location. It uses the OpenWeatherMap API to fetch real-time weather data based on the user's input. The application is built with a user-friendly interface using the Tkinter library and includes features such as search suggestions, search history, and the ability to store and manage weather data.

---

#### **2. Key Features**

1. **Real-time Weather Data Retrieval:**
   - Users can input a city name, and the application fetches real-time weather data including temperature, humidity, pressure, wind speed, and a brief description of the weather conditions.

2. **Search Suggestions:**
   - As the user types a city name, the application provides location suggestions using the OpenWeatherMap API, improving the user experience by making it easier to find locations.

3. **Search History:**
   - The application keeps track of the user's search history, allowing quick access to previously searched locations.

4. **Data Storage:**
   - Users can save the weather data for a location to a CSV file. This allows for easy retrieval and analysis of weather data at a later time.

5. **Saved Data Management:**
   - The application provides a dedicated interface for viewing saved weather data and allows users to delete specific entries.

6. **Collapsible Menu:**
   - A collapsible menu is available for easy access to saved locations and search history.

---

#### **3. Technical Components**

1. **Python Libraries Used:**
   - **Tkinter:** For creating the graphical user interface.
   - **geopy:** For converting city names into geographical coordinates.
   - **timezonefinder:** For determining the time zone of a location based on geographical coordinates.
   - **pytz:** For handling timezone conversions.
   - **requests:** For making API calls to fetch weather data.
   - **PIL (Pillow):** For handling image processing (used to display icons and images).
   - **CSV:** For reading and writing data to CSV files.

2. **API Integration:**
   - **OpenWeatherMap API:** The application uses this API to fetch both weather data and location suggestions. The API is accessed via HTTP requests, and the data is parsed from JSON format.

3. **User Interface (UI):**
   - The UI is built using Tkinter, with a focus on simplicity and ease of use. Key components include an input field for the city name, labels for displaying weather data, buttons for saving data, and a collapsible menu for additional features.

4. **Error Handling:**
   - The application includes basic error handling, such as handling cases where no data is returned for a city or when there is a failure in fetching suggestions.

---

#### **4. Code Breakdown**

- **Main Application Window:**
   - The main window of the application is created using `Tk()`, with a fixed size and title. It hosts all the interactive components such as the search bar, weather information display, and buttons.

- **Weather Data Retrieval (`getWeather` function):**
   - This function is triggered when the user searches for a city's weather. It uses the `geopy` library to obtain the geographical coordinates of the city, then uses the `timezonefinder` library to get the time zone. The weather data is fetched via the OpenWeatherMap API, and the results are displayed on the UI.

- **Search Suggestions (`fetch_location_suggestions` and `update_suggestions` functions):**
   - As the user types in the search bar, these functions are responsible for fetching and displaying city suggestions. The `fetch_location_suggestions` function queries the OpenWeatherMap API for location suggestions based on the input string.

- **Data Storage (`save_weather_to_csv` function):**
   - This function allows users to save the fetched weather data into a CSV file. If the file doesn’t exist, it creates one with appropriate headers. Each search result is appended as a new row in the CSV file.

- **Saved Data Management (`show_saved_data` and `delete_selected_rows` functions):**
   - The `show_saved_data` function displays the stored weather data in a new window, allowing users to view and manage their saved locations. Users can select rows to delete, and the `delete_selected_rows` function handles the deletion process.

- **Search History (`show_search_history` function):**
   - The application keeps a record of all the cities searched during the session. The `show_search_history` function allows users to view and re-select from their search history.

- **Collapsible Menu (`toggle_menu` function):**
   - The menu is hidden by default and can be toggled on and off. It provides quick access to saved locations and search history.

---

#### **5. Conclusion**

The Weather Forecaster Application is a comprehensive tool that leverages Python's capabilities to deliver real-time weather information in an intuitive and user-friendly manner. By integrating various libraries and APIs, it provides a robust solution for accessing and managing weather data. The additional features like search suggestions, search history, and data storage enhance the usability and functionality of the application.

---

#### **6. Future Enhancements**

- **Enhanced Error Handling:**
   - Implement more robust error handling, especially for network-related issues and invalid API responses.

- **Graphical Data Representation:**
   - Incorporate graphical representation of weather data (e.g., temperature trends over time) using libraries like Matplotlib.

- **Multiple Language Support:**
   - Add support for multiple languages to cater to a broader audience.

- **Mobile Version:**
   - Develop a mobile-friendly version of the application using a framework like Kivy.

---