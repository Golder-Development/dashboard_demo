import pandas as pd
import matplotlib.pyplot as plt


# Load data
df = pd.read_csv("/output/cleaned_data.csv", low_memory=False)

# Parse dates
df["ReceivedDate"] = pd.to_datetime(df["ReceivedDate"], errors="coerce")
df["Year"] = df["ReceivedDate"].dt.year

# --- Chart 1: Donations by Party Over Time ---
if "Party_Group" not in df.columns:
    raise ValueError("Party_Group column not found in dataset.")

annual = (
    df.dropna(subset=["Year"])
      .groupby(["Year", "Party_Group"], as_index=False)["Value"]
      .sum()
)

plt.figure(figsize=(14, 8))
for party in sorted(annual["Party_Group"].dropna().unique()):
    temp = annual[annual["Party_Group"] == party]
    plt.plot(temp["Year"], temp["Value"], marker='o', label=party)

plt.xlabel("Year")
plt.ylabel("Total Donations (£)")
plt.title("Donations by Party Over Time")
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize="small")
plt.tight_layout()
plt.savefig("/mnt/data/donations_by_party_over_time.png", dpi=200)
plt.close()

# --- Determine latest reporting period ---
if "ReportingPeriodName" in df.columns:
    period_last_dates = (
        df.dropna(subset=["ReportingPeriodName", "ReceivedDate"])
          .groupby("ReportingPeriodName")["ReceivedDate"]
          .max()
    )
    if not period_last_dates.empty:
        latest_period = period_last_dates.sort_values().index[-1]
    else:
        latest_period = None
else:
    latest_period = None

# --- Chart 2: Donations by Donor Type & Party (Latest Reporting Period) ---
if latest_period is not None and "DonorStatus" in df.columns:
    period_df = df[df["ReportingPeriodName"] == latest_period].copy()
    donor_party = (
        period_df.groupby(["Party_Group", "DonorStatus"], as_index=False)["Value"]
        .sum()
    )

    if not donor_party.empty:
        pivot = donor_party.pivot(index="Party_Group", columns="DonorStatus", values="Value").fillna(0)

        plt.figure(figsize=(16, 9))
        pivot.plot(kind="bar", stacked=True)
        plt.xlabel("Party")
        plt.ylabel("Total Donations (£)")
        plt.title(f"Donations by Donor Type and Party – {latest_period}")
        plt.tight_layout()
        plt.savefig("/mnt/data/donations_by_donor_type_party.png", dpi=200)
        plt.close()

# --- Chart 3: Donations vs Maximum Public Funding ---
MAX_PUBLIC_FUNDING = 340_000_000  # loaf-of-bread democracy figure

if "ReportingPeriodName" in df.columns:
    cycle_totals = (
        df.dropna(subset=["ReportingPeriodName"])
          .groupby("ReportingPeriodName", as_index=False)["Value"]
          .sum()
    )

    period_last_dates = (
        df.dropna(subset=["ReportingPeriodName", "ReceivedDate"])
          .groupby("ReportingPeriodName")["ReceivedDate"]
          .max()
          .reset_index()
    )
    cycle_totals = cycle_totals.merge(period_last_dates, on="ReportingPeriodName", how="left")
    cycle_totals = cycle_totals.sort_values("ReceivedDate")

    # last 12 reporting periods
    cycle_totals = cycle_totals.tail(12)

    x = range(len(cycle_totals))

    plt.figure(figsize=(14, 8))
    plt.bar(x, cycle_totals["Value"], width=0.4, label="Actual Donations")
    plt.bar([i + 0.4 for i in x],
            [MAX_PUBLIC_FUNDING] * len(cycle_totals),
            width=0.4,
            label="Max Public Funding (5-year cycle)")
    plt.xticks([i + 0.2 for i in x],
               cycle_totals["ReportingPeriodName"],
               rotation=45,
               ha="right")
    plt.ylabel("£")
    plt.title("Donations Received vs Maximum Public Funding Required\n(by Reporting Period)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("/mnt/data/donations_vs_publicfunding.png", dpi=200)
    plt.close()

"/mnt/data/donations_by_party_over_time.png, /mnt/data/donations_by_donor_type_party.png, /mnt/data/donations_vs_publicfunding.png regenerated."
