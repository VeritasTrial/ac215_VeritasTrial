/**
 * @file RetrievePanelFilterAgeRange.tsx
 *
 * The filter for ages in the retrieval panel.
 */

import { Dispatch, SetStateAction } from "react";
import { Flex, Slider, Text } from "@radix-ui/themes";
import { TrialFilters } from "../types";

interface RetrievePanelFilterAgeRangeProps {
  filters: TrialFilters;
  setFilters: Dispatch<SetStateAction<TrialFilters>>;
}

export const RetrievePanelFilterAgeRange = ({
  filters,
  setFilters,
}: RetrievePanelFilterAgeRangeProps) => {
  const values = [filters.minAge ?? 0, filters.maxAge ?? 100];

  const handleValueChange = (newValues: number[]) => {
    setFilters((prevFilters) => ({
      ...prevFilters,
      minAge: newValues[0],
      maxAge: newValues[1],
    }));
  };

  return (
    <Flex align="center" gapX="3" pl={{ initial: "1", sm: "0" }}>
      <Slider
        min={0}
        max={100}
        step={1}
        size="1"
        color="gray"
        value={values}
        onValueChange={handleValueChange}
        orientation="horizontal"
        css={{ width: "150px" }}
      />
      <Text size="2">
        {values[0]}~{values[1]} years old
      </Text>
    </Flex>
  );
};
