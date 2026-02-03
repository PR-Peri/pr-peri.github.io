import os
import json
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest
import yaml

# GA4 property ID from workflow secrets
PROPERTY_ID = os.environ.get("GA_PROPERTY_ID")
# Service account JSON from workflow secret
GA_CREDENTIALS_JSON = os.environ.get("GA_CREDENTIALS_JSON")

# Save JSON to a temp file
with open("ga_key.json", "w") as f:
    f.write(GA_CREDENTIALS_JSON)

client = BetaAnalyticsDataClient.from_service_account_file("ga_key.json")

request = RunReportRequest(
    property=f"properties/{PROPERTY_ID}",
    dimensions=[Dimension(name="pagePath")],
    metrics=[Metric(name="screenPageViews")],
    date_ranges=[DateRange(start_date="2026-01-01", end_date="today")],
    limit=10  # Top 10 pages
)

response = client.run_report(request)

most_read = []

for row in response.rows:
    path = row.dimension_values[0].value
    # Include only articles
    if "/articles/" in path:
        most_read.append({
            "url": path,
            "views": int(row.metric_values[0].value)
        })

# Write to Jekyll _data folder
os.makedirs("_data", exist_ok=True)
with open("_data/most_read.yml", "w") as f:
    yaml.dump(most_read, f)

print("✅ _data/most_read.yml content:")
print(yaml.dump(most_read))
