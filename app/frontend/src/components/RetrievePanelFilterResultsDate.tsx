/**
 * @file RetrievePanelFilterResultsDate.tsx
 *
 * The filter for results date in the retrieval panel
 */

import { useState } from "react";
import { DateRange, DayPicker } from "react-day-picker";
import "react-day-picker/dist/style.css";
import { TrialFilters } from "../types";

interface RetrievePanelFilterResultsDateProps {
  filters: TrialFilters;
  setFilters: (filters: TrialFilters) => void;
}

export const RetrievePanelFilterResultsDate = ({
  filters,
  setFilters,
}: RetrievePanelFilterResultsDateProps) => {
  const [range, setRange] = useState<DateRange>({
    from: undefined,
    to: undefined,
  });

  const formatDate = (date: Date | undefined): string =>
    date ? date.toISOString().split("T")[0] : "";

  const handleSelect = (selectedRange: DateRange | undefined) => {
    if (!selectedRange) {
      setRange({ from: undefined, to: undefined });
      setFilters({
        ...filters,
        resultsDate: "",
      });
      return;
    }

    const fromDate = selectedRange.from
      ? formatDate(selectedRange.from)
      : undefined;
    const toDate = selectedRange.to ? formatDate(selectedRange.to) : undefined;

    setRange(selectedRange);

    // update filters
    setFilters({
      ...filters,
      resultsDate: fromDate && toDate ? `${fromDate} to ${toDate}` : "",
    });
  };

  const handleReset = () => {
    setRange({ from: undefined, to: undefined });
    setFilters({
      ...filters,
      resultsDate: "",
    });
  };

  return (
    <div style={{ maxWidth: "400px", textAlign: "center" }}>
      <DayPicker
        mode="range"
        selected={range}
        onSelect={handleSelect}
        captionLayout="dropdown"
      />

      <div style={{ marginTop: "16px", fontSize: "14px" }}>
        {range.from && range.to ? (
          <p>
            Selected: {formatDate(range.from)} to {formatDate(range.to)}
          </p>
        ) : (
          <p>Please pick the first day.</p>
        )}
      </div>

      <button
        onClick={handleReset}
        style={{
          marginTop: "10px",
          padding: "8px 12px",
          backgroundColor: "#3b82f6",
          color: "white",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer",
        }}
      >
        Reset
      </button>
    </div>
  );
};
