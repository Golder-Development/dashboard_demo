import pandas as pd
import matplotlib.pyplot as plt
import os

# Create output directory if it doesn't exist
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load data - fixed path to use local output directory
df = pd.read_csv("output/cleaned_data.csv", low_memory=False)

# Parse dates
df["ReceivedDate"] = pd.to_datetime(df["ReceivedDate"], errors="coerce")
df["Year"] = df["ReceivedDate"].dt.year

# Filter out partial data years (1997 and 2024)
df_filtered = df[~df["parliamentary_sitting"].isin(
    [1997, 2024]
)].copy()

# --- Chart 1: Donations by Party Over Time ---
if "Party_Group" not in df_filtered.columns:
    raise ValueError("Party_Group column not found in dataset.")

annual = (
    df_filtered.dropna(subset=["Year"])
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
plt.savefig(os.path.join(output_dir,
                         "donations_by_party_over_time.png"),
            dpi=200)
plt.close()

# --- Determine latest reporting period ---
if "parliamentary_sitting" in df_filtered.columns:
    period_last_dates = (
        df_filtered.dropna(subset=["parliamentary_sitting",
                                    "ReceivedDate"])
          .groupby("parliamentary_sitting")["ReceivedDate"]
          .max()
    )
    if not period_last_dates.empty:
        latest_period = period_last_dates.sort_values().index[-1]
    else:
        latest_period = None
else:
    latest_period = None

# --- Chart 2: Donations by Donor Type & Party
# (Latest Reporting Period) ---
if latest_period is not None and "DonorStatus" in df_filtered.columns:
    period_df = df_filtered[
        df_filtered["parliamentary_sitting"] == latest_period
    ].copy()
    donor_party = (
        period_df.groupby(
            ["Party_Group", "DonorStatus"],
            as_index=False
        )["Value"]
        .sum()
    )

    if not donor_party.empty:
        pivot = donor_party.pivot(
            index="Party_Group",
            columns="DonorStatus",
            values="Value"
        ).fillna(0)

        plt.figure(figsize=(16, 9))
        pivot.plot(kind="bar", stacked=True)
        plt.xlabel("Party")
        plt.ylabel("Total Donations (£)")
        plt.title(f"Donations by Donor Type and Party – {latest_period}")
        plt.xticks(fontsize=9, rotation=45, ha='right')
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                   ncol=4, frameon=True, fontsize=9)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir,
                                 "donations_by_donor_type_party.png"),
                    dpi=200)
        plt.close()

# --- Chart 3: Donations vs Maximum Public Funding ---
MAX_PUBLIC_FUNDING = 340_000_000  # loaf-of-bread democracy figure

if "parliamentary_sitting" in df_filtered.columns:
    cycle_totals = (
        df_filtered.dropna(subset=["parliamentary_sitting"])
          .groupby("parliamentary_sitting", as_index=False)["Value"]
          .sum()
    )

    period_last_dates = (
        df_filtered.dropna(subset=["parliamentary_sitting",
                                    "ReceivedDate"])
          .groupby("parliamentary_sitting")["ReceivedDate"]
          .max()
          .reset_index()
    )
    cycle_totals = cycle_totals.merge(
        period_last_dates,
        on="parliamentary_sitting",
        how="left"
    )
    cycle_totals = cycle_totals.sort_values("ReceivedDate")

    # last 12 reporting periods (already filtered to exclude 1997, 2024)
    cycle_totals = cycle_totals.tail(12)

    x = range(len(cycle_totals))

    plt.figure(figsize=(14, 8))
    plt.bar(x, cycle_totals["Value"] / 1_000_000, width=0.4,
            label="Actual Donations")
    plt.bar([i + 0.4 for i in x],
            [MAX_PUBLIC_FUNDING / 1_000_000] * len(cycle_totals),
            width=0.4,
            label="Max Public Funding (5-year cycle)")
    plt.xticks([i + 0.2 for i in x],
               cycle_totals["parliamentary_sitting"],
               rotation=45,
               ha="right")
    plt.xlabel("Parliamentary Sitting")
    plt.ylabel("Donations (£ Millions)")
    plt.title(
        "Donations Received vs Maximum Public Funding Required\n"
        "(by Parliamentary Sitting)"
    )
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir,
                             "donations_vs_publicfunding.png"),
                dpi=200)
    plt.close()

# --- Chart 4: Average Donations by Electoral Cycle Phase ---
if "ElectoralCyclePhase" in df_filtered.columns:
    phase_avg = (
        df_filtered.dropna(subset=["ElectoralCyclePhase"])
          .groupby("ElectoralCyclePhase", as_index=False)["Value"]
          .mean()
          .sort_values("Value", ascending=False)
    )

    if not phase_avg.empty:
        plt.figure(figsize=(12, 7))
        bars = plt.bar(phase_avg["ElectoralCyclePhase"],
                       phase_avg["Value"],
                       color='steelblue',
                       edgecolor='black',
                       alpha=0.7)

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                     f'£{height:,.0f}',
                     ha='center', va='bottom', fontsize=10)

        plt.xlabel("Electoral Cycle Phase")
        plt.ylabel("Average Donation Value (£)")
        plt.title(
            "Average Donation Value by Electoral Cycle Phase\n"
            "(excluding 1997 and 2024)"
        )
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir,
                                 "avg_donations_by_cycle_phase.png"),
                    dpi=200)
        plt.close()

print(
    "Charts saved successfully:\n"
    f"  - {os.path.join(output_dir, 'donations_by_party_over_time.png')}\n"
    f"  - {os.path.join(output_dir, 'donations_by_donor_type_party.png')}\n"
    f"  - {os.path.join(output_dir, 'donations_vs_publicfunding.png')}\n"
    f"  - {os.path.join(output_dir, 'avg_donations_by_cycle_phase.png')}"
)
