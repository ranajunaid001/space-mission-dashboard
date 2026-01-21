"""
Space Missions Data Functions
Contains 8 required functions for programmatic grading.
"""

import pandas as pd
from typing import List, Tuple, Dict

# Global variable to cache the dataframe
_df = None


def _load_data() -> pd.DataFrame:
    """
    Load the space missions data from CSV file.
    Caches the dataframe to avoid repeated file reads.
    """
    global _df
    if _df is None:
        _df = pd.read_csv('space_missions.csv')
        # Ensure Date column is parsed as datetime
        _df['Date'] = pd.to_datetime(_df['Date'])
    return _df


def GetMissionCountByCompany(companyName: str) -> int:
    """
    Returns the total number of missions for a given company.
    
    Args:
        companyName: Name of the company (e.g., "SpaceX", "NASA", "RVSN USSR")
    
    Returns:
        Integer representing the total number of missions
    """
    if not companyName or not isinstance(companyName, str):
        return 0
    
    df = _load_data()
    count = len(df[df['Company'] == companyName])
    return int(count)


def GetSuccessRate(companyName: str) -> float:
    """
    Calculates the success rate for a given company as a percentage.
    
    Args:
        companyName: Name of the company
    
    Returns:
        Float representing success rate as a percentage (0-100), rounded to 5 decimal places.
        Only "Success" missions count as successful.
        Returns 0.0 if company has no missions.
    """
    if not companyName or not isinstance(companyName, str):
        return 0.0
    
    df = _load_data()
    company_df = df[df['Company'] == companyName]
    
    total_missions = len(company_df)
    if total_missions == 0:
        return 0.0
    
    successful_missions = len(company_df[company_df['MissionStatus'] == 'Success'])
    success_rate = (successful_missions / total_missions) * 100
    
    return round(success_rate, 5)


def GetMissionsByDateRange(startDate: str, endDate: str) -> list:
    """
    Returns a list of all mission names launched between startDate and endDate (inclusive).
    
    Args:
        startDate: Start date in "YYYY-MM-DD" format
        endDate: End date in "YYYY-MM-DD" format
    
    Returns:
        List of strings containing mission names, sorted chronologically
    """
    if not startDate or not endDate:
        return []
    
    try:
        df = _load_data()
        
        # Convert string dates to datetime
        start = pd.to_datetime(startDate)
        end = pd.to_datetime(endDate)
        
        # Filter by date range (inclusive)
        mask = (df['Date'] >= start) & (df['Date'] <= end)
        filtered_df = df[mask].sort_values('Date')
        
        # Return list of mission names
        return filtered_df['Mission'].tolist()
    except Exception:
        return []


def GetTopCompaniesByMissionCount(n: int) -> list:
    """
    Returns the top N companies ranked by total number of missions.
    
    Args:
        n: Number of top companies to return
    
    Returns:
        List of tuples: [(companyName, missionCount), ...]
        Sorted by mission count in descending order.
        If companies have the same count, sort alphabetically by company name.
    """
    if not isinstance(n, int) or n <= 0:
        return []
    
    df = _load_data()
    
    # Count missions per company
    company_counts = df['Company'].value_counts()
    
    # Convert to dataframe for easier sorting
    counts_df = company_counts.reset_index()
    counts_df.columns = ['Company', 'Count']
    
    # Sort by count descending, then by company name ascending (for ties)
    counts_df = counts_df.sort_values(
        by=['Count', 'Company'], 
        ascending=[False, True]
    )
    
    # Get top n and convert to list of tuples
    top_n = counts_df.head(n)
    result = [(row['Company'], int(row['Count'])) for _, row in top_n.iterrows()]
    
    return result


def GetMissionStatusCount() -> dict:
    """
    Returns the count of missions for each mission status.
    
    Returns:
        Dictionary with status as key and count as value.
        Keys: "Success", "Failure", "Partial Failure", "Prelaunch Failure"
    """
    df = _load_data()
    
    # Get counts for each status
    status_counts = df['MissionStatus'].value_counts().to_dict()
    
    # Ensure all expected keys are present (even if count is 0)
    expected_statuses = ["Success", "Failure", "Partial Failure", "Prelaunch Failure"]
    result = {}
    for status in expected_statuses:
        result[status] = int(status_counts.get(status, 0))
    
    return result


