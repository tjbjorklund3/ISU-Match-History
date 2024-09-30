import ROFL_Converter
import ROFL_Add_to_DF
import calculate_stats

def main():
    # Step 1: Process all .rofl files and convert them to JSON
    print("Starting ROFL to JSON conversion...")
    ROFL_Converter.main()

    # Step 2: Update the DataFrame with new JSON data
    print("Updating DataFrame with new data from JSON files...")
    ROFL_Add_to_DF.main()

    # Step 3: Calculate statistics for "Wave Control"
    print("Calculating statistics for 'Wave Control'...")
    calculate_stats.calculate_average_kills("Wave Control")

if __name__ == "__main__":
    main()
