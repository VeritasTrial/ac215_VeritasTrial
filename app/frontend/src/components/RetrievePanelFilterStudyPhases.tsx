/**
 * @file RetrievePanelFilterStudyPhases.tsx
 *
 * The filter for study phases in the retrieval panel.
 */

import { CheckboxGroup, Flex } from "@radix-ui/themes";
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
  const value = filters.studyPhases ?? [];

  const handler = (value: string[]) => {
    setFilters((prevFilters) => ({
      ...prevFilters,
      studyPhases: value.length === 0 ? undefined : value,
    }));
  };

  return (
    <CheckboxGroup.Root value={value} onValueChange={handler}>
      <Flex direction="row" gapX="4" wrap="wrap">
        <CheckboxGroup.Item value="EARLY_PHASE1">
          Early Phase I
        </CheckboxGroup.Item>
        <CheckboxGroup.Item value="PHASE1">Phase I</CheckboxGroup.Item>
        <CheckboxGroup.Item value="PHASE2">Phase II</CheckboxGroup.Item>
        <CheckboxGroup.Item value="PHASE3">Phase III</CheckboxGroup.Item>
        <CheckboxGroup.Item value="PHASE4">Phase IV</CheckboxGroup.Item>
      </Flex>
    </CheckboxGroup.Root>
  );
};
