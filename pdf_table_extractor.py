#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PDF Table Extractor

This script extracts tables from a PDF file using Camelot and saves them to a single CSV file.

Usage:
    python pdf_table_extractor.py

Requirements:
    - camelot-py[cv]
    - pandas
    - ghostscript
    - OpenCV
"""

import os
import requests
import camelot
import pandas as pd
from google.cloud import storage

def write_file():
    client = storage.Client()
    bucket = client.get_bucket('bucket-name')
    blob = bucket.blob('path/to/new-blob.txt')
    with blob.open(mode='w') as f:
        for line in object:
            f.write(line)

def download_pdf(url, save_path, timeout=60):
    """
    Download a PDF file from a URL and save it to the specified path.

    Args:
        url (str): URL of the PDF file to download
        save_path (str): Path where the PDF file will be saved
        timeout (int): Request timeout in seconds

    Returns:
        str: Path to the downloaded file or None if download failed
    """
    try:
        print(f"Downloading PDF from {url}...")
        # Create directory if it doesn't exist
        save_dir = os.path.dirname(save_path)
        if save_dir and not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Make request with timeout
        response = requests.get(url, stream=True, timeout=timeout)
        response.raise_for_status()  # Raise exception for non-200 status codes

        # Check if the content is PDF
        content_type = response.headers.get('Content-Type', '')
        if 'application/pdf' not in content_type.lower() and not url.lower().endswith('.pdf'):
            print(f"Warning: Content might not be a PDF. Content-Type: {content_type}")

        # Save the file
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

        file_size = os.path.getsize(save_path)
        print(f"PDF downloaded successfully to {save_path} ({file_size/1024:.1f} KB)")
        return save_path

    except requests.RequestException as e:
        print(f"Error downloading PDF: {e}")
        return None
    except IOError as e:
        print(f"Error saving PDF file: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error during download: {e}")
        return None



def extract_tables_to_single_csv(pdf_path, output_dir='output'):
    """
    Extract tables from PDF and save them to a single CSV file with table identifiers.

    Args:
        pdf_path (str): Path to the PDF file
        output_dir (str): Directory to save the CSV file

    Returns:
        str: Path to the saved CSV file or None if extraction failed
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get the filename without extension
    base_filename = os.path.splitext(os.path.basename(pdf_path))[0]
    output_file = os.path.join(output_dir, f"{base_filename}_all_tables.csv")

    # Extract tables using both Lattice and Stream methods for better results
    print(f"Extracting tables from {pdf_path}...")

    try:
        # Try default method first
        print("Reading PDF file...")
        tables = camelot.read_pdf(pdf_path, pages='all')
        print(f"Found {len(tables)} tables.")

        # Combine all tables into a single DataFrame
        all_tables_df = pd.DataFrame()

        for i, table in enumerate(tables):
            # Convert table to DataFrame
            df = table.df

            # Add table identifier column
            df['table_id'] = i + 1
            df['table_page'] = table.page

            # Print accuracy score
            print(f"Table {i+1} accuracy: {table.accuracy}")

            # Append to the combined DataFrame
            if all_tables_df.empty:
                all_tables_df = df
            else:
                all_tables_df = pd.concat([all_tables_df, df], ignore_index=True)

        # Save combined DataFrame to CSV
        all_tables_df.to_csv(output_file, index=False)
        print(f"All tables exported to: {output_file}")

        return output_file

    except Exception as e:
        print(f"Error extracting tables: {e}")
        return None


def main():
    # PDF file URL and local path
    pdf_url = "https://platforma.org/upload/document/187/attachments/544/Rejestr_umow.pdf"  # Replace with actual URL
    pdf_path = "./tmp/rejestr-umow.pdf"

    # Download PDF file
    downloaded_pdf = download_pdf(pdf_url, pdf_path)

    if not downloaded_pdf:
        print("Failed to download PDF. Exiting.")
        return

    # Extract tables and save as a single CSV
    csv_file = extract_tables_to_single_csv(downloaded_pdf)

    # Print summary
    if csv_file:
        print("\nExtraction completed successfully!")
        print(f"All tables saved to: {csv_file}")
    else:
        print("\nNo tables were extracted or an error occurred.")


if __name__ == "__main__":
    main()
