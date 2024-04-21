#!/bin/bash

# Check if a stock symbol was provided
if [ -z "$1" ]; then
    echo "Usage: $0 <stock_symbol>"
    exit 1
fi

# Check if API_KEY is set in the environment
if [ -z "$API_KEY" ]; then
    echo "Please export your API_KEY before running this script."
    exit 1
fi

# Set the symbol variable from the first command line argument
SYMBOL="$1"

# Define the URL with the stock symbol dynamically inserted
URL="https://api.twelvedata.com/time_series?format=CSV&delimiter=,&order=ASC&interval=1day&outputsize=1000&apikey=${API_KEY}&symbol=${SYMBOL}"

# Replace any slashes in the symbol with a pipe symbol
SAFE_SYMBOL="${SYMBOL//\//|}"
DATA_FILE="data/${SAFE_SYMBOL}.csv"

# Use curl to attempt to download the file. Fail silently on server errors (-f) and operate silently (-s)
if curl -fs -o "${DATA_FILE}" "${URL}"; then
    echo "Data for ${SAFE_SYMBOL} downloaded successfully."
else
    echo "Failed to download data. Please check your API key and stock symbol."
    exit 1
fi
