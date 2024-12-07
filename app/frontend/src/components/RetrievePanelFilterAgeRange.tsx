/**
 * @file RetrievePanelFilterAgeRange.tsx
 *
 * The filter for age in the retrieval panel, using @radix-ui/themes Slider.
 */

import { Dispatch, SetStateAction, useState } from "react";
import { Slider } from "@radix-ui/themes";
import { TrialFilters } from "../types";

interface RetrievePanelFilterAgeRangeProps {
  filters: TrialFilters;
  setFilters: Dispatch<SetStateAction<TrialFilters>>;
}

export const RetrievePanelFilterAgeRange = ({
  filters,
  setFilters,
}: RetrievePanelFilterAgeRangeProps) => {
  const [values, setValues] = useState<number[]>([
    filters.minAge ?? 0,
    filters.maxAge ?? 100,
  ]);

  const handleValueChange = (newValues: number[]) => {
    setValues(newValues); 
    setFilters((prevFilters) => ({
      ...prevFilters,
      minAge: newValues[0],
      maxAge: newValues[1],
    }));
  };

  return (
    <div style={{ padding: "20px" }}>
      <label style={{ display: "block", marginBottom: "8px" }}>
        Age Range: {values[0]} - {values[1]} years
      </label>
      <Slider
        min={0}
        max={100}
        step={1}
        defaultValue={[values[0], values[1]]}
        value={values}
        onValueChange={handleValueChange}
        orientation="horizontal"
        style={{ width: "100%" }}
      />
    </div>
  );
};
