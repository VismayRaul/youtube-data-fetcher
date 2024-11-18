import os
import pandas as pd
from datetime import datetime

from constant import DOWNLOAD_FOLDER

def export_to_excel(video_data, comments_data):
    """
    Export video and comment data to a dynamically named Excel file in the Downloads folder.
    """
    # Determine the Downloads directory
    downloads_folder = os.path.join(os.path.expanduser("~"), DOWNLOAD_FOLDER)

    # Create a dynamic file name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"YouTube_Data_{timestamp}.xlsx"
    file_path = os.path.join(downloads_folder, file_name)

    try:
        # Write the data to the Excel file
        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            # Video Data Sheet
            video_df = pd.DataFrame(video_data)
            video_df.to_excel(writer, sheet_name="Video Data", index=False)

            # Comments Data Sheet
            comments_df = pd.DataFrame(comments_data)
            comments_df.to_excel(writer, sheet_name="Comments Data", index=False)

        print(f"File has been saved to: {file_path}")
        return file_path
    except Exception as e:
        print(f"An error occurred while exporting to Excel: {e}")
        return None
