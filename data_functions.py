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


def getMissionCountByCompany(companyName: str) -> int:
    """
    Returns the total number of missions for a given company.
    
    Args:
        companyName: Name of the company (e.g., "SpaceX", "NASA", "RVSN USSR")
    
    Returns:
        Integer representing the total number of missions
    """
    df = _load_data()
    count = len(df[df['Company'] == companyName])
    return int(count)


def getSuccessRate(companyName: str) -> float:
    """
    Calculates the success rate for a given company as a percentage.
    
    Args:
        companyName: Name of the company
    
    Returns:
        Float representing success rate as a percentage (0-100), rounded to 2 decimal places.
        Only "Success" missions count as successful.
        Returns 0.0 if company has no missions.
    """
    df = _load_data()
    company_df = df[df['Company'] == companyName]
    
    total_missions = len(company_df)
    if total_missions == 0:
        return 0.0
    
    successful_missions = len(company_df[company_df['MissionStatus'] == 'Success'])
    success_rate = (successful_missions / total_missions) * 100
    
    return round(success_rate, 2)


def getMissionsByDateRange(startDate: str, endDate: str) -> list:
    """
    Returns a list of all mission names launched between startDate and endDate (inclusive).
    
    Args:
        startDate: Start date in "YYYY-MM-DD" format
        endDate: End date in "YYYY-MM-DD" format
    
    Returns:
        List of strings containing mission names, sorted chronologically
    """
    df = _load_data()
    
    # Convert string dates to datetime
    start = pd.to_datetime(startDate)
    end = pd.to_datetime(endDate)
    
    # Filter by date range (inclusive)
    mask = (df['Date'] >= start) & (df['Date'] <= end)
    filtered_df = df[mask].sort_values('Date')
    
    # Return list of mission names
    return filtered_df['Mission'].tolist()


def getTopCompaniesByMissionCount(n: int) -> list:
    """
    Returns the top N companies ranked by total number of missions.
    
    Args:
        n: Number of top companies to return
    
    Returns:
        List of tuples: [(companyName, missionCount), ...]
        Sorted by mission count in descending order.
        If companies have the same count, sort alphabetically by company name.
    """
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


def getMissionStatusCount() -> dict:
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


def getMissionsByYear(year: int) -> int:
    """
    Returns the total number of missions launched in a specific year.
    
    Args:
        year: Year (e.g., 2020)
    
    Returns:
        Integer representing the total number of missions in that year
    """
    df = _load_data()
    
    # Extract year from Date column and filter
    missions_in_year = df[df['Date'].dt.year == year]
    
    return int(len(missions_in_year))


def getMostUsedRocket() -> str:
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


def getAverageMissionsPerYear(startYear: int, endYear: int) -> float:
    """
    Calculates the average number of missions per year over a given range.
    
    Args:
        startYear: Starting year (inclusive)
        endYear: Ending year (inclusive)
    
    Returns:
        Float representing average missions per year, rounded to 2 decimal places
    """
    df = _load_data()
    
    # Filter missions within the year range
    mask = (df['Date'].dt.year >= startYear) & (df['Date'].dt.year <= endYear)
    filtered_df = df[mask]
    
    # Count missions per year
    missions_per_year = filtered_df.groupby(filtered_df['Date'].dt.year).size()
    
    # Calculate average
    if len(missions_per_year) == 0:
        return 0.0
    
    # Calculate average over the number of years in the range (not just years with missions)
    num_years = endYear - startYear + 1
    total_missions = len(filtered_df)
    average = total_missions / num_years
    
    return round(average, 2)


# For testing purposes
if __name__ == "__main__":
    print("Testing Space Missions Data Functions")
    print("=" * 50)
    
    print(f"\n1. getMissionCountByCompany('NASA'): {getMissionCountByCompany('NASA')}")
    print(f"   getMissionCountByCompany('SpaceX'): {getMissionCountByCompany('SpaceX')}")
    print(f"   getMissionCountByCompany('RVSN USSR'): {getMissionCountByCompany('RVSN USSR')}")
    
    print(f"\n2. getSuccessRate('NASA'): {getSuccessRate('NASA')}")
    print(f"   getSuccessRate('SpaceX'): {getSuccessRate('SpaceX')}")
    print(f"   getSuccessRate('NonExistentCompany'): {getSuccessRate('NonExistentCompany')}")
    
    print(f"\n3. getMissionsByDateRange('1957-10-01', '1957-12-31'): {getMissionsByDateRange('1957-10-01', '1957-12-31')}")
    
    print(f"\n4. getTopCompaniesByMissionCount(5): {getTopCompaniesByMissionCount(5)}")
    
    print(f"\n5. getMissionStatusCount(): {getMissionStatusCount()}")
    
    print(f"\n6. getMissionsByYear(2020): {getMissionsByYear(2020)}")
    print(f"   getMissionsByYear(1957): {getMissionsByYear(1957)}")
    
    print(f"\n7. getMostUsedRocket(): {getMostUsedRocket()}")
    
    print(f"\n8. getAverageMissionsPerYear(2010, 2020): {getAverageMissionsPerYear(2010, 2020)}")
