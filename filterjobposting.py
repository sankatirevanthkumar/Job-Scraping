#!/usr/bin/env python3
import pandas as pd
import re

# Load the CSV file produced by scraper.py
df = pd.read_csv("internshipjobs_updated.csv")

# Define the roles/keywords you want to filter
keywords = ["Software Engineer", "Full stack Developer", "python"]

# Convert column names to lowercase for consistency
df.columns = df.columns.str.lower()

# Create a regex pattern from keywords (matches any of the specified keywords)
pattern = "|".join(re.escape(keyword) for keyword in keywords)

# Filter rows where 'title' contains any of the keywords (case-insensitive)
filtered_df = df[df["title"].str.contains(pattern, case=False, na=False, regex=True)]

# Print the filtered job listings
print(filtered_df)

# Save the filtered data to a new CSV file
filtered_df.to_csv("filtered1_internships.csv", index=False)
