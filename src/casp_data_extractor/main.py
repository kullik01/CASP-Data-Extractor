import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import os
import io


def download_url(url) -> str:
  """Download the given url."""
  try:
    response = requests.get(url)
    response.raise_for_status()
  except Exception as e:
    print(f"Error processing {url}: {str(e)}")
    exit(1)
  return response.text


def parse_summary_file(file_content: str) -> pd.DataFrame:
  """Parse the summary file into a pandas DataFrame.

  Returns:
    A pandas DataFrame. An empty DataFrame is returned if the parsing failed.
  """
  try:
    # Parse with column-aware configuration
    df = pd.read_csv(
      io.StringIO(file_content),
      sep=r'\s{2,}',  # Match 2+ whitespace as column separator
      engine='python',
      header=0,
      dtype={
        'N1': 'int32',
        'N2': 'int32',
        'DIST': 'float32',
        'N': 'int32',
        'RMSD': 'float32',
        'GDT_TS': 'float32',
        'LGA_S3': 'float32',
        'LGA_Q': 'float32'
      }
    )
    # Clean up the NAME column
    df['NAME'] = df['NAME'].str.replace(r':SUMMARY\(GDT\).lga$', '', regex=True)
    return df
  except Exception as e:
    print(f"Parsing error: {str(e)}")
    return pd.DataFrame()


def extract_winner_data(the_winners_group_id: str, the_dataframe: pd.DataFrame) -> pd.DataFrame:
  """
  Extract rows where NAME contains the specified group ID in the format:
  TXXXXTS<GROUP_ID>_X-DX (e.g., T1024TS427_1-D1)

  Args:
      the_winners_group_id: Target group ID to filter (e.g., "427")
      the_dataframe: DataFrame containing parsed summary data

  Returns:
      Filtered DataFrame containing only entries matching the target group ID
  """
  if the_dataframe.empty:
    return pd.DataFrame()

  # Create regex pattern to match the specific group ID format
  pattern = rf'TS{the_winners_group_id}_\d+-D\d+'

  # Filter the dataframe using the pattern
  filtered_df = the_dataframe[
    the_dataframe['NAME'].str.contains(pattern, regex=True, na=False)
  ]

  return filtered_df.reset_index(drop=True)



def main():
  t_list = [
    "T1024-D1",
    "T1024-D2",
    "T1024",
    "T1025-D1",
    "T1026-D1",
    "T1027-D1",
    "T1028-D1",
    "T1029-D1",
    "T1030-D1",
    "T1030-D2",
    "T1030",
    "T1031-D1",
    "T1032-D1",
    "T1033-D1",
    "T1034-D1",
    "T1035-D1",
    "T1036s1-D1",
    "T1037-D1",
    "T1038-D1",
    "T1038-D2",
    "T1038",
    "T1039-D1",
    "T1040-D1",
    "T1041-D1",
    "T1042-D1",
    "T1043-D1",
    "T1045s1-D1",
    "T1045s2-D1",
    "T1046s1-D1",
    "T1046s2-D1",
    "T1047s1-D1",
    "T1047s2-D1",
    "T1047s2-D2",
    "T1047s2-D3",
    "T1047s2",
    "T1048",
    "T1049-D1",
    "T1050-D1",
    "T1050-D2",
    "T1050-D3",
    "T1050",
    "T1052-D1",
    "T1052-D2",
    "T1052-D3",
    "T1052",
    "T1053-D1",
    "T1053-D2",
    "T1053",
    "T1054-D1",
    "T1054",
    "T1055-D1",
    "T1056-D1",
    "T1057-D1",
    "T1058-D1",
    "T1058-D2",
    "T1058",
    "T1060s2-D1",
    "T1060s3-D1",
    "T1061-D1",
    "T1061-D2",
    "T1061-D3",
    "T1061",
    "T1062",
    "T1064-D1",
    "T1065s1-D1",
    "T1065s2-D1",
    "T1067-D1",
    "T1068-D1",
    "T1070-D1",
    "T1070-D2",
    "T1070-D3",
    "T1070-D4",
    "T1070",
    "T1072s1",
    "T1073-D1",
    "T1074-D1",
    "T1076-D1",
    "T1078-D1",
    "T1079-D1",
    "T1080-D1",
    "T1082-D1",
    "T1083-D1",
    "T1084-D1",
    "T1085-D1",
    "T1085-D2",
    "T1085-D3",
    "T1085",
    "T1086-D1",
    "T1086-D2",
    "T1086",
    "T1087-D1",
    "T1088-D1",
    "T1089-D1",
    "T1090-D1",
    "T1091-D1",
    "T1091-D2",
    "T1091-D3",
    "T1091-D4",
    "T1091",
    "T1092-D1",
    "T1092-D2",
    "T1092",
    "T1093-D1",
    "T1093-D2",
    "T1093-D3",
    "T1093",
    "T1094-D1",
    "T1094-D2",
    "T1094",
    "T1095-D1",
    "T1095",
    "T1096-D1",
    "T1096-D2",
    "T1096",
    "T1098-D1",
    "T1098-D2",
    "T1098",
    "T1099-D1",
    "T1100-D1",
    "T1100-D2",
    "T1100",
    "T1101-D1",
    "T1101-D2",
    "T1101",
    "T1104-D1"
  ]
  target_summary_file_urls = []
  for tmp_target_name in t_list:
    target_summary_file_urls.append(f"https://predictioncenter.org/download_area/CASP14/results/sda/{tmp_target_name}.SUMMARY.lga_sda.txt")

  # for tmp_url in target_summary_file_urls:
  #   tmp_df: pd.DataFrame = parse_summary_file(download_url(tmp_url))
  #   extract_winner_data("427", tmp_df)

  winner_results = []

  for tmp_url in target_summary_file_urls:
    tmp_df: pd.DataFrame = parse_summary_file(download_url(tmp_url))
    if not tmp_df.empty:
      winner_df = extract_winner_data("427", tmp_df)
      if not winner_df.empty:
        winner_results.append(winner_df)

  if winner_results:
    final_df = pd.concat(winner_results, ignore_index=True)
    # Save with only NAME and GDT_TS
    final_df[['NAME', 'GDT_TS', 'RMSD']].to_csv('group_427_results.csv', index=False)
    print(f"Saved results with {len(final_df)} entries")
  else:
    print("No matching entries found for group 427")

  # # Download and parse using threading (adjust max_workers as needed)
  # with ThreadPoolExecutor(max_workers=5) as executor:
  #   results = list(executor.map(download_and_parse, target_summary_file_urls))

  # # Combine and deduplicate results
  # combined_df = pd.concat([df for df in results if df is not None]) \
  #   .drop_duplicates(subset=['NAME'])
  # combined_df.to_csv('combined_analysis.csv', index=False)
  # # Save with original name + .csv
  # filename = os.path.basename(url).split('?')[0] + '.csv'
  # df.to_csv(filename, index=False)
  # print(f"Processed: {url}")


if __name__ == '__main__':
  # main()
  pass
