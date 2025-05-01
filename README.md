# 🎧 Spotify End-to-End Data Engineering Project (ETL Pipeline)

This project demonstrates a complete end-to-end ETL pipeline using the **Spotify Web API**, **AWS Lambda**, **S3**, **Glue**, and **Athena**. The pipeline extracts Spotify playlist data, transforms it, and loads it into a queryable format for analytics.

---

## 🧱 Architecture Overview

![Architecture Diagram](unnamed.png)

### 📦 Components

- **Spotify API**: Source of playlist and track data.
- **AWS Lambda (Extraction)**: Pulls raw data from Spotify and stores it in S3.
- **Amazon S3 (Raw & Transformed)**: Data lake storage for raw and processed data.
- **AWS Lambda (Transformation)**: Cleans/transforms raw JSON into structured format.
- **Amazon S3 Trigger**: Initiates transformation upon new data upload.
- **AWS Glue Crawler**: Automatically infers schema and creates a catalog table.
- **AWS Glue Data Catalog**: Stores metadata to make data queryable via Athena.
- **Amazon Athena**: SQL-based analytics directly on transformed S3 data.
- **Amazon CloudWatch**: Scheduled trigger (e.g., daily) for Lambda extraction.

---

## 🚀 Workflow Summary

1. **Extract**: Lambda fetches Spotify playlist items using Spotipy and stores them in S3 as raw JSON.
2. **Transform**: A triggered Lambda cleans and flattens the JSON structure into tabular form.
3. **Load**:
   - Transformed data is written to a separate S3 bucket/path.
   - AWS Glue Crawler infers the schema and registers it in the Glue Data Catalog.
   - Athena can now query this data using standard SQL.

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

## 📊 Example Use Case

Analyze:
- Most frequently occurring artists in a playlist
- Average track duration per genre
- Trends across multiple curated playlists

---

## 📂 Folder Structure

