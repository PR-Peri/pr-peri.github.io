import os
import json
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest
import yaml

# 1️⃣ Load GA credentials from GitHub secret
creds_json = os.environ["GA_CREDENTIALS_JSON"]
creds = json.loads(creds_json)

# 2️⃣ Write temporary JSON file for Google library
with open("ga_creds.json", "w") as f:
    json.dump(creds, f)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ga_creds.json"

# 3️⃣ GA4 property ID from secret
PROPERTY_ID = os.environ["GA_PROPERTY_ID"]

# 4️⃣ Initialize GA4 client
client = BetaAnalyticsDataClient()

# 5️⃣ Request top pages in last 30 days
request = RunReportRequest(
    property=f"properties/{PROPERTY_ID}",
    dimensions=[Dimension(name="pagePath")],
    metrics=[Metric(name="screenPageViews")],
    date_ranges=[DateRange(start_date="30daysAgo", end_date="today")],
    limit=10  # top 10 pages
)

response = client.run_report(request)

# 6️⃣ Filter articles and store in list
articles = []
for row in response.rows:
    path = row.dimension_values[0].value
    views = int(row.metric_values[0].value)

    # Only include /articles/ paths
    if path.startswith("/articles/"):
        articles.append({
            "url": path,
            "views": views
        })

# 7️⃣ Save to _data/most_read.yml
os.makedirs("_data", exist_ok=True)
with open("_data/most_read.yml", "w") as f:
    yaml.dump(articles, f, sort_keys=False)

print("✅ _data/most_read.yml updated successfully!")
