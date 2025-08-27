# 📊 Data Cleanup and Processing Instructions for XLSX File

## Step 1: Clean the Data

### 1.1 Sort by Email
- **Delete rows** where:
  - Email address is missing
  - Email is `cayala@stuartrental.com` AND row is an Inventory Adjustment
  - Email belongs to Accounts Payable (e.g. `ap@company.com`, `invoices@company.com`)
  - Row is a duplicate (multiple contracts for same event)
  - More than one email is listed → keep only the one matching the Contact Name
  - Contact Name and Email do not match

### 1.2 Clean Contact Name Field
- **Remove** phone numbers or extensions from Contact Name cells
- **Trim** leading spaces from email addresses
- **Correct** obvious spelling errors in Contact Name and Email
- **Ensure** Contact Name is in `FirstName LastName` format
  - If missing, check Customer Name or infer from Email

---

## Step 2: Sort by Salesperson and Assign Location

### 2.1 Default Location by Salesperson
- **Dublin:** Cindy Foster, Mark Pringle  
- **San Jose:** Lorie Cataelli  
- **Milpitas:** All others

### 2.2 Override by Delivery/Pickup Location
- If `DEL` and `PU` fields show a different location than Salesperson, use `DEL/PU` location

---

## Step 3: Convert Contact Name to Proper Case

### 3.1 Create Proper Case Column
- Insert blank column next to `Contact Name`
- Use formula: `=PROPER(<Contact Name>)`
- Drag formula down to apply to all rows

### 3.2 Replace Original Names
- Copy Proper Case column
- Paste values into original `Contact Name` column
- Delete formula column

---

## Step 4: Split Contact Name into First and Last Name

### 4.1 Prepare Columns
- Insert 3 blank columns to the right of `Contact Name`

### 4.2 Use Text to Columns
- Select `Contact Name` column
- Go to `Data` → `Text to Columns`
- Step 1: Select **Delimited**
- Step 2: Check **Space** delimiter
- Step 3: Finish and confirm overwrite

### 4.3 Merge Multi-Part Last Names
- Combine last names split across multiple columns (e.g. "De La Cruz")

---

## Step 5: Validate Business Type

### 5.1 Review and Assign Categories
| Code | Category Description |
|------|----------------------|
| B    | Business Retail (brick & mortar) |
| C/D  | Caterer / Restaurant |
| T    | Construction |
| W    | Corporate Caterer |
| O    | Corporate Company (tech/web) |
| E    | Stuart Employee |
| P    | Events/Entertainment / Planner/Designer |
| G    | Government |
| H    | Homeowner |
| I    | Hotel/Venue |
| M    | Medical/Hospital |
| N    | Non-Profit |
| RELIGIOUS | Religious Organization |
| S    | School/Education |
| R    | Rental Company |
| VENDOR | Vendor/Supplier |

---

## Step 6: Submit Emails to Broadly ### -- commented out for automation testing

### 6.1 Open Broadly Dashboard
###- URL: `https://app.broadly.com`

### 6.2 Add Subscribers by Location
###- For each person:
###  - Use **First Name only**
###  - Use **Email**
###  - Submit to correct location:

###| Location  | URL |
###|-----------|-----|
###| Milpitas  | [Broadly Milpitas](https://app.broadly.com/#/58408c2e62d85a650034fd1f/add/one) |
###| Dublin    | [Broadly Dublin](https://app.broadly.com/#/5865673133e39f66005bc087/add/one) |
###| San Jose  | [Broadly San Jose](https://app.broadly.com/#/586567abbb8d906500b698f4/add/one) |

---

