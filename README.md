# Nxtgen Petty Cash

A complete Petty Cash Management solution for Frappe/ERPNext that covers the full lifecycle — from fund setup and employee advances through expense settlement, accounting entries, and replenishment — with real-time balance tracking and built-in audit trails.

---

## Table of Contents

- [What This App Does](#what-this-app-does)
- [Key Concepts](#key-concepts)
- [How It Works — Step by Step](#how-it-works--step-by-step)
  - [Step 1: Set Up a Petty Cash Float](#step-1-set-up-a-petty-cash-float)
  - [Step 2: Fund the Cashbox (Opening Balance)](#step-2-fund-the-cashbox-opening-balance)
  - [Step 3: Employee Requests a Cash Advance (IOU Request)](#step-3-employee-requests-a-cash-advance-iou-request)
  - [Step 4: Approver Reviews and Approves](#step-4-approver-reviews-and-approves)
  - [Step 5: Disburse the Cash](#step-5-disburse-the-cash)
  - [Step 6: Employee Settles the Advance (IOU Settlement)](#step-6-employee-settles-the-advance-iou-settlement)
  - [Step 7: Finance Posts GL Entries (Petty Cash Payment Entry)](#step-7-finance-posts-gl-entries-petty-cash-payment-entry)
  - [Step 8: Replenish the Cashbox](#step-8-replenish-the-cashbox)
- [Doctypes Reference](#doctypes-reference)
- [Reports](#reports)
- [Balance Tracking](#balance-tracking)
- [Accounting Integration](#accounting-integration)
- [Requirement Coverage](#requirement-coverage)
- [Installation](#installation)
- [License](#license)

---

## What This App Does

Nxtgen Petty Cash manages the complete petty cash process for organisations using Frappe/ERPNext:

- **Multiple cashboxes** — maintain separate petty cash floats per department, branch, or location
- **Employee cash advances (IOU)** — employees request cash in advance, with a full approval and disbursement workflow
- **Expense settlement** — employees reconcile what they spent, attach receipts, and return unused cash
- **Real-time balance** — the available balance updates instantly on every transaction
- **Accounting integration** — GL entries are posted directly to ERPNext's chart of accounts via Petty Cash Payment Entries
- **Fund replenishment** — generate replenishment requests linked to ERPNext Payment Entries for treasury/bank processing
- **Audit trail** — every debit and credit is recorded in the Petty Cash Ledger with voucher references

---

## Key Concepts

| Term | What It Means |
|---|---|
| **Petty Cash Floating** | The master record for a cashbox. Defines the float ceiling, GL account, approver, and company. One record per cashbox (department/branch/location). |
| **Petty Cash Fund** | A request to add money to a cashbox — either as the opening balance or a replenishment. Submitting it records a Receipt in the ledger. |
| **IOU Request** | An employee's request for a cash advance. Goes through Pending → Approved → Disbursed → Settled. |
| **IOU Settlement** | The employee's reconciliation after spending: line-by-line expenses with receipts, return of unused cash, and variance tracking. |
| **Petty Cash Payment Entry** | A batch document used by finance to select multiple settled IOUs and post the corresponding double-entry GL records. |
| **Petty Cash Ledger** | An immutable transaction log. Every receipt (DR) and payment (CR) for each cashbox is recorded here. The balance is always computed from this ledger. |

---

## How It Works — Step by Step

### Step 1: Set Up a Petty Cash Float

Go to **Nxtgen Petty Cash > Petty Cash Floating** and create a new record.

| Field | What to Enter |
|---|---|
| Title | A unique name for this cashbox, e.g., "Finance Dept — Head Office" |
| Floating Amount | The maximum cash limit for this cashbox, e.g., LKR 50,000 |
| Account | The petty cash GL account in ERPNext's Chart of Accounts |
| Approver | The user who will approve IOU Requests from this cashbox |
| Company | The company this cashbox belongs to |

Submit the record. One Petty Cash Floating record can be created for each department, branch, or location — there is no limit on the number of cashboxes.

> **Tip:** Name your floats descriptively — e.g., "Warehouse — Kandy", "HR Dept — Colombo" — so they are easily identifiable in dropdowns and reports.

---

### Step 2: Fund the Cashbox (Opening Balance)

Go to **Petty Cash Fund** and create a new record.

- Select the **Petty Cash Floating** you just created
- Enter the **Request Amount** (the opening cash amount)
- Tick **Is Opening** — this marks it as an opening balance, not a replenishment
- Submit the document

On submission, a **Petty Cash Ledger** Receipt entry is created automatically. The cashbox now has a live balance equal to the opening amount.

---

### Step 3: Employee Requests a Cash Advance (IOU Request)

Go to **IOU Request** and create a new record (employees can do this themselves).

| Field | What to Enter |
|---|---|
| Employee | Select the employee making the request |
| Amount | The cash amount needed |
| Date | Today (auto-populated) |
| Expenses Type | Select the expense category (e.g., Travel, Office Supplies) |
| Description | What the money will be used for |
| Cost Center / Project | Optional — for cost allocation |

On saving, the **status is set to Pending** and the approver (fetched from the employee's designated expense approver) is notified automatically.

> The approver is auto-populated from the Employee master's `expense_approver` field. If the employee does not have one set, it falls back to the Petty Cash Floating's approver.

---

### Step 4: Approver Reviews and Approves

The approver opens the IOU Request and clicks the **Approve** button (primary action button, visible when status is Pending).

A dialog appears asking for the **Approved Amount** — the approver can approve the full amount or a lower amount. On confirming:

- Status changes to **Approved**
- `approved_on` and `approver` are recorded
- The approved amount is saved

---

### Step 5: Disburse the Cash

After approval, a **Disbursed** button becomes the primary action. The cashbox custodian clicks it and a dialog asks for:

- **Petty Cash Floating** — which cashbox is providing the funds
- **Disbursed Amount** — the actual cash given to the employee (may differ from approved amount)

On confirming, the form is submitted automatically:

- Status changes to **Disbursed**
- `disbursed_by`, `disbursed_on`, and `disbursed_ammount` are recorded
- A **Petty Cash Ledger** Payment (Credit) entry is created — the cashbox balance reduces by the disbursed amount

The **available balance** on the cashbox updates immediately.

---

### Step 6: Employee Settles the Advance (IOU Settlement)

After spending, the employee goes to **IOU Settlement** (or clicks the **IOU Settlement** button from the IOU Request form).

**Header:**
- **Employee** — auto-linked to the employee
- **IOU Request** — select the disbursed advance being settled (dropdown filters to submitted, non-settled IOUs)
- **Requested Amount** — auto-fetched from the disbursed amount
- **Settle Date** — today

**Expenses table** — add one row per expense:

| Column | What to Enter |
|---|---|
| Expenses Type | Category of this expense |
| Amount | How much was spent |
| Proof Document | Attach the receipt or invoice |
| Description | Details of the purchase |

As rows are added, the form calculates:

- **Total Expenses** — sum of all expense lines
- **Expected Return Amount** — disbursed amount minus total expenses (the cash the employee should return)
- **Actual Return Amount** — the cash the employee is actually handing back
- **Variance Amount** — difference between expected and actual return (flags any discrepancy)

If expenses **exceed** the disbursed amount, an **Additional Amount Requested** field appears for the employee to declare the shortfall.

Submit the settlement:

- IOU Request status changes to **Settled**
- If cash was returned: a Petty Cash Ledger Receipt entry is created (cashbox balance increases)
- If additional funds were needed: a Petty Cash Ledger Payment entry is created
- The settlement is flagged as ready for GL processing (`is_gl_done = 0`)

---

### Step 7: Finance Posts GL Entries (Petty Cash Payment Entry)

At end-of-period (or as required), the finance team posts the accounting entries.

Go to **Petty Cash Payment Entry** and create a new record.

| Field | What to Enter |
|---|---|
| Posting Date | The accounting date for GL entries |
| Petty Cash Floating | The cashbox being processed |
| Company | Company |
| Cost Center | Default cost centre for GL entries (optional — falls back to company default) |

Click the **IOU Settlement** button to open a selection dialog. This shows all **submitted, unprocessed settlements** for the selected cashbox (`is_gl_done = 0`). Select the settlements (or individual expense items) to include in this batch.

The items table populates with:
- IOU Settlement reference
- IOU Request reference
- Expense type
- Description
- Amount

Submit the Petty Cash Payment Entry. For each line item, the system posts:

```
Dr  Expense Account (from Expense Claim Type mapping)    amount
    Cr  Petty Cash Account (from Petty Cash Floating)    amount
```

After submission:
- GL entries appear in ERPNext's General Ledger
- Each IOU Settlement included is marked `is_gl_done = 1` (preventing duplicate processing)
- The **Ledger** button on the submitted form links directly to the General Ledger report filtered to this voucher

**To reverse:** Cancel the Petty Cash Payment Entry — the GL entries are reversed automatically.

---

### Step 8: Replenish the Cashbox

When the cashbox balance runs low, a new **Petty Cash Fund** is created (same as Step 2, but with **Is Opening unchecked**).

On submission:
- System validates that the requested amount does not exceed the remaining headroom (`floating_amount − balance_amount`)
- A Petty Cash Ledger Receipt entry is created, increasing the balance immediately

To process the actual bank transfer, click the **Payment** button on the submitted Petty Cash Fund. This creates an ERPNext **Payment Entry** with:
- Payment Type: Internal Transfer
- Paid To: the petty cash GL account
- Amount: the requested fund amount
- A reference back to this Petty Cash Fund

When the Payment Entry is submitted by finance, the Petty Cash Fund is automatically flagged as `has_payment_entry = 1`, confirming the bank transfer has been processed.

---

## Doctypes Reference

### Petty Cash Floating

The master cashbox configuration. Submit once and keep active.

| Field | Type | Purpose |
|---|---|---|
| Title | Data (unique) | Cashbox identifier |
| Floating Amount | Currency | Maximum cash ceiling |
| Account | Link → Account | GL account for this cashbox |
| Approver | Link → User | Default approver for requests |
| Company | Link → Company | Owning company |
| Balance Amount | Virtual Currency | Live available balance (computed from ledger) |
| Outstanding Amount | Virtual Currency | Total disbursed but not yet settled |

### Petty Cash Fund

| Field | Type | Purpose |
|---|---|---|
| Petty Cash Floating | Link | Which cashbox |
| Request Amount | Currency | Amount to add |
| Request By | Link → User | Who raised the request |
| Required On | Date | When funds are needed |
| Is Opening | Check | Opening balance flag |
| Has Payment Entry | Check (read-only) | Payment Entry processed flag |

### IOU Request

| Field | Type | Purpose |
|---|---|---|
| Employee | Link → Employee | Requesting employee |
| Department | Link (fetched) | From employee master |
| Amount | Currency | Amount requested |
| Expenses Type | Link → Expense Claim Type | Expense category |
| Description / Remark | Text | Purpose of advance |
| Project / Cost Center | Link | Cost allocation |
| Status | Select | Pending / Approved / Disbursed / Settled / Cancelled |
| Approver | Link → User | Assigned approver |
| Approved Amount | Currency | Approver-confirmed amount |
| Disbursed By/On/Amount | Various | Disbursement details |
| Petty Cash Floating | Link | Source cashbox |

### IOU Settlement

| Field | Type | Purpose |
|---|---|---|
| Employee | Link → Employee | Settling employee |
| IOU Request | Link | The advance being settled |
| Requested Amount | Currency (fetched) | Disbursed amount |
| Expenses (child table) | Table | Line-by-line actual expenses |
| Total Expenses | Currency (calculated) | Sum of expense lines |
| Expected Return Amount | Currency (calculated) | Disbursed − Total Expenses |
| Actual Return Amount | Currency | Cash physically returned |
| Variance Amount | Currency (calculated) | Expected − Actual return |
| Additional Amount Requested | Currency | Extra funds needed if over-spent |

### IOU Settlement Items (child table)

| Field | Type | Purpose |
|---|---|---|
| Expenses Type | Link → Expense Claim Type | Category |
| Amount | Currency | Expense amount |
| Proof Document | Attach | Receipt / invoice file |
| Description | Small Text | Expense detail |

### Petty Cash Payment Entry

| Field | Type | Purpose |
|---|---|---|
| Posting Date | Date | GL posting date |
| Petty Cash Floating | Link | Source cashbox |
| Company | Link | Company |
| Cost Center | Link | Default for GL entries |
| Items (child table) | Table | Settlement expense lines |
| Total | Currency (calculated) | Sum of all items |

### Petty Cash Ledger

| Field | Type | Purpose |
|---|---|---|
| Date | Date | Transaction date |
| Voucher Type / No | Dynamic Link | Source document reference |
| Transaction Type | Data | "Receipt" or "Payment" |
| Received DR | Currency | Debit (money in) |
| Paid CR | Currency | Credit (money out) |
| Petty Cash Floating | Link | Which cashbox |
| Is Cancel | Check | Soft-cancel flag |

---

## Reports

### Cashbox Transaction Register

Found under **Nxtgen Petty Cash > Reports**.

Shows all IOU Requests with status "Disbursed". Columns:

- Reference number, Cashbox, Department
- Request Date, Approval Date, Disbursement Date
- Requester, Request Amount, Approved Amount, Disbursed Amount

**Filters:** Date range, Department, Cashbox

Use this report to see all cash currently in employees' hands and track the disbursement timeline.

---

### IOU Outstanding Summary

Shows all submitted IOU Settlements. Columns:

- Settlement ID, IOU Request, Cashbox, Department
- Request Date, Disbursement Date, Settlement Date
- Employee, Disbursed Amount, Expended Amount, Additional Amount Requested

**Filters:** Date range, Department, Cashbox

Use this report to review how much was spent vs. disbursed, and to identify settlements with variances or additional requests.

---

## Balance Tracking

The **balance_amount** on each Petty Cash Floating is a live virtual field — it queries the Petty Cash Ledger on every page load:

```
Balance = SUM(received_dr) − SUM(paid_cr)   [excluding cancelled entries]
```

**Outstanding Amount** tracks cash currently held by employees:

```
Outstanding = SUM(disbursed_ammount) from IOU Requests where status ≠ 'Settled'
```

These two fields together give a complete cash position:
- **Balance** = physical cash available in the cashbox
- **Outstanding** = cash given out but not yet reconciled

Both are visible directly on the Petty Cash Floating record and surfaced in the Petty Cash Fund dashboard.

---

## Accounting Integration

The app integrates with ERPNext's accounting module at two points:

**1. Replenishment — Payment Entry**

When a Petty Cash Fund is replenished, a Payment Entry (Internal Transfer) is generated and linked to the fund. This processes the bank-to-petty-cash transfer through ERPNext's standard payment workflow.

**2. Expense GL Posting — Petty Cash Payment Entry**

When the Petty Cash Payment Entry is submitted, double-entry GL records are created for each expense line:

```
Dr  [Expense Account mapped to Expense Claim Type]
    Cr  [Petty Cash Account from Petty Cash Floating]
```

The expense account is resolved from the **Expense Claim Type → Expense Claim Account** mapping per company in ERPNext. Each Expense Claim Type must have a default account configured for the relevant company before GL entries can be posted.

**To set up expense accounts:**
1. Go to **HR > Expense Claim Type**
2. Open each expense type used in petty cash
3. In the Accounts table, add the company and map it to the correct expense GL account

---

## Requirement Coverage

| Area | Feature | Status |
|---|---|---|
| Multiple cashboxes per dept/branch | Petty Cash Floating — create one per location | Supported |
| Custodian assignment | `approver` field on Petty Cash Floating | Supported |
| Fund ceiling enforcement | Validated on Petty Cash Fund submission | Supported |
| Expense categories | Expense Claim Type integration | Supported |
| Single-level approval workflow | Pending → Approved → Disbursed → Settled | Supported |
| Cash advance to employees | IOU Request with disbursement | Supported |
| Expense recording with receipts | IOU Settlement Items with proof_document | Supported |
| Return and variance tracking | IOU Settlement calculated fields | Supported |
| Real-time balance | Virtual balance_amount on Petty Cash Floating | Supported |
| Fund replenishment | Petty Cash Fund + Payment Entry | Supported |
| Auto balance update after replenishment | Ledger Receipt on Petty Cash Fund submit | Supported |
| GL posting to ERPNext | Petty Cash Payment Entry double-entry | Supported |
| GL reversal on cancel | on_cancel reverses GL entries | Supported |
| Transaction audit trail | Petty Cash Ledger — all debits and credits | Supported |
| Transaction register report | Cashbox Transaction Register | Supported |
| Outstanding expense summary | IOU Outstanding Summary | Supported |
| Department-level filtering | Department field on IOU Request | Supported |
| Cost centre allocation | Cost Center on IOU Request and GL entries | Supported |
| Mobile access | Frappe responsive web interface | Browser-based |

---

## Installation

Install using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app nxtgen_petty_cash
```

**Post-installation setup checklist:**

1. Create at least one **Petty Cash Floating** record with a valid GL account
2. Ensure each **Expense Claim Type** used for petty cash has a default account mapped for your company (HR > Expense Claim Type)
3. Configure roles and permissions for your users:
   - Who can create and submit IOU Requests (employees/custodians)
   - Who can approve (approvers)
   - Who can submit Petty Cash Payment Entries (finance team)
4. Create an opening **Petty Cash Fund** with **Is Opening** checked to initialise the cashbox balance

---

## Contributing

This app uses `pre-commit` for code formatting and linting. Install and enable it before contributing:

```bash
cd apps/nxtgen_petty_cash
pre-commit install
```

Pre-commit runs the following tools on each commit:

- ruff — Python linting and formatting
- eslint — JavaScript linting
- prettier — code formatting
- pyupgrade — Python syntax upgrades

---

## License

MIT
