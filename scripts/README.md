# Utility Scripts

## verify_platform_city_listings.py

Smart verification tool for Yongin Platform City (용인 플랫폼시티) subscription listings on 청약Home.

### Purpose
Queries the 청약Home API (via data.go.kr) to identify current and historical Platform City listings, categorize them by housing type (국민주택 vs 민영), and recommend whether the notification system scope should be expanded.

### Key Finding
Historical data analysis shows that "플랫폼시티" projects are classified as **민영 (private housing)**, not 국민주택 (public housing). The current notification system only tracks 국민주택, creating a potential gap.

### Usage

```bash
# Set up API key
export DATA_GO_KR_KEY="<your_data.go.kr_service_key>"

# Run verification
python3 scripts/verify_platform_city_listings.py "$DATA_GO_KR_KEY"
```

### What It Checks

1. **Direct search**: `HOUSE_NM::LIKE=플랫폼시티`
   - Finds properties with "플랫폼시티" in the name
   - Most direct match for the specific project

2. **City-level search**: `HSSPLY_ADRES::LIKE=용인`
   - Finds all listings in Yongin city
   - Provides broader context of Yongin market

3. **District search**: `HSSPLY_ADRES::LIKE=기흥구`
   - Finds listings in Giheung district
   - Platform City is actually located in Giheung-gu

### Output

- Total matches count and listing details
- Housing type distribution (민영 vs 국민주택)
- Recommendation on system scope (expand if 민영 found)

### Example Output

```
📊 Total matches: 3 (displayed: 3)

  🏢 라온프라이빗 아르디에
     Type: 민영 (Private)
     Address: 경기도 용인시 기흥구...
     Announce: 2026-03-13

📈 Summary by Housing Type:
  • 민영 (Private): 1 listings
  • 국민주택 (Public): 0 listings

💡 NOTIFICATION SYSTEM SCOPE:
   ⚠️  Yongin Platform City historical data shows PRIVATE (민영) housing.
   ❌ Current system: Tracks 국민주택 (public housing) ONLY
   ✅ RECOMMENDATION: Expand scope to include BOTH 국민주택 & 민영 types
```

### Automation

This script is automatically run by the GitHub Actions workflow (`.github/workflows/verify-platform-city.yml`) when:
- The script itself is modified and pushed
- The workflow is manually triggered via GitHub Actions UI

To trigger manually:
```bash
gh workflow run verify-platform-city.yml
```

### Related Files

- `.github/workflows/verify-platform-city.yml` - GitHub Actions automation
- `data/manual_inputs/subscription_notices.yaml` - Where to add actual Platform City notice
- `engine/personal/housing.py` - Housing readiness scoring engine
