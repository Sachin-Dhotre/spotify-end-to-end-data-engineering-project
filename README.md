# 🎧 Spotify End-to-End Data Engineering Project (ETL Pipeline)

This project demonstrates a complete end-to-end ETL pipeline using the **Spotify Web API**, **AWS Lambda**, **S3**, **Glue**, and **Athena**. The pipeline extracts Spotify playlist data, transforms it, and loads it into a queryable format for analytics.

---

## 🧱 Architecture Overview

![Architecture Diagram](https://github.com/Sachin-Dhotre/spotify-end-to-end-data-engineering-project/blob/main/Architecture.png)

### 📦 Components

- **Spotify API**: Source of playlist and track data.
- **Amazon CloudWatch**: Scheduled trigger (e.g., daily) for Lambda extraction.
- **AWS Lambda (Extraction)**: Pulls raw data from Spotify and stores it in S3.
- **Amazon S3 (Raw & Transformed)**: Data lake storage for raw and processed data.
- **AWS Lambda (Transformation)**: Cleans/transforms raw JSON into structured format.
- **Amazon S3 Trigger**: Initiates transformation upon new data upload.
- **AWS Glue Crawler**: Automatically infers schema and creates a catalog table.
- **AWS Glue Data Catalog**: Stores metadata to make data queryable via Athena.
- **Amazon Athena**: SQL-based analytics directly on transformed S3 data.


---

### 🔄 Workflow:

1. **Extract**  
   - A Lambda function extracts album data for a specific Spotify artist using the [Spotipy](https://spotipy.readthedocs.io/en/2.22.1/) library.  
   - The raw JSON is stored in the `raw_data/to_processed/` folder in an S3 bucket.

2. **Transform**  
   - Another Lambda function processes new files from the `raw_data/to_processed/` folder.  
   - It parses and cleans the album and artist information into separate CSV files.  
   - These transformed files are saved to the `transformed_data/album_data/` and `transformed_data/artist_data/` folders respectively.

3. **File Management**  
   - After successful transformation, the original raw JSON files are moved from `raw_data/to_processed/` to `raw_data/processed/` to avoid reprocessing.

4. **Load**  
   - A Glue Crawler updates the Data Catalog based on the transformed data.  
   - Data becomes queryable using Amazon Athena via SQL.

---

## 🛠️ Technologies Used

- 🐍 Python (Spotipy)
- ☁️ AWS Lambda
- 🪣 Amazon S3
- 🔁 AWS Glue (Crawler + Catalog)
- 🔍 Amazon Athena
- 🕒 Amazon CloudWatch Events
- 🔐 IAM Roles for secure access

---

## 🚀 Setup Instructions

### 🔑 Prerequisites
- AWS Account with permissions for Lambda, S3, Glue, and Athena
- Spotify Developer account ([https://developer.spotify.com](https://developer.spotify.com))

### ⚙️ Environment Variables for Lambda

| Variable        | Description                         |
|----------------|-------------------------------------|
| `client_id`     | Spotify Client ID                   |
| `client_secret` | Spotify Client Secret               |

### 🪄 Steps

1. **Deploy Lambda functions** (use AWS Console or SAM/Terraform)
2. **Create S3 buckets** (e.g., `spotify-etl-project-sachin-dhotre`)
3. **Schedule extraction** via CloudWatch (daily or hourly)
4. **Configure Glue Crawler** for `transformed_data/`
5. **Query with Athena** using the created database and tables

---

## 📊 Sample Athena Query

```sql
SELECT album_name, album_release_date
FROM album_data
WHERE album_artist_name = 'Shreya Ghoshal'
ORDER BY album_release_date DESC;