def GetMissionsByYear(year: int) -> int:
    """
    Returns the total number of missions launched in a specific year.
    
    Args:
        year: Year (e.g., 2020)
    
    Returns:
        Integer representing the total number of missions in that year
    """
    if not isinstance(year, int):
        return 0
    
    df = _load_data()
    
    # Extract year from Date column and filter
    missions_in_year = df[df['Date'].dt.year == year]
    
    return int(len(missions_in_year))


def GetMostUsedRocket() -> str:
    """
    Returns the name of the rocket that has been used the most times.
    
    Returns:
        String containing the rocket name.
        If multiple rockets have the same count, return the first one alphabetically.
    """
    df = _load_data()
    
    # Count rocket usage
    rocket_counts = df['Rocket'].value_counts()
    
    # Get the maximum count
    max_count = rocket_counts.max()
    
    # Get all rockets with the maximum count
    top_rockets = rocket_counts[rocket_counts == max_count].index.tolist()
    
    # Sort alphabetically and return the first one
    top_rockets.sort()
    
    return top_rockets[0]


def GetAverageMissionsPerYear(startYear: int, endYear: int) -> float:
    """
    Calculates the average number of missions per year over a given range.
    
    Args:
        startYear: Starting year (inclusive)
        endYear: Ending year (inclusive)
    
    Returns:
        Float representing average missions per year, rounded to 5 decimal places
    """
    if not isinstance(startYear, int) or not isinstance(endYear, int):
        return 0.0
    
    if startYear > endYear:
        return 0.0
    
    df = _load_data()
    
    # Filter missions within the year range
    mask = (df['Date'].dt.year >= startYear) & (df['Date'].dt.year <= endYear)
    filtered_df = df[mask]
    
    # Calculate average over the number of years in the range
    num_years = endYear - startYear + 1
    total_missions = len(filtered_df)
    
    if num_years == 0:
        return 0.0
    
    average = total_missions / num_years
    
    return round(average, 5)


# Aliases with camelCase for backward compatibility (optional)
getMissionCountByCompany = GetMissionCountByCompany
getSuccessRate = GetSuccessRate
getMissionsByDateRange = GetMissionsByDateRange
getTopCompaniesByMissionCount = GetTopCompaniesByMissionCount
getMissionStatusCount = GetMissionStatusCount
getMissionsByYear = GetMissionsByYear
getMostUsedRocket = GetMostUsedRocket
getAverageMissionsPerYear = GetAverageMissionsPerYear


# For testing purposes
if __name__ == "__main__":
    print("Testing Space Missions Data Functions (PascalCase)")
    print("=" * 60)
    
    print(f"\n1. GetMissionCountByCompany('NASA'): {GetMissionCountByCompany('NASA')}")
    print(f"   GetMissionCountByCompany('SpaceX'): {GetMissionCountByCompany('SpaceX')}")
    print(f"   GetMissionCountByCompany('RVSN USSR'): {GetMissionCountByCompany('RVSN USSR')}")
    print(f"   GetMissionCountByCompany(''): {GetMissionCountByCompany('')}")
    
    print(f"\n2. GetSuccessRate('NASA'): {GetSuccessRate('NASA')}")
    print(f"   GetSuccessRate('SpaceX'): {GetSuccessRate('SpaceX')}")
    print(f"   GetSuccessRate('NonExistentCompany'): {GetSuccessRate('NonExistentCompany')}")
    
    print(f"\n3. GetMissionsByDateRange('1957-10-01', '1957-12-31'): {GetMissionsByDateRange('1957-10-01', '1957-12-31')}")
    
    print(f"\n4. GetTopCompaniesByMissionCount(5): {GetTopCompaniesByMissionCount(5)}")
    
    print(f"\n5. GetMissionStatusCount(): {GetMissionStatusCount()}")
    
    print(f"\n6. GetMissionsByYear(2020): {GetMissionsByYear(2020)}")
    print(f"   GetMissionsByYear(1957): {GetMissionsByYear(1957)}")
    
    print(f"\n7. GetMostUsedRocket(): {GetMostUsedRocket()}")
    
    print(f"\n8. GetAverageMissionsPerYear(2010, 2020): {GetAverageMissionsPerYear(2010, 2020)}")
