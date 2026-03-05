# Region Update - ap-south-2 (Hyderabad)

## Updated Files

The following files have been updated to use the correct region `ap-south-2` (Hyderabad):

### 1. test_petition_verifier.py
- **Old**: `https://ked0qedvxi.execute-api.ap-south-1.amazonaws.com/prod`
- **New**: `https://ked0qedvxi.execute-api.ap-south-2.amazonaws.com/prod`

### 2. check_lambda_config.py
- **Old**: `region_name='ap-south-1'`
- **New**: `region_name='ap-south-2'`

### 3. check_lambda_logs.py
- **Old**: `region_name='ap-south-1'`
- **New**: `region_name='ap-south-2'`

### 4. DIAGNOSTIC_TOOLS_README.md
- Updated documentation to reflect ap-south-2 region

## Verification

The API endpoint URL is now correctly formatted:
- Base URL: `https://ked0qedvxi.execute-api.ap-south-2.amazonaws.com/prod`
- No trailing slash to avoid double slashes
- Endpoints append paths like `/petition/generate`

## Test Now

Run the diagnostic tool to test with the correct endpoint:

```bash
./diagnose_and_fix.sh
```

Or test directly:

```bash
python3 test_petition_verifier.py
```

The script will now connect to the correct Hyderabad (ap-south-2) endpoint.
