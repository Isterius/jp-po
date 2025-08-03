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
import camelot
import pandas as pd


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
    # PDF file path
    pdf_path = "./rejestr_umow.pdf"

    # Extract tables and save as a single CSV
    csv_file = extract_tables_to_single_csv(pdf_path)

    # Print summary
    if csv_file:
        print("\nExtraction completed successfully!")
        print(f"All tables saved to: {csv_file}")
    else:
        print("\nNo tables were extracted or an error occurred.")


if __name__ == "__main__":
    main()
