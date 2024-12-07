/**
 * @file RetrievePanelFilterAgeRange.tsx
 *
 * The filter for age in the retrieval panel, using @radix-ui/themes Slider.
 */

import { Dispatch, SetStateAction, useState } from "react";
import { Slider, Flex} from "@radix-ui/themes";
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
    <Flex align="center" gap="4">
      <div style={{ flex: 1 }}> 
        <label style={{ display: "block", marginBottom: "8px" }}>
          {values[0]} - {values[1]} years old
        </label>
        <Slider
          min={0}
          max={100}
          step={1}
          defaultValue={[values[0], values[1]]}
          value={values}
          onValueChange={handleValueChange}
          orientation="horizontal"
          style={{
            height: "20px", 
            padding: "10px 0",
            width: "300px", 
          }}
        />
      </div>
    </Flex>
  );
};
