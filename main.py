import pandas as pd
from datetime import datetime
import json
import duckdb

class Solution():

    def execute(self):
        df = pd.read_csv('source/scrap.csv')

        # Get current datetime with datetime libraries with specified format
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

        # Split duplicated and non-duplicate id
        df['dates'] = pd.to_datetime(df['dates'], format='%d/%m/%Y', errors='coerce') # Clean and Convert date column in csv into data type format in DataFrame
        duplicates_df = df[df.duplicated(subset='ids', keep='first')]
        unique_df = df.sort_values('dates', ascending=False).drop_duplicates(subset='ids', keep='first') # Get latest data based on 'dates' column

        # Declare target path and filename
        reject_dest = f"target/data_reject_{timestamp}.csv"
        cleaned_dest = f"target/data_{timestamp}.json"

        # Save duplicates to CSV file with specified format, Rejected data don't need to be cleaned according to the CSV file in example folder.
        duplicates_df.to_csv(reject_dest, index=False)

        # Convert string to list for certain columns (in example folder, genres and feat_track_ids is in list while in csv it only comma-separated)
        def parse_list(value):
            if pd.isna(value) or value.strip() == "":
                return []
            if isinstance(value, str):
                return [v.strip() for v in value.split(",")]
            return value
        
        # Clean data to follow specified format
        unique_df['dates'] = pd.to_datetime(unique_df['dates'], errors='coerce').dt.strftime('%Y-%m-%d')
        unique_df['names'] = unique_df['names'].str.upper()
        unique_df['first_release'] = unique_df['first_release'].astype(str).str[:4]
        unique_df['last_release'] = unique_df['last_release'].astype(str).str[:4]
        unique_df['genres'] = unique_df['genres'].apply(parse_list)
        unique_df['feat_track_ids'] = unique_df['feat_track_ids'].apply(parse_list)
        duplicates_df['genres'] = duplicates_df['genres'].apply(parse_list)
        duplicates_df['feat_track_ids'] = duplicates_df['feat_track_ids'].apply(parse_list)

        # Display row count and data
        result = {
            "row_count": len(unique_df),
            "data": unique_df.to_dict(orient='records')
        }

        # Save to JSON file with specified filename format
        with open(cleaned_dest, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        print(f"Saved duplicates to: {reject_dest}") # Log Purposes
        print(f"Saved unique data to: {cleaned_dest}") # Log Purposes

        # Create new Database
        db = duckdb.connect('music.duckdb') 

        # Access ddl.sql file and execute DDL script
        with open('ddl.sql', 'r') as f:  
            ddl_sql = f.read()
        db.execute(ddl_sql) 
        
        # Enable DuckDB access to DataFrame
        db.register('unique_df_temp', unique_df)
        db.register('duplicates_df_temp', duplicates_df)

        # Insert into target table
        db.execute("INSERT INTO data SELECT * FROM unique_df_temp")
        db.execute("INSERT INTO data_reject SELECT * FROM duplicates_df_temp")

        print ('Tables created') # Log Purposes
        db.close()

        return


if __name__ == "__main__":
    Solution().execute()