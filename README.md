# **YouTube Data Fetcher**

This Python script retrieves video data and comments from a given YouTube channel URL (with a handle), then exports the data into an Excel file. The script makes use of the YouTube Data API v3, `requests`, and `pandas` to fetch and process the data.

---

## **Features**

- Fetches the **channel ID** using a YouTube channel handle (e.g., `@channelhandle`).
- Retrieves **video data** (ID, Title, Description, Views, etc.) for the given channel.
- Fetches the **latest 100 comments** (and their replies) for each video.
- Exports the data into an **Excel file** with two sheets:
  - **Video Data**
  - **Comments Data**

---

## **Requirements**

- **Python 3.7+**: This script is written in Python and requires version 3.7 or higher.
- **YouTube Data API v3 Key**: You need a YouTube Data API key to access YouTube data.

---

## **Setup Instructions**

### **1. Install Python and Dependencies**

If you haven't already, you need to install Python 3.7 or higher. You can download it from [here](https://www.python.org/downloads/).

After installing Python, you can install the required dependencies.

- Clone or download the project files.

  ```bash
  git clone https://github.com/VismayRaul/youtube-data-fetcher.git
  cd youtube-data-fetcher
  ```

- Create a virtual environment (optional but recommended):

  ```bash
  python3 -m venv venv
  ```

- Activate the virtual environment:

  - **For Windows**:
    ```bash
    venv\Scripts\activate
    ```

  - **For macOS/Linux**:
    ```bash
    source venv/bin/activate
    ```

- Install the dependencies using `pip`:

  ```bash
  pip install -r requirements.txt
  ```

---

### **2. Get YouTube Data API v3 Key**

To interact with the YouTube API, you need a YouTube Data API key.

1. Go to the [Google Developers Console](https://console.developers.google.com/).
2. Create a new project.
3. Navigate to **APIs & Services > Library**.
4. Search for **YouTube Data API v3** and enable it.
5. Go to **APIs & Services > Credentials**.
6. Create a new API key.
7. Copy the generated API key and paste it into the `.env` file.

   In `.env`, find the line where the API key is defined and replace `__YOUTUBE_API_KEY__` with your actual key:

   ```python
   YOUTUBE_API_KEY = '__YOUTUBE_API_KEY__'  # Replace with your actual API key
   ```

---

### **3. Running the Script**

Once you've set up the environment and the API key, you can run the script.

- Open the terminal/command prompt and navigate to the folder where the script is located.

  ```bash
  cd youtube-data-fetcher
  ```

- Run the script:

  ```bash
  python main.py
  ```

  The script will prompt you to enter a YouTube channel handle, such as `@channelhandle`. After that, it will fetch the video and comment data for the given channel and export the data into an Excel file.

---

### **4. Output File**

The script will create an Excel file in your **Downloads** folder. The file name will be in the format `YouTube_Data_YYYYMMDD_HHMMSS.xlsx`, where `YYYYMMDD_HHMMSS` is the timestamp when the file was created.

Inside the Excel file, there will be two sheets:

- **Video Data**: Contains the basic details about each video (ID, Title, Description, Published Date, View Count, etc.).
- **Comments Data**: Contains the latest 100 comments for each video, including the replies to those comments.

---

## **Dependencies**

The following Python libraries are required to run the script:

- `requests`: For making HTTP requests to the YouTube Data API.
- `pandas`: For processing and exporting data to Excel.
- `openpyxl`: A dependency for `pandas` to write Excel files.

You can install them manually using:

```bash
pip install requests pandas openpyxl
```

Or if you've set up the virtual environment, you can simply install all the dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Here’s the content for the `requirements.txt` file:

```txt
requests==2.28.1
pandas==1.5.3
openpyxl==3.1.2
```

---

## **File Structure**

The project has the following structure:

```
youtube-data-fetcher/
|
├── helper_functions
    ├── channels.py         # Functions for channel related data
    ├── comments.py         # Functions for comment related data
    ├── videos.py           # Functions for video related data
    ├── excel_export.py     # Handles exporting data to Excel
├── main.py                 # Main script to run the application
├── constant.py             # Stores all the required constants
├── requirements.txt        # List of dependencies
├── README.md               # Project documentation (this file)
├── .env                    # Stores sensative information
├── .gitignore              # Restrict pushing sensative files to the repo
```

---

## **Error Handling**

The script contains error handling to handle potential issues such as:

- Invalid channel handle.
- Failed API requests.
- No videos or comments found.
- Issues during Excel export.

The script will print error messages to the console to guide you in troubleshooting.

---

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## **Contact Information**

If you have any questions or need further assistance, feel free to reach out at [vismayraul25@gmail.com].

---

This README provides all the necessary instructions for setting up, running, and using the script.