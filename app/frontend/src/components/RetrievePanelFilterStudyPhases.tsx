/**
 * @file RetrievePanelFilterStudyPhases.tsx
 *
 * The filter for study phases in the retrieval panel
 */

import { useState } from "react";
import { Checkbox, Flex, Text } from "@radix-ui/themes";
import { Dispatch, SetStateAction } from "react";
import { TrialFilters } from "../types";

interface RetrievePanelFilterStudyPhasesProps {
  filters: TrialFilters;
  setFilters: Dispatch<SetStateAction<TrialFilters>>;
}

export const RetrievePanelFilterStudyPhases = ({
  filters,
  setFilters,
}: RetrievePanelFilterStudyPhasesProps) => {
  const options = [
    { value: "EARLY_PHASE1", label: "Early Phase 1" },
    { value: "PHASE1", label: "Phase 1" },
    { value: "PHASE2", label: "Phase 2" },
    { value: "PHASE3", label: "Phase 3" },
    { value: "PHASE4", label: "Phase 4" },
  ];

  const [selectedValues, setSelectedValues] = useState<string[]>(
    filters.studyPhases?.split(", ") ?? [],
  );

  const handleCheckboxChange = (value: string) => {
    const newValues = selectedValues.includes(value)
      ? selectedValues.filter((v) => v !== value) // cancel selection
      : [...selectedValues, value]; // add selection

    setSelectedValues(newValues);

    setFilters((prevFilters) => ({
      ...prevFilters,
      studyPhases: newValues.length > 0 ? newValues.join(", ") : undefined,
    }));
  };

  return (
    <Flex direction="row" gapX="4" wrap="wrap">
      {options.map((option) => (
        <Flex key={option.value} align="center" gap="2">
          <Checkbox
            checked={selectedValues.includes(option.value)}
            onCheckedChange={() => handleCheckboxChange(option.value)}
            id={option.value}
          />
          <Text as="label" htmlFor={option.value}>
            {option.label}
          </Text>
        </Flex>
      ))}
    </Flex>
  );
};
