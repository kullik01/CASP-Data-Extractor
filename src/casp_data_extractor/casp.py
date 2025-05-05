import enum
import io
from collections import defaultdict

import pandas as pd

import utils


class Metrics(enum.IntEnum):
    """Enum for CASP metrics."""
    N1 = 0
    N2 = 1
    DIST = 2
    N = 3
    RMSD = 4
    GDT_TS = 5
    LGA_S3 = 6
    LGA_Q = 7


class Model:
  """Class for representing a CASP model."""
  def __init__(self, metrics: dict[Metrics, float]):
    self.metrics: dict[Metrics, float] = metrics


class Group:
  """Class for representing a CASP group."""
  def __init__(self, models: dict[str, list[Model]]):
    self.models: dict[str, list[Model]] = models


class Casp:
  """Class for representing a CASP dataset."""
  def __init__(self, name: str, data_url: str, targets: list[str], groups: dict[str, Group]):
    self.name: str = name
    self.data_url: str = data_url
    self.targets: list[str] = targets
    self.groups: dict[str, Group] = groups
    self.winner = None
    self.metric = [tmp_metric for tmp_metric in Metrics]

  def extract_data(self):
    """Downloads the CASP sda results data."""
    # Add loop so to download all summaries
    all_groups = defaultdict(list)

    for tmp_target_name in self.targets:
      tmp_url = f"{self.data_url}/{tmp_target_name}.SUMMARY.lga_sda.txt"
      df = self._parse_data(utils.download_url(tmp_url))
      if df.empty:
        continue
      # Group by extracted GROUP_ID
      for group_id, group_df in df.groupby('GROUP_ID'):
        # Select only required columns
        all_groups[group_id].append(group_df[['NAME', 'GDT_TS']])

    # Save results for each group
    for group_id, dfs in all_groups.items():
      if not dfs:  # Skip empty groups
        continue

      # Combine all entries for this group
      combined_df = pd.concat(dfs, ignore_index=True)

      # Save to CSV
      filename = f"group_results/group_{group_id}_results.csv"
      combined_df.to_csv(filename, index=False)
      print(f"Saved {len(combined_df)} entries for group {group_id}")

  def _parse_data(self, content):
    """Parse the summary file into a pandas DataFrame.

    Returns:
      A pandas DataFrame. An empty DataFrame is returned if the parsing failed.
    """
    try:
      # Parse with column-aware configuration
      df = pd.read_csv(
        io.StringIO(content),
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
      # Clean and extract group ID
      df['NAME'] = df['NAME'].str.replace(r':SUMMARY\(GDT\).lga$', '', regex=True)
      df['GROUP_ID'] = df['NAME'].str.extract(r'TS(\d+)_', expand=False)
      return df.dropna(subset=['GROUP_ID'])  # Remove rows without valid group IDs
    except Exception as e:
      print(f"Parsing error: {str(e)}")
      return pd.DataFrame()

  def calculate_winner(self):
    raise NotImplementedError()
