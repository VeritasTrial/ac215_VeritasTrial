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
  const value = filters.ageRange ?? [0, 100];

  const handler = (value: number[]) => {
    setFilters((prevFilters) => ({
      ...prevFilters,
      ageRange: [value[0], value[1]],
    }));
  };

  return (
    <Flex align="center" gapX="3">
      <Slider
        min={0}
        max={100}
        step={1}
        size="1"
        value={value}
        onValueChange={handler}
        orientation="horizontal"
        css={{
          width: "150px",
          opacity: 0.8,
          "& .rt-SliderThumb::after": { inset: 0 },
        }}
      />
      <Text size="2">
        {value[0]}~{value[1]} years
      </Text>
    </Flex>
  );
};
