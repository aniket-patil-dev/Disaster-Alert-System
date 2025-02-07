# 🌍 Real-Time Earthquake Alert System

## 📌 Overview
This project is a **serverless earthquake alert system** built using **AWS Lambda**, **Amazon S3**, **Amazon SNS**, and **CloudWatch Events**. It fetches real-time earthquake data from the **USGS API**, processes it, filters new events, and sends alerts via **AWS SNS** to notify users.

### 🔹 Key Features
- Fetches **real-time earthquake data** from the USGS API.
- Filters earthquakes **based on a minimum magnitude threshold** (default: 5.0).
- **Stores last processed earthquake ID** in Amazon S3 to prevent duplicate alerts.
- **Publishes alerts via AWS SNS** (email/SMS notifications).
- Runs **every 1 minute** using **CloudWatch Events schedule**.

---

## 🏢 Architecture & Workflow

1. **AWS Lambda Execution**
   - Runs every **1 minute**, triggered by **CloudWatch Events**.
   - Fetches earthquake data from **USGS API**, filtering for earthquakes from the last 24 hours.

2. **Data Processing**
   - Extracts **magnitude, location, time, coordinates, and URL**.
   - Compares event IDs with the **last processed ID stored in S3**.
   - Processes **only new earthquakes** to prevent duplicate notifications.

3. **Publishing Alerts**
   - New earthquakes trigger **AWS SNS notifications** (email/SMS).

4. **Updating the Last Event ID**
   - **Latest earthquake ID** is stored in **S3** for future comparisons.

---

## 💪 Technologies Used

- **AWS Lambda** – Executes the serverless function every minute.
- **Amazon S3** – Stores the last processed earthquake ID.
- **AWS SNS** – Sends alerts to users via email/SMS.
- **CloudWatch Events** – Triggers the Lambda function every minute.
- **USGS Earthquake API** – Provides real-time earthquake data.
- **Python (Boto3, Requests)** – Used for API requests and AWS service interactions.

---

## 🌐 Environment Variables
In AWS Lambda, set the following environment variables:

```plaintext
EARTHQUAKE_API_LINK=https://earthquake.usgs.gov/fdsnws/event/1/query
S3_BUCKET_NAME=your-bucket-name
SNS_TOPIC_ARN=arn:aws:sns:region:account-id:your-sns-topic
```

---

## 🔄 Deployment Instructions

### 1️⃣ Create an S3 Bucket
1. Go to **Amazon S3**
2. Create a new bucket (e.g., `earthquake-alerts-bucket`)
3. Add an empty JSON file `last_event_id.json` with the content:
   ```json
   { "last_event_id": "" }
   ```

### 2️⃣ Set Up AWS SNS
1. Create an **SNS Topic** (e.g., `EarthquakeAlerts`)
2. Subscribe your **email or phone number** to receive alerts.

### 3️⃣ Deploy the Lambda Function
1. Upload the Lambda function code to **AWS Lambda**.
2. Attach the necessary **IAM Role Permissions**:
   - `AmazonS3FullAccess`
   - `AmazonSNSFullAccess`
   - `AWSLambdaBasicExecutionRole`

### 4️⃣ Add a Layer for the Requests Module
1. Go to your AWS Lambda function.
2. Navigate to the **Layers** section and click **Add a Layer**.
3. Choose **Custom Layer** and select a layer that includes the `requests` module.
4. If a layer is not available, create a zip package with `requests`, upload it to S3, and add it as a Lambda layer.

### 5️⃣ Schedule Lambda Execution using CloudWatch Events
1. Go to **Amazon EventBridge** → Create a Rule
2. Set the schedule to **every 1 minute** (`rate(1 minute)`)
3. Choose **Lambda function** as the target and select your function.

---

## 📊 Example Alert Message

```
Earthquake Alert!
Magnitude: 6.2
Location: 20km SE of Tokyo, Japan
Time: 2025-02-07 15:30:00 UTC
Details: https://earthquake.usgs.gov/earthquakes/eventpage/us7000jklm
```

---

## 💡 Future Enhancements

- 🔹 Support for **custom magnitude thresholds** per user.
- 🔹 **Geographical filtering** (alerts only for specific regions).
- 🔹 **Integration with Telegram & Discord bots** for real-time notifications.
- 🔹 **Machine learning-based earthquake impact prediction**.

---

## 🌐 License
This project is **open-source** under the **MIT License**.

---

### 🚀 Contributions & Feedback
Have suggestions or improvements? Feel free to open an **issue** or **pull request**! 

---
